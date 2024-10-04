import asyncio
import os
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from functools import partial
from http import HTTPStatus
from typing import Any, Callable, Dict, Optional, Union

import granian
import granian.constants
import granian.log
from fastapi import Body, Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from granian import Granian

from ..channel import runner_context
from ..clients.gateway import (
    EndTaskRequest,
    GatewayServiceStub,
    StartTaskRequest,
)
from ..logging import StdoutJsonInterceptor
from ..runner.common import FunctionHandler
from ..runner.common import config as cfg
from ..type import TaskStatus
from .common import FunctionContext, end_task_and_send_callback

try:
    _loop = asyncio.get_running_loop()
except RuntimeError:
    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)


@dataclass
class TaskState:
    status: TaskStatus = TaskStatus.Pending
    result: Any = None
    override_callback_url: Optional[str] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    with runner_context() as channel:
        app.state.gateway_stub = GatewayServiceStub(channel)
        yield


@contextmanager
def env_vars(env_vars: Dict[str, Any]):
    os.environ.update(env_vars)
    yield
    for key in env_vars:
        os.environ.pop(key)


def call_function(
    handler: Union[Callable[..., Any], Callable[..., Any]],
    *args: Any,
    **kwargs: Any,
) -> Dict:
    if asyncio.iscoroutinefunction(handler):
        if _loop.is_running():
            return _loop.run_until_complete(handler(*args, **kwargs))
        return asyncio.run(handler(*args, **kwargs))

    return handler(*args, **kwargs)


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
def dispatch(request: Request, call_next: Callable[[Request], Any]) -> Any:
    if request.url.path == "/health":
        return call_next(request)

    task_id = request.headers.get("X-TASK-ID")
    if not task_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Task ID missing")

    with StdoutJsonInterceptor(task_id=task_id):
        print(f"Received task <{task_id}>")

        start_request = StartTaskRequest(task_id=task_id, container_id=cfg.container_id)
        start_response = request.app.state.gateway_stub.start_task(start_request)
        if not start_response.ok:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to start task",
            )

        request.state.task = TaskState(status=TaskStatus.Running)
        try:
            response = call_next(request)
            request.state.task.status = TaskStatus.Complete
            print(f"Task <{task_id}> finished")
            return response
        except BaseException:
            request.state.task.status = TaskStatus.Error
        finally:
            res = end_task_and_send_callback(
                gateway_stub=request.app.state.gateway_stub,
                payload=request.state.task.result,
                end_task_request=EndTaskRequest(
                    task_id=task_id,
                    container_id=cfg.container_id,
                    keep_warm_seconds=cfg.keep_warm_seconds,
                    task_status=request.state.task.status,
                ),
                override_callback_url=request.state.task.override_callback_url,
            )
            if not res.ok:
                print(f"Task <{task_id}> failed to end task")


@app.get("/health")
def health():
    return Response(status_code=HTTPStatus.OK)


@app.get("/", response_model=None)
@app.post("/", response_model=None)
def func(
    request: Request,
    x_task_id: Union[str, None] = Header(None),
    body: Any = Body(default_factory=dict),
    handler: FunctionHandler = Depends(FunctionHandler),
) -> Union[Response, JSONResponse]:
    args = body.get("args", {})
    kwargs = body.get("kwargs", {})

    if callback_url := kwargs.get("callback_url"):
        request.state.task.override_callback_url = callback_url

    try:
        with env_vars({"TASK_ID": x_task_id}):
            function = partial(handler, context=FunctionContext.new(config=cfg, task_id=x_task_id))
            response = call_function(function, *args, **kwargs)
            request.state.task.result = response

        return response if isinstance(response, Response) else JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


def target_loader(target: str):
    import importlib

    module = importlib.import_module("beta9.runner.main")
    return getattr(module, "app")


if __name__ == "__main__":
    gran = Granian(
        target="app",
        address="0.0.0.0",
        port=cfg.bind_port,
        interface=granian.constants.Interfaces.ASGI,
        log_level=granian.log.LogLevels.debug,
        workers=cfg.workers,
        threads=4,
        backlog=1024,
        backpressure=1024,
        respawn_failed_workers=True,
        loop=granian.constants.Loops.uvloop,
        # log_access=True,
    )
    gran.serve(target_loader=target_loader)
