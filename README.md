# Shotgrid ORM Generator
## For Autodesk Flow Production Tracking system (formerly Shotgun/Shotgrid - SG)

This tool generates a SQAlchemy ORM for a Shotgrid schema for the purposes of reporting, BI, datawarehousing, etc.  It does not generate foreign keys and primary keys are not auto-increment.  This allows maximum freedom to transfer data from Shotgrid into a target database, retaining its native primary keys (ids).

```python
import os
from shotgrid_orm import SGORM, SchemaType

# Create model script

# option 1: create python script from JSON schema file
sg_orm = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source="schema.json", echo=ECHO)
print("creating python script")
sg_orm.create_script("sgmodel.py")
Shot = sg_orm.classes.get("Shot")

# option 2: create python script from live connection using SCRIPT KEY
sg_orm = SGORM(sg_schema_type=SchemaType.SG_SCRIPT, sg_schema_source={"url": os.getenv("SG_URL"), "script": os.getenv("SG_SCRIPT"), "api_key": os.getenv("SG_API_KEY")}, echo=ECHO)
print("creating python script")
sg_orm.create_script("sgmodel.py")
Shot = sg_orm.classes.get("Shot")

###

from sqlalchemy import create_engine

# create database from orm
print("creating engine and session to Sqlite db")
engine = create_engine("sqlite+pysqlite:///sgmodel.db", echo=ECHO)

print("dropping all tables")
sg_orm.Base.metadata.drop_all(bind=engine)

print("creating all tables")
sg_orm.Base.metadata.create_all(engine)

###

# manipulating records

from sqlalchemy.orm import Session
from sqlalchemy import select
import sgmodel # created in the create model script step

engine.connect()
session = Session(engine)

asset = sgmodel.Asset()
asset.id = 1

# query an asset
asset = session.execute(select(sgmodel.Asset).where(sgmodel.Asset.id==1)).scalar_one_or_none()
if (asset):
    print(f"deleting asset id: {asset.id}, code: {asset.code}")
    session.delete(asset)
    session.flush()
    session.commit()

# create a new asset
new_asset = sgmodel.Asset()
new_asset.id = 1
new_asset.code = "TestAsset"

session.add(new_asset)
print(f"sesion new asset: {session.new}")
session.flush()

print(f"new asset id: {new_asset.id}, code: {new_asset.code}")
session.commit()

new_asset.code = "UpdatedAssetName"
session.commit()

changed_asset = session.execute(select(sgmodel.Asset).where(sgmodel.Asset.id==new_asset.id)).scalar_one()
print(f"updated asset id: {changed_asset.id}, code: {changed_asset.code}")

shot_class = sgmodel.CLASSES.get("Shot")
print(f"shot_class: {shot_class}")

shot = session.execute(select(shot_class).where(shot_class.id==1)).scalar_one_or_none()
if (shot):
    print(f"deleting shot id: {shot.id}, code: {shot.code}")
    session.delete(shot)
    session.flush()
    session.commit()

# this is important for dynamcially setting SG data
args = {"id": 1, "code": "TestShot"}
new_shot = shot_class(**args)
# other methods:
# new_shot = shot_class(id=1, code="TestShot")
# new_shot.id = 1
# new_shot.code = "TestShot"

session.add(new_shot)
print(f"sesion new shot: {session.new}")
session.flush()

print(f"new shot id: {new_shot.id}, code: {new_shot.code}")
session.commit()

session.close()


```
