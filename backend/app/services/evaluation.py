from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    question_id: int
    question_text: str
    user_answer: str
    expected_answer: str
    score: float          # 0.0 to 100.0
    matched_keywords: list[str]
    missing_keywords: list[str]
    feedback: str


class EvaluationService:
    """
    Lightweight keyword-overlap scoring service.
    Compares a learner's answer to the expected answer and question keywords.
    Returns a score percentage, matched/missing keyword lists, and a feedback tip.
    """

    def _tokenize(self, text: str) -> set[str]:
        return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}

    def evaluate(
        self,
        question_id: int,
        question_text: str,
        user_answer: str,
        expected_answer: str,
        keywords: list[str],
    ) -> EvaluationResult:
        user_tokens = self._tokenize(user_answer)
        expected_tokens = self._tokenize(expected_answer)

        # Combine target tokens: keywords + top tokens from expected answer
        keyword_tokens = {kw.strip().lower() for kw in keywords if kw.strip()}
        all_target_tokens = keyword_tokens | expected_tokens

        # Content overlap: how many target tokens appear in the user's answer
        matched = sorted(all_target_tokens & user_tokens)
        missing_keywords = sorted(keyword_tokens - user_tokens)

        if not all_target_tokens:
            score = 100.0 if user_answer.strip() else 0.0
        else:
            score = round(len(matched) / len(all_target_tokens) * 100, 1)

        # Cap at 100 to guard against edge cases
        score = min(score, 100.0)

        # Generate contextual feedback tip
        if score >= 80:
            feedback = "Excellent answer! You covered the key concepts clearly."
        elif score >= 55:
            feedback = (
                f"Good start! To improve, try including these concepts: "
                f"{', '.join(missing_keywords[:3]) if missing_keywords else 'more detail'}."
            )
        elif score >= 30:
            feedback = (
                f"Partial answer. Review these key ideas: "
                f"{', '.join(missing_keywords[:5]) if missing_keywords else 'the core concepts'}. "
                f"Expected answer hint: {expected_answer[:120]}..."
            )
        else:
            feedback = (
                f"Keep practicing! The expected answer covers: {expected_answer[:180]}..."
                f" Focus on: {', '.join(list(keyword_tokens)[:4]) if keyword_tokens else 'the topic fundamentals'}."
            )

        return EvaluationResult(
            question_id=question_id,
            question_text=question_text,
            user_answer=user_answer,
            expected_answer=expected_answer,
            score=score,
            matched_keywords=matched,
            missing_keywords=missing_keywords,
            feedback=feedback,
        )
