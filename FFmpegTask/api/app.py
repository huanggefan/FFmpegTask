import os
import pathlib

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from FFmpegTask.api.services.api_gen_command import api_gen_command, ApiGenCommandBody
from FFmpegTask.api.services.api_parse_task import api_parse_task, ApiParseTaskBody
from FFmpegTask.api.services.api_submit_task import api_submit_task, ApiSubmitTaskBody
from FFmpegTask.api.services.api_task_list import api_task_list, sse_task_list

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/parse_task")
async def _api_parse_task(body: ApiParseTaskBody):
    return api_parse_task(body)


@app.post("/api/gen_command")
async def _api_gen_command(body: ApiGenCommandBody):
    return api_gen_command(body)


@app.post("/api/submit_task")
async def _api_submit_task(body: ApiSubmitTaskBody):
    return api_submit_task(body)


@app.get("/api/task_list")
async def _api_task_list():
    return api_task_list()


@app.get("/sse/task_list")
async def _api_task_list(request: Request):
    return EventSourceResponse(
        content=sse_task_list(request),
        status_code=200,
        sep="\n"
    )


@app.get("/")
async def root():
    return FileResponse(path=pathlib.Path(__file__).parent.parent.parent / "data" / "ui" / "index.html")


@app.get("/{whatever:path}")
async def page_whatever(whatever: str):
    path_root = pathlib.Path(__file__).parent.parent.parent / "data" / "ui"
    path_file = path_root / whatever
    path_404 = path_root / "404.html"

    ra = path_file.absolute()
    fa = path_file.absolute()

    if fa.is_relative_to(ra) and os.path.exists(path_file) and os.path.isfile(path_file):
        return FileResponse(path_file)

    return FileResponse(path=path_404, status_code=404)
