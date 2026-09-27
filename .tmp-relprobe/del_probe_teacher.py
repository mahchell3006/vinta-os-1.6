"""Delete a probe teacher, its groups, and everything hanging off them.

Throwaway cleanup. Ids are given on the command line, and the counts are printed
before the commit: a teacher whose group still had 12 sessions on the calendar
cannot be removed quietly, and `sessions.teacher_id` is NOT NULL, so the order
matters — register, sessions, schedules, group, teacher.

Log rows that name any of these rows are removed too. They are written by
`log_activity` with the entity id, and this project has already been bitten once
by deleting a row and leaving its log entries pointing at nothing.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.attendance import SessionStudent  # noqa: E402
from app.models.audit import ActivityLog  # noqa: E402
from app.models.billing import RevenueEntry  # noqa: E402
from app.models.class_room import Class  # noqa: E402
from app.models.scheduling import Schedule, Session  # noqa: E402
from app.models.student import Enrollment  # noqa: E402
from app.models.teacher import Teacher, TeacherHoursLog, TeacherPayroll, TeacherSubject  # noqa: E402

IDS = sys.argv[1:]
if not IDS:
    print("usage: del_probe_teacher.py <teacher-id> [more...]")
    sys.exit(1)

app = create_app("development")
with app.app_context():
    for tid in IDS:
        t = db.session.get(Teacher, tid)
        if t is None:
            print(f"  {tid}  NOT FOUND — skipped")
            continue
        print(f"  {tid}  {t.first_name!r} {t.last_name!r}  email={t.email!r}  status={t.status}")
        counts: dict[str, int] = {}

        groups = db.session.query(Class).filter_by(teacher_id=tid).all()
        for g in groups:
            print(f"      group {g.id} {g.name!r}")
            # Register rows first: session_students points at both.
            sess_ids = [s.id for s in db.session.query(Session).filter_by(class_id=g.id).all()]
            counts["register"] = (
                db.session.query(SessionStudent)
                .filter(SessionStudent.session_id.in_(sess_ids))
                .delete(synchronize_session=False)
                if sess_ids
                else 0
            )
            counts["sessions"] = db.session.query(Session).filter_by(class_id=g.id).delete(
                synchronize_session=False
            )
            counts["schedules"] = db.session.query(Schedule).filter_by(class_id=g.id).delete(
                synchronize_session=False
            )
            counts["enrollments"] = db.session.query(Enrollment).filter_by(class_id=g.id).delete(
                synchronize_session=False
            )
            counts["class_logs"] = (
                db.session.query(ActivityLog)
                .filter(ActivityLog.entity_type == "class", ActivityLog.entity_id == g.id)
                .delete(synchronize_session=False)
            )
            # revenue_entries points at the group as `group_id` and at the
            # session as `session_id` — not `class_id`, and it carries
            # `recorded_at` rather than `created_at`.
            from sqlalchemy import or_
            counts["revenue"] = (
                db.session.query(RevenueEntry)
                .filter(
                    or_(
                        RevenueEntry.group_id == g.id,
                        RevenueEntry.session_id.in_(sess_ids) if sess_ids else False,
                    )
                )
                .delete(synchronize_session=False)
            )
            counts["class"] = db.session.query(Class).filter(Class.id == g.id).delete(
                synchronize_session=False
            )

        counts["payroll"] = db.session.query(TeacherPayroll).filter_by(teacher_id=tid).delete(
            synchronize_session=False
        )
        counts["hours"] = db.session.query(TeacherHoursLog).filter_by(teacher_id=tid).delete(
            synchronize_session=False
        )
        counts["subject_links"] = db.session.query(TeacherSubject).filter_by(teacher_id=tid).delete(
            synchronize_session=False
        )
        counts["teacher_logs"] = (
            db.session.query(ActivityLog)
            .filter(ActivityLog.entity_type == "teacher", ActivityLog.entity_id == tid)
            .delete(synchronize_session=False)
        )
        counts["teacher"] = db.session.query(Teacher).filter(Teacher.id == tid).delete(
            synchronize_session=False
        )
        db.session.commit()
        print("      " + "  ".join(f"{k}={v}" for k, v in counts.items()))
        print(f"      gone: {db.session.get(Teacher, tid) is None}")
