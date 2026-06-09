from __future__ import annotations

import heapq
from collections import deque

from src.graph.abstract_graph import AbstractGraph


# ---------------------------------------------------------------------------
# API Pública
# ---------------------------------------------------------------------------


def degree_centrality(graph: AbstractGraph) -> dict[int, dict[str, float]]:
    """Calcula a centralidade de grau (in e out) normalizada para cada vértice.

    Cada valor é normalizado por ``(n - 1)``, onde *n* é a quantidade de vértices.

    Args:
        graph: Um grafo simples dirigido.

    Returns:
        Dicionário ``{vértice: {"in": float, "out": float}}``.
    """

    vertex_count = graph.get_vertex_count()
    normalization = max(vertex_count - 1, 1)
    result: dict[int, dict[str, float]] = {}
    for vertex in range(vertex_count):
        result[vertex] = {
            "in": graph.get_vertex_in_degree(vertex) / normalization,
            "out": graph.get_vertex_out_degree(vertex) / normalization,
        }
    return result


def betweenness_centrality(graph: AbstractGraph) -> dict[int, float]:
    """Calcula a centralidade de intermediação via algoritmo de Brandes.

    Utiliza BFS quando todos os pesos das arestas são zero, e Dijkstra caso contrário.
    Os resultados são normalizados por ``(n - 1)(n - 2)`` para grafos dirigidos.

    Args:
        graph: Um grafo simples dirigido.

    Returns:
        Dicionário ``{vértice: float}`` com valores normalizados de intermediação.
    """

    vertex_count = graph.get_vertex_count()
    centrality: dict[int, float] = {vertex: 0.0 for vertex in range(vertex_count)}
    if vertex_count < 3:
        return centrality

    weighted = _is_weighted(graph)

    for source in range(vertex_count):
        if weighted:
            stack, predecessors, sigma = _dijkstra_brandes(graph, source)
        else:
            stack, predecessors, sigma = _bfs_brandes(graph, source)

        delta = [0.0] * vertex_count
        while stack:
            current = stack.pop()
            for predecessor in predecessors[current]:
                coefficient = (sigma[predecessor] / sigma[current]) * (1.0 + delta[current])
                delta[predecessor] += coefficient
            if current != source:
                centrality[current] += delta[current]

    normalization = (vertex_count - 1) * (vertex_count - 2)
    if normalization > 0:
        for vertex in centrality:
            centrality[vertex] /= normalization

    return centrality


def closeness_centrality(graph: AbstractGraph) -> dict[int, float]:
    """Calcula a centralidade de proximidade baseada nas distâncias de caminhos mínimos.

    Para cada vértice *v*, ``C(v) = alcançáveis / soma(d(v, u))`` sobre os
    vértices alcançáveis *u*. Vértices isolados recebem ``0.0``.

    Args:
        graph: Um grafo simples dirigido.

    Returns:
        Dicionário ``{vértice: float}`` com valores de proximidade.
    """

    vertex_count = graph.get_vertex_count()
    result: dict[int, float] = {}
    weighted = _is_weighted(graph)

    for source in range(vertex_count):
        distances = _shortest_distances(graph, source, weighted)
        total_distance = 0.0
        reachable = 0
        for target in range(vertex_count):
            if target != source and distances[target] < float("inf"):
                total_distance += distances[target]
                reachable += 1

        if reachable > 0 and total_distance > 0:
            result[source] = reachable / total_distance
        else:
            result[source] = 0.0

    return result


def pagerank(
    graph: AbstractGraph,
    damping: float = 0.85,
    tolerance: float = 1e-6,
    max_iterations: int = 100,
) -> dict[int, float]:
    """Calcula o PageRank usando o método de iteração de potência.

    Nós pendentes (grau de saída zero) distribuem seu rank uniformemente.

    Args:
        graph: Um grafo simples dirigido.
        damping: Fator de amortecimento (padrão ``0.85``).
        tolerance: Limiar de convergência sobre a mudança absoluta máxima.
        max_iterations: Limite superior de iterações.

    Returns:
        Dicionário ``{vértice: float}`` com scores de PageRank cuja soma ≈ 1.0.
    """

    vertex_count = graph.get_vertex_count()
    if vertex_count == 0:
        return {}

    in_neighbors: list[list[int]] = [[] for _ in range(vertex_count)]
    out_degree: list[int] = [0] * vertex_count
    for source, target, _ in graph.iter_edges():
        in_neighbors[target].append(source)
        out_degree[source] += 1

    rank = [1.0 / vertex_count] * vertex_count

    for _ in range(max_iterations):
        dangling_sum = sum(rank[vertex] for vertex in range(vertex_count) if out_degree[vertex] == 0)
        new_rank = [0.0] * vertex_count

        for vertex in range(vertex_count):
            incoming = sum(rank[neighbor] / out_degree[neighbor] for neighbor in in_neighbors[vertex])
            new_rank[vertex] = (
                (1.0 - damping) / vertex_count
                + damping * (incoming + dangling_sum / vertex_count)
            )

        max_diff = max(abs(new_rank[vertex] - rank[vertex]) for vertex in range(vertex_count))
        rank = new_rank
        if max_diff < tolerance:
            break

    return {vertex: rank[vertex] for vertex in range(vertex_count)}


