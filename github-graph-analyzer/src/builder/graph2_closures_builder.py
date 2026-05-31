from __future__ import annotations

from src.builder.base_builder import BaseBuilder

CLOSURE_TYPE = "close_issue"


class Graph2ClosuresBuilder(BaseBuilder):
    """G2: directed edges for users closing another user's issues."""

    OUTPUT_GEXF = "graph2_closures.gexf"

    def _filter_interactions(self, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        return [row for row in rows if self._is_closure_type(str(row["type"]))]

    @staticmethod
    def _is_closure_type(interaction_type: str) -> bool:
        return interaction_type == CLOSURE_TYPE
