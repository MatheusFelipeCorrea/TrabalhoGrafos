# Documentação Técnica — GitHub Graph Analyzer

## 1. Visão Geral do Projeto

O GitHub Graph Analyzer é uma ferramenta acadêmica que minera dados de colaboração de um repositório GitHub e os representa como grafos direcionados ponderados. A análise cobre comentários em issues, fechamentos, revisões de pull requests e merges — transformando atividade social em estruturas de grafo analisáveis.

O repositório analisado é o `github/spec-kit`. Todo o pipeline é executado localmente, sem dependência de bibliotecas externas de grafos (networkx, igraph etc. são proibidos pelo enunciado).

### 1.1 Fluxo Geral de Dados

| Etapa | Comando CLI | Entrada | Saída |
|-------|-------------|---------|-------|
| Mineração (F1) | `--mine` | GitHub API | `users.csv`, `interactions.csv`, `events.csv` |
| Build dos grafos (F3) | `--build` | CSVs de `data/raw/` | 4 arquivos `.gexf` em `output/graphs/` |
| Análise (F4) | `--analyze` | CSVs de `data/raw/` | `centrality.csv`, `communities.csv`, `structure.json` |
| Frontend (F5.5) | `npm run dev` | GEXF + CSVs de métricas | Visualização interativa no browser |

A F2 (Graph Structures) não aparece como etapa separada na CLI — ela é a biblioteca de grafos que as frentes F3 e F4 usam internamente. O comando `--all` executa `mine → build → analyze` em sequência.

### 1.2 Os Quatro Grafos

| Grafo | O que modela | Tipos de interação usados |
|-------|-------------|--------------------------|
| G1 — Comentários | Quem comentou na issue/PR de quem | `comment_issue`, `comment_pr` |
| G2 — Fechamentos | Quem fechou a issue de quem | `close_issue` |
| G3 — Revisões | Quem revisou/aprovou/mergeu o PR de quem | `review_pr`, `merge_pr` |
| G4 — Integrado | Combinação ponderada de todos os tipos | Todos os tipos válidos (soma de pesos) |

Em todos os grafos, uma aresta A → B significa que o usuário A realizou uma ação sobre um artefato do usuário B. Os grafos são direcionados, simples (sem laços, sem multi-arestas) e os vértices são indexados de 0 a n-1.

### 1.3 Pesos Oficiais das Interações

| Tipo de interação | Significado | Peso |
|-------------------|-------------|------|
| `comment_issue` | Comentário em uma issue | 2 |
| `comment_pr` | Comentário em um PR | 2 |
| `open_issue_commented` | Autor da issue quando ela recebe comentário | 3 |
| `close_issue` | Fechamento de issue por outro usuário | 3 |
| `review_pr` | Revisão de PR (qualquer status) | 4 |
| `merge_pr` | Merge de PR feito por outro usuário | 5 |

---

# PARTE 1 — F1 Mining

**Pasta:** `src/mining/` · **Entrada:** GitHub API · **Saída:** CSVs em `data/raw/`

## 1.1 Visão geral

O minerador coleta dados de `github/spec-kit` via **PyGithub** e gera três arquivos:

- `users.csv` — usuários vistos na mineração
- `interactions.csv` — arestas usuario→usuario para os builders
- `events.csv` — log bruto de eventos (nem tudo vira aresta)

```bash
python -m src.app.main --mine --repo github/spec-kit
```

Se `--repo` for omitido, o padrão também é `github/spec-kit`.

## 1.2 Configuração

Dependências (`requirements.txt`): PyGithub, python-dotenv, pandas, tqdm, pytest, pytest-cov.

Token em `.env` (baseado em `.env.example`):

```env
GITHUB_TOKEN=seu_token_aqui
```

Sem token a mineração pode funcionar em repos pequenos, mas tende a bater rate limit. **Nunca versionar `.env` com token real.**

## 1.3 Fluxo de `run_mining()` (`main.py`)

1. Criar `GitHubClient`
2. Criar `IssueMiner` e `PRMiner`
3. `issue_miner.mine(repo)` → lista de `Interaction`
4. `pr_miner.mine(repo)` → lista de `Interaction`
5. Juntar interações e eventos brutos
6. `users_from_interactions()` → lista de usuários
7. `DataExporter` grava os três CSVs
8. Imprime estatísticas (`scanned_items`, `mined_issues`, `skipped_pull_requests`)

## 1.4 `github_client.py` — `GitHubClient`

Encapsula acesso ao GitHub com retry e rate limit.

