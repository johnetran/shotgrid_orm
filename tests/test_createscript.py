import os

from shotgrid_orm import SGORM, SchemaType

ECHO = False

# create python script from JSON schema file
# sg_orm = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source="schema.json", echo=ECHO)
# print("creating python script")
# sg_orm.create_script("sgmodel.py")

# create python script from live connection using SCRIPT KEY
sg_orm = SGORM(
    sg_schema_type=SchemaType.SG_SCRIPT,
    sg_schema_source={"url": os.getenv("SG_URL"), "script": os.getenv("SG_SCRIPT"), "api_key": os.getenv("SG_API_KEY")},
    echo=ECHO,
)
print("creating python script")
sg_orm.create_script("sgmodel.py")
