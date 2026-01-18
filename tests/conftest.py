"""Pytest configuration and fixtures for shotgrid_orm tests."""

import shutil
from pathlib import Path

import pytest
from shotgrid_orm import SGORM, SchemaType


@pytest.fixture(scope="session")
def example_schema_path():
    """Provide path to example schema file."""
    return Path(__file__).parent.parent / "examples" / "example_schema.json"


@pytest.fixture(scope="session")
def temp_dir(tmp_path_factory):
    """Provide a temporary directory for test files."""
    return tmp_path_factory.mktemp("shotgrid_orm_tests")


@pytest.fixture(scope="session")
def schema_file(example_schema_path, temp_dir):
    """Copy example schema to temp directory for tests."""
    schema_dest = temp_dir / "schema.json"
    shutil.copy(example_schema_path, schema_dest)
    yield schema_dest


@pytest.fixture(scope="session")
def sg_orm(schema_file):
    """Provide a configured SGORM instance for testing.

    Session-scoped to avoid Base class conflicts when creating
    multiple SGORM instances with the same entity names.
    """
    # Use absolute path to schema file
    return SGORM(sg_schema_type=SchemaType.JSON_FILE, sg_schema_source=str(schema_file.absolute()), echo=False)


@pytest.fixture(scope="function")
def test_db_path(tmp_path):
    """Provide path for test database.

    Function-scoped to ensure each test gets a fresh database.
    """
    return str(tmp_path / "test.db")
