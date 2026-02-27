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


def test_entity_field_columns(sg_orm):
    """entity fields with a single valid type produce {field}_id (with FK) but NO {field}_type column."""
    Shot = sg_orm["Shot"]
    assert hasattr(Shot, "project_id")
    # Single valid type -> no _type column
    assert not hasattr(Shot, "project_type")
    # Old cross-table name must NOT exist
    assert not hasattr(Shot, "Project_project_id")


def test_multi_entity_field_columns(sg_orm):
    """multi_entity fields with a single valid type produce {field}_ids but NO {field}_type column."""
    Asset = sg_orm["Asset"]
    assert hasattr(Asset, "shots_ids")
    # Single valid type -> no _type column
    assert not hasattr(Asset, "shots_type")
    # Old cross-table injection must NOT exist on Shot
    Shot = sg_orm["Shot"]
    assert not hasattr(Shot, "Asset_shots_id")


def test_entity_field_single_valid_type_fk(sg_orm, test_db_path):
    """entity field with 1 valid type gets a FK constraint to that table."""
    from sqlalchemy import create_engine
    from sqlalchemy import inspect as sa_inspect

    engine = create_engine(f"sqlite+pysqlite:///{test_db_path}", echo=False)
    sg_orm.Base.metadata.create_all(engine)
    inspector = sa_inspect(engine)

    fks = inspector.get_foreign_keys("Shot")
    project_fks = [fk for fk in fks if "project_id" in fk["constrained_columns"]]
    assert len(project_fks) == 1
    assert project_fks[0]["referred_table"] == "Project"
    assert project_fks[0]["referred_columns"] == ["id"]


def test_entity_field_single_valid_type_no_type_col(sg_orm):
    """entity fields with exactly 1 valid type must not have a _type column."""
    Shot = sg_orm["Shot"]
    assert not hasattr(Shot, "project_type")
    assert not hasattr(Shot, "sg_sequence_type")


def test_entity_field_multi_valid_type_keeps_type_col(sg_orm):
    """entity field with >1 valid types gets _id + _type (polymorphic), no FK."""
    Asset = sg_orm["Asset"]
    assert hasattr(Asset, "entity_source_id")
    assert hasattr(Asset, "entity_source_type")


def test_entity_field_multi_valid_type_no_fk(sg_orm, test_db_path):
    """entity field with >1 valid types must NOT carry a FK constraint."""
    from sqlalchemy import create_engine
    from sqlalchemy import inspect as sa_inspect

    engine = create_engine(f"sqlite+pysqlite:///{test_db_path}", echo=False)
    sg_orm.Base.metadata.create_all(engine)
    inspector = sa_inspect(engine)

    fks = inspector.get_foreign_keys("Asset")
    entity_source_fks = [fk for fk in fks if "entity_source_id" in fk["constrained_columns"]]
    assert len(entity_source_fks) == 0


def test_multi_entity_field_single_valid_type_no_type_col(sg_orm):
    """multi_entity field with 1 valid type has _ids but no _type column."""
    Asset = sg_orm["Asset"]
    assert hasattr(Asset, "shots_ids")
    assert not hasattr(Asset, "shots_type")


def test_multi_entity_field_multi_valid_type_keeps_type_col(sg_orm):
    """multi_entity field with >1 valid types keeps _ids + _type columns."""
    Asset = sg_orm["Asset"]
    assert hasattr(Asset, "task_assignees_ids")
    assert hasattr(Asset, "task_assignees_type")


def test_dangling_fk_not_generated(tmp_path):
    """entity field whose single valid_type is absent from the schema must not emit a FK.

    Reproduces: 'Foreign key associated with column ... could not find table ...'
    which previously crashed metadata.create_all() for internal SG entities like
    AppWelcome that are referenced by other tables but not present in the schema.
    """
    import json

    schema = {
        "Child": {
            "name": {"visible": True},
            "fields": {
                "id": {
                    "data_type": {"value": "number"},
                    "editable": False,
                    "entity_type": {"value": "Child"},
                    "mandatory": {"value": False},
                    "name": {"value": "id"},
                    "properties": {"default_value": {"value": None}},
                    "unique": False,
                    "visible": {"value": True},
                },
                "ghost_link": {
                    # Single valid type that is NOT in this schema
                    "data_type": {"value": "entity"},
                    "editable": True,
                    "entity_type": {"value": "Child"},
                    "mandatory": {"value": False},
                    "name": {"value": "ghost_link"},
                    "properties": {
                        "default_value": {"value": None},
                        "valid_types": {"value": ["GhostEntity"]},
                    },
                    "unique": False,
                    "visible": {"value": True},
                },
            },
        }
    }

    schema_path = tmp_path / "schema.json"
    schema_path.write_text(json.dumps(schema))

    orm = SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source=str(schema_path), echo=False)

    # Must not raise when creating tables — no dangling FK
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    orm.Base.metadata.create_all(engine)  # Would raise before the fix

    # The column must exist but without a FK constraint
    inspector = inspect(engine)
    fks = inspector.get_foreign_keys("Child")
    ghost_fks = [fk for fk in fks if "ghost_link_id" in fk["constrained_columns"]]
    assert len(ghost_fks) == 0, "No FK should be generated for a target table absent from the schema"

    Child = orm["Child"]
    assert hasattr(Child, "ghost_link_id"), "ghost_link_id column must still be present"


def test_entity_field_fk_enforced_in_db(sg_orm, test_db_path):
    """FK constraints appear on single-type entity fields but not on multi-type fields."""
    from sqlalchemy import create_engine
    from sqlalchemy import inspect as sa_inspect

    engine = create_engine(f"sqlite+pysqlite:///{test_db_path}", echo=False)
    sg_orm.Base.metadata.create_all(engine)
    inspector = sa_inspect(engine)

    # Shot.project_id -> Project.id (single type)
    shot_fks = inspector.get_foreign_keys("Shot")
    project_fks = [fk for fk in shot_fks if "project_id" in fk["constrained_columns"]]
    assert len(project_fks) == 1, "Shot.project_id should have a FK to Project.id"
    assert project_fks[0]["referred_table"] == "Project"

    # Asset.entity_source_id has NO FK (multi-type)
    asset_fks = inspector.get_foreign_keys("Asset")
    entity_source_fks = [fk for fk in asset_fks if "entity_source_id" in fk["constrained_columns"]]
    assert len(entity_source_fks) == 0, "Asset.entity_source_id must NOT have a FK (polymorphic field)"
