"""Delete the probe students this session created, and everything that points at them.

Throwaway cleanup. Every id is given explicitly on the command line: the whole
point is that the rows are named, not matched, because the duplicate-name case is
exactly the one where a query-shaped guess deletes the wrong person's record.
Real rows in this database include a student with the same name and the same
phone number as one of the probes, so `filter_by(phone=...)` would have taken it.

Counts are printed per table before and after, so "deleted" is a number and not
a claim.
"""
import os
import sys

BACKEND = r"E:\vinta-os-app-essembled-main\Backend\vinta-academy-backend"
os.chdir(BACKEND)
sys.path.insert(0, BACKEND)

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models.attendance import SessionStudent  # noqa: E402
from app.models.billing import RevenueEntry, StudentBilling, StudentSubscription  # noqa: E402
from app.models.student import Enrollment, Guardian, Student  # noqa: E402

IDS = sys.argv[1:]
if not IDS:
    print("usage: del_probe_students.py <student-id> [more...]")
    sys.exit(1)

app = create_app("development")
with app.app_context():
    for sid in IDS:
        s = db.session.get(Student, sid)
        if s is None:
            print(f"  {sid}  NOT FOUND — skipped")
            continue
        print(f"  {sid}  {s.first_name!r} {s.last_name!r}  phone={s.phone!r}  created={s.created_at}")
        counts = {}
        counts["enrollment"] = db.session.query(Enrollment).filter_by(student_id=sid).delete(
            synchronize_session=False
        )
        counts["guardian"] = db.session.query(Guardian).filter_by(student_id=sid).delete(
            synchronize_session=False
        )
        counts["session_student"] = db.session.query(SessionStudent).filter_by(student_id=sid).delete(
            synchronize_session=False
        )
        counts["student_billing"] = db.session.query(StudentBilling).filter_by(student_id=sid).delete(
            synchronize_session=False
        )
        counts["student_subscription"] = db.session.query(StudentSubscription).filter_by(
            student_id=sid
        ).delete(synchronize_session=False)
        counts["revenue_entry"] = db.session.query(RevenueEntry).filter_by(student_id=sid).delete(
            synchronize_session=False
        )
        counts["student"] = db.session.query(Student).filter(Student.id == sid).delete(
            synchronize_session=False
        )
        db.session.commit()
        print("      " + "  ".join(f"{k}={v}" for k, v in counts.items()))
        print(f"      gone: {db.session.get(Student, sid) is None}")
