from __future__ import annotations

from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.graph.adjacency_matrix_graph import AdjacencyMatrixGraph


def _print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def _demo_graph_operations(name: str, graph: AdjacencyMatrixGraph | AdjacencyListGraph) -> None:
    _print_section(name)
    print(f"get_vertex_count() -> {graph.get_vertex_count()}")
    print(f"get_edge_count() -> {graph.get_edge_count()}")
    print(f"is_empty_graph() -> {graph.is_empty_graph()}")

    graph.set_vertex_label(0, "alice")
    graph.set_vertex_label(1, "bob")
    graph.set_vertex_label(2, "carol")
    graph.set_vertex_weight(0, 1.0)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.set_edge_weight(0, 1, 2.0)
    graph.set_edge_weight(1, 2, 4.0)
    graph.set_edge_weight(2, 0, 5.0)

    print(f"has_edge(0, 1) -> {graph.has_edge(0, 1)}")
    print(f"remove_edge preview skipped; current edge_count -> {graph.get_edge_count()}")
    print(f"is_successor(0, 1) -> {graph.is_successor(0, 1)}")
    print(f"is_predecessor(1, 0) -> {graph.is_predecessor(1, 0)}")
    print(f"is_divergent(0, 1, 0, 2) -> {graph.is_divergent(0, 1, 0, 2)}")
    print(f"is_convergent(1, 2, 2, 0) -> {graph.is_convergent(1, 2, 2, 0)}")
    print(f"is_incident(0, 1, 1) -> {graph.is_incident(0, 1, 1)}")
    print(f"get_vertex_in_degree(1) -> {graph.get_vertex_in_degree(1)}")
    print(f"get_vertex_out_degree(1) -> {graph.get_vertex_out_degree(1)}")
    print(f"get_vertex_weight(0) -> {graph.get_vertex_weight(0)}")
    print(f"get_vertex_label(0) -> {graph.get_vertex_label(0)}")
    print(f"get_edge_weight(0, 1) -> {graph.get_edge_weight(0, 1)}")
    print(f"is_connected() -> {graph.is_connected()}")
    print(f"is_complete_graph() -> {graph.is_complete_graph()}")

    graph.remove_edge(2, 0)
    print(f"after remove_edge(2, 0), edge_count -> {graph.get_edge_count()}")
    output_path = "output/demo/graph_demo.gexf"
    graph.export_to_gephi(output_path)
    print(f"export_to_gephi('{output_path}') completed")


def main() -> None:
    _demo_graph_operations("AdjacencyMatrixGraph API demo", AdjacencyMatrixGraph(3))
    _demo_graph_operations("AdjacencyListGraph API demo", AdjacencyListGraph(3))


if __name__ == "__main__":
    main()
