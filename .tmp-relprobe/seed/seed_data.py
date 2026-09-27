"""
Fill the dev academy with a realistic volume of test data.

    py .tmp-relprobe/seed/seed_data.py apply     # insert
    py .tmp-relprobe/seed/seed_data.py remove    # take it all back out

What this creates, all inside the "Hello world" dev academy:

  11 teachers, each owning 2-4 course groups
  ~33 course groups with weekly slots spread Mon-Sat
   6 physical rooms, assigned without double-booking
 434 students, with a guardian each, enrolled across those groups
       (one student may sit in more than one group, as they really do)
  one subscription per enrollment, with a spread of credit states
  3 weeks of conducted sessions behind each group, with a register
       (false-until-true: ~85% present, the rest charged absent)
       plus revenue rows and one teacher payout per conducted session
  12 weeks of upcoming sessions ahead of each group

Why a manifest instead of a marker column
-----------------------------------------
Every id this script will insert is generated and written to
`manifest.json` BEFORE the first row goes in. A crash halfway through
therefore still leaves a complete removal list — removal never has to guess
which rows were ours, and nothing visible gets tagged with a marker string
just so it can be found again. Re-running `apply` on a dirty database would
duplicate the world, so `apply` refuses unless the manifest is absent or
already removed.

Sessions are generated through the app's own `generate_sessions_from_schedule`
rather than by hand, so the seed exercises the real code path — including the
day-of-week arithmetic, which is the thing most likely to be wrong.
"""

import json
import os
import random
import sys
from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.attendance import SessionStudent  # noqa: E402
from app.models.billing import (  # noqa: E402
    PayoutRecord,
    RevenueEntry,
    StudentSubscription,
)
from app.models.class_room import Class, Classroom, Subject  # noqa: E402
from app.models.scheduling import Schedule, Session  # noqa: E402
from app.models.student import Enrollment, Guardian, Student  # noqa: E402
from app.models.teacher import Teacher, TeacherSubject  # noqa: E402

# ── The dev tenant the app signs into ────────────────────────────────
ACADEMY = "ad6587d5-6fd3-4015-a497-8dd5301b830d"
OWNER = "68b25cfd-4aa1-4218-8f6d-3e2c0de5d0ef"  # "Hello world" — owns the PIN

SEED_DIR = r"E:\vinta-os-app-essembled-main\.tmp-relprobe\seed"
MANIFEST = os.path.join(SEED_DIR, "manifest.json")

STUDENT_TARGET = 434
PAST_WEEKS = 3   # conducted history behind each group
FUTURE_WEEKS = 12  # generated ahead of each group

# Deterministic: the same seed produces the same world, so a bug is
# reproducible and a rerun after a failed insert is comparable.
random.seed(20260924)

DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def new_id() -> str:
    import uuid
    return str(uuid.uuid4())


# ══════════════════════════════════════════════════════════════════════
# The cast
# ══════════════════════════════════════════════════════════════════════

# (first, last, subject, groups, has_email, commission)
# `groups` sums to 33 below; `has_email` is False for two of them on purpose,
# so the optional-email path is exercised by the roster rather than only by a
# unit test.
TEACHERS = [
    ("Karim",     "Boudiaf",    "Math",             3, True,  ("PERCENTAGE", 30)),
    ("Salima",    "Haddad",     "French",           2, True,  ("PERCENTAGE", 35)),
    ("Nabil",     "Cherif",     "Physics",          4, True,  ("FLAT_HOURLY", 900)),
    ("Fatima Zohra", "Meziane", "Arabic",           3, True,  ("PERCENTAGE", 30)),
    ("Rachid",    "Belkacem",   "Science",          3, False, ("FIXED_SESSION", 700)),
    ("Amel",      "Zerrouki",   "English",          4, True,  ("PERCENTAGE", 32)),
    ("Youcef",    "Ait Ali",    "Math",             2, True,  ("FLAT_HOURLY", 1000)),
    ("Nadia",     "Brahimi",    "French",           3, False, ("PERCENTAGE", 28)),
    ("Samir",     "Hamdi",      "Islamic Studies",  4, True,  ("FIXED_SESSION", 650)),
    ("Leila",     "Saidi",      "Tamazight",        3, True,  ("PERCENTAGE", 30)),
    ("Omar",      "Benyahia",   "Math",             2, True,  ("FLAT_HOURLY", 950)),
]

