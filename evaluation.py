# evaluation.py

import re
from typing import List, Dict
from sentence_transformers import SentenceTransformer, util
from questions import QUESTIONS
from typing import Tuple

# Load model ONCE
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def keyword_score(user_answer: str, keywords: List[str]) -> Tuple[int, List[str]]:
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
    words = len(user_answer.split())

    if words == 0:
        return 0
    elif words < 20:
        return 3
    elif words <= 80:
        return 8
    else:
        return 6


def semantic_similarity_score(user_answer: str, ideal_answer: str) -> float:
    embeddings = semantic_model.encode(
        [user_answer, ideal_answer],
        convert_to_tensor=True
    )
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return float(similarity.item())


def evaluate_answer(qid: str, user_answer: str) -> Dict:
    if qid not in QUESTIONS:
        raise ValueError(f"Unknown question id: {qid}")

    question = QUESTIONS[qid]
    ideal_answer = question["ideal_answer"]

    # ---- individual scores ----
    kw_score, missing = keyword_score(user_answer, question["keywords"])
    len_score = length_score(user_answer)

    semantic_raw = semantic_similarity_score(user_answer, ideal_answer)
    semantic_score = round(semantic_raw * 10, 1)

    # ---- final weighted score ----
    final_score = round(
        (0.4 * kw_score) +
        (0.4 * semantic_score) +
        (0.2 * len_score),
        1
    )

    # ---- feedback ----
    feedback_parts = []

    if missing:
        feedback_parts.append(
            "You missed these important points: " + ", ".join(missing) + "."
        )

    if len_score <= 3:
        feedback_parts.append(
            "Your answer is quite short. Try adding more explanation."
        )
    elif len_score >= 8:
        feedback_parts.append(
            "Good length for an interview answer."
        )

    feedback = " ".join(feedback_parts) if feedback_parts else (
        "Great answer! You covered the key ideas clearly."
    )

    return {
        "total_score": final_score,
        "keyword_score": kw_score,
        "length_score": len_score,
        "semantic_score": semantic_score,
        "feedback": feedback,
        "missing_keywords": missing,
        "ideal_answer": ideal_answer
    }


