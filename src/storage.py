
import sqlite3
import os
from dataclasses import dataclass
from typing import List, Tuple, Optional
from .config import DB

@dataclass
class Measurement:
    ts: float
    humidity: Optional[float]

@dataclass
class Event:
    ts: float
    action: str
    reason: str

class Storage:
    def __init__(self, path: str = DB.PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS measurements(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL NOT NULL,
                    humidity REAL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS events(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL NOT NULL,
                    action TEXT NOT NULL,
                    reason TEXT NOT NULL
                )
                """
            )
            con.commit()

    def insert_measurements(self, rows: List[Measurement]):
        if not rows:
            return
        with sqlite3.connect(self.path) as con:
            con.executemany(
                "INSERT INTO measurements(ts, humidity) VALUES (?, ?)",
                [(m.ts, m.humidity) for m in rows]
            )
            con.commit()

    def insert_event(self, ev: Event):
        with sqlite3.connect(self.path) as con:
            con.execute(
                "INSERT INTO events(ts, action, reason) VALUES (?, ?, ?)",
                (ev.ts, ev.action, ev.reason)
            )
            con.commit()

    def history(self, limit: int = 10) -> Tuple[list, list]:
        with sqlite3.connect(self.path) as con:
            m = con.execute("SELECT ts, humidity FROM measurements ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
            e = con.execute("SELECT ts, action, reason FROM events ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return m, e
