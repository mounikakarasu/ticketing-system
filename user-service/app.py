import os
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "usersdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}", future=True)

app = FastAPI(title="user-service")

with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      username TEXT UNIQUE NOT NULL
    )"""))

class UserIn(BaseModel):
    username: str

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/users")
def list_users():
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id, username FROM users ORDER BY id")).mappings().all()
        return list(rows)

@app.post("/users")
def create_user(u: UserIn):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO users (username) VALUES (:username)"),
            dict(username=u.username)
        )
    return {"created": True}
