

from shotgrid_orm import SGORM

sg_orm = SGORM(sqa_url="sqlite+pysqlite:///test.db", echo=True)
# shot_class = sg_orm["Shot"]
shot_class = sg_orm.get("Shot")
print(shot_class)

