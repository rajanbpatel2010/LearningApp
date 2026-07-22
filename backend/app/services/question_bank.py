from __future__ import annotations

import os
import re
import sqlite3
from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    id: int
    category: str
    topic: str
    difficulty: str
    question_text: str
    expected_answer: str
    keywords: List[str]
    source: str = "uploaded"


class QuestionBankService:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or os.environ.get("QUESTION_BANK_DB_PATH", "question_bank.db")
        self._connect()
        self._questions = self._load_questions()
        self._next_id = self._get_next_id()

    def _connect(self) -> None:
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                topic TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question_text TEXT NOT NULL,
                expected_answer TEXT NOT NULL,
                keywords TEXT NOT NULL,
                source TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def _load_questions(self) -> list[Question]:
        rows = self._conn.execute(
            "SELECT id, category, topic, difficulty, question_text, expected_answer, keywords, source FROM questions ORDER BY id"
        ).fetchall()
        return [
            Question(
                id=row["id"],
                category=row["category"],
                topic=row["topic"],
                difficulty=row["difficulty"],
                question_text=row["question_text"],
                expected_answer=row["expected_answer"],
                keywords=row["keywords"].split("|") if row["keywords"] else [],
                source=row["source"],
            )
            for row in rows
        ]

    def _get_next_id(self) -> int:
        row = self._conn.execute("SELECT MAX(id) AS max_id FROM questions").fetchone()
        return (row["max_id"] or 0) + 1

    def import_questions(self, questions: list[dict]) -> list[Question]:
        imported: list[Question] = []
        for item in questions:
            question = Question(
                id=self._next_id,
                category=item.get("category", "general"),
                topic=item.get("topic", "general"),
                difficulty=item.get("difficulty", "medium"),
                question_text=item.get("question_text", ""),
                expected_answer=item.get("expected_answer", ""),
                keywords=item.get("keywords", []),
                source=item.get("source", "uploaded"),
            )
            self._conn.execute(
                "INSERT INTO questions (id, category, topic, difficulty, question_text, expected_answer, keywords, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    question.id,
                    question.category,
                    question.topic,
                    question.difficulty,
                    question.question_text,
                    question.expected_answer,
                    "|".join(question.keywords),
                    question.source,
                ),
            )
            self._conn.commit()
            self._questions.append(question)
            imported.append(question)
            self._next_id += 1
        return imported

    def search(self, query: str) -> list[Question]:
        tokens = {token for token in re.findall(r"[a-z0-9]+", query.lower()) if token}
        if not tokens:
            return []

        results: list[Question] = []
        for question in self._questions:
            haystack = " ".join(
                [
                    question.question_text,
                    question.expected_answer,
                    question.topic,
                    question.category,
                    " ".join(question.keywords),
                ]
            ).lower()
            if any(token and token in haystack for token in tokens):
                results.append(question)
        return results

    def list_questions(self) -> list[Question]:
        self._questions = self._load_questions()
        return list(self._questions)

    def delete_question(self, question_id: int) -> bool:
        cursor = self._conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        self._conn.commit()
        if cursor.rowcount > 0:
            self._questions = [q for q in self._questions if q.id != question_id]
            return True
        return False

    def update_question(self, question_id: int, updates: dict) -> Question | None:
        """Update allowed fields on an existing question. Returns updated Question or None if not found."""
        question = next((q for q in self._questions if q.id == question_id), None)
        if question is None:
            return None

        # Apply updates to the in-memory object
        question.category        = updates.get("category",        question.category)
        question.topic           = updates.get("topic",           question.topic)
        question.difficulty      = updates.get("difficulty",      question.difficulty)
        question.question_text   = updates.get("question_text",   question.question_text)
        question.expected_answer = updates.get("expected_answer", question.expected_answer)
        if "keywords" in updates:
            kw = updates["keywords"]
            question.keywords = kw if isinstance(kw, list) else [k.strip() for k in str(kw).split("|") if k.strip()]

        self._conn.execute(
            """UPDATE questions
               SET category=?, topic=?, difficulty=?, question_text=?, expected_answer=?, keywords=?
               WHERE id=?""",
            (
                question.category,
                question.topic,
                question.difficulty,
                question.question_text,
                question.expected_answer,
                "|".join(question.keywords),
                question_id,
            ),
        )
        self._conn.commit()
        return question

