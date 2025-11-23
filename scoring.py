# scoring.py
"""
Scoring logic for Nirmaan – Spoken Introduction Tool.

- Reads rubric from Excel
- Computes keyword coverage
- Computes semantic similarity using sentence-transformers
- Applies length penalty
- Produces per-criterion + overall score
"""

from typing import Dict, Any, List
import re

import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------
# Global model – loaded once
# ---------------------------------------------------------
try:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    model = None
    print("WARNING: could not load sentence-transformers model:", e)


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------
def preprocess_text(text: str) -> str:
    """Basic cleaning: strip, collapse whitespace."""
    text = str(text).strip()
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def load_rubric(path: str) -> pd.DataFrame:
    """
    Load the rubric from an Excel file.

    Expected columns (any of these variants will work):
      - Criterion / Criteria / Parameter  → criterion name
      - Description / Criteria Description / Detail → text description
      - Keywords / Keyword / Key words   → comma-separated keywords
      - Weight                           → numeric weight
      - MinWords / Min Words             → minimum word count (optional)
      - MaxWords / Max Words             → maximum word count (optional)
    """
    df = pd.read_excel(path)
    df.columns = [str(c).strip() for c in df.columns]

    # Drop completely empty rows (if any)
    df = df.dropna(how="all")

    return df


def compute_keyword_score(transcript: str, keyword_str: str) -> Dict[str, Any]:
    """Return coverage (0–1) and lists of found/missing keywords."""
    transcript_lower = transcript.lower()
    keywords = [
        k.strip().lower()
        for k in str(keyword_str).split(",")
        if str(k).strip()
    ]

    found = []
    missing = []

    for kw in keywords:
        if kw and kw in transcript_lower:
            found.append(kw)
        else:
            missing.append(kw)

    if len(keywords) == 0:
        coverage = 1.0
    else:
        coverage = len(found) / len(keywords)

    return {
        "score": float(coverage),
        "found": found,
        "missing": missing,
    }


def compute_length_penalty(
    word_count: int,
    min_words: float,
    max_words: float,
) -> Dict[str, Any]:
    """
    Returns penalty between 0.4 and 1.0 and a short suggestion.
    If no limits are defined, penalty = 1.
    """
    suggestion = ""
    penalty = 1.0

    if not (np.isfinite(min_words) or np.isfinite(max_words)):
        return {"penalty": penalty, "suggestion": suggestion}

    if np.isfinite(min_words) and word_count < min_words:
        diff = min_words - word_count
        penalty = max(0.4, 1 - diff / max(min_words, 1))
        suggestion = (
            f"Too short by about {int(diff)} words. Try adding a bit more detail."
        )

    elif np.isfinite(max_words) and word_count > max_words:
        diff = word_count - max_words
        penalty = max(0.4, 1 - diff / max(max_words, 1))
        suggestion = (
            f"Too long by about {int(diff)} words. Try being a bit more concise."
        )

    return {"penalty": float(penalty), "suggestion": suggestion}


def compute_semantic_score(transcript: str, rubric_description: str) -> float:
    """
    Semantic similarity (0–1) between transcript and criterion description.
    If model is missing, default to 0.5 (neutral).
    """
    if model is None:
        return 0.5

    sentences = [str(transcript), str(rubric_description)]
    embeddings = model.encode(sentences)
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    # cosine similarity -1..1 → 0..1
    sim = (sim + 1) / 2
    return float(sim)


# ---------------------------------------------------------
# Main scoring pipeline
# ---------------------------------------------------------
def _get_criterion_name(row: pd.Series) -> str:
    """Try to pick a nice human-readable name from the row."""
    # Try a few common column names
    for col in ["Criterion", "Criteria", "Parameter", "Aspect"]:
        if col in row and pd.notna(row[col]):
            return str(row[col]).strip()

    # Fall back to the first non-null value in the row
    for val in row:
        if pd.notna(val):
            return str(val).strip()

    return "Unnamed Criterion"


def _get_first_existing(row: pd.Series, candidates) -> Any:
    for col in candidates:
        if col in row:
            return row[col]
    return np.nan


def score_transcript(transcript: str, rubric_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Core function: given transcript text + rubric DataFrame,
    returns overall score and per-criterion breakdown.
    """
    transcript = preprocess_text(transcript)
    words = transcript.split()
    word_count = len(words)

    per_criterion_results: List[Dict[str, Any]] = []
    weighted_sum = 0.0
    total_weight = 0.0

    for _, row in rubric_df.iterrows():
        criterion_name = _get_criterion_name(row)

        description = _get_first_existing(
            row,
            ["Description", "Criteria Description", "Detail", "Details"],
        )

        keywords = _get_first_existing(
            row,
            ["Keywords", "Keyword", "Key words", "KeyWords"],
        )

        weight_raw = _get_first_existing(row, ["Weight", "Weights", "MaxScore"])
        try:
            weight = float(weight_raw) if pd.notna(weight_raw) else 1.0
        except Exception:
            weight = 1.0

        min_words = _get_first_existing(row, ["MinWords", "Min Words"])
        max_words = _get_first_existing(row, ["MaxWords", "Max Words"])

        # Ensure numeric
        min_words = float(min_words) if pd.notna(min_words) else np.nan
        max_words = float(max_words) if pd.notna(max_words) else np.nan

        # Rule-based keyword coverage
        kw_result = compute_keyword_score(transcript, keywords)

        # Semantic similarity
        semantic = compute_semantic_score(transcript, description)

        # Length penalty
        length_info = compute_length_penalty(word_count, min_words, max_words)

        # Combine rule-based + semantic (50%-50% here, tunable)
        base_score = 0.5 * kw_result["score"] + 0.5 * semantic

        # Apply length penalty
        final_score_0_1 = base_score * length_info["penalty"]

        # Weighting
        weighted = final_score_0_1 * weight
        weighted_sum += weighted
        total_weight += weight

        per_criterion_results.append(
            {
                "criterion": criterion_name,
                "weight": weight,
                "keyword_score": round(kw_result["score"], 3),
                "semantic_score": round(semantic, 3),
                "length_penalty": round(length_info["penalty"], 3),
                "final_score_0_1": round(final_score_0_1, 3),
                "keywords_found": kw_result["found"],
                "keywords_missing": kw_result["missing"],
                "length_feedback": length_info["suggestion"],
            }
        )

    if total_weight == 0:
        overall_0_1 = 0.0
    else:
        overall_0_1 = weighted_sum / total_weight

    overall_score_0_100 = round(overall_0_1 * 100, 2)

    return {
        "overall_score": overall_score_0_100,
        "word_count": word_count,
        "per_criterion": per_criterion_results,
    }
