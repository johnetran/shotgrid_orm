
from datetime import date
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select, bindparam


class Base(DeclarativeBase):
    pass



class SGType():
    id: Mapped[int]
    type: Mapped[str]

class SGUrl():
    content_type: Mapped[str]
    link_type: Mapped[str]
    name: Mapped[str]
    url: Mapped[str]
    local_path: Mapped[str]
    local_path_linux: Mapped[str]
    local_path_mac: Mapped[str]
    local_path_windows: Mapped[str]
    local_storage: Mapped[dict]

    def __repr__(self) -> str:
        return f"SGUrl(content_type={self.content_type!r}, link_type={self.link_type!r}, name={self.name!r}, url={self.url!r}"

sg_types = {
    "addressing": {"hint": Mapped[str], "type": mapped_column(String)},
    "checkbox": {"hint": Mapped[bool], "type": mapped_column(Boolean)},

    "color": {"hint": Mapped[str], "type": mapped_column(String)},
    "currency": {"hint": Mapped[float], "type": mapped_column(Float)},
    "date": {"hint": Mapped[str], "type": mapped_column(String)},
    "date_time": {"hint": Mapped[datetime], "type": mapped_column(DateTime)},

    # "entity": {"hint": Mapped[SGType], "type": relationship(back_populates="id")},
    "entity": {"hint": Mapped[int], "type": mapped_column(Integer)}, # TODO

    "float": {"hint": Mapped[float], "type": mapped_column(Float)},
    "footage": {"hint": Mapped[str], "type": mapped_column(String)},
    "image": {"hint": Mapped[str], "type": mapped_column(String)}, # readonly
    "list": {"hint": Mapped[str], "type": mapped_column(String)},

    # "multi_entity": {"hint": Mapped[List["SGType"]], "type": None},
    "multi_entity": {"hint": Mapped[str], "type": mapped_column(String)}, # TODO

    "number": {"hint": Mapped[int], "type": mapped_column(Integer)},
    "password": {"hint": Mapped[str], "type": mapped_column(String)},
    "percent": {"hint": Mapped[int], "type": mapped_column(Integer)},
    "serializable": {"hint": Mapped[str], "type": mapped_column(String)}, # TODO: handle dict
    "status_list": {"hint": Mapped[str], "type": mapped_column(String)},

    "status_list": {"hint": Mapped[str], "type": mapped_column(String)},
    "system_task_type": {"hint": Mapped[str], "type": mapped_column(String)},
    "tag_list": {"hint": Mapped[str], "type": mapped_column(String)},
    "text": {"hint": Mapped[str], "type": mapped_column(String)},

    "timecode": {"hint": Mapped[int], "type": mapped_column(Integer)},
    "url": {"hint": Mapped[str], "type": mapped_column(String)}, # handle dict
    "number": {"hint": Mapped[int], "type": mapped_column(Integer)},
    "number": {"hint": Mapped[int], "type": mapped_column(Integer)},
}


sg_types_optional = {
    "addressing": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "checkbox": {"hint": Mapped[Optional[bool]], "type": mapped_column(Boolean)},

    "color": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "currency": {"hint": Mapped[Optional[float]], "type": mapped_column(Float)},
    "date": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "date_time": {"hint": Mapped[Optional[datetime]], "type": mapped_column(DateTime)},

    # "entity": {"hint": Mapped[Optional[SGType]], "type": relationship(back_populates="id")},
    "entity": {"hint": Mapped[Optional[int]], "type": mapped_column(Integer)}, # TODO

    "float": {"hint": Mapped[Optional[float]], "type": mapped_column(Float)},
    "footage": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "image": {"hint": Mapped[Optional[str]], "type": mapped_column(String)}, # readonly
    "list": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},

    # "multi_entity": {"hint": Mapped[Optional[List["SGType"]]], "type": None},
    "multi_entity": {"hint": Mapped[Optional[str]], "type": mapped_column(String)}, # TODO

    "number": {"hint": Mapped[Optional[int]], "type": mapped_column(Integer)},
    "password": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "percent": {"hint": Mapped[Optional[int]], "type": mapped_column(Integer)},
    "serializable": {"hint": Mapped[Optional[str]], "type": mapped_column(String)}, # TODO: handle dict
    "status_list": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},

    "status_list": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "system_task_type": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "tag_list": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},
    "text": {"hint": Mapped[Optional[str]], "type": mapped_column(String)},

    "timecode": {"hint": Mapped[Optional[int]], "type": mapped_column(Integer)},
    "url": {"hint": Mapped[Optional[str]], "type": mapped_column(String)}, # handle dict
    "number": {"hint": Mapped[Optional[int]], "type": mapped_column(Integer)},
    "number": {"hint": Mapped[Optional[int]], "type": mapped_column(Integer)},
}