| Método | O que faz |
|--------|-----------|
| `__init__(token=None, sleep=time.sleep)` | Usa `token` ou `GITHUB_TOKEN` do ambiente; `sleep` injetável para testes |
| `get_repo(full_name)` | Recebe `owner/repo`; lança `ValueError` se formato inválido |
| `request_with_retry(op_name, operation, max_retries=5)` | Executa `operation()` com retry exponencial + jitter |
| `_is_retryable_error(error)` | Retentável: rate limit, 403/429/5xx, timeout, connection error |
| `_rate_limit_delay(error)` | Espera até `x-ratelimit-reset` quando disponível |

## 1.5 `interaction_model.py`

### `Interaction` — vira aresta de grafo

Campos: `src_login`, `dst_login`, `type`, `weight`, `timestamp`, `source_id`

**Tipos permitidos:**

```text
comment_issue | comment_pr | open_issue_commented | review_pr | merge_pr | close_issue
```

**Validações (`__post_init__`):** logins não vazios; `type` válido; `src ≠ dst`; `weight > 0`; `timestamp` obrigatório.

`to_row()` → dicionário para CSV.

### `MiningEvent` — log bruto (não vira aresta diretamente)

Campos: `event_type`, `actor_login`, `target_login`, `source_kind`, `source_id`, `timestamp`, `state`

**Tipos:** `issue_comment`, `issue_closed`, `pr_opened`, `pr_comment`, `pr_review`, `pr_approval`, `pr_merged`

| | `Interaction` | `MiningEvent` |
|---|---------------|---------------|
| Destino | obrigatório | pode ser vazio |
| Auto-interação | proibida | permitida no log |
| Peso | sim | não |
| Arquivo | `interactions.csv` | `events.csv` |

## 1.6 `issue_miner.py` — `IssueMiner`

### Por que filtrar PRs na API de issues?

`repo.get_issues(state="all")` retorna **issues + PRs** (PRs têm campo `pull_request`). O `IssueMiner` ignora itens com `pull_request` preenchido.

**Stats:** `scanned_items`, `mined_issues`, `skipped_pull_requests`

### `_extract_issue_interactions(issue)`

Para cada **issue real**:

**Comentários** (`issue.get_comments()`):

- Evento: `issue_comment`
- Aresta: `commenter → author` (`comment_issue`, peso 2)
- Aresta reversa: `author → commenter` (`open_issue_commented`, peso 3)

Exemplo: alice abriu, bob comentou → `bob→alice` (2) e `alice→bob` (3)

**Fechamento** (`issue.get_events()`, filtro `event == "closed"`):

- Evento: `issue_closed`
- Aresta: `quem_fechou → author` (`close_issue`, peso 3)

`_should_skip_self_interaction(src, dst)` descarta origem=destino ou vazios.

## 1.7 `pr_miner.py` — `PRMiner`

Fluxo: `repo.get_pulls(state="all")` → `_extract_pr_interactions(pr)` por PR.

| Situação | Evento (`events.csv`) | Interação (`interactions.csv`) |
|----------|----------------------|-------------------------------|
| Abertura de PR | `pr_opened` | **não cria** (sem destino outro usuário) |
| Comentário geral | `pr_comment` | `commenter → author` (`comment_pr`, 2) |
| Comentário em linha (review) | `pr_comment` | idem |
| Review APPROVED | `pr_approval` | `reviewer → author` (`review_pr`, 4) |
| Review CHANGES_REQUESTED / COMMENTED | `pr_review` | idem (`review_pr`, 4) |
| Merge (por terceiro) | `pr_merged` | `merged_by → author` (`merge_pr`, 5) |
| Merge pelo próprio autor | `pr_merged` | evento sim, aresta **não** (evita laço) |

Fontes de comentário: `pr.get_issue_comments()` e `pr.get_review_comments()`. Reviews: `pr.get_reviews()`.

## 1.8 `data_exporter.py` — `DataExporter`

| Método | Saída | Observação |
|--------|-------|------------|
| `export_users_csv` | `users.csv` | dedup por `login`, ordenado |
| `export_interactions_csv` | `interactions.csv` | via `Interaction.to_row()` |
| `export_events_csv` | `events.csv` | via `MiningEvent.to_row()` |
| `users_from_interactions` | (lista) | logins de interações + eventos |

`user_id` e `name` podem ficar vazios na versão atual.

## 1.9 Schemas dos CSVs (contrato com F3)

### `users.csv`

```csv
login,user_id,name
```

### `interactions.csv`

```csv
src_login,dst_login,type,weight,timestamp,source_id
```

