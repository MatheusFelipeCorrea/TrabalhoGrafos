from __future__ import annotations

from src.builder.base_builder import BaseBuilder
from src.builder.interaction_weights import official_weight
from src.mining.interaction_model import Interaction


class Graph4IntegratedBuilder(BaseBuilder):
    """G4: all interaction types with official weights summed on repeated edges."""

    OUTPUT_GEXF = "graph4_integrated.gexf"
    accumulate_edge_weights = True

    def _filter_interactions(self, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        allowed = Interaction.ALLOWED_TYPES
        return [row for row in rows if str(row["type"]).strip() in allowed]

    def _interaction_weight(self, row: dict[str, object]) -> float:
        return official_weight(str(row["type"]))