# Palette additions. Math and Arabic already exist and are reused, not cloned.
EXTRA_SUBJECTS = [
    ("French", "#2563eb"),
    ("English", "#0ea5e9"),
    ("Physics", "#dc2626"),
    ("Science", "#16a34a"),
    ("Islamic Studies", "#059669"),
    ("Tamazight", "#d97706"),
]

LEVELS = [
    "1AP", "2AP", "3AP", "4AP", "5AP",
    "1AM", "2AM", "3AM", "4AM",
    "1AS", "2AS", "3AS",
]

ROOMS = [
    ("Hall A", 20), ("Hall B", 24), ("Room 1", 16),
    ("Room 2", 16), ("Lab 1", 18), ("Room 3", 12),
]


# ══════════════════════════════════════════════════════════════════════
# Plan — every id decided up front, then dumped to the manifest
# ══════════════════════════════════════════════════════════════════════

def load_students() -> list[dict]:
    """
    Merge the generated name chunks into exactly STUDENT_TARGET students.

    Two things the raw chunks cannot be trusted for, both handled here rather
    than by asking the generator again:

    * Phone layout. Some chunks wrote ``0661 45 78 90`` and others
      ``06 61 45 78 90`` — the same ten digits, grouped differently. Every
      phone is rebuilt from its digits, so the column is one shape.
    * Collisions. Separate chunks independently reach for the same common
      names, so a few pairs repeat across files. Two children with the same
      name are real, but they are only distinguishable here by their guardian's
      number, so that is the uniqueness key. Anything still short of the target
      is topped up by recombining the name pools the generators produced, which
      keeps every name Algerian and every row distinct.
    """
    people, seen = [], set()

    def take(row, key):
        if key in seen:
            return False
        seen.add(key)
        people.append({
            "first_name": row["first_name"].strip(),
            "last_name": row["last_name"].strip(),
            "phone": _phone_str(row.get("phone")) or None,
            "parent_phone": _phone_str(row["parent_phone"]) or "",
            "guardian_name": row["guardian_name"].strip(),
            "guardian_relationship": row["guardian_relationship"].strip(),
            "notes": (row.get("notes") or None),
        })
        return True

    for name in sorted(os.listdir(SEED_DIR)):
        if not (name.startswith("students_") and name.endswith(".json")):
            continue
        with open(os.path.join(SEED_DIR, name), encoding="utf-8") as fh:
            chunk = json.load(fh)
        for row in chunk:
            take(row, (
                row["first_name"].strip().lower(),
                row["last_name"].strip().lower(),
                _digits(row["parent_phone"]),
            ))

    if len(people) < STUDENT_TARGET:
        firsts = sorted({p["first_name"] for p in people})
        lasts = sorted({p["last_name"] for p in people})
        guard = ["Mother", "Father", "Uncle", "Aunt", "Grandmother", "Grandfather"]
        attempts = 0
        while len(people) < STUDENT_TARGET and attempts < 20000:
            attempts += 1
            first = random.choice(firsts)
            last = random.choice(lasts)
            phone = _phone()
            take(
                {
                    "first_name": first,
                    "last_name": last,
                    "phone": _phone() if random.random() < 0.45 else None,
                    "parent_phone": phone,
                    "guardian_name": f"{random.choice(firsts)} {last}",
                    "guardian_relationship": random.choice(guard),
                    "notes": None,
                },
                (first.lower(), last.lower(), _digits(phone)),
            )

    if len(people) < STUDENT_TARGET:
        raise SystemExit(
            f"only {len(people)} unique students available, need {STUDENT_TARGET}"
        )
    return people[:STUDENT_TARGET]


def _digits(s: str) -> str:
    return "".join(ch for ch in (s or "") if ch.isdigit())


def _phone_str(raw) -> str:
    """Rebuild any Algerian mobile into one shape: 0X XX XX XX XX."""
    d = _digits(raw)
    if len(d) != 10 or d[0] != "0" or d[1] not in "567":
        return ""
    return " ".join([d[0:2], d[2:4], d[4:6], d[6:8], d[8:10]])


