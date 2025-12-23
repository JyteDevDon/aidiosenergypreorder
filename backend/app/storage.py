import os
import re
from datetime import datetime, timezone

SUBMISSIONS_DIR = "/data/submissions"

def _safe_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")[:60] or "submission"

def write_submission_text(kind: str, display_name: str, content: str) -> str:
    os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"{kind}_{ts}_{_safe_name(display_name)}.txt"
    path = os.path.join(SUBMISSIONS_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