### `events.csv`

```csv
event_type,actor_login,target_login,source_kind,source_id,timestamp,state
```

## 1.10 Pontos de atenção (F1)

- `interactions.csv` **não** conta issues: uma issue gera várias linhas (comentários, reversas, fechamento).
- `source_id` = número da issue ou PR, não contagem sequencial por tipo.
- `events.csv` é mais completo para auditoria; `interactions.csv` alimenta os grafos.
- Contagem confiável de issues reais: log `Issue scan: X items, Y issues, Z PRs skipped`.

## 1.11 Testes F1

Arquivo: `tests/test_mining.py`

Cobre: cenário feliz com mocks; filtro de PRs na API de issues; validações de `Interaction`/`MiningEvent`; retry; exportação CSV; repo inválido.

```bash
python -m pytest tests/test_mining.py -q
python -m pytest tests/test_mining.py --cov=src.mining --cov-report=term-missing -q
```

Meta de cobertura: **≥ 98%** em `src/mining/`.

## 1.12 Resumo rápido F1

1. `GitHubClient` — API resiliente
2. `IssueMiner` + `PRMiner` — API → `Interaction` + `MiningEvent`
3. `DataExporter` — persiste CSVs
4. `interactions.csv` = grafo · `events.csv` = auditoria

---

# PARTE 2 — F2 Graph Structures

**Pasta:** `src/graph/` · **Demo:** `src/app/api_demo.py`

Base usada pela F3 (builders) e F4 (análise). Grafos do trabalho são:

- **dirigidos**, **simples** (sem laços, sem multi-arestas)
- vértices `0 .. n-1`
- reciprocidade via **arestas anti-paralelas** (`A→B` e `B→A`)

```text
src/graph/
├── exceptions.py
├── abstract_graph.py
├── adjacency_matrix_graph.py   # numpy
├── adjacency_list_graph.py     # dict por vértice
└── gephi_exporter.py           # GEXF 1.3 manual
```

## 2.1 Decisões de implementação

| Tema | Decisão |
|------|---------|
| Matriz | **numpy** (`AdjacencyMatrixGraph`) |
| Lista | **dict** por vértice (`AdjacencyListGraph`) |
| Peso default | **0.0** (vértice e aresta nova) |
| `add_edge` | **idempotente** — repetir não duplica nem altera peso |
| `is_connected()` | conectividade **fraca** |
| `is_complete_graph()` | todo par ordenado `(u,v)`, `u ≠ v` |
| GEXF | versão **1.3**, atributo `weight` nas arestas |
| Bibliotecas de grafos | **proibidas** (networkx, igraph, etc.) |

## 2.2 `exceptions.py`

| Exceção | Quando |
|---------|--------|
| `InvalidVertexError` | índice fora de `[0, n-1]` |
| `SelfLoopError` | `add_edge(u, u)` |
| `EdgeNotFoundError` | `remove_edge` / peso em aresta inexistente |

## 2.3 `abstract_graph.py` — `AbstractGraph`

Centraliza: contagem; pesos e rótulos de vértice; validações; relações; propriedades globais; `export_to_gephi`.

### API obrigatória (Etapa 2)

```text
get_vertex_count()          get_edge_count()
has_edge(u, v)              add_edge(u, v)              remove_edge(u, v)
is_successor(u, v)          is_predecessor(u, v)
is_divergent(u1,v1,u2,v2)   is_convergent(u1,v1,u2,v2)
is_incident(u, v, x)
get_vertex_in_degree(u)     get_vertex_out_degree(u)
set_vertex_weight(v, w)     get_vertex_weight(v)
set_edge_weight(u, v, w)    get_edge_weight(u, v)
is_connected()              is_empty_graph()          is_complete_graph()
export_to_gephi(path)
set_vertex_label(v, label)  get_vertex_label(v)       # extras alinhados ao PDF
```

### Semântica das relações (arco `u → v`)

- `is_successor(u, v)` — existe `u → v`
- `is_predecessor(u, v)` — existe `u → v` (u é predecessor de v)
- `is_divergent` — mesma origem `u1 == u2` e ambas arestas existem
- `is_convergent` — mesmo destino `v1 == v2` e ambas existem
- `is_incident(u, v, x)` — `x` é `u` ou `x` é `v`

### Idempotência de `add_edge`

1. Primeira chamada cria aresta com peso **0.0** e incrementa contagem
2. Repetições não alteram peso nem contagem
3. Peso definido com `set_edge_weight` **depois** de `add_edge`

## 2.4 `AdjacencyMatrixGraph`