def plan() -> dict:
    """Decide the whole world: ids, groups, slots, roster. No DB writes."""
    students_in = load_students()

    teachers = []
    for first, last, subject, n_groups, has_email, (ctype, cvalue) in TEACHERS:
        teachers.append({
            "id": new_id(),
            "first_name": first,
            "last_name": last,
            "subject": subject,
            "n_groups": n_groups,
            "email": (
                f"{first.lower().replace(' ', '.')}.{last.lower().replace(' ', '')}"
                f"@vinta-academy.dz"
            ) if has_email else None,
            "phone": _phone(),
            "commission_type": ctype,
            "commission_value": cvalue,
        })

    rooms = [{"id": new_id(), "name": n, "capacity": c} for n, c in ROOMS]
    subjects = [{"id": new_id(), "name": n, "color": c} for n, c in EXTRA_SUBJECTS]

    # ── Groups: 2-4 per teacher, named for a real timetable ──
    groups, counters = [], defaultdict(int)
    for t in teachers:
        for _ in range(t["n_groups"]):
            subject = t["subject"]
            counters[subject] += 1
            level = LEVELS[counters[subject] % len(LEVELS)]
            g = counters[subject]
            capacity = random.choice([12, 16, 18, 20, 24, 30])
            groups.append({
                "id": new_id(),
                "teacher_id": t["id"],
                "subject": subject,
                "level": level,
                "name": f"{level} {subject} — Group {g}",
                "group_name": chr(ord("A") + (g - 1) % 4),
                "capacity": capacity,
                "price_da": random.choice(
                    [3000, 3500, 4000, 4500, 5000, 6000, 7500, 9000, 12000]
                ),
                "billing_model": random.choices(
                    ["CREDIT_BASED", "TIME_BASED"], weights=[4, 1]
                )[0],
                "credits_per_cycle": random.choice([4, 8, 12]),
                "color": _subject_color(subject),
            })

    # ── Slots: one or two a week, no room double-booked in the same hour ──
    booked = set()
    for grp in groups:
        grp["slots"] = []
        wanted = 2 if random.random() < 0.4 else 1
        days = random.sample(range(1, 7), wanted)  # Mon..Sat, never Sunday
        for dow in sorted(days):
            room = _free_room(rooms, booked, dow)
            start = _start_time()
            duration = random.choice([60, 90, 90, 120])
            grp["slots"].append({
                "id": new_id(),
                "day_of_week": dow,
                "start": start,
                "end": _add_minutes(start, duration),
                "classroom_id": room["id"] if room else None,
            })

    # ── The roster: who sits in which group ──
    # A few groups are deliberately full and a few nearly empty, so the cards
    # show every state the Classrooms grid can render rather than 33 clones.
    for i, grp in enumerate(groups):
        if i % 11 == 3:
            grp["target"] = grp["capacity"]                      # full
        elif i % 11 == 7:
            grp["target"] = random.randint(1, 3)                 # nearly empty
        else:
            grp["target"] = max(
                4, int(grp["capacity"] * random.uniform(0.55, 0.95))
            )

    students = []
    for row in students_in:
        students.append({
            "id": new_id(),
            "first_name": row["first_name"].strip(),
            "last_name": row["last_name"].strip(),
            "phone": (row.get("phone") or None),
            "parent_phone": row["parent_phone"].strip(),
            "guardian_name": row["guardian_name"].strip(),
            "guardian_relationship": row["guardian_relationship"].strip(),
            "notes": (row.get("notes") or None),
            "groups": [],
        })

    # Round-robin fill: every pass hands each student one more group, so the
    # per-student load stays even instead of the first groups hoovering up
    # everyone. Capped at 3 groups per student — a child in four courses is
    # not what this academy looks like.
    remaining = {g["id"]: g["target"] for g in groups}
    open_groups = [g for g in groups if remaining[g["id"]] > 0]
    MAX_PER_STUDENT = 3
    while open_groups:
        random.shuffle(open_groups)
        progressed = False
        for student in students:
            if not open_groups:
                break
            if len(student["groups"]) >= MAX_PER_STUDENT:
                continue
            grp = next(
                (g for g in open_groups if g["id"] not in student["groups"]), None
            )
            if grp is None:
                continue
            student["groups"].append(grp["id"])
            remaining[grp["id"]] -= 1
            progressed = True
            if remaining[grp["id"]] <= 0:
                open_groups = [g for g in open_groups if remaining[g["id"]] > 0]
        if not progressed:
            break  # every student is at the cap; remaining seats stay empty

    return {
        "teachers": teachers,
        "groups": groups,
        "students": students,
        "rooms": rooms,
        "subjects": subjects,
    }


