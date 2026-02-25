"""Tests for SGORM class and basic ORM functionality."""

import warnings

from sqlalchemy import create_engine, inspect, select
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import Session

from shotgrid_orm import SGORM, SchemaType


def test_sgorm_initialization(sg_orm):
    """Test that SGORM can be initialized from JSON schema."""
    assert sg_orm is not None
    assert hasattr(sg_orm, "Base")


def test_get_entity_class(sg_orm):
    """Test retrieving entity classes from SGORM."""
    Shot = sg_orm["Shot"]
    assert Shot is not None
    assert hasattr(Shot, "__tablename__")


def test_create_script(sg_orm, temp_dir):
    """Test creating a Python script from schema."""
    script_path = temp_dir / "sgmodel.py"
    sg_orm.create_script(str(script_path))
    assert script_path.exists()
    assert script_path.stat().st_size > 0


def test_create_database_tables(sg_orm, test_db_path):
    """Test creating database tables from schema."""
    engine = create_engine(f"sqlite+pysqlite:///{test_db_path}", echo=False)

    # Create tables
    sg_orm.Base.metadata.create_all(engine)

    # Verify tables were created
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    assert "Shot" in table_names
    assert "Asset" in table_names
    assert "Project" in table_names


def test_crud_operations(sg_orm, test_db_path):
    """Test basic CRUD operations with generated ORM."""
    engine = create_engine(f"sqlite+pysqlite:///{test_db_path}", echo=False)
    sg_orm.Base.metadata.create_all(engine)

    Shot = sg_orm["Shot"]
    session = Session(engine)

    # Create shots
    shots_to_create = []
    for shot_id in range(1, 5):
        shot = Shot()
        shot.id = shot_id
        shot.code = f"SHOT_{shot_id:03d}"
        shots_to_create.append(shot)
        session.add(shot)

    session.flush()

    # Read - get specific shot
    retrieved_shot = session.get(Shot, 3)
    assert retrieved_shot is not None
    assert retrieved_shot.id == 3
    assert retrieved_shot.code == "SHOT_003"

    # Commit
    session.commit()

    # Query all shots
    all_shots = session.execute(select(Shot)).scalars().all()
    assert len(all_shots) == 4

    # Query with where clause
    specific_shot = session.execute(select(Shot).where(Shot.id == 2)).scalar_one()
    assert specific_shot.id == 2
    assert specific_shot.code == "SHOT_002"

    session.close()


def test_schema_types_support(sg_orm):
    """Test that schema was loaded successfully."""
    # Verify SGORM instance was created
    assert sg_orm is not None

    # Verify we can get entity classes
    Project = sg_orm["Project"]
    assert Project is not None
    assert hasattr(Project, "__tablename__")


def test_multiple_instantiations_no_warning(schema_file):
    """SGORM must be safe to instantiate multiple times in the same process.

    Each instance should have its own DeclarativeBase so SQLAlchemy never
    emits SAWarning about duplicate class names, and entity lookups must
    return valid classes for every instance.
    """
    orm1 = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source=str(schema_file.absolute()), echo=False)

    with warnings.catch_warnings():
        warnings.simplefilter("error", SAWarning)
        orm2 = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source=str(schema_file.absolute()), echo=False)

    # Both instances must resolve entity classes successfully.
    assert orm1["Shot"] is not None
    assert orm2["Shot"] is not None

    # The two instances must have independent class registries.
    assert orm1["Shot"] is not orm2["Shot"]
    assert orm1.Base is not orm2.Base
