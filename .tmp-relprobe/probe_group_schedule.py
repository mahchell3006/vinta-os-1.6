"""A group created with Start At / End At must actually get sessions.

Throwaway probe against the running server on :5000.

Reproduces exactly what ClassesPage.handleAddClass now does:

    POST /classes                        (the group)
    POST /classes/<id>/schedules         (its time -> generates the sessions)

and asserts:

  1. the session count lands on the calendar afterwards
  2. each generated session carries the times that were asked for
  3. posting the SAME block again is refused 409, not added a second time
     (this is what left Group A with three identical schedules and every date
     carrying three duplicate classes)
  4. a different room, or a different day, is still accepted

Everything it creates is deleted by explicit id in the finally block.

Run: py .tmp-relprobe/probe_group_schedule.py
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
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Schedule, Session  # noqa: E402
from app.models.teacher import Teacher  # noqa: E402
from app.models.user import User  # noqa: E402

BASE = "http://127.0.0.1:5000/api"

app = create_app("development")
with app.app_context():
    owner = db.session.query(User).filter_by(role="owner").first()
    ACADEMY = owner.academy_id
    H = {"Authorization": f"Bearer {create_access_token(identity=owner.id)}",
         "X-Academy-Id": ACADEMY}
    teacher = db.session.query(Teacher).filter_by(academy_id=ACADEMY).first()
    TEACHER = teacher.id if teacher else None

print(f"academy {ACADEMY}, teacher {TEACHER}")
if TEACHER is None:
    raise SystemExit("No teacher in this academy — cannot probe session generation.")


failures = []
created_classes = []


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  — {detail}" if detail else ""))
    if not ok:
        failures.append(label)


def sessions_of(class_id):
    with app.app_context():
        return Session.query.filter_by(class_id=class_id).all()


try:
    # 10:00–11:30 on a Tuesday (day_of_week 2), purely so the numbers are
    # recognisable in the output.
    DOW, START, END = 2, "10:00", "11:30"

    print("\n0. a weekly group with no teacher is refused, not 500'd")
    # sessions.teacher_id is NOT NULL, so the generator dies on its first
    # INSERT for a teacherless group. That used to surface as an HTML 500 with
    # the schedule already committed behind it.
    r0 = requests.post(f"{BASE}/classes",
                       json={"name": "ZZ NoTeacher Probe", "subject": "Probe",
                             "capacity": 0, "class_type": "weekly"},
                       headers=H, timeout=15)
    check("the teacherless group is created", r0.status_code == 201,
          f"got {r0.status_code}")
    if r0.status_code == 201:
        nid = r0.json()["id"]
        created_classes.append(nid)
        r0b = requests.post(f"{BASE}/classes/{nid}/schedules",
                            json={"day_of_week": DOW, "start_time": START, "end_time": END},
                            headers=H, timeout=20)
        check("adding its time is refused 400, not 500", r0b.status_code == 400,
              f"got {r0b.status_code}")
        print(f"        server said: {r0b.json().get('error')!r}")
        with app.app_context():
            left = Schedule.query.filter_by(class_id=nid).count()
        check("no orphan schedule row was left behind", left == 0, f"{left} rows")

    print("\n1. create the group, then its time — the new two-call sequence")
    r = requests.post(f"{BASE}/classes",
                      json={"name": "ZZ Schedule Probe", "subject": "Probe",
                            "capacity": 0, "class_type": "weekly",
                            "teacher_id": TEACHER},
                      headers=H, timeout=15)
    check("POST /classes", r.status_code == 201, f"got {r.status_code}")
    if r.status_code != 201:
        raise SystemExit(1)
    cid = r.json()["id"]
    created_classes.append(cid)

    check("a brand-new group starts with no sessions",
          len(sessions_of(cid)) == 0, f"{len(sessions_of(cid))} already there")

    r = requests.post(f"{BASE}/classes/{cid}/schedules",
                      json={"day_of_week": DOW, "start_time": START, "end_time": END},
                      headers=H, timeout=20)
    check("POST /classes/<id>/schedules", r.status_code == 201, f"got {r.status_code}")
    if r.status_code != 201:
        print(f"        server said: {r.text[:200]}")
        raise SystemExit(1)

    made = r.json().get("sessions_created", 0)
    check("the endpoint reports generated sessions", made > 0, f"sessions_created={made}")

    rows = sessions_of(cid)
    check("those sessions are really in the database", len(rows) == made,
          f"{len(rows)} rows vs {made} reported")
    print(f"        {len(rows)} sessions, "
          f"{min((s.date for s in rows), default=None)} .. {max((s.date for s in rows), default=None)}")

    print("\n2. each session carries the times that were asked for")
    times = {(s.start_time.strftime('%H:%M'), s.end_time.strftime('%H:%M')) for s in rows}
    check(f"every session is {START}–{END}", times == {(START, END)}, str(times))
    check("every session lands on the requested weekday",
          all(s.date.weekday() == DOW for s in rows),
          str(sorted({s.date.weekday() for s in rows})))

    print("\n3. the same block again is refused, not duplicated")
    r2 = requests.post(f"{BASE}/classes/{cid}/schedules",
                       json={"day_of_week": DOW, "start_time": START, "end_time": END},
                       headers=H, timeout=20)
    check("identical block -> 409", r2.status_code == 409, f"got {r2.status_code}")
    print(f"        server said: {r2.json().get('error')!r}")
    with app.app_context():
        n_sched = Schedule.query.filter_by(class_id=cid).count()
    check("exactly one schedule exists", n_sched == 1, f"{n_sched} schedules")
    check("no extra sessions appeared", len(sessions_of(cid)) == len(rows),
          f"{len(sessions_of(cid))} vs {len(rows)}")

    print("\n4. a genuinely different block is still accepted")
    r3 = requests.post(f"{BASE}/classes/{cid}/schedules",
                       json={"day_of_week": 4, "start_time": "14:00", "end_time": "15:30"},
                       headers=H, timeout=20)
    check("another day -> 201", r3.status_code == 201, f"got {r3.status_code}")
    with app.app_context():
        n_sched = Schedule.query.filter_by(class_id=cid).count()
    check("now two schedules", n_sched == 2, f"{n_sched}")

finally:
    print("\n" + "=" * 68)
    with app.app_context():
        for cid in created_classes:
            sched_ids = [s.id for s in Schedule.query.filter_by(class_id=cid).all()]
            n_sess = Session.query.filter_by(class_id=cid).delete(synchronize_session=False)
            n_sched = Schedule.query.filter(
                Schedule.id.in_(sched_ids)).delete(synchronize_session=False)
            db.session.commit()
            print(f"  removed {n_sess} session(s), {n_sched} schedule(s) for {cid}")
    for cid in created_classes:
        d = requests.delete(f"{BASE}/classes/{cid}", headers=H, timeout=10)
        print(f"  removed class {cid} -> {d.status_code}")
    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + ', '.join(failures)}")