- `_adjacency`: matriz booleana `n×n`
- `_weights`: matriz float

| Operação | Complexidade |
|----------|--------------|
| `has_edge`, `add_edge`, `remove_edge` | O(1) |
| graus | O(n) |
| iterar arestas | O(n²) |

Indicada para grafos densos.

## 2.5 `AdjacencyListGraph`

- `_adjacency[u]`: dict `v → peso`

| Operação | Complexidade |
|----------|--------------|
| `has_edge`, `add_edge`, `remove_edge` | O(1) amortizado |
| `get_vertex_out_degree` | O(1) |
| `get_vertex_in_degree` | O(n) pior caso |
| iterar arestas | O(n + m) |

**Padrão dos builders** (grafos esparsos GitHub). Matriz e lista produzem resultados equivalentes (testado).

## 2.6 `gephi_exporter.py`

Gera **GEXF 1.3** manualmente:

```python
graph.export_to_gephi("output/graphs/exemplo.gexf")
# ou: export_to_gephi(graph, path)
```

- grafo `directed`, `static`
- nós: `id` (índice) + `label` (login)
- arestas: atributo `weight`

Abre no **Gephi** ou no **GrafoGen** (Parte 5).

## 2.7 Contrato esperado pela F3

1. `AdjacencyListGraph(n)` ou `AdjacencyMatrixGraph(n)` com `n = |usuários|`
2. `set_vertex_label(i, login)` para cada usuário
3. Por interação: `add_edge(src, dst)` + `set_edge_weight(src, dst, peso)`
4. No G4: se aresta existe, **somar** pesos

## 2.8 Testes F2

```bash
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py -v
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py --cov=src.graph -q
```

46 testes · meta **≥ 98%** em `src/graph/`.

Cenários: fluxo feliz; idempotência; exceções; equivalência matriz/lista; GEXF válido; vazio/unitário/completo/desconectado.

## 2.9 Demo `api_demo.py`

Aplicação **separada** que executa **todas** as operações da API em grafo de 3 vértices (matriz e lista) e exporta `output/demo/graph_demo.gexf`.

```bash
python -m src.app.api_demo
```

## 2.10 Resumo rápido F2

Responde: *"Como representamos e manipulamos o grafo no código?"*

1. `AbstractGraph` — contrato único
2. Duas implementações intercambiáveis
3. `exceptions.py` — proteção de estado
4. `gephi_exporter.py` — visualização

---

# PARTE 3 — F3 Builders

**Pasta:** `src/builder/` · **Entrada:** CSVs da F1 · **Saída:** GEXF em `output/graphs/`

Transforma CSVs em quatro grafos G1–G4 usando a API da F2.

```bash
python -m src.app.main --build
python -m src.app.main --build --output-dir data/raw --graph-output-dir output/graphs
```

**Não chama a API do GitHub.**

## 3.1 Arquivos

```text
src/builder/
├── exceptions.py
├── interaction_weights.py      # tabela oficial de pesos
├── user_registry.py
├── base_builder.py
├── graph1_comments_builder.py  # G1
├── graph2_closures_builder.py  # G2
├── graph3_reviews_builder.py   # G3
└── graph4_integrated_builder.py # G4
```

## 3.2 Saída por grafo

| Grafo | Builder | Filtro (`type`) | Arquivo GEXF |
|-------|---------|-----------------|--------------|
| G1 | `Graph1CommentsBuilder` | `comment_issue`, `comment_pr` | `graph1_comments.gexf` |
| G2 | `Graph2ClosuresBuilder` | `close_issue` | `graph2_closures.gexf` |
| G3 | `Graph3ReviewsBuilder` | `review_pr`, `merge_pr` | `graph3_reviews.gexf` |
| G4 | `Graph4IntegratedBuilder` | todos `ALLOWED_TYPES` | `graph4_integrated.gexf` |

Semântica das arestas: `src_login → dst_login` (quem agiu → autor do artefato).

## 3.3 `user_registry.py` — `UserRegistry`

| Método | Comportamento |
|--------|---------------|
| `add_user(login)` | Registra; retorna índice existente se já cadastrado |
| `get_index(login)` | Índice ou `UnknownLoginError` |
| `get_login(index)` | Login ou `UnknownIndexError` |

Ordem de inserção define índices `0..n-1`. Preenchido de `users.csv` + logins que aparecem só em `interactions.csv`.

## 3.4 `base_builder.py` — `BaseBuilder`

Fluxo template de `build(interactions_csv, users_csv)`:

