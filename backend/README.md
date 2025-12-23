# Aidios Bridgeway – Minimal FastAPI Backend

This backend provides:
- Global Priority Slots counter stored in SQLite
- Atomic decrement (prevents going below 0)
- Server-side text file writing per submission
- Automatic email sending via SMTP (BackgroundTasks)

## Quick start (local)

1) Copy env file:
```bash
cp .env.example .env
```

2) Update `.env` with your SMTP provider details.

3) Run:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API will be at `http://localhost:8000`.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

SQLite DB and generated submission files are stored under `./data/`.

## Endpoints

- `GET /api/status`
- `POST /api/priority`
- `POST /api/insider`

### Example payload: Priority

```json
{
  "full_name":"John Doe",
  "email":"john@example.com",
  "whatsapp":"+2348012345678",
  "install_type":"Residential",
  "generator_size":"75 kVA",
  "daily_load":"100 kW/h"
}
```

Response includes:
- `queue_id`
- `slots_remaining`
- `percent_remaining`

## Frontend integration (example)

Replace your “simulate success” section with:

```js
const res = await fetch("http://localhost:8000/api/priority", {
  method: "POST",
  headers: {"Content-Type":"application/json"},
  body: JSON.stringify(payload)
});
if(!res.ok) { const err = await res.json(); throw new Error(err.detail || "Failed"); }
const data = await res.json();
// data.queue_id, data.slots_remaining, data.percent_remaining
```

Then update the UI text:
```js
document.getElementById("ab-queue-id").textContent = data.queue_id;
document.getElementById("ab-slots-percent").textContent = `${data.percent_remaining}% of slots remaining`;
```
