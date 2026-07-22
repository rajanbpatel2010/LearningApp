from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List


@dataclass
class SessionRecord:
    id: int
    request: str
    intent: str
    summary: str
    created_at: str


class SessionHistoryService:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or os.environ.get("SESSION_HISTORY_DB_PATH", "session_history.db")
        self._connect()

    def _connect(self) -> None:
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS session_history (
                id INTEGER PRIMARY KEY,
                request TEXT NOT NULL,
                intent TEXT NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def record(self, request: str, intent: str, summary: str) -> SessionRecord:
        created_at = datetime.now(timezone.utc).isoformat()
        cursor = self._conn.execute(
            "INSERT INTO session_history (request, intent, summary, created_at) VALUES (?, ?, ?, ?)",
            (request, intent, summary, created_at),
        )
        self._conn.commit()
        return SessionRecord(
            id=cursor.lastrowid,
            request=request,
            intent=intent,
            summary=summary,
            created_at=created_at,
        )

    def list_recent(self, limit: int = 10) -> list[SessionRecord]:
        rows = self._conn.execute(
            "SELECT id, request, intent, summary, created_at FROM session_history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [
            SessionRecord(
                id=row["id"],
                request=row["request"],
                intent=row["intent"],
                summary=row["summary"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