1. Carregar e validar `users.csv`
2. Carregar `interactions.csv` (cada linha validada como `Interaction`)
3. `_filter_interactions()` — nas subclasses
4. Registrar logins
5. Instanciar grafo (`AdjacencyListGraph` por padrão)
6. `set_vertex_label(i, login)`
7. `_apply_interaction()` por linha filtrada

`build_and_export(...)` → grafo + registry + caminho GEXF.

Fabricas: `list_graph_factory(n)` (padrão), `matrix_graph_factory(n)` (testes).

### Arestas repetidas (G1–G3 vs G4)

Grafo **simples**: no máximo uma aresta `src → dst`.

| Builders | `accumulate_edge_weights` | Comportamento |
|----------|---------------------------|---------------|
| G1, G2, G3 | `False` | Primeira linha cria aresta; demais **ignoradas** |
| G4 | `True` | Cada linha **soma** peso oficial do tipo |

Exemplo: 3× `alice→bob` comentário → G1: uma aresta peso **2** · G4: peso **6** (2+2+2).

Auto-interações descartadas na validação do CSV.

## 3.5 `interaction_weights.py`

```python
official_weight(tipo)  # centraliza pesos do PDF (+ close_issue=3)
```

G4 usa `official_weight`, não apenas o campo `weight` do CSV.

## 3.6 `exceptions.py` (builder)

| Exceção | Quando |
|---------|--------|
| `BuilderError` | base |
| `UnknownLoginError` | login não registrado |
| `UnknownIndexError` | índice inválido |
| `InvalidCsvError` | arquivo ausente, coluna faltando, linha inválida |

## 3.7 `run_build()` em `main.py`

Executa os quatro builders com `AdjacencyListGraph` e grava os `.gexf`. Import de mining é **lazy** — `--build` não exige token.

## 3.8 Visualização

GEXF abre no Gephi ou GrafoGen. Dataset `spec-kit` minerado: G1 tipicamente **~2100 vértices** e **~2700 arestas** (varia com a mineração).

## 3.9 Testes F3

Arquivo: `tests/test_builder.py` + `builder_test_helpers.py`

- Filtro por tipo; agregação G4; exportação GEXF
- Parametrização **lista + matriz**
- Testes opcionais com `data/raw/` real

```bash
python -m pytest tests/test_builder.py -v
python -m pytest tests/test_builder.py --cov=src.builder --cov-report=term-missing
```

Meta: **≥ 98%** em `src/builder/`.

## 3.10 Resumo rápido F3

Responde: *"Como CSV vira grafo G1–G4?"*

1. `UserRegistry` mapeia login ↔ índice
2. Cada builder filtra tipos de interação
3. `BaseBuilder` popula `AbstractGraph` e exporta GEXF
4. G4 soma pesos oficiais por par `(src, dst)`

---

# PARTE 4 — F4 Analysis

**Pasta:** `src/analysis/` · **Entrada:** CSVs da F1 (reconstrói grafos via F3) · **Saída:** `output/reports/`

**Não lê `.gexf` diretamente.** `run_analysis()` instancia cada builder, monta o grafo em memória e calcula métricas.

```bash
python -m src.app.main --analyze
python -m src.app.main --analyze --output-dir data/raw --report-output-dir output/reports
```

## 4.1 Arquivos

```text
src/analysis/
├── centrality.py    # grau, betweenness, closeness, PageRank
├── structure.py     # densidade, clustering, assortatividade
└── community.py     # Louvain, modularidade, bridging ties
```

## 4.2 Algoritmos — `centrality.py`

| Função | Algoritmo | Normalização |
|--------|-----------|--------------|
| `degree_centrality(graph)` | grau in/out | ÷ `(n - 1)` |
| `betweenness_centrality(graph)` | **Brandes** (BFS se pesos zero; Dijkstra se ponderado) | ÷ `(n-1)(n-2)` dirigido |
| `closeness_centrality(graph)` | distâncias mínimas | inverso da soma das distâncias alcançáveis |
| `pagerank(graph, damping=0.85)` | iteração de potência | nós pendentes distribuem rank; soma ≈ 1 |

## 4.3 Algoritmos — `structure.py`

| Função | Fórmula / comportamento |
|--------|-------------------------|
| `density(graph)` | `\|E\| / (\|V\| × (\|V\| - 1))` |
| `clustering_coefficient(graph)` | local por vértice + global (transitividade dirigida) → `{"local": {...}, "global": float}` |
| `degree_assortativity(graph)` | Pearson entre grau de origem e destino das arestas |

## 4.4 Algoritmos — `community.py`

