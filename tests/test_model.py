from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import sgmodel

engine = create_engine("sqlite+pysqlite:///test_model.db", echo=False)
engine.connect()
session = Session(engine)

asset = sgmodel.Asset()
asset.id = 1

asset = session.execute(select(sgmodel.Asset).where(sgmodel.Asset.id == 1)).scalar_one_or_none()
if asset:
    print(f"deleting asset id: {asset.id}, code: {asset.code}")
    session.delete(asset)
    session.flush()
    session.commit()

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

changed_asset = session.execute(select(sgmodel.Asset).where(sgmodel.Asset.id == new_asset.id)).scalar_one()
print(f"updated asset id: {changed_asset.id}, code: {changed_asset.code}")


# import inspect
# members = inspect.getmembers(sgmodel, inspect.isclass)
# for m in members:
#     print(m)

# for c in sgmodel.classes:
#     print(c)


shot_class = sgmodel.CLASSES.get("Shot")
print(f"shot_class: {shot_class}")

shot = session.execute(select(shot_class).where(shot_class.id == 1)).scalar_one_or_none()
if shot:
    print(f"deleting shot id: {shot.id}, code: {shot.code}")
    session.delete(shot)
    session.flush()
    session.commit()


# this is important for dynamcially setting SG data
args = {"id": 1, "code": "TestShot"}
new_shot = shot_class(**args)
# new_shot = shot_class(id=1, code="TestShot")
# new_shot.id = 1
# new_shot.code = "TestShot"
session.add(new_shot)
print(f"sesion new shot: {session.new}")
session.flush()

print(f"new shot id: {new_shot.id}, code: {new_shot.code}")
session.commit()

session.close()
