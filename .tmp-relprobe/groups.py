"""Name every group with its capacity and enrollment count.

Throwaway. The capacity is printed raw so a probe group can be told apart from a
real one, and so the restore after a probe can be checked by number, not by eye.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.student import Enrollment  # noqa: E402

app = create_app("development")
ACADEMY = "ad6587d5-6fd3-4015-a497-8dd5301b830d"
with app.app_context():
    for c in db.session.query(Class).filter_by(academy_id=ACADEMY).all():
        n = db.session.query(Enrollment).filter_by(class_id=c.id).count()
        print(f"  {c.id}  {c.name!r:14s} subject={c.subject!r:10s} capacity={c.capacity!r} enrolled={n}")
