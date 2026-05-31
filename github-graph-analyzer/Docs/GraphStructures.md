# Documentacao da Frente 2 - Graph Structures

Este documento explica a implementacao em `src/graph/` e o demo em `src/app/api_demo.py`. A Frente 2 entrega a estrutura de grafo dirigido simples exigida pelo enunciado (Etapa 2), com duas representacoes concretas, excecoes de dominio e exportacao GEXF para o Gephi.

## Visao Geral

A camada de grafos e a base usada pelas Frentes 3 (Builders), 4 (Analysis) e pelo pipeline da aplicacao. Todos os grafos do trabalho sao:

- **dirigidos** (arestas tem origem e destino);
- **simples** (sem lacos e sem multi-arestas);
- **indexados por inteiros** `0 .. n-1`.

Quando uma interacao bidirecional precisa ser modelada, usam-se **arestas anti-paralelas** (`A -> B` e `B -> A`), conforme o PDF.

Arquivos principais:

```text
src/graph/
├── exceptions.py
├── abstract_graph.py
├── adjacency_matrix_graph.py
├── adjacency_list_graph.py
└── gephi_exporter.py
```

Testes:

```text
tests/test_graph_matrix.py
tests/test_graph_list.py
tests/graph_test_helpers.py
```

Demo da API (exigencia do enunciado):

```bash
python -m src.app.api_demo
```

## Decisoes de Implementacao

| Tema | Decisao |
|------|---------|
| Matriz de adjacencia | **numpy** (`AdjacencyMatrixGraph`) |
| Lista de adjacencia | **dict por vertice** (`AdjacencyListGraph`) |
| Peso default | **0.0** para vertice e aresta nova |
| `add_edge` idempotente | repetir nao duplica aresta nem altera peso |
| `is_connected()` | conectividade **fraca** |
| `is_complete_graph()` | todo par ordenado `(u,v)` com `u != v` |
| GEXF | versao **1.3**, atributo de aresta `weight` |

## `exceptions.py`

Excecoes de dominio usadas em toda a API:

| Classe | Quando ocorre |
|--------|----------------|
| `InvalidVertexError` | indice fora de `[0, n-1]` |
| `SelfLoopError` | tentativa de `add_edge(u, u)` |
| `EdgeNotFoundError` | `remove_edge`, `get_edge_weight` ou `set_edge_weight` em aresta inexistente |

Cada excecao inclui mensagem clara com os indices envolvidos.

## `abstract_graph.py`

Classe abstrata `AbstractGraph` centraliza:

- contagem de vertices e arestas;
- **pesos de vertice** (`set/get_vertex_weight`);
- **rotulos de vertice** (`set/get_vertex_label`), default `"0"`, `"1"`, ...;
- validacoes compartilhadas (`_validate_vertex`, `_validate_no_self_loop`);
- metodos de relacao e propriedades globais;
- delegacao de exportacao GEXF.

### API obrigatoria (Etapa 2)

Metodos implementados na base abstrata ou nas classes concretas:

```text
get_vertex_count()
get_edge_count()
has_edge(u, v)
add_edge(u, v)
remove_edge(u, v)
is_successor(u, v)
is_predecessor(u, v)
is_divergent(u1, v1, u2, v2)
is_convergent(u1, v1, u2, v2)
is_incident(u, v, x)
get_vertex_in_degree(u)
get_vertex_out_degree(u)
set_vertex_weight(v, w)
get_vertex_weight(v)
set_edge_weight(u, v, w)
get_edge_weight(u, v)
is_connected()
is_empty_graph()
is_complete_graph()
export_to_gephi(path)
```

Metodos extras alinhados ao PDF (rotulos):

```text
set_vertex_label(v, label)
get_vertex_label(v)
```

### Semantica das relacoes

Em um arco `u -> v`:

- `is_successor(u, v)` e verdadeiro quando existe `u -> v`.
- `is_predecessor(v, u)` e verdadeiro quando existe `u -> v` (ou seja, `u` e predecessor de `v`).
- `is_divergent(u1, v1, u2, v2)` e verdadeiro quando `u1 == u2` e ambas as arestas existem.
- `is_convergent(u1, v1, u2, v2)` e verdadeiro quando `v1 == v2` e ambas as arestas existem.
- `is_incident(u, v, x)` e verdadeiro quando `x` e `u` ou `x` e `v`.

### Idempotencia de `add_edge`

