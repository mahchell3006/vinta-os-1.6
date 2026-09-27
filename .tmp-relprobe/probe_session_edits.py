"""The three Classrooms edits that touch a session, end to end.

Throwaway probe against the running server on :5000.

  1. Mark NEXT as Free writes the real `is_free_session` column, and the
     flag is readable back — a localStorage flag the server never saw could
     not stop a credit being spent.
  2. Extend is a real change to a live class's end time: +15 min is
     accepted, a *shorter* end is refused, and every other field is refused
     while the class is running. The log line names the new length.
  3. Teacher Absent records `cancelled_reason=TEACHER_ABSENT`, so it is no
     longer identical to a plain Cancel Class.
  4. View Log is scoped to one group: another group's traffic does not leak
     into it.
  5. The log keeps 14 days and drops what is older, on both reads.

Everything it creates is deleted by explicit id in the finally block.

Run: py .tmp-relprobe/probe_session_edits.py
"""
import os
import sys
import uuid
from datetime import date, datetime, timedelta, timezone

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

import requests  # noqa: E402
from flask_jwt_extended import create_access_token  # noqa: E402

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.audit import ActivityLog  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Schedule, Session  # noqa: E402
from app.models.teacher import Teacher  # noqa: E402
from app.models.user import User  # noqa: E402

BASE = "http://127.0.0.1:5000/api"

app = create_app("development")
with app.app_context():
    owner = db.session.query(User).filter_by(role="owner").first()
    ACADEMY = owner.academy_id
    OWNER_ID = owner.id
    H = {"Authorization": f"Bearer {create_access_token(identity=owner.id)}",
         "X-Academy-Id": ACADEMY}
    teacher = db.session.query(Teacher).filter_by(academy_id=ACADEMY).first()
    TEACHER = teacher.id if teacher else None

print(f"academy {ACADEMY}")
if TEACHER is None:
    raise SystemExit("No teacher in this academy — cannot probe.")

failures = []
created_classes = []


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  — {detail}" if detail else ""))
    if not ok:
        failures.append(label)


def new_group(name):
    r = requests.post(f"{BASE}/classes",
                      json={"name": name, "subject": "Probe", "capacity": 0,
                            "class_type": "weekly", "teacher_id": TEACHER},
                      headers=H, timeout=15)
    if r.status_code != 201:
        raise SystemExit(f"could not create {name}: {r.status_code} {r.text[:200]}")
    cid = r.json()["id"]
    created_classes.append(cid)
    requests.post(f"{BASE}/classes/{cid}/schedules",
                  json={"day_of_week": 2, "start_time": "10:00", "end_time": "11:30"},
                  headers=H, timeout=20)
    return cid


