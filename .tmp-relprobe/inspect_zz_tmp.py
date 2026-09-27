"""What hangs off the leftover probe group, before anything is deleted."""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.audit import ActivityLog  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.teacher import Teacher  # noqa: E402

app = create_app("development")
with app.app_context():
    print("teachers:")
    for t in db.session.query(Teacher).all():
        print(f"  {t.id}  {t.first_name!r} {t.last_name!r}  email={getattr(t, 'email', None)!r}")
    c = db.session.get(Class, "zz-probe-tmp")
    print("\nzz-probe-tmp:", c.name if c else None)
    if c:
        for rel in ("schedules", "sessions", "enrollments"):
            try:
                v = getattr(c, rel)
                print(f"  {rel}: {len(list(v))}")
            except Exception as e:  # relationship may not exist
                print(f"  {rel}: n/a ({type(e).__name__})")
    logs = db.session.query(ActivityLog).filter(ActivityLog.entity_id == "zz-probe-tmp").all()
    print(f"  ActivityLog rows naming it: {len(logs)}")
    for l in logs:
        print(f"    {l.id} {l.entity_type}/{l.action}: {l.description!r}")
