"""
Create Database Example

This example demonstrates how to:
1. Load a Shotgrid schema
2. Create a SQLite database with all tables
3. Insert sample data
4. Query the data
"""

from shotgrid_orm import SGORM, SchemaType
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Initialize SGORM
sg_orm = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source="example_schema.json", echo=False)

# Get entity classes
Project = sg_orm["Project"]
Sequence = sg_orm["Sequence"]
Shot = sg_orm["Shot"]
Asset = sg_orm["Asset"]

# Create SQLite database engine
print("Creating database engine...")
engine = create_engine("sqlite:///example_shotgrid.db", echo=False)

# Create all tables
print("Creating all tables...")
sg_orm.Base.metadata.create_all(engine)
print(f"Created {len(sg_orm.Base.metadata.tables)} tables")
print()

# Insert sample data
print("Inserting sample data...")
session = Session(engine)

# Create a project
project = Project()
project.id = 1
project.code = "DEMO"
project.name = "Demo Project"
session.add(project)

# Create sequences
seq1 = Sequence()
seq1.id = 100
seq1.code = "SEQ010"
seq1.project_id = 1
seq1.project_type = "Project"
session.add(seq1)

seq2 = Sequence()
seq2.id = 101
seq2.code = "SEQ020"
seq2.project_id = 1
seq2.project_type = "Project"
session.add(seq2)

# Create shots
for i, code in enumerate(["010", "020", "030"], start=1):
    shot = Shot()
    shot.id = 1000 + i
    shot.code = f"SEQ010_{code}"
    shot.description = f"Shot {code}"
    shot.project_id = 1
    shot.project_type = "Project"
    shot.sg_sequence_id = 100
    shot.sg_sequence_type = "Sequence"
    session.add(shot)

# Create assets
for i, code in enumerate(["CHAR_HERO", "PROP_TABLE", "ENV_CITY"], start=1):
    asset = Asset()
    asset.id = 2000 + i
    asset.code = code
    asset.description = f"Asset {code}"
    asset.project_id = 1
    asset.project_type = "Project"
    session.add(asset)

# Commit the transaction
session.commit()
print(f"Inserted {len(session.new)} records")
print()

# Query and display data
print("Projects:")
for proj in session.query(Project).all():
    print(f"  [{proj.id}] {proj.code}: {proj.name}")
print()

print("Sequences:")
for seq in session.query(Sequence).all():
    print(f"  [{seq.id}] {seq.code}")
print()

print("Shots:")
for shot in session.query(Shot).all():
    print(f"  [{shot.id}] {shot.code}: {shot.description}")
print()

print("Assets:")
for asset in session.query(Asset).all():
    print(f"  [{asset.id}] {asset.code}: {asset.description}")
print()

session.close()
print("Database created successfully: example_shotgrid.db")
