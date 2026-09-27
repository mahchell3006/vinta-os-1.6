"""Create (or remove) one group with no capacity set, for the Classrooms check.

Throwaway. A capacity of 0 is the case the card used to read as a full room, so
the only way to see the fix is to have such a group on screen — and the only safe
way to have one is to make it, look, and delete it by id.
"""
import os
import sys
import uuid

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.class_room import Class  # noqa: E402

ACADEMY = "ad6587d5-6fd3-4015-a497-8dd5301b830d"
NAME = "ZZ No Capacity (throwaway)"
ID = "zz-capacity-probe"

app = create_app("development")
action = sys.argv[1] if len(sys.argv) > 1 else "make"

with app.app_context():
    if action == "make":
        if db.session.get(Class, ID):
            print("already exists:", ID)
            sys.exit(0)
        db.session.add(Class(id=ID, academy_id=ACADEMY, name=NAME, capacity=0))
        db.session.commit()
        c = db.session.get(Class, ID)
        print(f"created: {c.id}  {c.name!r}  capacity={c.capacity}")
    else:
        c = db.session.get(Class, ID)
        if c is None:
            print("nothing to remove")
            sys.exit(0)
        print(f"removing: {c.id}  {c.name!r}  capacity={c.capacity}")
        db.session.query(Class).filter(Class.id == ID).delete(synchronize_session=False)
        db.session.commit()
        print("gone:", db.session.get(Class, ID) is None)
