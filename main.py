from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

# CORS (important or you'll get errors in browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB INIT
def init_db():
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            event_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Event(BaseModel):
    title: str
    description: str | None = None
    event_date: str

# CREATE EVENT
@app.post("/events")
def create_event(event: Event):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO events (title, description, event_date) VALUES (?, ?, ?)",
        (event.title, event.description, event.event_date)
    )
    conn.commit()
    conn.close()
    return {"message": "Event created successfully"}

# GET ALL EVENTS
@app.get("/events")
def get_events():
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    rows = c.fetchall()
    conn.close()

    return [
        {"id": r[0], "title": r[1], "description": r[2], "event_date": r[3]}
        for r in rows
    ]

# UPDATE EVENT
@app.put("/events/{event_id}")
def update_event(event_id: int, event: Event):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute(
        "UPDATE events SET title=?, description=?, event_date=? WHERE id=?",
        (event.title, event.description, event.event_date, event_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Event updated successfully"}

# DELETE EVENT
@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    conn = sqlite3.connect("events.db")
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE id=?", (event_id,))
    conn.commit()
    conn.close()
    return {"message": "Event deleted successfully"}