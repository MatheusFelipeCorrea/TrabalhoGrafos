"""Domain exceptions for graph operations."""


class InvalidVertexError(Exception):
    """Raised when a vertex index is outside the valid range."""

    def __init__(self, vertex: int, num_vertices: int) -> None:
        self.vertex = vertex
        self.num_vertices = num_vertices
        super().__init__(
            f"Invalid vertex index {vertex}; expected value in [0, {num_vertices - 1}]"
        )


class SelfLoopError(Exception):
    """Raised when an operation would create a self-loop in a simple graph."""

    def __init__(self, vertex: int) -> None:
        self.vertex = vertex
        super().__init__(f"Self-loops are not allowed: edge ({vertex}, {vertex})")


class EdgeNotFoundError(Exception):
    """Raised when an operation targets a non-existent edge."""

    def __init__(self, source: int, target: int) -> None:
        self.source = source
        self.target = target
        super().__init__(f"Edge ({source}, {target}) does not exist")
