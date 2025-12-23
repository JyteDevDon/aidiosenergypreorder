from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .db import SessionLocal, engine, Base
from .config import CORS_ALLOW_ORIGINS
from .schemas import StatusOut, PriorityIn, PriorityOut, InsiderIn, InsiderOut
from .service import get_status, allocate_priority_slot, save_submission
from .storage import write_submission_text
from .emailer import send_email

app = FastAPI(title="Aidios Bridgeway Backend", version="1.0.0")

# CORS
origins = [o.strip() for o in (CORS_ALLOW_ORIGINS or "*").split(",")] if CORS_ALLOW_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    # Create tables
    Base.metadata.create_all(bind=engine)

@app.get("/api/status", response_model=StatusOut)
def status(db: Session = Depends(get_db)):
    total, remaining, pct = get_status(db)
    return StatusOut(total_slots=total, slots_remaining=remaining, percent_remaining=pct)

@app.post("/api/priority", response_model=PriorityOut)
def priority(payload: PriorityIn, background: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        queue_id, total, remaining, pct = allocate_priority_slot(db)
    except ValueError:
        raise HTTPException(status_code=409, detail="All 100 Priority Slots have been filled.")

    # Build server-side text file
    now = datetime.now(timezone.utc).isoformat()
    text_body = (
        "Aidios Bridgeway Energy – Priority Slot Submission\n"
        f"Timestamp (UTC): {now}\n\n"
        f"Full Name: {payload.full_name}\n"
        f"Email: {payload.email}\n"
        f"WhatsApp: {payload.whatsapp}\n"
        f"Installation Type: {payload.install_type}\n"
        f"Current Generator Size: {payload.generator_size}\n"
        f"Approx. Daily Load: {payload.daily_load}\n"
        f"Queue ID: {queue_id}\n"
        f"Slots Remaining: {remaining}/{total} ({pct}%)\n"
    )
    file_path = write_submission_text("priority", payload.full_name, text_body)

    # Persist submission record
    save_submission(db, "priority", payload.model_dump(), queue_id=queue_id, file_path=file_path)

    # Send email in background
    subject = f"Priority Slot Confirmed – {queue_id}"
    background.add_task(send_email, subject, text_body)

    return PriorityOut(queue_id=queue_id, total_slots=total, slots_remaining=remaining, percent_remaining=pct)

@app.post("/api/insider", response_model=InsiderOut)
def insider(payload: InsiderIn, background: BackgroundTasks, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).isoformat()
    text_body = (
        "Aidios Bridgeway Energy – Insider List Submission\n"
        f"Timestamp (UTC): {now}\n\n"
        f"First Name: {payload.first_name}\n"
        f"Email: {payload.email}\n"
        f"WhatsApp: {payload.whatsapp}\n"
    )
    file_path = write_submission_text("insider", payload.first_name, text_body)
    save_submission(db, "insider", payload.model_dump(), queue_id=None, file_path=file_path)

    subject = "New Insider List Signup"
    background.add_task(send_email, subject, text_body)

    return InsiderOut(ok=True)
