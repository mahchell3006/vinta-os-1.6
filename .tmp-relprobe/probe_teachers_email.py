"""Teachers: optional email, per-academy uniqueness, status filter.

Throwaway probe against the running server on :5000. Every teacher it creates is
deleted by explicit id in the finally block, so it leaves no rows behind.

Run: py .tmp-relprobe/probe_teachers_email.py
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

import requests  # noqa: E402
from flask_jwt_extended import create_access_token  # noqa: E402

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.user import User  # noqa: E402

BASE = "http://127.0.0.1:5000/api"

app = create_app("development")
with app.app_context():
    owner = db.session.query(User).filter_by(role="owner").first()
    academy_id = owner.academy_id
    token = create_access_token(identity=owner.id)

H = {"Authorization": f"Bearer {token}", "X-Academy-Id": academy_id}

created = []
failures = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got}, want {want}")
    if not ok:
        failures.append(label)


def post(body):
    r = requests.post(f"{BASE}/teachers", json=body, headers=H, timeout=10)
    return r


def new_teacher(first, last, **extra):
    r = post({"first_name": first, "last_name": last, **extra})
    if r.status_code == 201:
        created.append(r.json()["id"])
    return r


print("=" * 68)
print("1. no email at all — the case the desk actually hits")
r = new_teacher("Probe", "NoEmail")
check("create without email", r.status_code, 201)
check("email comes back null", r.json().get("email"), None)
check("status defaults ACTIVE", r.json().get("status"), "ACTIVE")

print("\n2. a SECOND teacher with no email — NULLs must not collide")
r = new_teacher("Probe", "AlsoNoEmail")
check("second email-less create", r.status_code, 201)
check("its email is null too", r.json().get("email"), None)

print("\n3. a malformed email is still refused")
r = post({"first_name": "Probe", "last_name": "BadEmail", "email": "not-an-email"})
check("malformed email", r.status_code, 400)
print(f"        server said: {r.json().get('error')!r}")

print("\n4. an empty string means 'no email', not 'invalid email'")
r = new_teacher("Probe", "EmptyString", email="")
check("empty-string email", r.status_code, 201)
check("stored as null", r.json().get("email"), None)

print("\n5. a real email is stored, lower-cased, and unique per academy")
r = new_teacher("Probe", "WithEmail", email="Probe.Teacher@Example.COM")
check("create with email", r.status_code, 201)
check("normalised to lower case", r.json().get("email"), "probe.teacher@example.com")

r = post({"first_name": "Probe", "last_name": "Duplicate", "email": "probe.teacher@example.com"})
check("same email again is a clash", r.status_code, 409)
print(f"        server said: {r.json().get('error')!r}")

print("\n6. PUT status INACTIVE, and the ?status= filter")
target = created[0]
r = requests.put(
    f"{BASE}/teachers/{target}", json={"status": "INACTIVE"}, headers=H, timeout=10
)
check("set INACTIVE", r.status_code, 200)
check("status applied", r.json().get("status"), "INACTIVE")

r = requests.put(f"{BASE}/teachers/{target}", json={"status": "NOPE"}, headers=H, timeout=10)
check("bogus status refused", r.status_code, 400)

r = requests.get(f"{BASE}/teachers", params={"status": "ACTIVE"}, headers=H, timeout=10)
active_ids = {t["id"] for t in r.json()["teachers"]}
check("inactive teacher absent from ?status=ACTIVE", target in active_ids, False)

r = requests.get(f"{BASE}/teachers", headers=H, timeout=10)
all_ids = {t["id"] for t in r.json()["teachers"]}
check("...but still on the full roster", target in all_ids, True)

r = requests.get(f"{BASE}/teachers", params={"status": "BOGUS"}, headers=H, timeout=10)
check("bogus status filter refused", r.status_code, 400)

print("\n7. PUT can clear an email back to null")
r = requests.put(
    f"{BASE}/teachers/{created[-1]}", json={"email": None}, headers=H, timeout=10
)
check("clear email", r.status_code, 200)
check("email is null again", r.json().get("email"), None)

print("\n" + "=" * 68)
for tid in created:
    d = requests.delete(f"{BASE}/teachers/{tid}", headers=H, timeout=10)
    print(f"  cleaned up {tid} -> {d.status_code}")
print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + ', '.join(failures)}")