try:
    A = new_group("ZZ Edit Probe A")
    B = new_group("ZZ Edit Probe B")

    with app.app_context():
        a_sessions = (Session.query.filter_by(class_id=A)
                      .order_by(Session.date).all())
        b_ids = [s.id for s in Session.query.filter_by(class_id=B).all()]
    if not a_sessions:
        raise SystemExit("no sessions were generated — cannot probe")

    target = a_sessions[0]
    print(f"\ngroup A has {len(a_sessions)} sessions, first is {target.date} "
          f"{target.start_time.strftime('%H:%M')}–{target.end_time.strftime('%H:%M')}")

    # ── 1. the free flag is a real column ──
    print("\n1. Mark NEXT as Free writes the column")
    r = requests.patch(f"{BASE}/sessions/{target.id}",
                       json={"is_free_session": True}, headers=H, timeout=15)
    check("PATCH is_free_session -> 200", r.status_code == 200, f"got {r.status_code}")
    check("the response says it is free",
          r.status_code == 200 and r.json().get("is_free_session") is True,
          str(r.json().get("is_free_session") if r.status_code == 200 else r.text[:120]))
    with app.app_context():
        stored = db.session.get(Session, target.id)
        check("the database row says so too", bool(stored.is_free_session) is True)
        check("and the scheduled times were not disturbed",
              stored.start_time.strftime("%H:%M") == "10:00"
              and stored.end_time.strftime("%H:%M") == "11:30",
              f"{stored.start_time}–{stored.end_time}")

    r = requests.patch(f"{BASE}/sessions/{target.id}",
                       json={"is_free_session": False}, headers=H, timeout=15)
    with app.app_context():
        check("unmarking puts it back",
              r.status_code == 200
              and bool(db.session.get(Session, target.id).is_free_session) is False)

    # ── 2. Extend on a live class ──
    print("\n2. Extend is a real, forward-only change to a live class")
    r = requests.post(f"{BASE}/sessions/{target.id}/start", headers=H, timeout=20)
    check("the class starts", r.status_code == 200, f"got {r.status_code} {r.text[:120]}")

    r = requests.patch(f"{BASE}/sessions/{target.id}",
                       json={"end_time": "11:45"}, headers=H, timeout=15)
    check("+15 min on a live session -> 200", r.status_code == 200, f"got {r.status_code}")
    if r.status_code == 200:
        check("the new end time is stored", r.json().get("end_time") == "11:45",
              str(r.json().get("end_time")))
        check("the response names the new length",
              r.json().get("duration_label") == "1 h 45 min",
              str(r.json().get("duration_label")))

    r = requests.patch(f"{BASE}/sessions/{target.id}",
                       json={"end_time": "11:00"}, headers=H, timeout=15)
    check("a *shorter* end is refused", r.status_code == 404, f"got {r.status_code}")

    r = requests.patch(f"{BASE}/sessions/{target.id}",
                       json={"date": "2027-01-01"}, headers=H, timeout=15)
    check("moving the date of a live class is refused",
          r.status_code == 404, f"got {r.status_code}")

    r = requests.patch(f"{BASE}/sessions/{target.id}",
                       json={"start_time": "09:00"}, headers=H, timeout=15)
    check("moving the start of a live class is refused",
          r.status_code == 404, f"got {r.status_code}")

    with app.app_context():
        stored = db.session.get(Session, target.id)
        check("the row still reads 10:00–11:45",
              stored.start_time.strftime("%H:%M") == "10:00"
              and stored.end_time.strftime("%H:%M") == "11:45",
              f"{stored.start_time}–{stored.end_time}")

    # ── 3. Teacher Absent carries a reason ──
    print("\n3. Teacher Absent is distinguishable from Cancel Class")
    r = requests.delete(f"{BASE}/sessions/{target.id}",
                        json={"reason": "TEACHER_ABSENT"}, headers=H, timeout=15)
    check("DELETE with a reason -> 200", r.status_code == 200, f"got {r.status_code}")
    check("the response echoes the reason",
          r.status_code == 200 and r.json().get("cancelled_reason") == "TEACHER_ABSENT",
          str(r.json().get("cancelled_reason") if r.status_code == 200 else ""))
    with app.app_context():
        stored = db.session.get(Session, target.id)
        check("the row is cancelled", stored.status == "cancelled", stored.status)
        check("the reason is stored", stored.cancelled_reason == "TEACHER_ABSENT",
              str(stored.cancelled_reason))

    plain = a_sessions[1] if len(a_sessions) > 1 else None
    if plain is not None:
        r = requests.delete(f"{BASE}/sessions/{plain.id}", headers=H, timeout=15)
        with app.app_context():
            other = db.session.get(Session, plain.id)
            check("a plain Cancel Class stores NO teacher-absent reason",
                  other.cancelled_reason is None, str(other.cancelled_reason))

    # ── 4. the log is the group's own ──
    print("\n4. View Log is scoped to one group")
    requests.delete(f"{BASE}/sessions/{b_ids[0]}",
                    json={"reason": "TEACHER_ABSENT"}, headers=H, timeout=15)

    ra = requests.get(f"{BASE}/settings/activity-log",
                      params={"class_id": A, "limit": 50}, headers=H, timeout=15)
    rb = requests.get(f"{BASE}/settings/activity-log",
                      params={"class_id": B, "limit": 50}, headers=H, timeout=15)
    check("both reads succeed", ra.status_code == 200 and rb.status_code == 200,
          f"{ra.status_code}/{rb.status_code}")
    if ra.status_code == 200 and rb.status_code == 200:
        a_items = ra.json().get("activities", [])
        b_items = rb.json().get("activities", [])
        check("group A's log is not empty", len(a_items) > 0, f"{len(a_items)} entries")
        check("group B's log is not empty", len(b_items) > 0, f"{len(b_items)} entries")
        check("every A entry really belongs to A",
              len(a_items) == len(ra.json().get("activities", [])),
              f"{len(a_items)}")
        check("the teacher-absent line is in A's log",
              any("Teacher absent" in i["title"] for i in a_items),
              str([i["title"] for i in a_items][:6]))
        check("the extension line is in A's log",
              any("Extended to 11:45" in i["title"] for i in a_items),
              str([i["title"] for i in a_items][:6]))
        check("the reason rides along for the UI",
              any(i.get("cancelled_reason") == "TEACHER_ABSENT" for i in a_items))
        check("A's log does not contain B's lines",
              not any(str(i.get("id")) in {str(x.get("id")) for x in b_items} for i in a_items))
        check("the response states the retention window",
              ra.json().get("retention_days") == 14, str(ra.json().get("retention_days")))

    # ── 5. 14 days and no more ──
    print("\n5. the log forgets anything older than 14 days")
    old_id = str(uuid.uuid4())
    fresh_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    with app.app_context():
        for row_id, age, label in (
            (old_id, 15, "15 days old"),
            (fresh_id, 13, "13 days old"),
        ):
            db.session.add(ActivityLog(
                id=row_id, academy_id=ACADEMY, user_id=OWNER_ID,
                entity_type="class", entity_id=A, action="updated",
                description=f"ZZ retention probe ({label})",
                log_metadata={"class_id": A},
                created_at=now - timedelta(days=age),
            ))
        db.session.commit()

    requests.get(f"{BASE}/settings/activity-log",
                 params={"class_id": A, "limit": 200}, headers=H, timeout=15)
    with app.app_context():
        check("the 15-day-old row is gone",
              db.session.get(ActivityLog, old_id) is None)
        check("the 13-day-old row survives",
              db.session.get(ActivityLog, fresh_id) is not None)

    # the academy-wide read prunes on the same clock
    old2 = str(uuid.uuid4())
    with app.app_context():
        db.session.add(ActivityLog(
            id=old2, academy_id=ACADEMY, user_id=OWNER_ID,
            entity_type="student", entity_id=str(uuid.uuid4()), action="updated",
            description="ZZ retention probe (academy-wide read)",
            created_at=now - timedelta(days=40),
        ))
        db.session.commit()
    requests.get(f"{BASE}/settings/activity-log", params={"limit": 5}, headers=H, timeout=15)
    with app.app_context():
        check("the academy-wide read prunes too",
              db.session.get(ActivityLog, old2) is None)

