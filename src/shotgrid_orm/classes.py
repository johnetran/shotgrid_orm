import os
import json
import copy
import traceback
from enum import Enum

from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select, bindparam

from sqlacodegen_v2 import generate_models
from sqlacodegen_v2 import generators


from . import sgtypes

class Base(DeclarativeBase):
    pass

class SchemaType(Enum):
    SG = 1
    JSON = 2

TABLE_IGNORE_LIST = [] # ["AppWelcome", "Banner"]
FIELD_IGNORE_LIST = [] # ["image_source_entity"]

SQLITE_MEMORY_SQA_URL = "sqlite+pysqlite:///:memory:"

DEFAULT_SCHEMA_TYPE = SchemaType.JSON
DEFAULT_SCHEMA_FILE = "schema.json"
DEFAULT_SQA_URL = "sqlite+pysqlite:///:memory:"
DEFAULT_OUT_SCRIPT = "sgmodel.py"

DEFAULT_GENERATOR_CLASS = generators.DeclarativeGenerator

class SGORM:
    
    SCHEMA_TYPES = ""
    def __init__(self, sg_schema_type=DEFAULT_SCHEMA_TYPE, sg_schema_source=DEFAULT_SCHEMA_FILE, ignored_tables=TABLE_IGNORE_LIST, ignored_fields=FIELD_IGNORE_LIST, echo=True):


        if (not sg_schema_type):
            sg_schema_type = DEFAULT_SCHEMA_TYPE
        if (not sg_schema_source):
            sg_schema_source = DEFAULT_SCHEMA_FILE
        self.sg_schema_type = sg_schema_type
        self.sg_schema_source = sg_schema_source

        self.echo = echo

        if (not ignored_tables):
            ignored_tables = TABLE_IGNORE_LIST
        if (not ignored_fields):
            ignored_fields = FIELD_IGNORE_LIST

        self.ignored_tables = ignored_tables
        self.ignored_fields = ignored_fields

        # read the SG schema0
        self.sg_schema = self.read_sg_schema()

        # create classes
        self.classes, self.tables = self.create_sg_classes()

        # create in-memory engine so that classes can be reflected
        self.engine = create_engine(SQLITE_MEMORY_SQA_URL, echo=self.echo)

        # if (drop_all):
        #     self.info("dropping all tables")
        #     Base.metadata.drop_all(bind=self.engine)

        # create the ORM
        self.session = self.create_sg_orm()

        self.Base = Base

        # self.create_script(out_script)

    def __getitem__(self, class_name):
        return self.classes.get(str(class_name))

    def get(self, class_name, default=None):
        return self.classes.get(str(class_name), default)

    def info(self, message, color=None, echo=None):
        if (not echo):
            echo = self.echo

        if (echo):
            print(message)

    def create_sg_orm(self):            
        Base.metadata.create_all(self.engine)
        session = Session(self.engine)
        return session

    def read_sg_schema(self):
        sg_schema = {}
        if (self.sg_schema_type == SchemaType.JSON and os.path.isfile(self.sg_schema_source)):
            with open(self.sg_schema_source, "r") as f:
                sg_schema = json.load(f)
        return sg_schema

    def create_sg_classes(self):

        classes = {}
        tables = {}
        for table in self.sg_schema:
            self.info(f"TABLE {table}")

            if (table in self.ignored_tables):
                self.info(f"ignoring table: {table}")
                continue

            t_def = self.sg_schema.get(table)
            if (not t_def):
                self.info(f"NO definition for table: {table}")
                continue

            if (table not in tables):
                tables[table] = {}

            t_namespace = tables[table].get("namespace")
            if (type(t_namespace) is not dict):
                t_namespace = { "__tablename__": table }
            t_annotations = tables[table].get("annotations")
            if (type(t_annotations) is not dict):
                t_annotations = {}

            tables[table]["definition"] = t_def

            fields = t_def.get("fields")
            for field in fields:

                if (field in self.ignored_fields):
                    self.info(f"ignoring field: {field}")
                    continue

                field_code = field
                if (field == "metadata"):
                    field_code = f"_{field}"

                field_def = fields.get(field)
                field_name = field_def.get("name")
                field_name_value = field_name.get("value")
                field_type = field_def.get("data_type")
                field_type_value = field_type.get("value")
                field_mandatory = field_def.get("manditory")
                field_unique = field_def.get("unique")
                field_entity_type = field_def.get("entity_type")
                field_custom_metadata = field_def.get("custom_metadata")
                field_properties = field_def.get("properties")
                field_default = field_properties.get("default_value")
                field_default_value = field_default.get("value")
                field_valid_values = field_properties.get("valid_values")
                field_valid_types = field_properties.get("valid_types")

                self.info(f"==> {field_code} ({field_type_value})")

                if (field_code == "id"):
                    self.info("* id field")
                    t_annotations[field_code] = Mapped[int]
                    t_namespace[field_code] = mapped_column(primary_key=True, autoincrement=False)

                else:
                    if (field_type_value in ["entity", "multi_entity"]):
                        self.info(f"* {field_type_value} field")                        
                        if (field_valid_types and field_valid_types.get("value")):
                            v_tables = field_valid_types.get("value")

                            if (field_type_value == "entity"):
                                # singe entity
                                if (len(v_tables) == 1):

                                    v_table = v_tables[0]
                                    if (v_table in self.ignored_tables):
                                        self.info(f"ignoring v_table: {v_table}")
                                        continue

                                    # table points to ONE type of v_table - need foreign key TO v_table
                                    foreign_field_code = f"{v_table}_{field_code}_id"
                                    t_annotations[foreign_field_code] = Mapped[Optional[int]] 
                                    # t_namespace[foreign_field_code] =  mapped_column(ForeignKey(f"{v_tables}.id")) #TODO

                                else:
                                    # table points to MANY types of v_table - need an id and type TO v_table
                                    # "number": {"hint": Mapped[int], "type": mapped_column(Integer)},
                                    self.info(f"assigning annotation for {field_code}_id")
                                    t_annotations[f"{field_code}_id"] = Mapped[Optional[int]] 
                                    # self.info(f"assigning namespace for {field_code}_id")
                                    # t_namespace[f"{field_code}_id"] = mapped_column(Integer)
                                    self.info(f"assigning annotation for {field_code}_type")
                                    t_annotations[f"{field_code}_type"] = Mapped[Optional[str]] 
                                    self.info(f"assigning namespace for {field_code}_type")
                                    # t_namespace[f"{field_code}_type"] = mapped_column(String)
                                    # self.info(f"done assigning field {field_code} to id and type")

                            else:
                                # multi entity
                                if (len(v_tables) == 1):

                                    v_table = v_tables[0]
                                    if (v_table in self.ignored_tables):
                                        self.info(f"ignoring v_table: {v_table}")
                                        continue

                                    if (v_table not in tables):
                                        tables[v_table] = {}

                                    v_namespace = tables[v_table].get("namespace")
                                    if (type(v_namespace) is not dict):
                                        v_namespace = { "__tablename__": v_table }
                                        
                                    v_annotations = tables[v_table].get("annotations")
                                    if (type(v_annotations) is not dict):
                                        v_annotations = {}

                                    # table points to ONE type of v_table - need foreign key FROM v_table
                                    foreign_field_code = f"{table}_{field_code}_id"
                                    if (not v_annotations.get(foreign_field_code) and not t_namespace.get(foreign_field_code)):
                                        # add to 
                                        v_annotations[foreign_field_code] = Mapped[Optional[int]] 
                                        # v_namespace[foreign_field_code] =  mapped_column(ForeignKey(f"{table}.id")) # TODO

                                    tables[v_table]["namespace"] = v_namespace
                                    tables[v_table]["annotations"] = v_annotations

                                # unsupported case? (because of multipe v_tables that we would need to point back to table)
                                # else:
                                #     # table points to MANY types of v_table - need an id and type FROM v_table
                                #     # "number": {"hint": Mapped[int], "type": mapped_column(Integer)},
                                #     self.info(f"assigning annotation for {field_code}_id")
                                #     v_annotations[f"{field_code}_id"] = Mapped[int] 
                                #     self.info(f"assigning namespace for {field_code}_id")
                                #     v_namespace[f"{field_code}_id"] = mapped_column(Integer)
                                #     self.info(f"assigning annotation for {field_code}_type")
                                #     v_annotations[f"{field_code}_type"] = Mapped[str] 
                                #     self.info(f"assigning namespace for {field_code}_type")
                                #     v_namespace[f"{field_code}_type"] = mapped_column(String)
                                #     self.info(f"done assigning field {field_code} to id and type")

                    else:
                        self.info(f"* {field_type_value} field")
                        if (field_type_value in list(sgtypes.sg_types.keys())):
                            self.info(f"assigning annotation for {field_code}")
                            t_annotations[field_code] = copy.deepcopy(sgtypes.sg_types_optional.get(field_type_value).get("hint")) 
                            # self.info(f"assigning namespace for {field_code}")
                            # t_namespace[field_code] = copy.deepcopy(sgtypes.sg_types.get(field_type_value).get("type"))
                            self.info("done assigning normal type")
                        else:
                            self.info(f"{field_type_value} unsupported")

            tables[table]["annotations"] = t_annotations
            tables[table]["namespace"] = t_namespace


        for node in tables:
            self.info(f"setting annotations in namespace for {node}")

            t_namespace = tables[node]["namespace"]
            t_annotations = tables[node]["annotations"]
            t_namespace["__annotations__"] = t_annotations

            try:
                self.info(f"creating class {node}")
                TClass = type(node, (Base, ), t_namespace)

                self.info(f"adding class {node}")
                tables[node]["class"] = TClass
                classes[node] = TClass

            except Exception as error:
                self.info(f"Error creating type {node}: {error}")
                self.info(traceback.format_exc())

        return classes, tables

    def create_script(self, out_script=DEFAULT_OUT_SCRIPT, generator_class=DEFAULT_GENERATOR_CLASS):

        if (not out_script):
            out_script = DEFAULT_OUT_SCRIPT
        if (not generator_class):
            generator_class = DEFAULT_GENERATOR_CLASS

        gen = generator_class(Base.metadata, self.engine, [])
        code = gen.generate()
        with open(out_script, "w") as f:
            # ensures no auto-increment since we are using SG's id's
            code = code.replace("id = mapped_column(Integer, primary_key=True)", "id = mapped_column(Integer, primary_key=True, autoincrement=False)")

            code += """

########################################
# generated classes dict for easy access
########################################
import inspect
CLASSES = {n: c for n, c in globals().copy().items() if inspect.isclass(c) }

"""
            f.write(code)

