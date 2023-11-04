
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from shotgrid_orm import SGORM, SchemaType

ECHO = False

sg_orm = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source="schema.json", echo=ECHO)

print("getting Shot class")
Shot = sg_orm["Shot"]

print("Shot fields:")
print(dir(Shot))

print("Shot class:")
print(Shot)

print("creating python script")
sg_orm.create_script("sgmodel2.py")

print("creating engine and session to Sqlite db")
engine = create_engine("sqlite+pysqlite:///test.db", echo=ECHO)
session = Session(engine)

print("dropping all tables")
sg_orm.Base.metadata.drop_all(bind=engine)

print("creating all tables")
sg_orm.Base.metadata.create_all(engine)


print("adding shot objects")
for id in range(1, 10):
    shot = Shot()
    shot.id = id
    shot.Asset_shots_id = random.randint(1, 100)
    session.add(shot)

print("shots in session")
print(session.new)

print("flushing session")
session.flush()

print("getting some shot")
some_shot = session.get(Shot, 3)
print(some_shot)

print("commiting shots to DB")
session.commit()

print("shots in session after committing")
print(session.new)

print("quering all shots")
shots = session.execute(select(Shot)).scalars().all()
for s in shots:
    print(f"{s.id}: {s.Asset_shots_id}")

print("query a shot using where clause")
first_shot = session.execute(select(Shot).where(Shot.id==5)).scalar_one()
print(f"{first_shot.id}: {first_shot.Asset_shots_id}")

shots = session.execute(select(Shot)).all()
for s in shots:
    print(s)
    print(s[0].Asset_shots_id)
    print(s[0].id)
    # print("shot data")
    # print(s._asdict()["Shot"].Asset_shots_id)

print("closing session")
session.close()

