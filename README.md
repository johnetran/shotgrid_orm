# Shotgrid SQAlchemy ORM Generator

This tool generates a SQAlchemy ORM for a Shotgrid schema for the purposes of reporting, BI, datawarehousing, etc.  It does not generate foreign keys and primary keys are not auto-increment.  This allows maximum freedom to transfer data from Shotgrid into a target database, retaining its native primary keys (ids).

```python
from shotgrid_orm import SGORM
sg_orm = SGORM(sqa_url="sqlite+pysqlite:///test.db", drop_all=True, echo=True)
print("creating python script")
sg_orm.create_script("sgmodel3.py")
Shot = sg_orm.classes.get("Shot")
```
