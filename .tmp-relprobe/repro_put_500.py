"""Reproduce the PUT /classes/<id> 500 and print the traceback.

The desk's Save on the group edit panel answers 500 for a group created without
a teacher. Sending the same body through the test client keeps the traceback,
which the browser only ever sees as "500 INTERNAL SERVER ERROR".
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.user import User  # noqa: E402
from flask_jwt_extended import create_access_token  # noqa: E402

ID = "zz-timeless-probe"

app = create_app("development")
with app.app_context():
    owner = db.session.query(User).filter_by(name="ZZ Owner Probe (throwaway)").first()
    token = create_access_token(identity=owner.id)
    academy = owner.academy_id
    c = db.session.get(Class, ID)
    print("before:", repr(c.name), "teacher_id=", c.teacher_id, "class_type=", c.class_type)

    body = {
        "name": c.name,
        "subject": c.subject,
        "color": None,
        "capacity": c.capacity,
        "teacher_id": None,
        "notes": None,
        "price_da": 0,
        "billing_model": "CREDIT_BASED",
        "credits_per_cycle": 4,
        "class_type": "weekly",
    }

    client = app.test_client()
    resp = client.put(
        f"/api/classes/{ID}",
        json=body,
        headers={"Authorization": f"Bearer {token}", "X-Academy-Id": academy},
    )
    print("status:", resp.status_code)
    print(resp.get_data(as_text=True)[:2000])
