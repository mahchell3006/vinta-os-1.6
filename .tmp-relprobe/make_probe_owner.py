"""Create (or remove) a throwaway OWNER profile for the browser check.

Same shape as make_staff.py, and for the same reason: the profile picker wants a
PIN for every profile, and the two real owners in this database are the user's —
guessing at their PIN would trip the rate limiter on a real account.

This one is an owner rather than a staff member because the screen under test is
owner-only in two places at once: Settings > Billing Rules hides its switches
from staff, and GET/PUT /settings/billing-config are @owner_only on the server.
A staff probe would have proved nothing about either.

  py make_probe_owner.py make     -> create, print the id
  py make_probe_owner.py remove   -> delete it and anything it wrote
"""
import os
import sys
import uuid

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.audit import ActivityLog  # noqa: E402
from app.models.user import User  # noqa: E402

# The tenant with the real rows in it: 2 students, 3 teachers, 3 groups, 36
# sessions. The other academy in this file is empty, and a browser check against
# an empty tenant says nothing about a page built out of lists.
ACADEMY = "ad6587d5-6fd3-4015-a497-8dd5301b830d"
MARKER = "ZZ Owner Probe (throwaway)"
PIN = "4321"

app = create_app("development")
action = sys.argv[1] if len(sys.argv) > 1 else "make"

with app.app_context():
    if action == "make":
        existing = db.session.query(User).filter_by(name=MARKER).all()
        if existing:
            print("already exists:", existing[0].id)
            sys.exit(0)
        u = User(
            id=str(uuid.uuid4()),
            academy_id=ACADEMY,
            name=MARKER,
            email="zz-owner-probe@example.invalid",
            role="owner",
            pin_hash=User.hash_pin(PIN),
        )
        db.session.add(u)
        db.session.commit()
        print("created:", u.id, "role: owner", "pin:", PIN)
    else:
        users = db.session.query(User).filter_by(name=MARKER).all()
        ids = [u.id for u in users]
        if not ids:
            print("nothing to remove")
            sys.exit(0)
        # A PIN check writes an audit row naming the user; deleting the user
        # without it would leave a dangling reference (the FK audit found this
        # exact hole once already).
        logs = db.session.query(ActivityLog).filter(
            ActivityLog.user_id.in_(ids)
        ).delete(synchronize_session=False)
        n = db.session.query(User).filter(User.id.in_(ids)).delete(
            synchronize_session=False
        )
        db.session.commit()
        print(f"removed {n} user(s), {logs} log row(s)")
        left = db.session.query(User).filter_by(name=MARKER).count()
        print("remaining:", left)
