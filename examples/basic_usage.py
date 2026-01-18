"""
Basic Usage Example

This example demonstrates how to:
1. Load a Shotgrid schema from a JSON file
2. Generate SQLAlchemy ORM classes dynamically
3. Access entity classes
4. Export the ORM to a standalone Python script
"""

from shotgrid_orm import SGORM, SchemaType

# Initialize SGORM with a JSON schema file
sg_orm = SGORM(
    sg_schema_type=SchemaType.JSON_FILE,
    sg_schema_source="example_schema.json",
    echo=False,  # Set to True to see SQL echoed
)

# Access entity classes using dictionary notation
Shot = sg_orm["Shot"]
Asset = sg_orm["Asset"]
Project = sg_orm["Project"]

# Inspect the Shot class
print("Shot class attributes:")
print([attr for attr in dir(Shot) if not attr.startswith("_")])
print()

# View the classes dictionary
print("Available entity classes:")
print(list(sg_orm.classes.keys()))
print()

# Export ORM to a standalone Python script
print("Generating standalone ORM script: example_sgmodel.py")
sg_orm.create_script("example_sgmodel.py")
print("Script created! You can now use 'example_sgmodel.py' independently.")
