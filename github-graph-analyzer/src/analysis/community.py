from __future__ import annotations

from src.graph.abstract_graph import AbstractGraph


# ---------------------------------------------------------------------------
# API Pública
# ---------------------------------------------------------------------------


def modularity(graph: AbstractGraph, partition: dict[int, int]) -> float:
    """Calcula a modularidade de Newman para um grafo dirigido.

    ``Q = (1/m) Σ_{ij} [w(i,j) - k_out(i)·k_in(j)/m] · δ(c_i, c_j)``

    Args:
        graph: Um grafo simples dirigido.
        partition: Dicionário ``{vértice: id_comunidade}``.

    Returns:
        Score de modularidade (tipicamente em ``[-0.5, 1.0]``).
    """

    vertex_count = graph.get_vertex_count()
    if vertex_count == 0:
        return 0.0

    edges = graph.iter_edges()
    if not edges:
        return 0.0

    # Detectar se o grafo é efetivamente não-ponderado (todos os pesos == 0.0)
    has_positive_weight = any(w > 0 for _, _, w in edges)

    out_strength = [0.0] * vertex_count
    in_strength = [0.0] * vertex_count
    edge_list: list[tuple[int, int, float]] = []

    for source, target, weight in edges:
        w = weight if has_positive_weight else 1.0
        out_strength[source] += w
        in_strength[target] += w
        edge_list.append((source, target, w))

    total_weight = sum(w for _, _, w in edge_list)
    if total_weight == 0:
        return 0.0

    score = 0.0
    for source, target, w in edge_list:
        if partition.get(source) == partition.get(target):
            score += w - (out_strength[source] * in_strength[target]) / total_weight

    return score / total_weight


def detect_communities(graph: AbstractGraph) -> dict[int, int]:
    """Detecta comunidades usando o algoritmo de Louvain para grafos dirigidos.

    A Fase 1 move vértices individuais para maximizar o ganho de modularidade.
    A Fase 2 agrega comunidades em super-nós e repete até a convergência.

    Args:
        graph: Um grafo simples dirigido.

    Returns:
        Dicionário ``{vértice: id_comunidade}``.
    """

    vertex_count = graph.get_vertex_count()
    if vertex_count == 0:
        return {}

    # Construção da adjacência ponderada interna
    out_adj: list[dict[int, float]] = [{} for _ in range(vertex_count)]
    in_adj: list[dict[int, float]] = [{} for _ in range(vertex_count)]
    for source, target, weight in graph.iter_edges():
        w = weight if weight > 0 else 1.0
        out_adj[source][target] = w
        in_adj[target][source] = w

    total_weight = sum(sum(targets.values()) for targets in out_adj)
    if total_weight == 0:
        return {vertex: vertex for vertex in range(vertex_count)}

    # Rastreamento: cada nó no nível atual mapeia para vértices originais
    members: list[list[int]] = [[i] for i in range(vertex_count)]
    current_out_adj = out_adj
    current_in_adj = in_adj

    while True:
        partition = _local_moving(current_out_adj, current_in_adj, total_weight)

        num_communities = len(set(partition))
        if num_communities == len(current_out_adj):
            break

        current_out_adj, current_in_adj, members = _aggregate(
            current_out_adj, partition, members,
        )

    # Mapeamento de volta para vértices originais
    result: dict[int, int] = {}
    for community_id, original_vertices in enumerate(members):
        for vertex in original_vertices:
            result[vertex] = community_id
    return result


def bridging_ties(
    graph: AbstractGraph,
    partition: dict[int, int],
) -> list[tuple[int, int, int, int]]:
    """Identifica arestas cujos extremos pertencem a comunidades diferentes.

    Args:
        graph: Um grafo simples dirigido.
        partition: Dicionário ``{vértice: id_comunidade}``.

    Returns:
        Lista de ``(origem, destino, comunidade_origem, comunidade_destino)``.
    """

    bridges: list[tuple[int, int, int, int]] = []
    for source, target, _ in graph.iter_edges():
        community_source = partition.get(source, source)
        community_target = partition.get(target, target)
        if community_source != community_target:
            bridges.append((source, target, community_source, community_target))
    return bridges