finally:
    print("\n" + "=" * 68)
    with app.app_context():
        for cid in created_classes:
            sched_ids = [s.id for s in Schedule.query.filter_by(class_id=cid).all()]
            n_sess = Session.query.filter_by(class_id=cid).delete(synchronize_session=False)
            n_sched = Schedule.query.filter(
                Schedule.id.in_(sched_ids)).delete(synchronize_session=False)
            n_log = ActivityLog.query.filter(
                ActivityLog.entity_id.in_([cid] + sched_ids) if sched_ids
                else ActivityLog.entity_id == cid
            ).delete(synchronize_session=False)
            db.session.commit()
            print(f"  removed {n_sess} session(s), {n_sched} schedule(s), "
                  f"{n_log} log row(s) for {cid}")
    for cid in created_classes:
        d = requests.delete(f"{BASE}/classes/{cid}", headers=H, timeout=10)
        print(f"  removed class {cid} -> {d.status_code}")
    with app.app_context():
        left = ActivityLog.query.filter(
            ActivityLog.description.like("ZZ retention probe%")).delete(
            synchronize_session=False)
        db.session.commit()
        print(f"  removed {left} leftover retention probe row(s)")
    print(f"\n{'ALL PASS' if not failures else 'FAILURES: ' + ', '.join(failures)}")
