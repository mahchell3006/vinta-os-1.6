"""Replace lines 358-577 of BillingConfig.tsx with the new rules block.

Boundaries are 1-based and inclusive, matching what the editor shows: the old
Toggle-1 row through the end of the old T6 row. Everything outside this range
(the gross-profit row above, the closing CardBody/Card below, the Currency card)
is left byte-for-byte alone.
"""
from pathlib import Path

ROOT = Path(r"E:\vinta-os-app-essembled-main")
TARGET = ROOT / "vinta-school-os/src/features/settings/BillingConfig.tsx"
BLOCK = ROOT / ".tmp-relprobe/rules_block.txt"

FIRST, LAST = 358, 577

lines = TARGET.read_text(encoding="utf-8").splitlines(keepends=True)
block = BLOCK.read_text(encoding="utf-8")
if not block.endswith("\n"):
    block += "\n"

before = lines[: FIRST - 1]
after = lines[LAST:]

# Guard against splicing into the wrong file: the first line replaced must open
# the old Toggle-1 row, and the last must close the old T6 row.
assert 'className="flex items-start justify-between gap-3">' in lines[FIRST - 1], lines[FIRST - 1]
block_range = "".join(lines[FIRST - 1 : LAST])
assert "toggle6Version" in block_range, "old T6 row not inside the replaced range"
assert "handleToggle1" in block_range, "old Toggle-1 row not inside the replaced range"
# The first line kept after the splice must still be the CardBody that closes
# this card — i.e. the replacement ends exactly where the old rows did.
assert "</CardBody>" in lines[LAST], lines[LAST]

out = "".join(before) + block + "".join(after)
TARGET.write_text(out, encoding="utf-8")
print(f"replaced {LAST - FIRST + 1} lines with {len(block.splitlines())}")
