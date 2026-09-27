"""Who is in the students table right now, newest first.

Throwaway. Printed by created_at so a probe row can be named exactly rather than
matched by name — the duplicate-name case is the one that bites.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.student import Student, Enrollment  # noqa: E402

app = create_app("development")
with app.app_context():
    rows = db.session.query(Student).order_by(Student.created_at.desc()).all()
    print(f"students: {len(rows)}")
    for s in rows:
        subs = db.session.query(Enrollment).filter_by(student_id=s.id).all()
        print(f"  {s.id}  {s.first_name!r} {s.last_name!r}  phone={s.phone!r}  created={s.created_at}")
        for sub in subs:
            print(f"      sub {sub.id} class={sub.class_id}")