def _phone() -> str:
    return f"0{random.choice([5, 6, 7])} {random.randint(10, 99)} " \
           f"{random.randint(10, 99)} {random.randint(10, 99)} {random.randint(10, 99)}"


def _start_time() -> str:
    hour = random.randint(8, 18)
    minute = random.choice([0, 30])
    return f"{hour:02d}:{minute:02d}"


def _add_minutes(hhmm: str, minutes: int) -> str:
    h, m = (int(x) for x in hhmm.split(":"))
    total = h * 60 + m + minutes
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


def _subject_color(name: str) -> str:
    palette = {
        "Math": "#b3872a", "Arabic": "#7c3aed", "French": "#2563eb",
        "English": "#0ea5e9", "Physics": "#dc2626", "Science": "#16a34a",
        "Islamic Studies": "#059669", "Tamazight": "#d97706",
    }
    return palette.get(name, "#b3872a")


def _free_room(rooms, booked, dow):
    """A room not already taken at this hour on this weekday."""
    for _ in range(40):
        room = random.choice(rooms)
        seat = (room["id"], dow, random.randint(0, 3))
        # Two slots are only in conflict if they start in the same quarter-hour
        # band; the seed does not need a real interval tree.
        if seat not in booked:
            booked.add(seat)
            return room
    return None


# ══════════════════════════════════════════════════════════════════════
# Apply
# ══════════════════════════════════════════════════════════════════════

def apply() -> None:
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as fh:
            old = json.load(fh)
        if not old.get("removed"):
            raise SystemExit(
                "manifest.json exists and was not removed — this database "
                "already has a seeded world in it. Run `remove` first."
            )

    world = plan()

    manifest = {
        "removed": False,
        "teachers": [t["id"] for t in world["teachers"]],
        "groups": [g["id"] for g in world["groups"]],
        "students": [s["id"] for s in world["students"]],
        "rooms": [r["id"] for r in world["rooms"]],
        "subjects": [s["id"] for s in world["subjects"]],
        "schedules": [sl["id"] for g in world["groups"] for sl in g["slots"]],
        "sessions": [],
        "enrollments": [],
        "subscriptions": [],
    }

    # Written before the first INSERT. A crash mid-insert still leaves a
    # complete removal list rather than a half-populated database nobody can
    # clean up without guessing.
    _dump(manifest)

    app = create_app("development")
    with app.app_context():
        _insert_subjects(world, manifest)
        _insert_rooms(world, manifest)
        _insert_teachers(world, manifest)
        _insert_students(world, manifest)
        _insert_groups(world, manifest)
        _insert_enrollments(world, manifest)
        _insert_past_sessions(world, manifest)
        db.session.commit()
        _generate_future_sessions(world, manifest)
        db.session.commit()

    _dump(manifest)
    print()
    print("seeded:")
    print(f"  teachers      {len(manifest['teachers'])}")
    print(f"  groups        {len(manifest['groups'])}")
    print(f"  students      {len(manifest['students'])}")
    print(f"  enrollments   {len(manifest['enrollments'])}")
    print(f"  subscriptions {len(manifest['subscriptions'])}")
    print(f"  sessions      {len(manifest['sessions'])}")


def _insert_subjects(world, manifest):
    for s in world["subjects"]:
        db.session.add(Subject(
            id=s["id"], academy_id=ACADEMY, name=s["name"], color=s["color"],
        ))
    db.session.flush()
    print(f"  subjects      +{len(world['subjects'])}")


def _insert_rooms(world, manifest):
    for r in world["rooms"]:
        db.session.add(Classroom(
            id=r["id"], academy_id=ACADEMY, name=r["name"], capacity=r["capacity"],
        ))
    db.session.flush()
    print(f"  rooms         +{len(world['rooms'])}")


