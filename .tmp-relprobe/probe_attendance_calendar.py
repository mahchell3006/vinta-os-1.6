"""Attendance calendar: the states, and that reading it changes nothing.

Throwaway probe against the running server on :5000.

  - GET /students/<id> carries attendance_calendar with the documented shape
  - every entry's `state` is one of the known values
  - a colour-class histogram is printed so the states can be eyeballed against
    real register data, not just asserted
  - reading the profile does not mutate subscriptions (the whole reason this
    does not reuse billing_service.find_active_subscription)

Run: py .tmp-relprobe/probe_attendance_calendar.py
"""
import os
import sys
from collections import Counter

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

import requests  # noqa: E402
from flask_jwt_extended import create_access_token  # noqa: E402

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.billing import StudentSubscription  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Session  # noqa: E402
from app.models.student import Enrollment, Student  # noqa: E402
from app.models.user import User  # noqa: E402

BASE = "http://127.0.0.1:5000/api"

KNOWN = {
    "attended", "absent", "unpaid", "upcoming",
    "cancelled", "not_enrolled", "unrecorded",
}

app = create_app("development")
with app.app_context():
    owner = db.session.query(User).filter_by(role="owner").first()
    ACADEMY = owner.academy_id
    H = {"Authorization": f"Bearer {create_access_token(identity=owner.id)}",
         "X-Academy-Id": ACADEMY}
    STUDENTS = [
        (s.id, s.full_name) for s in
        db.session.query(Student).filter_by(academy_id=ACADEMY, is_active=True).all()
    ]
    # Snapshot every subscription row before the reads, so any write the
    # calendar might have caused shows up as a diff.
    subs_before = {
        s.id: (s.status, s.remaining_credits, s.updated_at.isoformat() if s.updated_at else None)
        for s in db.session.query(StudentSubscription).filter_by(academy_id=ACADEMY).all()
    }

print(f"academy {ACADEMY}, {len(STUDENTS)} students")

failures = []


def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  — {detail}" if detail else ""))
    if not ok:
        failures.append(label)


histogram = Counter()
total_entries = 0
studied = 0

for student_id, name in STUDENTS:
    r = requests.get(f"{BASE}/students/{student_id}", headers=H, timeout=15)
    if r.status_code != 200:
        check(f"{name}: profile 200", False, f"got {r.status_code} {r.text[:120]}")
        continue

    cal = r.json().get("attendance_calendar")
    if cal is None:
        check(f"{name}: attendance_calendar present", False, "key missing")
        continue

    entries = cal.get("entries", [])
    total_entries += len(entries)
    if entries:
        studied += 1

    bad = [e for e in entries if e.get("state") not in KNOWN]
    if bad:
        check(f"{name}: all states known", False, f"{len(bad)} unknown, e.g. {bad[0]}")

    missing = [
        e for e in entries
        if not all(k in e for k in
                   ("date", "session_id", "class_id", "state", "covered", "enrolled"))
    ]
    if missing:
        check(f"{name}: entries carry the documented keys", False, str(missing[0])[:160])

    for e in entries:
        histogram[e["state"]] += 1

    print(f"    {name:<28} joined {cal.get('joined_on')}  "
          f"{len(entries):>3} entries  {dict(Counter(e['state'] for e in entries))}")

print("\n1. shape")
check("the key is present on every profile", total_entries > 0 or studied == 0,
      f"{total_entries} entries across {len(STUDENTS)} students")
check("every state is a known value", not any(f.startswith('all states known') for f in failures))

print("\n2. states actually occur (not a uniformly empty calendar)")
print(f"    histogram: {dict(histogram)}")
check("at least one non-upcoming, non-unrecorded state exists",
      any(histogram[s] for s in ("attended", "absent", "unpaid")),
      "otherwise the green/red/yellow paths are untested")

print("\n3. reading the profile did not write")
with app.app_context():
    subs_after = {
        s.id: (s.status, s.remaining_credits, s.updated_at.isoformat() if s.updated_at else None)
        for s in db.session.query(StudentSubscription).filter_by(academy_id=ACADEMY).all()
    }
    drifted = {k: (subs_before[k], subs_after.get(k))
               for k in subs_before if subs_before[k] != subs_after.get(k)}
    new_rows = set(subs_after) - set(subs_before)
check("no subscription changed status/credits/updated_at",
      not drifted, f"{len(drifted)} drifted" if drifted else "all identical")
check("no subscription was created", not new_rows, f"{len(new_rows)} new" if new_rows else "")

print("\n4. per-group coverage: the calendar spans exactly the groups that have "
      "sessions — no more, no fewer")
