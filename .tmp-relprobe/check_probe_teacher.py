"""Inspect the teacher the Add Teacher form just created.

Throwaway. Prints the row, its groups, those groups' schedules, and how many
sessions the schedule generated — the four things the form is supposed to cause.
An empty schedule is the failure this check exists for.
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

NAME = "EmailOptional"

app = create_app("development")
with app.app_context():
    teachers = db.session.query(Teacher).filter_by(last_name=NAME).all()
    print(f"teachers matching last_name={NAME!r}: {len(teachers)}")
    for t in teachers:
        print(f"  {t.id}  {t.first_name!r} {t.last_name!r}  email={t.email!r}  phone={t.phone!r}  status={t.status}")
        classes = db.session.query(Class).filter_by(teacher_id=t.id).all()
        print(f"    groups: {len(classes)}")
        for c in classes:
            scheds = db.session.query(Schedule).filter_by(class_id=c.id).all()
            sess = db.session.query(Session).filter_by(class_id=c.id).count()
            print(f"      {c.id}  {c.name!r}  capacity={c.capacity}  class_type={c.class_type}  dedicated_time={c.dedicated_time!r}")
            print(f"        schedules={len(scheds)} sessions={sess}")
            for s in scheds:
                print(f"          dow={s.day_of_week} {s.start_time}–{s.end_time}")
