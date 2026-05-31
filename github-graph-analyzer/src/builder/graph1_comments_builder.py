from __future__ import annotations

from src.builder.base_builder import BaseBuilder

COMMENT_TYPES = frozenset({"comment_issue", "comment_pr"})


class Graph1CommentsBuilder(BaseBuilder):
    """G1: directed edges for comments on issues and pull requests."""

    OUTPUT_GEXF = "graph1_comments.gexf"

    def _filter_interactions(self, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        return [row for row in rows if self._is_comment_type(str(row["type"]))]

    @staticmethod
    def _is_comment_type(interaction_type: str) -> bool:
        return interaction_type in COMMENT_TYPES
