from typing import List

from sqlalchemy import ForeignKey, Text, Integer, Double
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship

from FFmpegTask.utils.sql_utils import Base, get_engine


class TaskModel(Base):
    __tablename__ = "model_task"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        Text(),
        unique=True,
        comment="任务名称",
    )

    src: Mapped[str] = mapped_column(
        Text(),
        comment="源文件夹",
    )

    dist: Mapped[str] = mapped_column(
        Text(),
        comment="输出文件夹",
    )

    commands: Mapped[List["CommandModel"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )


class CommandModel(Base):
    __tablename__ = "model_command"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True,
    )

    task_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("model_task.id")
    )

    video_src: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        comment="视频输入文件",
    )

    video_dist: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
        comment="视频输出文件",
    )

    command: Mapped[str] = mapped_column(
        Text(),
        comment="命令",
    )

    log: Mapped[str] = mapped_column(
        Text(),
        comment="执行日志",
        default="",
    )

    progress: Mapped[float] = mapped_column(
        Double(),
        comment="执行进度",
        default=0.0,
    )

    status: Mapped[str] = mapped_column(
        Text(),
        comment="命令状态",
        default="wait",  # wait process finish
    )

    task: Mapped["TaskModel"] = relationship(
        back_populates="commands"
    )


def init_table():
    engine = get_engine()

    with Session(engine) as session:
        TaskModel.metadata.create_all(engine)
        CommandModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_table()
