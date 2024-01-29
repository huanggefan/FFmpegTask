import pathlib
from pydantic import BaseModel
from sqlalchemy.orm import Session

from FFmpegTask.utils.sql_utils import get_engine
from FFmpegTask.models.table import TaskModel, CommandModel


class ApiSubmitTaskBody(BaseModel):
    name: str

    src: pathlib.Path
    dist: pathlib.Path

    video_src_list: list[pathlib.Path]
    video_dist_list: list[pathlib.Path]

    commands: list[str]


def api_submit_task(body: ApiSubmitTaskBody):
    task = TaskModel(name=body.name, src=str(body.src), dist=str(body.dist))

    command_list = []

    for i in range(len(body.video_src_list)):
        vs = str(body.src / body.video_src_list[i])
        vd = str(body.src / body.video_dist_list[i])
        c = body.commands[i]
        command_list.append(
            CommandModel(video_src=vs, video_dist=vd, command=c)
        )

    engine = get_engine()

    with Session(engine) as session:
        session.add(task)

        session.flush()

        for command in command_list:
            command.task_id = task.id
            session.add(command)

        session.commit()
