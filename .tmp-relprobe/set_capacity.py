"""Set one group's capacity, printing before and after.

Throwaway, used only to make a probe group refuse an enrollment so the Add
Student modal's refusal path can be driven from the browser. Names the row it
touched and prints both values, because a restore that is not checked by number
is not a restore.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.class_room import Class  # noqa: E402

CLASS_ID = sys.argv[1]
NEW = int(sys.argv[2])

app = create_app("development")
with app.app_context():
    c = db.session.get(Class, CLASS_ID)
    if c is None:
        print("no such class:", CLASS_ID)
        sys.exit(1)
    before = c.capacity
    c.capacity = NEW
    db.session.commit()
    after = db.session.get(Class, CLASS_ID).capacity
    print(f"{CLASS_ID}  {c.name!r}  capacity {before} -> {after}")
