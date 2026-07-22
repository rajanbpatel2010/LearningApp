from __future__ import annotations

import os
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from typing import List


@dataclass
class KnowledgeChunk:
    id: int
    title: str
    content: str
    source: str


class RAGService:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or os.environ.get("RAG_DB_PATH", "rag.db")
        self._connect()
        self._chunks = self._load_chunks()
        self._next_id = self._get_next_id()

    def _connect(self) -> None:
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_chunks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def _load_chunks(self) -> list[KnowledgeChunk]:
        rows = self._conn.execute(
            "SELECT id, title, content, source FROM knowledge_chunks ORDER BY id"
        ).fetchall()
        return [
            KnowledgeChunk(id=row["id"], title=row["title"], content=row["content"], source=row["source"])
            for row in rows
        ]

    def _get_next_id(self) -> int:
        row = self._conn.execute("SELECT MAX(id) AS max_id FROM knowledge_chunks").fetchone()
        return (row["max_id"] or 0) + 1

    def ingest(self, title: str, content: str, source: str = "uploaded") -> KnowledgeChunk:
        chunk = KnowledgeChunk(id=self._next_id, title=title, content=content, source=source)
        self._conn.execute(
            "INSERT INTO knowledge_chunks (id, title, content, source) VALUES (?, ?, ?, ?)",
            (chunk.id, chunk.title, chunk.content, chunk.source),
        )
        self._conn.commit()
        self._chunks.append(chunk)
        self._next_id += 1
        return chunk

    def _tokenize(self, text: str) -> Counter[str]:
        return Counter(token for token in re.findall(r"[a-z0-9]+", text.lower()) if token)

    def search(self, query: str) -> list[KnowledgeChunk]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scored_chunks: list[tuple[float, KnowledgeChunk]] = []
        for chunk in self._chunks:
            chunk_text = " ".join([chunk.title, chunk.content]).lower()
            chunk_tokens = self._tokenize(chunk_text)
            if not chunk_tokens:
                continue

            overlap = sum(min(query_tokens[token], chunk_tokens[token]) for token in query_tokens)
            score = overlap / max(len(query_tokens), 1)
            if overlap > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored_chunks]

    def list_chunks(self) -> list[KnowledgeChunk]:
        self._chunks = self._load_chunks()
        return list(self._chunks)

    def delete_chunk(self, chunk_id: int) -> bool:
        """Remove a chunk by ID from DB and in-memory cache. Returns True if deleted."""
        cursor = self._conn.execute(
            "DELETE FROM knowledge_chunks WHERE id = ?", (chunk_id,)
        )
        self._conn.commit()
        if cursor.rowcount == 0:
            return False
        self._chunks = [c for c in self._chunks if c.id != chunk_id]
        return True

