"""
One-off repair: put Group A's 2026-10-06 session back to `scheduled`.

What happened
-------------
`start_session` had no clock guard, so this class was started on 2026-09-24 —
twelve days before its own date. It has sat `in_progress` ever since, which is
what put a permanent green lamp on the Classrooms tab for a class a fortnight
away, and what materialised a two-row register for a class nobody ran.

The desk's decision (asked and answered): reset it to `scheduled`.

Why the register rows are deleted and not left
----------------------------------------------
`start_session` calls `materialize_roster`, which only ADDS rows for students
who do not already have one. So leaving these two behind would mean the class,
when it genuinely starts on 2026-10-06, opens with two phantom rows already on
the register and no record of them being created — and "a `scheduled` session
has no register" is the invariant everything downstream is written against.
The rows carry no attendance (both ABSENT, `timestamp` NULL); they are pure
artifacts of the bogus start, so removing them restores the invariant rather
than discarding any fact.

The `started` ActivityLog line is deliberately NOT deleted. Audit history is
not something to quietly rewrite: it is the record that this start happened,
and it is how anyone later wondering why the status was reset finds out.

Run:  python .tmp-relprobe/reset_group_a_oct6.py
"""

import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

SESSION_ID = "40a3c48e-fbdf-4fc5-ae80-1062ca6c59c7"
DB = Path(__file__).resolve().parent.parent / "instance" / "vinta_dev.db"


def main() -> int:
    if not DB.exists():
        print(f"no database at {DB}", file=sys.stderr)
        return 1

    backup = DB.with_name(
        f"{DB.name}.bak-{datetime.now():%Y%m%d-%H%M%S}-preGroupARepair"
    )
    shutil.copy2(DB, backup)
    print(f"backed up -> {backup.name}")

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    before = conn.execute(
        "SELECT status, actual_start_time, started_by_staff_id FROM sessions WHERE id = ?",
        (SESSION_ID,),
    ).fetchone()
    if before is None:
        print(f"session {SESSION_ID} not found — nothing to do", file=sys.stderr)
        return 1

    print("before:", dict(before))

    if before["status"] != "in_progress":
        print(
            f"status is {before['status']!r}, not 'in_progress' — already repaired "
            "or changed by something else. Refusing to guess.",
            file=sys.stderr,
        )
        return 1

    with conn:  # one transaction: either the reset lands whole or not at all
        removed = conn.execute(
            "DELETE FROM session_students WHERE session_id = ?", (SESSION_ID,)
        ).rowcount
        conn.execute(
            """UPDATE sessions
                  SET status = 'scheduled',
                      actual_start_time = NULL,
                      started_by_staff_id = NULL
                WHERE id = ?""",
            (SESSION_ID,),
        )

    after = conn.execute(
        """SELECT s.status, s.actual_start_time, s.started_by_staff_id, s.date,
                  (SELECT COUNT(*) FROM session_students WHERE session_id = s.id) AS rows_left
             FROM sessions s WHERE s.id = ?""",
        (SESSION_ID,),
    ).fetchone()
    print(f"deleted {removed} register row(s)")
    print("after: ", dict(after))

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
