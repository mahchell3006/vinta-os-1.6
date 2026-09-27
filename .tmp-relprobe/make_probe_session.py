"""Create (or remove) one throwaway session for the live Classrooms check.

A real tenant is the only honest place to test start/extend/void, because the
whole point of those paths is what they write into the register and the log. So
this makes one session far enough out that no real class is anywhere near it,
and records its id in probe_session_id.txt so the removal is exact rather than a
guess at which row was the probe.

  py make_probe_session.py make     -> create, print the id, record it
  py make_probe_session.py remove   -> delete it, its register rows and its log
"""
import os
import sys
from datetime import date, time

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
RECORD = r"E:\vinta-os-app-essembled-main\.tmp-relprobe\probe_session_id.txt"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.audit import ActivityLog  # noqa: E402
from app.models.attendance import SessionStudent  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Session  # noqa: E402

GROUP_A = "a41fd3be-807b-45ad-b298-69edb7a0ac21"
# A Wednesday in December: past the 12-week generation horizon of the group's
# schedule, so starting and cancelling it cannot collide with a real class.
PROBE_DATE = date(2026, 12, 30)

app = create_app("development")
action = sys.argv[1] if len(sys.argv) > 1 else "make"

with app.app_context():
    if action == "make":
        g = db.session.get(Class, GROUP_A)
        if not g:
            sys.exit("no Group A")
        s = Session(
            id="zz-probe-session",
            academy_id=g.academy_id,
            class_id=g.id,
            schedule_id=None,
            teacher_id=g.teacher_id,
            classroom_id=None,
            date=PROBE_DATE,
            start_time=time(10, 0),
            end_time=time(11, 30),
            subject=g.subject,
            status="scheduled",
        )
        db.session.add(s)
        db.session.commit()
        with open(RECORD, "w", encoding="utf-8") as fh:
            fh.write(s.id)
        print("created:", s.id, s.date.isoformat(), s.start_time, "-", s.end_time)
    else:
        with open(RECORD, encoding="utf-8") as fh:
            sid = fh.read().strip()
        reg = db.session.query(SessionStudent).filter_by(session_id=sid).delete(
            synchronize_session=False
        )
        logs = db.session.query(ActivityLog).filter_by(entity_id=sid).delete(
            synchronize_session=False
        )
        n = db.session.query(Session).filter_by(id=sid).delete(synchronize_session=False)
        db.session.commit()
        print(f"removed session={n} register_rows={reg} log_rows={logs}")
