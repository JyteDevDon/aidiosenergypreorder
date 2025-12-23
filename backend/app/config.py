import os
from dotenv import load_dotenv

load_dotenv()

def env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)

APP_ENV = env("APP_ENV", "dev")
CORS_ALLOW_ORIGINS = env("CORS_ALLOW_ORIGINS", "*")
DATABASE_URL = env("DATABASE_URL", "sqlite:////data/app.db")
TOTAL_SLOTS = int(env("TOTAL_SLOTS", "100") or 100)

SMTP_HOST = env("SMTP_HOST")
SMTP_PORT = int(env("SMTP_PORT", "587") or 587)
SMTP_USER = env("SMTP_USER")
SMTP_PASS = env("SMTP_PASS")
SMTP_FROM = env("SMTP_FROM", "no-reply@aidiosbridgeway.com")
SMTP_TO = env("SMTP_TO", "energy@aidiosbridgeway.com")
