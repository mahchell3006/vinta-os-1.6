"""Which academy is the live dev data, and who has a known PIN?

Throwaway. Prints one line per academy so a browser check can be pointed at the
tenant that actually has rows in it, rather than at whichever owner the query
happens to return first.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.academy import Academy  # noqa: E402
from app.models.student import Student  # noqa: E402
from app.models.teacher import Teacher  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Session  # noqa: E402
from app.models.user import User  # noqa: E402

app = create_app("development")
with app.app_context():
    for a in db.session.query(Academy).all():
        users = db.session.query(User).filter_by(academy_id=a.id).all()
        print(f"\nACADEMY {a.id}  {a.name!r}")
        print(f"  students={db.session.query(Student).filter_by(academy_id=a.id).count()}"
              f" teachers={db.session.query(Teacher).filter_by(academy_id=a.id).count()}"
              f" classes={db.session.query(Class).filter_by(academy_id=a.id).count()}"
              f" sessions={db.session.query(Session).filter_by(academy_id=a.id).count()}")
        for u in users:
            print(f"  - {u.role:8s} {u.name!r}  id={u.id}  email={u.email!r}")
