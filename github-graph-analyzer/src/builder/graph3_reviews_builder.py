from __future__ import annotations

from src.builder.base_builder import BaseBuilder

REVIEW_TYPES = frozenset({"review_pr", "merge_pr"})


class Graph3ReviewsBuilder(BaseBuilder):
    """G3: directed edges for PR reviews and merges."""

    OUTPUT_GEXF = "graph3_reviews.gexf"

    def _filter_interactions(self, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        return [row for row in rows if self._is_review_type(str(row["type"]))]

    @staticmethod
    def _is_review_type(interaction_type: str) -> bool:
        return interaction_type in REVIEW_TYPES
