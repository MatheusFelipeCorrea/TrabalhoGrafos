from __future__ import annotations

from src.mining.interaction_model import Interaction

INTERACTION_WEIGHT_BY_TYPE: dict[str, int] = {
    "comment_issue": 2,
    "comment_pr": 2,
    "open_issue_commented": 3,
    "review_pr": 4,
    "merge_pr": 5,
    "close_issue": 3,
}


def official_weight(interaction_type: str) -> float:
    """Return the official weight for an interaction type."""

    normalized = str(interaction_type).strip()
    if normalized not in Interaction.ALLOWED_TYPES:
        raise ValueError(f"Invalid interaction type: {normalized}")
    return float(INTERACTION_WEIGHT_BY_TYPE[normalized])
