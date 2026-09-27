"""Every teacher row, with what points at it.

Throwaway. Printed so the probe rows can be named by id before anything is
deleted — a teacher with sessions cannot simply be removed, and the count is what
says whether that is the case.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Schedule, Session  # noqa: E402
from app.models.teacher import Teacher  # noqa: E402

app = create_app("development")
with app.app_context():
    rows = db.session.query(Teacher).order_by(Teacher.created_at.desc()).all()
    print(f"teachers: {len(rows)}")
    for t in rows:
        groups = db.session.query(Class).filter_by(teacher_id=t.id).all()
        print(f"  {t.id}  {t.first_name!r} {t.last_name!r}  email={t.email!r}  status={t.status}  created={t.created_at}")
        for g in groups:
            scheds = db.session.query(Schedule).filter_by(class_id=g.id).count()
            sess = db.session.query(Session).filter_by(class_id=g.id).count()
            print(f"      group {g.id} {g.name!r} schedules={scheds} sessions={sess}")
