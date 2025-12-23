import json
from sqlalchemy import text
from sqlalchemy.orm import Session
from .models import Settings, Submission
from .config import TOTAL_SLOTS

def init_settings(db: Session) -> None:
    row = db.get(Settings, 1)
    if row:
        return
    s = Settings(id=1, total_slots=TOTAL_SLOTS, slots_remaining=TOTAL_SLOTS, queue_seq=385)
    db.add(s)
    db.commit()

def get_status(db: Session) -> tuple[int,int,int]:
    init_settings(db)
    s = db.get(Settings, 1)
    assert s is not None
    pct = round((s.slots_remaining / s.total_slots) * 100) if s.total_slots else 0
    return s.total_slots, s.slots_remaining, pct

def allocate_priority_slot(db: Session) -> tuple[str, int, int, int]:
    '''
    Atomic allocation using a single UPDATE guarded by slots_remaining > 0.
    Works reliably in SQLite and prevents negative slots in concurrent requests.
    '''
    init_settings(db)

    # Atomic decrement + increment queue_seq
    result = db.execute(text("""
        UPDATE settings
        SET slots_remaining = slots_remaining - 1,
            queue_seq = queue_seq + 1
        WHERE id = 1 AND slots_remaining > 0
    """))
    if result.rowcount != 1:
        db.rollback()
        raise ValueError("No slots remaining")

    # Fetch updated values
    s = db.get(Settings, 1)
    assert s is not None
    db.commit()

    queue_id = f"#AB-{str(s.queue_seq).zfill(3)}"
    pct = round((s.slots_remaining / s.total_slots) * 100) if s.total_slots else 0
    return queue_id, s.total_slots, s.slots_remaining, pct

def save_submission(db: Session, kind: str, payload: dict, queue_id: str | None, file_path: str | None) -> None:
    sub = Submission(type=kind, payload_json=json.dumps(payload, ensure_ascii=False), queue_id=queue_id, file_path=file_path)
    db.add(sub)
    db.commit()