| Função | Comportamento |
|--------|---------------|
| `detect_communities(graph)` | **Louvain** dirigido (fase local + agregação) |
| `modularity(graph, partition)` | Newman para grafo dirigido |
| `bridging_ties(graph, partition)` | lista `(origem, destino, com_origem, com_destino)` inter-comunidade |

Pesos zero tratados como peso unitário na detecção de comunidades.

## 4.5 Fluxo de `run_analysis()`

Para cada `(G1..G4, Builder)`:

1. `builder.build()` → `(graph, registry)`
2. Centralidades → linhas em `centrality_rows`
3. Densidade, clustering, assortatividade → `structure_data[graph]`
4. Louvain + modularidade + bridging → `structure_data` + `community_rows`
5. Escreve três arquivos em `output/reports/`

## 4.6 Schemas de saída

### `centrality.csv`

```csv
login,graph,degree_in,degree_out,betweenness,closeness,pagerank
```

Uma linha por `(login, graph)` com `graph ∈ {G1,G2,G3,G4}`. Valores com 6 casas decimais.

### `structure.json`

Por grafo: `density`, `clustering_coefficient_global`, `clustering_coefficient_local` (login→valor), `degree_assortativity`, `modularity`, `num_communities`, `num_bridging_ties`.

### `communities.csv`

```csv
login,community_id,graph
```

## 4.7 Restrições

- Sem networkx, igraph, etc.
- Funciona com `AdjacencyListGraph` e `AdjacencyMatrixGraph`

## 4.8 Testes F4

Arquivo: `tests/test_analysis.py` — 88 testes

Grafos de referência: estrela, ciclo, completo, desconectado, caminho. Propriedades conhecidas; PageRank soma ≈ 1; Louvain; bridging ties. Parametrização lista + matriz.

```bash
python -m pytest tests/test_analysis.py -v
python -m pytest tests/test_analysis.py --cov=src.analysis -q
```

Meta: **≥ 98%** em `src/analysis/`.

## 4.9 Resumo rápido F4

Responde: *"O que o grafo diz sobre a comunidade?"*

1. Reconstrói G1–G4 dos mesmos CSVs
2. Mede centralidade (grau, intermedição, proximidade, PageRank)
3. Mede estrutura (densidade, clustering, assortatividade)
4. Detecta comunidades (Louvain) e elos entre elas (bridging ties)
5. Exporta CSV/JSON para relatório e GrafoGen

---

# PARTE 5 — F5 Integração e GrafoGen

## 5.1 F5 — `src/app/main.py` (CLI)

**Responsável:** Diogo Meireles

Orquestra as frentes sem misturar responsabilidades:

| Flag | Função | Import lazy |
|------|--------|-------------|
| `--mine` | `run_mining()` — F1 | sim (exige `dotenv`/token) |
| `--build` | `run_build()` — F3, grava 4 GEXF | não |
| `--analyze` | `run_analysis()` — F4, grava relatórios | não |
| `--all` | mine → build → analyze | sim na etapa mine |

Argumentos úteis: `--repo`, `--output-dir`, `--graph-output-dir`, `--report-output-dir`.

`api_demo.py` (exigência Etapa 2): aplica **todas** as operações da API em grafo de 3 vértices (matriz + lista) e gera `output/demo/graph_demo.gexf`.

## 5.2 F5.5 — GrafoGen (`frontend-grafogen/`)

**Responsável:** Matheus Felipe

SPA que complementa o Gephi: detecta estado do pipeline, executa etapas Python, visualiza G1–G4 e exibe métricas de centralidade.

### Estrutura do projeto

```text
frontend-grafogen/
├── server/index.js              # API Express (porta 3001)
├── src/
│   ├── App.tsx                  # rotas React Router
│   ├── pages/
│   │   ├── HomePage.tsx         # pipeline + cards G1–G4
│   │   └── VisualizePage.tsx    # canvas + sidebar
│   ├── components/
│   │   ├── graph/               # GraphCanvas, GraphSidebar, ExportModal, MetricsPanel, ZoomControls
│   │   ├── home/GraphTypeCard.tsx
│   │   ├── pipeline/            # PipelineCard, LogsModal
│   │   └── layout/Navbar.tsx
│   ├── stores/                  # graphStore, pipelineStore, uiStore (Zustand)
│   ├── hooks/usePipelineStatus.ts
│   └── utils/                   # api.ts, gexfParser.ts, graphExporter.ts, graphOptions.ts
├── vite.config.ts               # proxy /api → :3001
└── package.json
```

### Stack

