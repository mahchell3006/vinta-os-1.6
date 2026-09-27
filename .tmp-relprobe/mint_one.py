"""Mint one access token for a named user id. Throwaway.

Same as mint.py but takes the user id on the command line, because the browser
check needs a token for the throwaway probe owner and mint.py returns whichever
owner the query finds first.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from flask_jwt_extended import create_access_token  # noqa: E402

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.user import User  # noqa: E402

user_id = sys.argv[1]
app = create_app("development")
with app.app_context():
    u = db.session.get(User, user_id)
    if not u:
        sys.exit(f"no such user: {user_id}")
    print("NAME", u.name, "ROLE", u.role)
    print("ACADEMY", u.academy_id)
    # Long-lived on purpose: the browser check outlives the 1h default and a
    # token expiring mid-pass would look like a bug in the page under test.
    print("TOKEN", create_access_token(identity=u.id, expires_delta=False))
