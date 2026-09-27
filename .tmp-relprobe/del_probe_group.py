"""Delete a probe group and everything that points at it.

Throwaway cleanup. The id is given on the command line so the row is named, and
every dependent count is printed before the delete commits, so a group that still
had sessions could not be removed quietly.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.audit import ActivityLog  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Schedule, Session  # noqa: E402
from app.models.student import Enrollment  # noqa: E402

CLASS_ID = sys.argv[1]

app = create_app("development")
with app.app_context():
    c = db.session.get(Class, CLASS_ID)
    if c is None:
        print("no such class:", CLASS_ID)
        sys.exit(1)
    print(f"  {c.id}  {c.name!r}  capacity={c.capacity}")
    counts = {}
    counts["schedules"] = db.session.query(Schedule).filter_by(class_id=CLASS_ID).delete(
        synchronize_session=False
    )
    counts["sessions"] = db.session.query(Session).filter_by(class_id=CLASS_ID).delete(
        synchronize_session=False
    )
    counts["enrollments"] = db.session.query(Enrollment).filter_by(class_id=CLASS_ID).delete(
        synchronize_session=False
    )
    # activity_logs has no class_id column: a row names a class either as its
    # entity (entity_type == "class") or in its metadata. Both are checked, and
    # the ids are printed, because "the log rows went too" has to be inspectable.
    log_rows = [
        row
        for row in db.session.query(ActivityLog).all()
        if (row.entity_type == "class" and row.entity_id == CLASS_ID)
        or (row.log_metadata or {}).get("class_id") == CLASS_ID
    ]
    for row in log_rows:
        print(f"      log {row.id}  {row.action}  {row.entity_type}={row.entity_id}  {row.description!r}")
    counts["logs"] = len(log_rows)
    for row in log_rows:
        db.session.delete(row)
    counts["class"] = db.session.query(Class).filter(Class.id == CLASS_ID).delete(
        synchronize_session=False
    )
    db.session.commit()
    print("      " + "  ".join(f"{k}={v}" for k, v in counts.items()))
    print(f"      gone: {db.session.get(Class, CLASS_ID) is None}")