# ---------------------------------------------------------------------------
# Funções auxiliares internas
# ---------------------------------------------------------------------------


def _is_weighted(graph: AbstractGraph) -> bool:
    """Retorna True quando ao menos uma aresta possui peso diferente de zero."""

    for _, _, weight in graph.iter_edges():
        if weight != 0.0:
            return True
    return False


def _bfs_brandes(
    graph: AbstractGraph,
    source: int,
) -> tuple[list[int], list[list[int]], list[float]]:
    """Caminhos mínimos de fonte única via BFS para o algoritmo de Brandes."""

    vertex_count = graph.get_vertex_count()
    stack: list[int] = []
    predecessors: list[list[int]] = [[] for _ in range(vertex_count)]
    sigma = [0.0] * vertex_count
    sigma[source] = 1.0
    distance = [-1.0] * vertex_count
    distance[source] = 0.0
    queue: deque[int] = deque([source])

    while queue:
        current = queue.popleft()
        stack.append(current)
        for neighbor in range(vertex_count):
            if current != neighbor and graph.has_edge(current, neighbor):
                if distance[neighbor] < 0:
                    distance[neighbor] = distance[current] + 1.0
                    queue.append(neighbor)
                if distance[neighbor] == distance[current] + 1.0:
                    sigma[neighbor] += sigma[current]
                    predecessors[neighbor].append(current)

    return stack, predecessors, sigma


def _dijkstra_brandes(
    graph: AbstractGraph,
    source: int,
) -> tuple[list[int], list[list[int]], list[float]]:
    """Caminhos mínimos de fonte única via Dijkstra para o algoritmo de Brandes."""

    vertex_count = graph.get_vertex_count()
    stack: list[int] = []
    predecessors: list[list[int]] = [[] for _ in range(vertex_count)]
    sigma = [0.0] * vertex_count
    sigma[source] = 1.0
    distance = [float("inf")] * vertex_count
    distance[source] = 0.0
    visited = [False] * vertex_count
    heap: list[tuple[float, int]] = [(0.0, source)]

    while heap:
        dist_current, current = heapq.heappop(heap)
        if visited[current]:
            continue
        visited[current] = True
        stack.append(current)

        for neighbor in range(vertex_count):
            if current == neighbor or not graph.has_edge(current, neighbor):
                continue
            edge_weight = graph.get_edge_weight(current, neighbor)
            cost = edge_weight if edge_weight > 0 else 1.0
            candidate = dist_current + cost
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                sigma[neighbor] = sigma[current]
                predecessors[neighbor] = [current]
                heapq.heappush(heap, (candidate, neighbor))
            elif abs(candidate - distance[neighbor]) < 1e-12:
                sigma[neighbor] += sigma[current]
                predecessors[neighbor].append(current)

    return stack, predecessors, sigma


def _shortest_distances(graph: AbstractGraph, source: int, weighted: bool) -> list[float]:
    """Retorna as distâncias mínimas de *source* até todos os outros vértices."""

    vertex_count = graph.get_vertex_count()

    if not weighted:
        distance = [float("inf")] * vertex_count
        distance[source] = 0.0
        queue: deque[int] = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in range(vertex_count):
                if current != neighbor and graph.has_edge(current, neighbor):
                    if distance[neighbor] == float("inf"):
                        distance[neighbor] = distance[current] + 1.0
                        queue.append(neighbor)
        return distance

    distance = [float("inf")] * vertex_count
    distance[source] = 0.0
    visited = [False] * vertex_count
    heap: list[tuple[float, int]] = [(0.0, source)]
    while heap:
        dist_current, current = heapq.heappop(heap)
        if visited[current]:
            continue
        visited[current] = True
        for neighbor in range(vertex_count):
            if current != neighbor and graph.has_edge(current, neighbor):
                edge_weight = graph.get_edge_weight(current, neighbor)
                cost = edge_weight if edge_weight > 0 else 1.0
                candidate = dist_current + cost
                if candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))
    return distance
