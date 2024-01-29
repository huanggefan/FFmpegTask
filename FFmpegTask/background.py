import multiprocessing
from multiprocessing import sharedctypes
import pathlib
import time
import ctypes

import psutil
from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from FFmpegTask.utils.sql_utils import get_engine
from FFmpegTask.models.table import TaskModel, CommandModel
from FFmpegTask.ffmpeg.info import FFMPEGInfo
from FFmpegTask.ffmpeg.task import exec_ffmpeg_task
from utils.queue_utils import queue_loader


class _Task():
    task: TaskModel

    commands: list[CommandModel]


def _load_task() -> list[_Task]:
    result = []

    engine = get_engine()

    with Session(engine) as session:
        task_list = session.query(TaskModel)
        task_list = list(task_list)

        for task in task_list:
            command_list = session.query(CommandModel).order_by(CommandModel.status.desc()).filter(
                and_(
                    CommandModel.task_id == task.id,
                    not_(
                        CommandModel.status == "finish",
                    )
                )
            )
            command_list = list(command_list)

            item = _Task()
            item.task = task
            item.commands = command_list

            result.append(item)

    return result


def _start_ffmpeg(process_number, command: CommandModel):
    input_info = FFMPEGInfo(pathlib.Path(command.video_src))
    progress_queue = multiprocessing.Queue()
    engine = get_engine()

    with Session(engine) as session:
        obj = session.query(CommandModel).filter(CommandModel.id == command.id).first()
        obj.progress = 0
        obj.status = "process"
        session.commit()

    exec_ffmpeg_task(input_info, command.command, progress_queue)

    for rate in queue_loader(progress_queue, stop="1"):
        with Session(engine) as session:
            obj = session.query(CommandModel).filter(CommandModel.id == command.id).first()
            obj.progress = rate
            obj.status = "process"
            session.commit()

    with Session(engine) as session:
        obj = session.query(CommandModel).filter(CommandModel.id == command.id).first()
        obj.progress = 1
        obj.status = "finish"
        session.commit()

    process_number.value -= 1


def background():
    max_process_number = psutil.cpu_count(logical=True) - 2 if psutil.cpu_count(logical=True) > 2 else 1
    process_number = sharedctypes.Value(ctypes.c_int, 0, lock=True)

    while True:
        if process_number.value >= max_process_number:
            time.sleep(60)
            continue

        command_list = [command for task in _load_task() for command in task.commands]

        for command in command_list:
            if process_number.value >= max_process_number:
                break

            process_number.value += 1
            p = multiprocessing.Process(target=_start_ffmpeg, args=(process_number, command,))
            p.start()

        time.sleep(60)
