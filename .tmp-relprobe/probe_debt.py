"""Find every row any probe left behind in the dev database. Read-only.

The probe scripts create real rows in a real tenant (that is the point of them),
and each one is supposed to delete its own. This lists what is still there so
nothing is left for a person to find later. Anything named ZZ* or with an id
starting zz- came from this work, never from the user.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.academy import Academy  # noqa: E402
from app.models.audit import ActivityLog  # noqa: E402
from app.models.class_room import Class, Classroom  # noqa: E402
from app.models.scheduling import Session  # noqa: E402
from app.models.student import Student  # noqa: E402
from app.models.teacher import Teacher  # noqa: E402
from app.models.user import User  # noqa: E402

app = create_app("development")
with app.app_context():
    for model in (User, Student, Teacher, Class, Classroom, Session):
        rows = db.session.query(model).all()
        hits = []
        for r in rows:
            label = getattr(r, "name", None) or getattr(r, "class_name", None) or ""
            if str(label).startswith("ZZ") or str(r.id).startswith("zz-"):
                hits.append(f"    {r.id}  {label!r}")
        print(f"{model.__name__}: {len(rows)} rows, {len(hits)} probe")
        for h in hits:
            print(h)
    logs = db.session.query(ActivityLog).all()
    probes = [l for l in logs if str(l.entity_id or "").startswith("zz-")]
    print(f"ActivityLog: {len(logs)} rows, {len(probes)} naming a zz- entity")
    for l in probes[:10]:
        print(f"    {l.id}  {l.entity_type}/{l.entity_id}  {l.action}")
    print("users:", [(u.name, u.role) for u in db.session.query(User).all()])
