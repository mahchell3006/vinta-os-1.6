"""Put session a2ea5439 back exactly as it was.

That row was started by a mis-aimed "Start Class" click during the live check
(the Classrooms card prefers an already-running session, and this duplicate on
06 Oct was the card's pick before the probe session existed). It was a plain
`scheduled` row with no register before; this restores that, then prints the
row so the restore is checked by reading it back rather than by trusting the
writes above it.
"""
import os, sys
BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND); sys.path.insert(0, BACKEND)
from app import create_app
from app.extensions import db
from app.models.attendance import SessionStudent
from app.models.audit import ActivityLog
from app.models.scheduling import Session

SID = "a2ea5439-f584-4ff2-bfd3-48e984472005"

app = create_app("development")
with app.app_context():
    s = db.session.get(Session, SID)
    print("before:", s.status, s.actual_start_time, s.started_by_staff_id, s.is_free_session)
    reg = db.session.query(SessionStudent).filter_by(session_id=SID).all()
    print("register rows before:", [(r.student_id, r.status) for r in reg])

    db.session.query(SessionStudent).filter_by(session_id=SID).delete(synchronize_session=False)
    logs = db.session.query(ActivityLog).filter(
        ActivityLog.entity_id == SID, ActivityLog.action == "started"
    ).delete(synchronize_session=False)
    s.status = "scheduled"
    s.actual_start_time = None
    s.actual_end_time = None
    s.started_by_staff_id = None
    s.ended_by_staff_id = None
    s.cancelled_reason = None
    s.is_free_session = False
    db.session.commit()

    s = db.session.get(Session, SID)
    print("after :", s.status, s.actual_start_time, s.started_by_staff_id, s.is_free_session)
    print("register rows after:", db.session.query(SessionStudent).filter_by(session_id=SID).count())
    print("started-log rows removed:", logs)