1. Primeira chamada `add_edge(u, v)` cria a aresta com peso **0.0** e incrementa `get_edge_count()`.
2. Chamadas repetidas nao alteram peso nem contagem.
3. Para definir peso, usar `set_edge_weight(u, v, w)` apos a aresta existir.

A Frente 3 (Builders) deve chamar `add_edge` e depois `set_edge_weight` (ou somar pesos no G4 integrado).

## `adjacency_matrix_graph.py`

Implementacao densa com **numpy**:

- `_adjacency`: matriz booleana `n x n` indica existencia de arca;
- `_weights`: matriz `float` com peso de cada arco existente.

Complexidade tipica:

- `has_edge`, `add_edge`, `remove_edge`: **O(1)**
- graus em matriz: **O(n)**
- iteracao de arestas: **O(n^2)**

Indicada quando o grafo tende a ser denso ou quando se quer operacoes matriciais simples.

## `adjacency_list_graph.py`

Implementacao esparca com **lista de dicionarios**:

- `_adjacency[u]` mapeia `v -> peso` para sucessores de `u`.

Complexidade tipica:

- `has_edge`, `add_edge`, `remove_edge`: **O(1)** amortizado
- `get_vertex_out_degree`: **O(1)**
- `get_vertex_in_degree`: **O(n)** no pior caso
- iteracao de arestas: **O(n + m)**

Indicada para grafos esparsos (caso tipico das interacoes GitHub).

As duas classes expoem a **mesma API** e produzem resultados equivalentes para a mesma sequencia de operacoes (validado nos testes).

## `gephi_exporter.py`

Gera arquivo **GEXF 1.3** manualmente (sem networkx ou libs de grafos):

```python
from src.graph.gephi_exporter import export_to_gephi

export_to_gephi(graph, "output/graphs/g4_integrated.gexf")
```

Estrutura gerada:

- grafo `directed`, modo `static`;
- nos com `id` (indice) e `label` (rotulo do vertice);
- arestas com atributo `weight` (float).

Tambem e possivel chamar `graph.export_to_gephi(path)` em qualquer instancia de `AbstractGraph`.

## Integracao com outras frentes

```text
F1 Mining   -> interactions.csv (arestas potenciais com pesos)
F3 Builder  -> cria AbstractGraph, mapeia login -> indice, set_vertex_label, add_edge, set_edge_weight
F4 Analysis -> usa apenas a API abstrata (independente de matriz ou lista)
Gephi       -> importa .gexf gerado pela F2/F3
```

Contrato esperado pelo Builder:

1. Instanciar `AdjacencyMatrixGraph(n)` ou `AdjacencyListGraph(n)` com `n = |usuarios|`.
2. Para cada usuario, `set_vertex_label(indice, login)`.
3. Para cada interacao filtrada, `add_edge(src, dst)` e `set_edge_weight(src, dst, peso)`.
4. No G4 integrado, se ja existir aresta, **somar** pesos com `get_edge_weight` + `set_edge_weight`.

## Testes

Comando:

```bash
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py -v
```

Com cobertura da frente:

```bash
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py --cov=src.graph --cov-report=term-missing -q
```

Meta atingida: **>= 95%** em `src/graph/`.

Cenarios cobertos:

- fluxo feliz (criacao, pesos, graus, relacoes, propriedades globais);
- idempotencia de `add_edge`;
- excecoes (`InvalidVertexError`, `SelfLoopError`, `EdgeNotFoundError`);
- equivalencia matrix vs list;
- exportacao GEXF valida (parser XML nos testes);
- grafos vazios, unitarios, completos e desconectados.

## Restricoes do enunciado respeitadas

- implementacao propria (sem networkx, igraph, etc.);
- heranca e abstracao (`AbstractGraph` + 2 concretas);
- grafos simples e dirigidos;
- excecoes para entradas invalidas;
- demo separada consumindo toda a API (`api_demo.py`).

## Como explicar rapidamente para a turma

A Frente 2 responde: **"Como representamos e manipulamos o grafo no codigo?"**

1. `AbstractGraph` define o contrato unico.
2. `AdjacencyMatrixGraph` e `AdjacencyListGraph` sao duas formas de armazenar o mesmo tipo de grafo.
3. `exceptions.py` protege o estado contra indices invalidos, lacos e arestas inexistentes.
4. `gephi_exporter.py` transforma o grafo em arquivo visualizavel no Gephi.

Tudo que vier depois (builders, metricas, relatorio) depende dessa API estar correta e estavel.