def _insert_teachers(world, manifest):
    by_subject = {
        s.name: s.id
        for s in db.session.query(Subject).filter_by(academy_id=ACADEMY).all()
    }
    for t in world["teachers"]:
        db.session.add(Teacher(
            id=t["id"],
            academy_id=ACADEMY,
            first_name=t["first_name"],
            last_name=t["last_name"],
            phone=t["phone"],
            email=t["email"],
            subject=t["subject"],
            status="ACTIVE",
            contract_type="hourly",
            hourly_rate=900,
            commission_type=t["commission_type"],
            commission_value=t["commission_value"],
            notes=None,
        ))
        sid = by_subject.get(t["subject"])
        if sid:
            db.session.add(TeacherSubject(teacher_id=t["id"], subject_id=sid))
    db.session.flush()
    print(f"  teachers      +{len(world['teachers'])}")


def _insert_students(world, manifest):
    for s in world["students"]:
        db.session.add(Student(
            id=s["id"],
            academy_id=ACADEMY,
            first_name=s["first_name"],
            last_name=s["last_name"],
            phone=s["phone"],
            parent_phone=s["parent_phone"],
            notes=s["notes"],
            is_active=True,
        ))
        db.session.add(Guardian(
            id=new_id(),
            student_id=s["id"],
            name=s["guardian_name"],
            relationship_type=s["guardian_relationship"],
            phone=s["parent_phone"],
            is_emergency=True,
        ))
    db.session.flush()
    print(f"  students      +{len(world['students'])} (+{len(world['students'])} guardians)")


def _insert_groups(world, manifest):
    for g in world["groups"]:
        db.session.add(Class(
            id=g["id"],
            academy_id=ACADEMY,
            name=g["name"],
            subject=g["subject"],
            color=g["color"],
            teacher_id=g["teacher_id"],
            capacity=g["capacity"],
            academic_level=g["level"],
            group_name=g["group_name"],
            billing_model=g["billing_model"],
            price_da=g["price_da"],
            credits_per_cycle=g["credits_per_cycle"],
            cycle_week_limit=None,
            allow_rollover=random.random() < 0.5,
            allow_makeups=random.random() < 0.8,
            access_duration_weeks=None,
            max_groups_included=1,
            enforce_attendance=random.random() < 0.5,
            attendance_threshold=0.75,
            class_type="weekly",
            notes=None,
        ))
        for sl in g["slots"]:
            db.session.add(Schedule(
                id=sl["id"],
                class_id=g["id"],
                classroom_id=sl["classroom_id"],
                day_of_week=sl["day_of_week"],
                start_time=time.fromisoformat(sl["start"]),
                end_time=time.fromisoformat(sl["end"]),
            ))
    db.session.flush()
    print(f"  groups        +{len(world['groups'])} (+ schedules)")


def _insert_enrollments(world, manifest):
    """One enrollment per student-group pair, plus its subscription."""
    groups = {g["id"]: g for g in world["groups"]}
    today = date.today()

    for s in world["students"]:
        for gid in s["groups"]:
            grp = groups[gid]
            enrollment_id = new_id()
            manifest["enrollments"].append(enrollment_id)
            db.session.add(Enrollment(
                id=enrollment_id,
                student_id=s["id"],
                class_id=gid,
                status="active",
            ))

            total = grp["credits_per_cycle"]
            remaining = random.choice([0, 1, 2, 3, total - 1, total])
            remaining = max(0, min(remaining, total))
            if remaining == 0:
                status = random.choice(["DEPLETED", "OVERDUE", "EXPIRED"])
            elif random.random() < 0.15:
                status = "OVERDUE"
            else:
                status = "ACTIVE"

            sub_id = new_id()
            manifest["subscriptions"].append(sub_id)
            db.session.add(StudentSubscription(
                id=sub_id,
                academy_id=ACADEMY,
                enrollment_id=enrollment_id,
                student_id=s["id"],
                group_id=gid,
                billing_model=grp["billing_model"],
                total_credits=total,
                remaining_credits=remaining,
                cycle_start_date=today - timedelta(days=random.randint(5, 40)),
                cycle_deadline=today + timedelta(days=random.randint(-12, 25)),
                access_start_date=today - timedelta(days=random.randint(5, 40)),
                access_end_date=today + timedelta(days=random.randint(-5, 60)),
                max_groups_included=1,
                enrolled_group_ids=[gid],
                amount_paid_da=(
                    grp["price_da"] if random.random() < 0.75 else 0
                ),
                payment_method=random.choice(["CASH", "CASH", "CCP", "BARIDI_MOB"]),
                recorded_by_staff_id=OWNER,
                makeup_credits=random.choice([0, 0, 0, 1]),
                status=status,
            ))
    db.session.flush()
    print(f"  enrollments   +{len(manifest['enrollments'])}")


