"""Enrollment capacity: 0 means "not set", not "full".

Throwaway probe against the running server on :5000.

  - a class with capacity 0 (the model default) must accept enrollments
  - a class with a real positive capacity must still refuse the one that
    would exceed it

Everything it creates is deleted by explicit id in the finally block.

Run: py .tmp-relprobe/probe_enroll_capacity.py
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
from app.models.student import Enrollment, Student  # noqa: E402
from app.models.user import User  # noqa: E402

BASE = "http://127.0.0.1:5000/api"

app = create_app("development")
with app.app_context():
    owner = db.session.query(User).filter_by(role="owner").first()
    ACADEMY = owner.academy_id
    H = {"Authorization": f"Bearer {create_access_token(identity=owner.id)}",
         "X-Academy-Id": ACADEMY}
    STUDENTS = [s.id for s in db.session.query(Student).filter_by(
        academy_id=ACADEMY, is_active=True).limit(3).all()]

print(f"academy {ACADEMY}, {len(STUDENTS)} students to work with")

classes, enrolled = [], []
failures = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got}, want {want}")
    if not ok:
        failures.append(label)


def make_class(name, capacity):
    r = requests.post(f"{BASE}/classes", json={"name": name, "capacity": capacity},
                      headers=H, timeout=10)
    print(f"  created '{name}' capacity={capacity} -> {r.status_code}")
    if r.status_code in (200, 201):
        classes.append(r.json()["id"])
        return r.json()["id"]
    return None


def enroll(student_id, class_id):
    r = requests.post(f"{BASE}/students/{student_id}/enroll",
                      json={"class_id": class_id}, headers=H, timeout=10)
    if r.status_code in (200, 201):
        body = r.json()
        eid = (body.get("enrollment") or body).get("id")
        if eid:
            enrolled.append(eid)
    return r


try:
    print("\n1. capacity 0 — the model default, and what the modal sends when "
          "nobody fills the field")
    c0 = make_class("ZZ Capacity Zero", 0)
    check("capacity-0 enroll succeeds", enroll(STUDENTS[0], c0).status_code, 201)
    check("...and a second student too", enroll(STUDENTS[1], c0).status_code, 201)

    print("\n2. a real capacity of 1 must still hold")
    c1 = make_class("ZZ Capacity One", 1)
    check("first student fits", enroll(STUDENTS[0], c1).status_code, 201)
    r = enroll(STUDENTS[1], c1)
    check("second is refused", r.status_code, 400)
    print(f"        server said: {r.json().get('error')!r}")

    print("\n3. capacity 2 accepts exactly two")
    c2 = make_class("ZZ Capacity Two", 2)
    check("first", enroll(STUDENTS[0], c2).status_code, 201)
    check("second", enroll(STUDENTS[1], c2).status_code, 201)
    if len(STUDENTS) > 2:
        check("third refused", enroll(STUDENTS[2], c2).status_code, 400)
    else:
        print("        skipped — this academy has only 2 active students")

finally:
    print("\n" + "=" * 68)
    with app.app_context():
        n = Enrollment.query.filter(Enrollment.id.in_(enrolled)).delete(
            synchronize_session=False)
        db.session.commit()
        print(f"  removed {n} enrollment(s)")
    for cid in classes:
        d = requests.delete(f"{BASE}/classes/{cid}", headers=H, timeout=10)
        print(f"  removed class {cid} -> {d.status_code}")
    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + ', '.join(failures)}")
