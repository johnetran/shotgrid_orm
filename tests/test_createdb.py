
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from shotgrid_orm import SGORM, SchemaType

ECHO = False

print("creating engine and session to Sqlite db")
engine = create_engine("sqlite+pysqlite:///test_model.db", echo=ECHO)
session = Session(engine)

print("getting sg ORM from schema")
sg_orm = SGORM(sg_schema_type=SchemaType.JSON, sg_schema_source="schema.json", echo=ECHO)

print("dropping all tables")
sg_orm.Base.metadata.drop_all(bind=engine)

print("creating all tables")
sg_orm.Base.metadata.create_all(engine)