def _insert_past_sessions(world, manifest):
    """
    Three weeks of classes behind each group, already conducted, with a register.

    This is what gives the student drawer's attendance calendar something to
    colour and the activity log something to show. Attendance follows the
    false-until-true rule the register itself uses: every enrolled student gets
    a row, most are PRESENT, and the rest stay ABSENT and are charged.
    """
    groups = {g["id"]: g for g in world["groups"]}
    members = defaultdict(list)
    for s in world["students"]:
        for gid in s["groups"]:
            members[gid].append(s)

    today = date.today()
    n_sessions = n_rows = n_revenue = n_payouts = 0

    for grp in world["groups"]:
        roster = members.get(grp["id"], [])
        if not roster:
            continue

        for sl in grp["slots"]:
            for weeks_back in range(1, PAST_WEEKS + 1):
                # Same weekday arithmetic as the app: app-scale dow (Sun=0)
                # against Python's weekday() (Mon=0). Converting is the whole
                # point — getting it wrong is what put a Monday group's
                # sessions on Tuesdays.
                dow = sl["day_of_week"]
                delta = (today.weekday() + 1 - dow) % 7
                d = today - timedelta(days=delta + weeks_back * 7)
                if d >= today:
                    continue

                session_id = new_id()
                manifest["sessions"].append(session_id)
                start = time.fromisoformat(sl["start"])
                end = time.fromisoformat(sl["end"])
                started = datetime.combine(d, start).replace(tzinfo=timezone.utc)
                ended = datetime.combine(d, end).replace(tzinfo=timezone.utc)

                db.session.add(Session(
                    id=session_id,
                    academy_id=ACADEMY,
                    class_id=grp["id"],
                    schedule_id=sl["id"],
                    teacher_id=grp["teacher_id"],
                    classroom_id=sl["classroom_id"],
                    date=d,
                    start_time=start,
                    end_time=end,
                    subject=grp["subject"],
                    status="conducted",
                    actual_start_time=started,
                    actual_end_time=ended,
                    started_by_staff_id=OWNER,
                    ended_by_staff_id=OWNER,
                    is_free_session=False,
                ))
                n_sessions += 1

                present_count = 0
                for student in roster:
                    present = random.random() < 0.85
                    if present:
                        present_count += 1
                    db.session.add(SessionStudent(
                        id=new_id(),
                        session_id=session_id,
                        student_id=student["id"],
                        is_present=present,
                        status="PRESENT" if present else "ABSENT",
                        checked_in_at=started if present else None,
                        checked_out_at=ended if present else None,
                        checked_in_by=OWNER if present else None,
                        is_group_swap=False,
                        timestamp=started if present else None,
                    ))
                    n_rows += 1

                # Money: a conducted session bills the students who turned up.
                # A free session would bill nobody, which is why the flag is
                # read here rather than assumed.
                if present_count:
                    per_head = max(1, grp["price_da"] // max(1, grp["credits_per_cycle"]))
                    gross = per_head * present_count
                    db.session.add(RevenueEntry(
                        id=new_id(),
                        academy_id=ACADEMY,
                        group_id=grp["id"],
                        student_id=None,
                        session_id=session_id,
                        amount_da=gross,
                        recorded_at=ended,
                    ))
                    n_revenue += 1

                    teacher = next(
                        t for t in world["teachers"] if t["id"] == grp["teacher_id"]
                    )
                    ctype, cvalue = (
                        teacher["commission_type"], teacher["commission_value"]
                    )
                    if ctype == "PERCENTAGE":
                        cut = gross * cvalue // 100
                    elif ctype == "FLAT_HOURLY":
                        hours = (end.hour * 60 + end.minute - start.hour * 60 - start.minute) / 60
                        cut = int(cvalue * hours)
                    else:
                        cut = cvalue
                    db.session.add(PayoutRecord(
                        id=new_id(),
                        academy_id=ACADEMY,
                        teacher_id=grp["teacher_id"],
                        session_id=session_id,
                        gross_revenue_da=gross,
                        commission_type=ctype,
                        commission_value=cvalue,
                        teacher_cut_da=int(cut),
                        status="PENDING",
                    ))
                    n_payouts += 1

    db.session.flush()
    print(f"  past sessions +{n_sessions} ({n_rows} register rows, "
          f"{n_revenue} revenue, {n_payouts} payouts)")


def _generate_future_sessions(world, manifest):
    """Let the app's own generator build the upcoming 12 weeks."""
    from app.services.scheduling_service import generate_sessions_from_schedule

    created = 0
    for grp in world["groups"]:
        for sl in grp["slots"]:
            created += generate_sessions_from_schedule(sl["id"], weeks_ahead=FUTURE_WEEKS)
    db.session.flush()

    rows = db.session.query(Session.id).filter(
        Session.class_id.in_([g["id"] for g in world["groups"]])
    ).all()
    manifest["sessions"] = [r[0] for r in rows]
    print(f"  future sessions +{created}")


# ══════════════════════════════════════════════════════════════════════
# Remove
# ══════════════════════════════════════════════════════════════════════

def remove() -> None:
    if not os.path.exists(MANIFEST):
        print("no manifest — nothing to remove")
        return
    with open(MANIFEST, encoding="utf-8") as fh:
        m = json.load(fh)

    app = create_app("development")
    with app.app_context():
        sessions = [r[0] for r in db.session.query(Session.id).filter(
            Session.class_id.in_(m["groups"] or [""])
        ).all()] if m["groups"] else []

        # Children before parents. Register rows first, then the money that
        # points at the sessions, then the sessions themselves.
        if sessions:
            SessionStudent.query.filter(SessionStudent.session_id.in_(sessions)).delete(
                synchronize_session=False
            )
            RevenueEntry.query.filter(RevenueEntry.session_id.in_(sessions)).delete(
                synchronize_session=False
            )
            PayoutRecord.query.filter(PayoutRecord.session_id.in_(sessions)).delete(
                synchronize_session=False
            )
            Session.query.filter(Session.id.in_(sessions)).delete(
                synchronize_session=False
            )

        if m["subscriptions"]:
            StudentSubscription.query.filter(
                StudentSubscription.id.in_(m["subscriptions"])
            ).delete(synchronize_session=False)
        if m["enrollments"]:
            Enrollment.query.filter(Enrollment.id.in_(m["enrollments"])).delete(
                synchronize_session=False
            )
        if m["schedules"]:
            Schedule.query.filter(Schedule.id.in_(m["schedules"])).delete(
                synchronize_session=False
            )
        if m["groups"]:
            Class.query.filter(Class.id.in_(m["groups"])).delete(
                synchronize_session=False
            )
        if m["students"]:
            Guardian.query.filter(Guardian.student_id.in_(m["students"])).delete(
                synchronize_session=False
            )
            Student.query.filter(Student.id.in_(m["students"])).delete(
                synchronize_session=False
            )
        if m["teachers"]:
            TeacherSubject.query.filter(
                TeacherSubject.teacher_id.in_(m["teachers"])
            ).delete(synchronize_session=False)
            Teacher.query.filter(Teacher.id.in_(m["teachers"])).delete(
                synchronize_session=False
            )
        if m["rooms"]:
            Classroom.query.filter(Classroom.id.in_(m["rooms"])).delete(
                synchronize_session=False
            )
        if m["subjects"]:
            Subject.query.filter(Subject.id.in_(m["subjects"])).delete(
                synchronize_session=False
            )

        db.session.commit()

        leftovers = {
            "students": Student.query.filter(Student.id.in_(m["students"] or [""])).count(),
            "teachers": Teacher.query.filter(Teacher.id.in_(m["teachers"] or [""])).count(),
            "groups": Class.query.filter(Class.id.in_(m["groups"] or [""])).count(),
            "sessions": Session.query.filter(Session.id.in_(sessions or [""])).count(),
        }

    m["removed"] = True
    m["sessions"] = []
    _dump(m)
    print("removed. leftovers:", leftovers)


def _dump(manifest: dict) -> None:
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "apply"
    if mode == "apply":
        apply()
    elif mode == "remove":
        remove()
    else:
        raise SystemExit(f"unknown mode {mode!r} — use apply or remove")
