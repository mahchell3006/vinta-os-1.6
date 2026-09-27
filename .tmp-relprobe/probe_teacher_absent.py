"""Second throwaway session, to check what "Teacher Absent" writes.

make/remove, same discipline as make_probe_session.py. This one exists only so a
cancellation with a reason lands on a row that is mine: the reason is the thing
under test, and a reason written onto the academy's own class would be a change
to real data for a labelling check.
"""
import os, sys, json
from datetime import date, time
BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND); sys.path.insert(0, BACKEND)
from app import create_app
from app.extensions import db
from app.models.attendance import SessionStudent
from app.models.audit import ActivityLog
from app.models.class_room import Class
from app.models.scheduling import Session

SID = "zz-probe-absent"
GROUP_A = "a41fd3be-807b-45ad-b298-69edb7a0ac21"
app = create_app("development")
action = sys.argv[1] if len(sys.argv) > 1 else "make"

with app.app_context():
    if action == "make":
        g = db.session.get(Class, GROUP_A)
        s = Session(
            id=SID, academy_id=g.academy_id, class_id=g.id, schedule_id=None,
            teacher_id=g.teacher_id, classroom_id=None, date=date(2026, 12, 30),
            start_time=time(10, 0), end_time=time(11, 30), subject=g.subject,
            status="scheduled",
        )
        db.session.add(s); db.session.commit()
        print("created:", s.id, s.date.isoformat())
    else:
        reg = db.session.query(SessionStudent).filter_by(session_id=SID).delete(synchronize_session=False)
        logs = db.session.query(ActivityLog).filter_by(entity_id=SID).delete(synchronize_session=False)
        n = db.session.query(Session).filter_by(id=SID).delete(synchronize_session=False)
        db.session.commit()
        print(f"removed session={n} register_rows={reg} log_rows={logs}")
