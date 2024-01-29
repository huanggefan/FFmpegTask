import asyncio
import json

from fastapi.requests import Request
from sse_starlette import ServerSentEvent
from sqlalchemy.orm import Session

from FFmpegTask.utils.sql_utils import get_engine
from FFmpegTask.models.table import TaskModel, CommandModel


def _task_list():
    result = []

    engine = get_engine()

    with Session(engine) as session:
        task_list = session.query(TaskModel)
        task_list = list(task_list)

        for task in task_list:
            command_list = session.query(CommandModel).filter(CommandModel.task_id == task.id)
            command_list = list(command_list)

            d = {
                "id": task.id,
                "name": task.name,
                "commands": [
                    {"video_src": command.video_src, "command": command.command, "log": command.log, "progress": command.progress, "status": command.status}
                    for command in command_list
                ],
                "progress": sum(command.progress for command in command_list) / len(command_list),
            }

            result.append(d)

    return result


async def sse_task_list(request: Request):
    index = 0

    while True:
        result = _task_list()

        if not await request.is_disconnected():
            yield ServerSentEvent(id=index, event=None, data=json.dumps(result, ensure_ascii=False, indent=None))
        else:
            break

        index += 1
        await asyncio.sleep(3)


def api_task_list():
    return _task_list()