| Camada | Tecnologia |
|--------|------------|
| UI | React 19 + TypeScript + Vite 8 |
| Estilo | Tailwind CSS 4 |
| Grafo | vis-network (canvas) |
| Estado | Zustand 5 |
| Rotas | React Router 7 |
| API local | Express 5 (Node.js) |
| Orquestração | `spawn('python', ['-m', 'src.app.main', '--{stage}'])` |

### Como rodar

```bash
cd frontend-grafogen
npm install
npm run dev          # concurrently: API + Vite
```

| URL / porta | Serviço |
|-------------|---------|
| http://localhost:5173 | Frontend Vite |
| http://localhost:3001 | API Express (`API_PORT` opcional) |

Scripts: `dev:web` (só Vite), `dev:api` (só Express), `build` (produção).

**Pré-requisitos:** Node 18+; Python 3.10+ com `requirements.txt` do backend; dados opcionais em `github-graph-analyzer/data/raw/` e `output/`.

### Arquitetura runtime

```text
Browser (:5173)  ──/api/* (proxy Vite)──►  Express (:3001)
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    │ spawn python            │ leitura FS                  │
                    ▼                         ▼                             │
            src.app.main                 data/raw/                          │
            --mine|--build|--analyze     output/graphs/*.gexf               │
                                         output/reports/*                    │
```

`BACKEND_ROOT` em `server/index.js` resolve para `../../github-graph-analyzer` (caminho relativo ao `server/`).

### API Express (`/api`)

| Método | Rota | Comportamento |
|--------|------|---------------|
| GET | `/status` | Estado do pipeline (poll a cada 3s na Home via `usePipelineStatus`) |
| GET | `/graphs/:type` | GEXF XML; `:type` ∈ `{G1,G2,G3,G4}` |
| GET | `/reports/:name` | `centrality.csv`, `communities.csv` ou `structure.json` |
| POST | `/pipeline/:stage` | `mine`, `build` ou `analyze`; 409 se já houver processo |
| POST | `/pipeline/cancel` | `SIGTERM` no processo ativo |

**Mapeamento GEXF** (igual aos builders F3):

| Tipo | Arquivo |
|------|---------|
| G1 | `graph1_comments.gexf` |
| G2 | `graph2_closures.gexf` |
| G3 | `graph3_reviews.gexf` |
| G4 | `graph4_integrated.gexf` |

**Detecção de etapas em `/status`:**

| Campo | Critério no código |
|-------|-------------------|
| `stage1Complete` | existem `data/raw/users.csv` e `interactions.csv` |
| `stage2Complete` | os 4 GEXF existem |
| `stage3Complete` | existem `centrality.csv` **e** `communities.csv` em `output/reports/` |
| `metricsAvailable` | igual a `stage3Complete` |
| `interactionCount` | linhas de `interactions.csv` menos cabeçalho |

Logs da execução Python ficam em `logs` (últimas 200 linhas).

### Rotas e telas (React)

| Rota | Componente | Função |
|------|------------|--------|
| `/` | `HomePage` | Cards do pipeline (mine → build → analyze), logs, cards G1–G4 |
| `/visualize/:graphId` | `VisualizePage` | Visualização (`graphId` = `G1`…`G4`) |

**Home:** ao clicar em card de grafo disponível → `fetchGraphGexf` → `parseGEXF` → `navigate('/visualize/G1')` (etc.). Após `--analyze`, carrega `centrality.csv` no store. Há também **importação de GEXF** (upload com seletor de tipo) e lista de **grafos recentes** (`localStorage`).

**Visualize:** se o grafo já está em memória, reutiliza; senão busca GEXF na API (ou cache de upload). Carrega `centrality.csv` e `communities.csv` para métricas e coloração.

### Componentes principais

| Componente | Função |
|------------|--------|
| `GraphCanvas` | Vis-Network; filtro `minWeight`; destaque na busca; cores por comunidade; foco animado no vértice |
| `GraphSidebar` | Troca de grafo, busca/foco por login (Enter), slider de peso mínimo (G4), exportar/métricas |
| `MetricsPanel` | Top 10 por **pagerank**, **betweenness**, **degree_in** ou **closeness**; toggle colorir por comunidade |
| `ExportModal` | PNG (1920×1080 ou 3840×2160), **SVG** vetorial ou DOT |
| `ZoomControls` | Zoom in/out e fit |
| `PipelineCard` + `LogsModal` | Disparo e acompanhamento das etapas Python |

### `gexfParser.ts`

Converte GEXF 1.3 (saída de `gephi_exporter.py`) para o modelo interno:

