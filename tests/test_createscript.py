
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from shotgrid_orm import SGORM, SchemaType

ECHO = False

# sg_orm = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source="schema.json", echo=ECHO)
# print("creating python script")
# sg_orm.create_script("sgmodel.py")

sg_orm = SGORM(sg_schema_type=SchemaType.SG_SCRIPT, sg_schema_source="schema.json", echo=ECHO)
print("creating python script")
sg_orm.create_script("sgmodel1.py")
