"""Create (or remove) one weekly group with NO schedule, for the ClassDetail check.

Throwaway. A group with no slots is exactly the state the old "Dedicated Time"
box left behind — it looks configured and produces no sessions — so it is the
case the new Meets On / Start At / End At fields exist to fix. Making one is the
only safe way to look at it; it is deleted by id afterwards.
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
from app.models.student import Enrollment  # noqa: E402

ACADEMY = "ad6587d5-6fd3-4015-a497-8dd5301b830d"
ID = "zz-timeless-probe"

app = create_app("development")
action = sys.argv[1] if len(sys.argv) > 1 else "make"

with app.app_context():
    if action == "make":
        if db.session.get(Class, ID):
            print("already exists:", ID)
            sys.exit(0)
        db.session.add(Class(
            id=ID,
            academy_id=ACADEMY,
            name="ZZ Timeless (throwaway)",
            subject="Math",
            capacity=10,
            class_type="weekly",
        ))
        db.session.commit()
        c = db.session.get(Class, ID)
        print(f"created: {c.id}  {c.name!r}  capacity={c.capacity}  class_type={c.class_type}")
        print(f"  schedules={Schedule.query.filter_by(class_id=ID).count()}"
              f"  sessions={Session.query.filter_by(class_id=ID).count()}")
    else:
        c = db.session.get(Class, ID)
        if c is None:
            print("nothing to remove")
            sys.exit(0)
        schedules = Schedule.query.filter_by(class_id=ID).all()
        sessions = Session.query.filter_by(class_id=ID).all()
        print(f"removing: {c.id}  {c.name!r}")
        for s in schedules:
            print(f"  schedule {s.id}  dow={s.day_of_week} {s.start_time}-{s.end_time}")
        for s in sessions:
            print(f"  session  {s.id}  {s.date} {s.start_time}-{s.end_time}  status={s.status}")
        print(f"  enrollments={Enrollment.query.filter_by(class_id=ID).count()}")
        for s in sessions:
            db.session.delete(s)
        for s in schedules:
            db.session.delete(s)
        db.session.delete(c)
        db.session.commit()
        print("gone:", db.session.get(Class, ID) is None,
              "| schedules left:", Schedule.query.filter_by(class_id=ID).count(),
              "| sessions left:", Session.query.filter_by(class_id=ID).count())