- **Nó:** `id` (índice), `label` (login)
- **Aresta:** `source`, `target`, `weight` (atributo GEXF `for="0"`)
- G1–G3: peso default 1 se ausente; G4: default 0 até ler atributo

`parseCSVMetrics(csv)` → lista para `graphStore.metrics` (campos: login, graph, degree_in, degree_out, betweenness, closeness, pagerank).

### `graphOptions.ts` — regras de performance

| Vértices | Comportamento |
|----------|---------------|
| ≤ 500 | labels visíveis no canvas |
| > 500 | labels ocultos; **tooltip** (`title`) no hover |
| ≤ 1000 | física Vis-Network habilitada (`forceAtlas2Based`) |
| > 1000 | física **desligada** |

Tamanho do nó: 16 px (≤500 vértices) ou 8 px (>500). Largura da aresta proporcional a `log(weight+1)` no canvas.

### Cliente `api.ts`

- `fetchStatus()`, `fetchGraphGexf(type)`, `fetchReport(name)`
- `runPipelineStage('mine'|'build'|'analyze')`, `cancelPipeline()`

### Integração com F1–F4

| Frente | Artefato consumido |
|--------|-------------------|
| F1 | `users.csv`, `interactions.csv` (status etapa 1) |
| F3 | `output/graphs/*.gexf` (visualização) |
| F4 | `centrality.csv` (métricas) e `communities.csv` (coloração); `structure.json` exposto pela API |

### Limitações conhecidas (código atual)

| Item | Status |
|------|--------|
| `structure.json` na UI | não consumido (disponível via `GET /api/reports/structure.json`) |
| Persistência de posições do layout | não salva entre sessões (física Vis-Network recalcula) |
| Upload GEXF muito grande | cache em `localStorage` pode falhar por quota do navegador |

### Resumo rápido F5 / GrafoGen

- **F5:** `main.py` liga F1+F3+F4 na linha de comando.
- **GrafoGen:** mesma pipeline via browser; lê GEXF e `centrality.csv`; interface mínima exigida pela Etapa 2, estendida para estudo visual do caso `spec-kit`.

---

# Anexo — Comandos e checklists

## Comandos de teste por frente

```bash
pytest tests/test_mining.py -q
pytest tests/test_graph_matrix.py tests/test_graph_list.py -q
pytest tests/test_builder.py -q
pytest tests/test_analysis.py -q
pytest tests/ -q                    # todos (290+ testes; ≥98% em src/ via pytest.ini)
pytest --cov=src tests/             # cobertura backend (~99%)

cd ../frontend-grafogen
npm test                            # Vitest — parsers, export, comunidades, recentes
npm run test:coverage               # meta ≥ 90% em src/utils/
```

## Checklists de entrega

### F1 — Mining
- [x] `GitHubClient` (auth, rate limit, retry)
- [x] `IssueMiner` + `PRMiner` → `Interaction`
- [x] `users.csv`, `interactions.csv`, `events.csv`
- [x] Filtro PRs na API de issues; sem auto-interações
- [x] CLI `--mine`
- [x] Testes com mocks

### F2 — Graph
- [x] `AbstractGraph` + matriz + lista
- [x] API Etapa 2 completa + rótulos
- [x] Exceções; `add_edge` idempotente
- [x] GEXF 1.3; `api_demo.py`
- [x] Testes ≥ 98%

### F3 — Builders
- [x] `UserRegistry` + `BaseBuilder`
- [x] G1, G2, G3, G4 + exportação GEXF
- [x] CLI `--build`
- [x] Testes ≥ 98%

### F4 — Analysis
- [x] Todas as métricas do enunciado
- [x] Relatórios em `output/reports/`
- [x] CLI `--analyze`
- [x] Testes com grafos de referência

### F5 — Integração
- [x] CLI `--mine`, `--build`, `--analyze`, `--all`
- [x] `api_demo.py` demonstrando toda API do grafo
- [x] Testes em `tests/test_app.py` (pipeline CLI + demo)

### F5.5 — GrafoGen
- [x] SPA Home + Visualize
- [x] API Express + spawn Python
- [x] Vis-Network, export PNG/SVG/DOT, métricas (centrality + closeness)
- [x] Coloração por comunidade, foco em vértice, upload GEXF, histórico recente
- [x] Testes Vitest em `src/utils/` (cobertura ≥ 90%)

## Outros materiais

- [diagramas/](./diagramas/) — UML PlantUML + PNG
- [tp-es.pdf](../Orientação%20Trabalho/tp-es.pdf) — enunciado oficial
