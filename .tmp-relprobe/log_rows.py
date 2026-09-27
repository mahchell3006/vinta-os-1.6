"""Read the activity rows for Group A, exactly as the per-class log would."""
import os, sys
BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND); sys.path.insert(0, BACKEND)
from app import create_app
from app.extensions import db
from app.models.audit import ActivityLog
app = create_app("development")
with app.app_context():
    rows = (db.session.query(ActivityLog)
            .filter(ActivityLog.entity_id == "zz-probe-session")
            .order_by(ActivityLog.created_at.asc()).all())
    print(f"rows naming the probe session: {len(rows)}")
    for r in rows:
        print(f"  {r.created_at}  {r.action:8s} {r.entity_type:8s} {r.description!r}  meta={r.log_metadata}")
    print()
    # Any duplicate (action, description, entity_id) within the same minute.
    all_rows = db.session.query(ActivityLog).filter(ActivityLog.entity_type == "session").all()
    seen = {}
    for r in all_rows:
        key = (r.entity_id, r.action, r.description, str(r.created_at)[:16])
        seen.setdefault(key, []).append(r.id)
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"same-minute identical session log rows: {len(dupes)}")
    for k, v in list(dupes.items())[:8]:
        print(f"  x{len(v)}  {k[1]} {k[2]!r} at {k[3]}")
