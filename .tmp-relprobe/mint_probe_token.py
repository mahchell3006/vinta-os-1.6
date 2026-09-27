"""Print a JWT for the throwaway owner probe, to paste into the page's localStorage.

Throwaway. Nothing is written to disk in the frontend tree — the token goes to
stdout and the browser call sets it there — so there is no `public/__session.json`
to forget to delete.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from flask_jwt_extended import create_access_token, create_refresh_token  # noqa: E402

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.user import User  # noqa: E402

MARKER = sys.argv[1] if len(sys.argv) > 1 else "ZZ Owner Probe (throwaway)"

app = create_app("development")
with app.app_context():
    u = db.session.query(User).filter_by(name=MARKER).first()
    if u is None:
        print("no such user:", MARKER, file=sys.stderr)
        sys.exit(1)
    print(create_access_token(identity=u.id))
    print(create_refresh_token(identity=u.id))
    print(u.academy_id)