with app.app_context():
    checked = 0
    for student_id, name in STUDENTS:
        enrolled = [e.class_id for e in
                    Enrollment.query.filter_by(student_id=student_id).all()]
        with_sessions = {
            cid for cid in enrolled if Session.query.filter_by(class_id=cid).first()
        }
        empty = [c for c in enrolled if c not in with_sessions]
        if not with_sessions:
            continue

        r = requests.get(f"{BASE}/students/{student_id}", headers=H, timeout=15)
        groups = {e["class_id"] for e in r.json()["attendance_calendar"]["entries"]}
        checked += 1

        check(f"{name}: {len(groups)} group(s) on the calendar == "
              f"{len(with_sessions)} enrolled group(s) with sessions",
              groups == with_sessions,
              f"missing {groups - with_sessions}" if with_sessions - groups else "")
        if empty:
            names = [db.session.get(Class, c).name for c in empty]
            print(f"        note: {names} have no sessions at all, so they cannot "
                  f"appear — that is the missing-Schedule defect, not this code")

    if not checked:
        print("    skipped — no student has an enrolled group with sessions")

print("\n5. the attended/unpaid branches, forced through the real code path")
# Every register row in this dev database is ABSENT, so green and yellow would
# otherwise ship untested. One row is flipped to PRESENT inside the session and
# rolled back at the end — nothing is committed.
from datetime import date as _date, datetime as _dt, timedelta as _timedelta  # noqa: E402

from app.models.attendance import SessionStudent  # noqa: E402
from app.services import student_service  # noqa: E402

with app.app_context():
    # Not filtered to past sessions: the only register rows in this database
    # sit on a future-dated session that was already started and conducted.
    # What matters is that the row reaches the attended/unpaid branch, which
    # means it must not be cancelled and must not read as upcoming.
    row = next(
        (
            r for r in SessionStudent.query.all()
            if (s := db.session.get(Session, r.session_id)) is not None
            and s.status not in ("cancelled", "scheduled", "in_progress")
        ),
        None,
    )
    original = row.status if row else None

    if row is None:
        print("    skipped — no past register row to flip")
    else:
        row.status = "PRESENT"
        row.checked_in_at = _dt.now()
        db.session.flush()

        cal = student_service._get_attendance_calendar(row.student_id)
        hit = [e for e in cal["entries"] if e["session_id"] == row.session_id]
        check("the flipped session still appears exactly once", len(hit) == 1,
              f"{len(hit)} entries")
        if hit:
            e = hit[0]
            expected = "attended" if e["covered"] else "unpaid"
            check(f"PRESENT with covered={e['covered']} reads as {expected!r}",
                  e["state"] == expected, f"got {e['state']!r}")
            print(f"        attendance={e['attendance']!r} covered={e['covered']} "
                  f"enrolled={e['enrolled']}")

        # Yellow is the same register with no plan behind it. Driving the
        # decision function directly is the only way to hold everything else
        # fixed and vary one thing.
        sess = db.session.get(Session, row.session_id)
        yellow = student_service._session_state(
            session=sess, attendance="PRESENT", has_register_row=True,
            enrolled_on=None, paid=False, today=_date.today(),
        )
        green = student_service._session_state(
            session=sess, attendance="PRESENT", has_register_row=True,
            enrolled_on=None, paid=True, today=_date.today(),
        )
        check("PRESENT + unpaid is 'unpaid' (yellow)", yellow == "unpaid", yellow)
        check("PRESENT + paid is 'attended' (green)", green == "attended", green)

        # The remaining states. `_session_state` reads exactly two attributes
        # off the session, so a stand-in keeps the real row untouched.
        class _Stub:
            def __init__(self, status, day):
                self.status, self.date = status, day

        today = _date.today()

        upcoming = student_service._session_state(
            session=_Stub("scheduled", today + _timedelta(days=3)),
            attendance=None, has_register_row=False, enrolled_on=None,
            paid=True, today=today,
        )
        check("a scheduled session three days out is 'upcoming'",
              upcoming == "upcoming", upcoming)

        unrec = student_service._session_state(
            session=_Stub("conducted", today - _timedelta(days=9)),
            attendance=None, has_register_row=False, enrolled_on=None,
            paid=True, today=today,
        )
        check("past, conducted, no register, is 'unrecorded' not 'absent'",
              unrec == "unrecorded", unrec)

        notyet = student_service._session_state(
            session=_Stub("conducted", today - _timedelta(days=9)),
            attendance="ABSENT", has_register_row=True,
            enrolled_on=today - _timedelta(days=2), paid=True, today=today,
        )
        check("a day before they joined the group is 'not_enrolled'",
              notyet == "not_enrolled", notyet)

        cancelled = student_service._session_state(
            session=_Stub("cancelled", today - _timedelta(days=9)),
            attendance="PRESENT", has_register_row=True, enrolled_on=None,
            paid=True, today=today,
        )
        check("a cancelled session outranks the register",
              cancelled == "cancelled", cancelled)

        db.session.rollback()

    if row is not None:
        after = db.session.get(SessionStudent, row.id)
        check("the register row is back to its original status after rollback",
              after.status == original,
              f"status={after.status!r}, was {original!r}")

print("\n" + "=" * 68)
print("ALL PASS" if not failures else "FAILURES: " + ", ".join(sorted(set(failures))))
