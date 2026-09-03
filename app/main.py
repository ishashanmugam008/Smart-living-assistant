from __future__ import annotations

import json
import re
import sqlite3
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "aura.db"
STATIC = ROOT / "static"
DB.parent.mkdir(exist_ok=True)

app = FastAPI(title="AURA Assist API", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


def connection():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with connection() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS items (
          id TEXT PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL,
          due TEXT, priority TEXT NOT NULL DEFAULT 'medium', completed INTEGER DEFAULT 0,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, message TEXT, created_at TEXT
        );
        """)


init_db()

devices = {
    "light": {"id": "light", "name": "Living room lights", "icon": "lightbulb", "on": True, "value": 72, "unit": "%", "online": True},
    "fan": {"id": "fan", "name": "Bedroom fan", "icon": "mode_fan", "on": False, "value": 2, "unit": "speed", "online": True},
    "door": {"id": "door", "name": "Main door", "icon": "lock", "on": True, "value": "Locked", "unit": "", "online": True},
    "ac": {"id": "ac", "name": "Air conditioner", "icon": "ac_unit", "on": True, "value": 24, "unit": "°C", "online": True},
}


class ItemIn(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    category: Literal["task", "grocery"] = "task"
    due: str | None = None
    priority: Literal["low", "medium", "high"] = "medium"


class Command(BaseModel):
    text: str = Field(min_length=1, max_length=300)


class DeviceUpdate(BaseModel):
    on: bool | None = None
    value: int | str | None = None


def log(kind: str, message: str):
    with connection() as db:
        db.execute("INSERT INTO events(kind,message,created_at) VALUES(?,?,?)", (kind, message, datetime.now().isoformat(timespec="seconds")))


def parse_command(text: str):
    raw, lower = text.strip(), text.lower().strip()
    result = {"intent": "add_item", "message": "Added to your plan."}
    emergency_words = ("help me", "emergency", "sos", "i fell")
    if any(word in lower for word in emergency_words):
        return {"intent": "emergency", "message": "Emergency protocol activated. Your demo contact has been notified."}

    action = "on" if re.search(r"\b(turn on|switch on|start)\b", lower) else "off" if re.search(r"\b(turn off|switch off|stop)\b", lower) else None
    for device_id in devices:
        if device_id in lower and action:
            devices[device_id]["on"] = action == "on"
            return {"intent": "device", "device": device_id, "state": action, "message": f"{devices[device_id]['name']} turned {action}."}
    if "lock" in lower or "unlock" in lower:
        devices["door"]["on"] = "unlock" not in lower
        devices["door"]["value"] = "Locked" if devices["door"]["on"] else "Unlocked"
        return {"intent": "device", "device": "door", "state": devices["door"]["value"].lower(), "message": f"Main door {devices['door']['value'].lower()}."}

    foods = {"milk", "egg", "eggs", "bread", "rice", "apple", "fruit", "vegetable", "coffee", "tea", "grocery", "groceries"}
    category = "grocery" if any(re.search(rf"\b{re.escape(w)}\b", lower) for w in foods) else "task"
    due = date.today().isoformat()
    if "tomorrow" in lower:
        due = (date.today() + timedelta(days=1)).isoformat()
    match = re.search(r"(?:buy|add|remember to|remind me to|task)\s+(.+)", raw, re.I)
    title = (match.group(1) if match else raw)
    title = re.sub(r"\b(today|tomorrow|to groceries|to tasks|for groceries)\b", "", title, flags=re.I).strip(" .,!")
    result.update({"item": {"title": title.capitalize(), "category": category, "due": due, "priority": "high" if "urgent" in lower else "medium"}})
    return result


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/health")
def health():
    return {"status": "healthy", "mode": "simulation", "timestamp": datetime.now().isoformat()}


@app.get("/api/dashboard")
def dashboard():
    with connection() as db:
        rows = [dict(r) for r in db.execute("SELECT * FROM items ORDER BY completed, due IS NULL, due, created_at DESC")]
        events = [dict(r) for r in db.execute("SELECT * FROM events ORDER BY id DESC LIMIT 8")]
    for row in rows:
        row["completed"] = bool(row["completed"])
    return {"items": rows, "devices": list(devices.values()), "events": events, "environment": {"temperature": 24.1, "humidity": 48, "air_quality": "Good", "energy": 1.8}}


@app.post("/api/items", status_code=201)
def create_item(item: ItemIn):
    row = {"id": str(uuid.uuid4()), **item.model_dump(), "completed": False, "created_at": datetime.now().isoformat(timespec="seconds")}
    with connection() as db:
        db.execute("INSERT INTO items VALUES(:id,:title,:category,:due,:priority,:completed,:created_at)", row)
    log("item", f"Added {row['title']} to {row['category']} list")
    return row


@app.patch("/api/items/{item_id}")
def toggle_item(item_id: str):
    with connection() as db:
        row = db.execute("SELECT completed,title FROM items WHERE id=?", (item_id,)).fetchone()
        if not row:
            raise HTTPException(404, "Item not found")
        completed = 0 if row["completed"] else 1
        db.execute("UPDATE items SET completed=? WHERE id=?", (completed, item_id))
    log("item", f"{'Completed' if completed else 'Reopened'} {row['title']}")
    return {"id": item_id, "completed": bool(completed)}


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: str):
    with connection() as db:
        result = db.execute("DELETE FROM items WHERE id=?", (item_id,))
        if not result.rowcount:
            raise HTTPException(404, "Item not found")


@app.patch("/api/devices/{device_id}")
def update_device(device_id: str, update: DeviceUpdate):
    if device_id not in devices:
        raise HTTPException(404, "Device not found")
    data = update.model_dump(exclude_none=True)
    devices[device_id].update(data)
    if device_id == "door" and "on" in data:
        devices[device_id]["value"] = "Locked" if data["on"] else "Unlocked"
    log("device", f"Updated {devices[device_id]['name']}")
    return devices[device_id]


@app.post("/api/command")
def command(body: Command):
    parsed = parse_command(body.text)
    if parsed["intent"] == "add_item":
        created = create_item(ItemIn(**parsed["item"]))
        parsed["item"] = created
    log(parsed["intent"], parsed["message"])
    return parsed


@app.post("/api/demo/reset")
def reset_demo():
    with connection() as db:
        db.execute("DELETE FROM items")
        db.execute("DELETE FROM events")
    samples = [
        ItemIn(title="Physiotherapy session", category="task", due=date.today().isoformat(), priority="high"),
        ItemIn(title="Call the pharmacy", category="task", due=date.today().isoformat(), priority="medium"),
        ItemIn(title="Milk and fresh fruit", category="grocery", due=(date.today()+timedelta(days=1)).isoformat(), priority="medium"),
    ]
    for sample in samples:
        create_item(sample)
    log("system", "Demo home synchronized")
    return {"ok": True}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_text(json.dumps({"type": "sync", "at": datetime.now().isoformat()}))
    except WebSocketDisconnect:
        pass
