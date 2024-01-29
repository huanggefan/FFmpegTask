import pathlib

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def get_engine(echo: bool = False) -> Engine:
    sqlite3_file = pathlib.Path(__file__).parent.parent.parent / "data" / "database.sqlite3"
    url = f"sqlite:///{sqlite3_file.absolute()}"
    engine = create_engine(url=url, echo=echo)

    return engine
