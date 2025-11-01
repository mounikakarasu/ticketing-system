import os
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "ticketsdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}", future=True)

app = FastAPI(title="ticket-service")

with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS tickets (
      id SERIAL PRIMARY KEY,
      title TEXT NOT NULL,
      description TEXT,
      status TEXT NOT NULL DEFAULT 'OPEN',
      assignee TEXT
    )"""))

class TicketIn(BaseModel):
    title: str
    description: str | None = None
    assignee: str | None = None

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/tickets")
def list_tickets():
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id,title,description,status,assignee FROM tickets ORDER BY id")).mappings().all()
        return list(rows)

@app.post("/tickets")
def create_ticket(t: TicketIn):
    with engine.begin() as conn:
        conn.execute(text(
            "INSERT INTO tickets (title, description, assignee) VALUES (:title,:description,:assignee)"
        ), dict(title=t.title, description=t.description, assignee=t.assignee))
    return {"created": True}

@app.post("/tickets/{ticket_id}/status/{status}")
def update_status(ticket_id: int, status: str):
    with engine.begin() as conn:
        conn.execute(text("UPDATE tickets SET status=:s WHERE id=:i"), dict(s=status.upper(), i=ticket_id))
    return {"updated": True}
