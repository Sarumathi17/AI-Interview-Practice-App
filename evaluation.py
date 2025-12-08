# evaluation.py

import re
from typing import List, Dict
from questions import QUESTIONS


def preprocess(text: str) -> str:
    """Lowercase + remove special chars + normalize spaces."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def keyword_score(user_answer: str, keywords: List[str]) -> (int, List[str]):
    """Return how many keywords present + which are missing."""
    text = preprocess(user_answer)
    score = 0
    missing = []

    for kw in keywords:
        if kw.lower() in text:
            score += 1
        else:
            missing.append(kw)

    return score, missing


def length_score(user_answer: str) -> int:
    """Rough length quality score out of 10."""
    words = len(user_answer.split())

    if words == 0:
        return 0
    elif words < 20:
        return 3     # too short
    elif words <= 80:
        return 8     # good range
    else:
        return 6     # bit long but acceptable


def evaluate_answer(qid: str, user_answer: str) -> Dict:
    """Main function: given question id + user answer, return scores + feedback."""
    if qid not in QUESTIONS:
        raise ValueError(f"Unknown question id: {qid}")

    q = QUESTIONS[qid]
    kw_score, missing = keyword_score(user_answer, q["keywords"])
    len_score = length_score(user_answer)

    # You can tune this formula however you like
    total = kw_score * 1.0 + len_score * 0.5
    # cap between 0 and 10
    total = max(0, min(10, total))

    feedback_parts = []

    if missing:
        feedback_parts.append(
            "You missed these important points: " + ", ".join(missing) + "."
        )

    if len_score <= 3:
        feedback_parts.append(
            "Your answer is quite short. Try to add more explanation and details."
        )
    elif len_score >= 8:
        feedback_parts.append(
            "Good length for an interview answer."
        )

    if not feedback_parts:
        feedback = "Great answer! You covered the key ideas clearly."
    else:
        feedback = " ".join(feedback_parts)

    return {
        "question": q["question"],
        "total_score": round(total, 1),
        "keyword_score": kw_score,
        "length_score": len_score,
        "feedback": feedback,
        "ideal_answer": q["ideal_answer"],
        "missing_keywords": missing,
    }
