from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from src.graph.abstract_graph import AbstractGraph

GEXF_NAMESPACE = "http://www.gexf.net/1.3"
ET.register_namespace("", GEXF_NAMESPACE)
GEXF = f"{{{GEXF_NAMESPACE}}}"


def export_to_gephi(graph: AbstractGraph, path: str) -> str:
    """Write ``graph`` to a GEXF 1.3 file and return the output path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    root = _build_gexf_root(graph)
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return str(output_path)


def _build_gexf_root(graph: AbstractGraph) -> ET.Element:
    root = ET.Element(f"{GEXF}gexf", version="1.3")
    meta = ET.SubElement(root, f"{GEXF}meta")
    ET.SubElement(meta, f"{GEXF}creator").text = "github-graph-analyzer"
    graph_element = ET.SubElement(
        root,
        f"{GEXF}graph",
        {"defaultedgetype": "directed", "mode": "static"},
    )
    attributes = ET.SubElement(graph_element, f"{GEXF}attributes", {"class": "edge"})
    ET.SubElement(
        attributes,
        f"{GEXF}attribute",
        {"id": "0", "title": "weight", "type": "float"},
    )
    _append_nodes(graph_element, graph)
    _append_edges(graph_element, graph)
    return root


def _append_nodes(parent: ET.Element, graph: AbstractGraph) -> None:
    nodes_element = ET.SubElement(parent, f"{GEXF}nodes")
    for vertex in range(graph.get_vertex_count()):
        ET.SubElement(
            nodes_element,
            f"{GEXF}node",
            {"id": str(vertex), "label": graph.get_vertex_label(vertex)},
        )


def _append_edges(parent: ET.Element, graph: AbstractGraph) -> None:
    edges_element = ET.SubElement(parent, f"{GEXF}edges")
    for edge_id, (source, target, weight) in enumerate(_collect_edges(graph)):
        edge = ET.SubElement(
            edges_element,
            f"{GEXF}edge",
            {"id": str(edge_id), "source": str(source), "target": str(target)},
        )
        attvalues = ET.SubElement(edge, f"{GEXF}attvalues")
        ET.SubElement(attvalues, f"{GEXF}attvalue", {"for": "0", "value": str(weight)})


def _collect_edges(graph: AbstractGraph) -> list[tuple[int, int, float]]:
    return graph.iter_edges()
