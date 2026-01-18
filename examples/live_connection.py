"""
Live Connection Example

This example demonstrates how to:
1. Connect to a live Shotgrid instance
2. Download the schema directly from Shotgrid
3. Generate ORM classes from the live schema

NOTE: This requires valid Shotgrid credentials set as environment variables:
  - SG_URL: Your Shotgrid site URL (e.g., https://mystudio.shotgunstudio.com)
  - SG_SCRIPT: Your script name
  - SG_API_KEY: Your API key
"""

import os

from shotgrid_orm import SGORM, SchemaType

# Check if credentials are set
if not all([os.getenv("SG_URL"), os.getenv("SG_SCRIPT"), os.getenv("SG_API_KEY")]):
    print("ERROR: Missing required environment variables")
    print("Please set: SG_URL, SG_SCRIPT, SG_API_KEY")
    print()
    print("Example:")
    print('  export SG_URL="https://mystudio.shotgunstudio.com"')
    print('  export SG_SCRIPT="my_script_name"')
    print('  export SG_API_KEY="your_api_key_here"')
    exit(1)

# Initialize SGORM with live connection
print("Connecting to Shotgrid...")
sg_orm = SGORM(
    sg_schema_type=SchemaType.SG_SCRIPT,
    sg_schema_source={"url": os.getenv("SG_URL"), "script": os.getenv("SG_SCRIPT"), "api_key": os.getenv("SG_API_KEY")},
    echo=False,
)

print(f"Connected! Found {len(sg_orm.classes)} entity types")
print()

# List all entity types
print("Available entity types:")
for entity_name in sorted(sg_orm.classes.keys())[:10]:  # Show first 10
    print(f"  - {entity_name}")
print(f"  ... and {len(sg_orm.classes) - 10} more")
print()

# Generate standalone script from live schema
print("Generating ORM script from live schema...")
sg_orm.create_script("live_sgmodel.py")
print("Created: live_sgmodel.py")
print()

# You can now use this script to create databases, query data, etc.
print("You can now use the generated ORM:")
print("  from live_sgmodel import Shot, Asset, Project, CLASSES")