# ---------------------------------------------------------------------------
# Funções auxiliares internas — Louvain
# ---------------------------------------------------------------------------


def _local_moving(
    out_adj: list[dict[int, float]],
    in_adj: list[dict[int, float]],
    total_weight: float,
) -> list[int]:
    """Fase 1: move repetidamente vértices para a comunidade que maximiza ΔQ."""

    num_nodes = len(out_adj)
    if num_nodes == 0 or total_weight == 0:
        return list(range(num_nodes))

    out_strength = [sum(targets.values()) for targets in out_adj]
    in_strength = [sum(sources.values()) for sources in in_adj]

    community = list(range(num_nodes))
    comm_out_sum: dict[int, float] = {i: out_strength[i] for i in range(num_nodes)}
    comm_in_sum: dict[int, float] = {i: in_strength[i] for i in range(num_nodes)}

    improved = True
    while improved:
        improved = False
        for vertex in range(num_nodes):
            old_comm = community[vertex]

            # Remover vértice de sua comunidade
            comm_out_sum[old_comm] -= out_strength[vertex]
            comm_in_sum[old_comm] -= in_strength[vertex]

            # Pesos para/de cada comunidade vizinha
            weights_to: dict[int, float] = {}
            weights_from: dict[int, float] = {}

            for target, weight in out_adj[vertex].items():
                if target == vertex:
                    continue
                c = community[target]
                weights_to[c] = weights_to.get(c, 0.0) + weight

            for source, weight in in_adj[vertex].items():
                if source == vertex:
                    continue
                c = community[source]
                weights_from[c] = weights_from.get(c, 0.0) + weight

            # Avaliar todas as comunidades candidatas (inclui a antiga)
            candidates = set(weights_to) | set(weights_from)
            candidates.add(old_comm)

            best_comm = old_comm
            best_gain = -float("inf")

            for candidate in candidates:
                k_to = weights_to.get(candidate, 0.0)
                k_from = weights_from.get(candidate, 0.0)
                sigma_in = comm_in_sum.get(candidate, 0.0)
                sigma_out = comm_out_sum.get(candidate, 0.0)

                gain = (k_to + k_from) / total_weight
                gain -= (out_strength[vertex] * sigma_in + in_strength[vertex] * sigma_out) / (
                    total_weight * total_weight
                )

                if gain > best_gain:
                    best_gain = gain
                    best_comm = candidate

            # Alocar vértice na melhor comunidade
            community[vertex] = best_comm
            comm_out_sum[best_comm] = comm_out_sum.get(best_comm, 0.0) + out_strength[vertex]
            comm_in_sum[best_comm] = comm_in_sum.get(best_comm, 0.0) + in_strength[vertex]

            if best_comm != old_comm:
                improved = True

    return community


def _aggregate(
    out_adj: list[dict[int, float]],
    partition: list[int],
    members: list[list[int]],
) -> tuple[list[dict[int, float]], list[dict[int, float]], list[list[int]]]:
    """Fase 2: colapsa comunidades em super-nós."""

    unique_communities = sorted(set(partition))
    remap = {c: idx for idx, c in enumerate(unique_communities)}
    num_communities = len(unique_communities)

    # Reagrupar membros originais
    new_members: list[list[int]] = [[] for _ in range(num_communities)]
    for node, comm in enumerate(partition):
        new_members[remap[comm]].extend(members[node])

    # Construir adjacência agregada (inclui self-loops para peso intra-comunidade)
    new_out_adj: list[dict[int, float]] = [{} for _ in range(num_communities)]
    for source, targets in enumerate(out_adj):
        src_comm = remap[partition[source]]
        for target, weight in targets.items():
            tgt_comm = remap[partition[target]]
            new_out_adj[src_comm][tgt_comm] = new_out_adj[src_comm].get(tgt_comm, 0.0) + weight

    new_in_adj: list[dict[int, float]] = [{} for _ in range(num_communities)]
    for source_comm, targets in enumerate(new_out_adj):
        for target_comm, weight in targets.items():
            new_in_adj[target_comm][source_comm] = weight

    return new_out_adj, new_in_adj, new_members
