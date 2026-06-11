# Documentação Técnica — GitHub Graph Analyzer

Documento **único** do projeto para estudo do caso e leitura em grupo. Descreve **o que cada frente faz**, **como faz** e **como se conecta** às demais — alinhado ao código em `github-graph-analyzer/` e `frontend-grafogen/`.

**Repositório analisado:** `github/spec-kit`

| Frente | Responsável | Pasta |
|--------|-------------|-------|
| F1 — Mining | Arthur Henrique | `src/mining/` |
| F2 — Graph Structures | Matheus Felipe | `src/graph/` |
| F3 — Builders | Alice Shikida | `src/builder/` |
| F4 — Analysis | Diogo Meireles | `src/analysis/` |
| F5 — Integração (CLI) | Diogo Meireles | `src/app/main.py`, `src/app/api_demo.py` |
| F5.5 — Frontend (GrafoGen) | Matheus Felipe | `frontend-grafogen/` |

## Índice

1. [Panorama do pipeline](#1-panorama-do-pipeline)
2. [PARTE 1 — F1 Mining](#parte-1--f1-mining)
3. [PARTE 2 — F2 Graph Structures](#parte-2--f2-graph-structures)
4. [PARTE 3 — F3 Builders](#parte-3--f3-builders)
5. [PARTE 4 — F4 Analysis](#parte-4--f4-analysis)
6. [PARTE 5 — F5 Integração e GrafoGen](#parte-5--f5-integração-e-grafogen)
7. [Anexo — Comandos e checklists](#anexo--comandos-e-checklists)

---

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

**Responsável: Arthur Henrique**

A frente de mineração é o ponto de entrada do pipeline. Ela acessa a API do GitHub via PyGithub e transforma a atividade do repositório em arquivos CSV estruturados que alimentam as demais frentes.

O minerador coleta dados de `github/spec-kit` via **PyGithub** e gera três arquivos:

- `users.csv` — usuários vistos na mineração
- `interactions.csv` — arestas usuario→usuario para os builders
- `events.csv` — log bruto de eventos (nem tudo vira aresta)

### 2.1 Configuração e Dependências

Dependências principais (`requirements.txt`): `PyGithub`, `python-dotenv`, `pandas`, `tqdm`, `pytest`, `pytest-cov`.

O token de acesso é lido do arquivo `.env` (baseado em `.env.example`):

```
GITHUB_TOKEN=seu_token_aqui
```

Sem token, a mineração pode funcionar em repositórios pequenos, mas tende a atingir o rate limit da API do GitHub rapidamente. O arquivo `.env` nunca deve ser versionado.

### 2.2 Execução

```bash
python -m src.app.main --mine
python -m src.app.main --mine --repo github/spec-kit
```

Se `--repo` for omitido, o padrão já é `github/spec-kit`.

### 2.3 Fluxo de `run_mining()` (`main.py`)

1. Criar `GitHubClient`
2. Criar `IssueMiner` e `PRMiner`
3. `issue_miner.mine(repo)` → lista de `Interaction`
4. `pr_miner.mine(repo)` → lista de `Interaction`
5. Juntar interações e eventos brutos
6. `users_from_interactions()` → lista de usuários
7. `DataExporter` grava os três CSVs
8. Imprime estatísticas (`scanned_items`, `mined_issues`, `skipped_pull_requests`)

### 2.4 Arquivos e Classes

### 2.5 `interaction_model.py`

#### `Interaction` — vira aresta de grafo

Campos: `src_login`, `dst_login`, `type`, `weight`, `timestamp`, `source_id`

**Tipos permitidos:**

- `comment_issue` — comentário em issue
- `comment_pr` — comentário em PR
- `open_issue_commented` — autor da issue ao receber comentário
- `review_pr` — revisão de PR
- `merge_pr` — merge de PR por terceiro
- `close_issue` — fechamento de issue por terceiro

#### `MiningEvent` — log bruto (não vira aresta diretamente) - Registros

Campos: `event_type`, `actor_login`, `target_login`, `source_kind`, `source_id`, `timestamp`, `state`

**Tipos:** `issue_comment`, `issue_closed`, `pr_opened`, `pr_comment`, `pr_review`, `pr_approval`, `pr_merged`

| | `Interaction` | `MiningEvent` |
|---|---------------|---------------|
| Destino | obrigatório | pode ser vazio |
| Auto-interação | proibida | permitida no log |
| Peso | sim | não |
| Arquivo | `interactions.csv` | `events.csv` |

A Interaction já é o dado processado: extraiu origem, destino, calculou o peso, validou que não é auto-interação, e tá pronto pra virar aresta no grafo.

`MiningEvent`s vão para `events.csv` (auditoria); `Interaction`s vão para `interactions.csv` (grafo).

### 2.6 `issue_miner.py` — `IssueMiner`

#### Por que filtrar PRs na API de issues?

`repo.get_issues(state="all")` retorna **issues + PRs** (PRs têm campo `pull_request`). O `IssueMiner` ignora itens com `pull_request` preenchido.


Para cada issue real, o método `_extract_issue_interactions(issue)` executa:

| Situação | Evento gerado | Arestas geradas |
|----------|---------------|-----------------|
| Alguém comenta na issue | `issue_comment` | `commenter → author` (`comment_issue`, peso 2) e `author → commenter` (`open_issue_commented`, peso 3) |
| A issue é fechada por outra pessoa | `issue_closed` | `quem_fechou → author` (`close_issue`, peso 3) |

O método `_should_skip_self_interaction(src, dst)` descarta qualquer interação onde origem e destino são o mesmo login ou onde algum dos dois está vazio.

#### `pr_miner.py` — `PRMiner` 

Usa `repo.get_pulls(state='all')` e extrai interações de cada PR via `_extract_pr_interactions(pr)`. As fontes de dados são: `pr.get_issue_comments()` para comentários gerais, `pr.get_review_comments()` para comentários em linhas de código, e `pr.get_reviews()` para aprovações e pedidos de mudança.

| Situação | Evento (`events.csv`) | Aresta (`interactions.csv`) |
|----------|----------------------|----------------------------|
| Abertura do PR | `pr_opened` | Nenhuma (sem outro usuário envolvido) |
| Comentário geral ou em linha | `pr_comment` | `commenter → author` (`comment_pr`, peso 2) |
| Review `APPROVED` | `pr_approval` | `reviewer → author` (`review_pr`, peso 4) |
| Review `CHANGES_REQUESTED` ou `COMMENTED` | `pr_review` | `reviewer → author` (`review_pr`, peso 4) |
| Merge por outra pessoa | `pr_merged` | `merged_by → author` (`merge_pr`, peso 5) |
| Merge pelo próprio autor | `pr_merged` | Evento sim, aresta não (evita laço no grafo) |


### 2.7 Schemas dos CSVs (contrato com F3)

#### `users.csv`

```csv
login,user_id,name
```

#### `interactions.csv`

```csv
src_login,dst_login,type,weight,timestamp,source_id
```

#### `events.csv`

```csv
event_type,actor_login,target_login,source_kind,source_id,timestamp,state
```

### 2.8 Fluxo Completo de `run_mining()`

1. Criação do `GitHubClient` com o token do ambiente
2. Criação das instâncias de `IssueMiner` e `PRMiner`
3. `issue_miner.mine(repo)` percorre todas as issues e retorna lista de `Interaction`
4. `pr_miner.mine(repo)` percorre todos os PRs e retorna lista de `Interaction`
5. As listas de interações e eventos são combinadas
6. `users_from_interactions()` extrai os logins únicos
7. `DataExporter` grava os três CSVs em `data/raw/`
8. Estatísticas são impressas no terminal

### 2.9 Testes F1

Meta de cobertura: **>= 98%** em `src/mining/`. Cenários cobertos: mineração completa com mocks, filtro de PRs na API de issues, validações de `Interaction` e `MiningEvent`, retry exponencial, exportação CSV e repositório com formato inválido.

```bash
python -m pytest tests/test_mining.py -q
python -m pytest tests/test_mining.py --cov=src.mining --cov-report=term-missing -q
```

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
**Responsável: Matheus Felipe**

A frente que implementa do zero a lógica dos 4 grafos, através da duas matriz de adjacência e lista de adjacência, sem uso de bibliotecas externas como networkx ou igraph. Toda a F3 (builders) e F4 (análise) usam essa API.

Foi criado uma hierarquia de classes proprias
AbstractGraph  ←  classe base abstrata
    ├── AdjacencyMatrixGraph  (usa numpy)
    └── AdjacencyListGraph   (usa dict) 

## 3.1 `abstract_graph.py` — `AbstractGraph`
O AbstractGraph define o contrato — todas as funções que qualquer implementação precisa ter. As duas subclasses implementam isso de formas diferentes internamente, mas produzem o mesmo resultado.
- Classe base que centraliza o contrato da API, validações comuns, contagem de vértices e arestas, pesos e rótulos de vértices e exportação GEXF. Ambas as implementações herdam desta classe.

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
  
### 3.2 `exceptions.py`

| Exceção | Quando é lançada |
|---------|------------------|
| `InvalidVertexError` | Índice fora do intervalo [0, n-1] |
| `SelfLoopError` | Chamada de `add_edge(u, u)` |
| `EdgeNotFoundError` | `remove_edge` ou consulta de peso em aresta inexistente |

### 3.3 AdjacencyMatrixGraph
AdjacencyMatrixGraph usa duas matrizes n×n: uma booleana pra saber se a aresta existe e uma float pro peso. Acesso O(1) mas ocupa sempre n² de espaço.- guarda true ou false

AdjacencyMatrixGraph — matriz n×n onde: (i,j sao indices dos usuarios)

	•	_adjacency[i][j] = True/False → aresta existe?
	•	_weights[i][j] = float → qual o peso?

| Operação | Complexidade |
|----------|-------------|
| `has_edge`, `add_edge`, `remove_edge` | O(1) |
| `get_vertex_in_degree`, `get_vertex_out_degree` | O(n) — percorre linha ou coluna |
| Iterar todas as arestas | O(n²) |

### 3.4 AdjacencyListGraph
AdjacencyListGraph usa um dict de dicts onde _adjacency[u][v] = peso, guardando só as arestas que realmente existem. - Armazwna pares de chave.
- É naturalmente boa pra vizinhança porque a estrutura já é organizada por vértice. A lista de adjacência é naturalmente boa pra vizinhança porque a estrutura já é organizada por vértice.
Quando você quer saber os vizinhos de u, é só olhar _adjacency[u] — ele já é um dict com todos os vizinhos diretos.

AdjacencyListGraph — dicionário onde:

	•	_adjacency[u] = {v: peso, v2: peso2, ...}

Mantém `_adjacency[u]` como um dicionário que mapeia `v → peso` para cada vizinho `v` do vértice `u`.

| Operação | Complexidade |
|----------|-------------|
| `has_edge`, `add_edge`, `remove_edge` | O(1) amortizado |
| `get_vertex_out_degree(u)` | O(1) — apenas `len(dict)` |
| `get_vertex_in_degree(u)` | O(n) no pior caso — precisa checar todos os dicts |
| Iterar todas as arestas | O(n + m) — proporcional a vértices + arestas |

É a implementação padrão usada pelos builders (F3) porque os grafos de colaboração no GitHub são esparsos. As duas implementações produzem resultados idênticos em todos os testes de equivalência.

### 3.5 Resumo - Decisões de Implementação

| Tema | Decisão tomada |
|------|----------------|
| Matriz de adjacência | Implementada com numpy (`AdjacencyMatrixGraph`) |
| Lista de adjacência | Implementada com dict por vértice (`AdjacencyListGraph`) |
| Peso padrão | `0.0` para vértice e aresta nova |
| `add_edge` | Idempotente — repetir a mesma aresta não duplica nem altera o peso |
| `is_connected()` | Verifica conectividade fraca (ignorando direção das arestas) |
| `is_complete_graph()` | Verifica se todo par ordenado (u,v) com u != v possui aresta |
| GEXF | Versão 1.3, com atributo `weight` nas arestas |
| Bibliotecas de grafos | Proibidas pelo enunciado |

### Semântica das relações (arco `u → v`)

- `is_successor(u, v)` — existe `u → v`
- `is_predecessor(u, v)` — existe `u → v` (u é predecessor de v)
- `is_divergent` — mesma origem `u1 == u2` e ambas arestas existem
- `is_convergent` — mesmo destino `v1 == v2` e ambas existem
- `is_incident(u, v, x)` — `x` é `u` ou `x` é `v`

**Idempotência de `add_edge`:**
- Primeira chamada: cria a aresta com peso `0.0` e incrementa o contador interno
- Chamadas repetidas: não alteram o peso nem incrementam o contador
- Para definir o peso: usar `set_edge_weight(u, v, peso)` após o `add_edge`

### 3.6 `gephi_exporter.py`

Gera **GEXF 1.3** manualmente:

```python
graph.export_to_gephi("output/graphs/exemplo.gexf")
# ou: export_to_gephi(graph, path)
```

- grafo `directed`, `static`
- nós: `id` (índice) + `label` (login)
- arestas: atributo `weight`

Abre no **Gephi** ou no **GrafoGen** (Parte 5).

### 3.7 Contrato esperado pela F3

1. `AdjacencyListGraph(n)` ou `AdjacencyMatrixGraph(n)` com `n = |usuários|`
2. `set_vertex_label(i, login)` para cada usuário
3. Por interação: `add_edge(src, dst)` + `set_edge_weight(src, dst, peso)`
4. No G4: se aresta existe, **somar** pesos

### 3.8 `api_demo.py`

Aplicação separada que executa todas as operações da API em um grafo de 3 vértices (nas duas implementações) e exporta `output/demo/graph_demo.gexf`. É a demonstração exigida pela Etapa 2 do enunciado.

```bash
python -m src.app.api_demo
```

### 3.9 Testes F2

```bash
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py -v
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py --cov=src.graph -q
```

46 testes · meta **≥ 98%** em `src/graph/`.

Cenários: fluxo feliz; idempotência; exceções; equivalência matriz/lista; GEXF válido; vazio/unitário/completo/desconectado.

### 3.10 Resumo rápido F2

Responde: *"Como representamos e manipulamos o grafo no código?"*

1. `AbstractGraph` — contrato único
2. Duas implementações intercambiáveis
3. `exceptions.py` — proteção de estado
4. `gephi_exporter.py` — visualização

---

# PARTE 3 — F3 Builders

**Pasta:** `src/builder/` · **Entrada:** CSVs da F1 · **Saída:** GEXF em `output/graphs/`

**Responsável: Alice Shikida**

A frente de builders é a ponte entre os CSVs gerados pela mineração (F1) e os grafos em memória/GEXF. Ela lê os arquivos CSV, registra os usuários como vértices, filtra as interações por tipo e popula os grafos G1 a G4 usando a API da F2.

### 4.1 Execução

```bash
python -m src.app.main --build
python -m src.app.main --build --output-dir data/raw --graph-output-dir output/graphs
```

O `--build` não precisa de token nem acessa a API do GitHub. Funciona apenas com os CSVs já existentes em `data/raw/`.

### 4.2 Arquivos

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

### 4.3 Saída por grafo

| Grafo | Builder | Filtro (`type`) | Arquivo GEXF |
|-------|---------|-----------------|--------------|
| G1 | `Graph1CommentsBuilder` | `comment_issue`, `comment_pr` | `graph1_comments.gexf` |
| G2 | `Graph2ClosuresBuilder` | `close_issue` | `graph2_closures.gexf` |
| G3 | `Graph3ReviewsBuilder` | `review_pr`, `merge_pr` | `graph3_reviews.gexf` |
| G4 | `Graph4IntegratedBuilder` | todos `ALLOWED_TYPES` | `graph4_integrated.gexf` |

### 4.4 `user_registry.py` — `UserRegistry`

| Método | Comportamento |
|--------|---------------|
| `add_user(login)` | Registra; retorna índice existente se já cadastrado |
| `get_index(login)` | Índice ou `UnknownLoginError` |
| `get_login(index)` | Login ou `UnknownIndexError` |

O `UserRegistry` é preenchido a partir de `users.csv` primeiro e depois com logins adicionais que apareçam somente em `interactions.csv`.

### 4.5 `base_builder.py` — `BaseBuilder`

Implementa o fluxo template de construção do grafo. As subclasses (G1 a G4) sobrescrevem apenas `_filter_interactions()` e `_apply_interaction()`.

**Fluxo de `build(interactions_csv, users_csv)`:**

1. Carrega e valida `users.csv` — lança `InvalidCsvError` se o arquivo estiver ausente ou mal formatado
2. Carrega `interactions.csv` linha por linha — cada linha é validada como objeto `Interaction`
3. Chama `_filter_interactions()` — cada subclasse implementa o filtro por tipo
4. Registra todos os logins no `UserRegistry`
5. Instancia `AdjacencyListGraph(n)` com `n` = número de usuários únicos
6. Chama `set_vertex_label(i, login)` para cada usuário registrado
7. Para cada interação filtrada, chama `_apply_interaction()` — adiciona aresta e peso

O método `build_and_export(...)` executa o build e ainda serializa o resultado como GEXF no caminho configurado, retornando o grafo e o registry.

**Comportamento com arestas repetidas:**

| Builders | `accumulate_edge_weights` | Comportamento |
|----------|--------------------------|---------------|
| G1, G2, G3 | `False` | Primeira linha cria a aresta com seu peso. Linhas subsequentes para o mesmo par são ignoradas. |
| G4 | `True` | Cada linha soma o peso oficial do tipo ao peso já existente na aresta. |

Exemplo com 3 comentários de `alice → bob`: no G1 a aresta tem peso 2 (apenas a primeira interação). No G4 a aresta tem peso 6 (2 + 2 + 2, somando todas).

### 4.6 `interaction_weights.py`

Centraliza a tabela de pesos oficiais do enunciado. A função `official_weight(tipo)` é usada pelo G4 para garantir que o peso somado seja sempre o peso canônico do tipo, independente do valor que vier no campo `weight` do CSV.

### 4.7 `exceptions.py` (builder)

| Exceção | Quando é lançada |
|---------|------------------|
| `BuilderError` | Classe base para erros da frente de builders |
| `UnknownLoginError` | Tentativa de acessar índice de login não registrado no `UserRegistry` |
| `UnknownIndexError` | Tentativa de acessar login de índice inexistente no `UserRegistry` |
| `InvalidCsvError` | Arquivo ausente, coluna faltando ou linha com dados inválidos |

### 4.8 Saída dos Builders

| Grafo | Arquivo GEXF gerado |
|-------|---------------------|
| G1 | `output/graphs/graph1_comments.gexf` |
| G2 | `output/graphs/graph2_closures.gexf` |
| G3 | `output/graphs/graph3_reviews.gexf` |
| G4 | `output/graphs/graph4_integrated.gexf` |

### 4.9 Testes F3

Meta de cobertura: **>= 98%** em `src/builder/`. Cenários: filtro por tipo de interação, acumulação de pesos no G4, exportação GEXF, parametrização com lista e matriz, e testes opcionais com os CSVs reais de `data/raw/`.

```bash
python -m pytest tests/test_builder.py -v
python -m pytest tests/test_builder.py --cov=src.builder --cov-report=term-missing
```

### 4.10 Resumo rápido F3

Responde: *"Como CSV vira grafo G1–G4?"*

1. `UserRegistry` mapeia login ↔ índice
2. Cada builder filtra tipos de interação
3. `BaseBuilder` popula `AbstractGraph` e exporta GEXF
4. G4 soma pesos oficiais por par `(src, dst)`

---

# PARTE 4 — F4 Analysis

**Pasta:** `src/analysis/` · **Entrada:** CSVs da F1 (reconstrói grafos via F3) · **Saída:** `output/reports/`

**Não lê `.gexf` diretamente.** `run_analysis()` instancia cada builder, monta o grafo em memória e calcula métricas.

**Responsável: Diogo Meireles**

A frente de análise calcula métricas de centralidade, estrutura e comunidade sobre os grafos G1 a G4. Ela não lê os arquivos `.gexf` — reconstrói os grafos em memória chamando os próprios builders (F3) sobre os CSVs.

### 5.1 Execução

```bash
python -m src.app.main --analyze
python -m src.app.main --analyze --output-dir data/raw --report-output-dir output/reports
```

### 5.2 Arquivos

```text
src/analysis/
├── centrality.py    # grau, betweenness, closeness, PageRank
├── structure.py     # densidade, clustering, assortatividade
└── community.py     # Louvain, modularidade, bridging ties
```

### 5.3 `centrality.py`

| Função | Algoritmo | Normalização |
|--------|-----------|-------------|
| `degree_centrality(graph) - mede quantas conexoes diretas cada colaborador tem` | Grau de entrada e saída de cada vértice | Dividido por (n - 1) |
| `betweenness_centrality(graph) - quais colaboradores atuam como ponte` | Algoritmo de Brandes — BFS se pesos zero, Dijkstra se ponderado | Dividido por (n-1)(n-2) para grafos dirigidos |
| `closeness_centrality(graph) - mostra quem esta mais proximo de todos os outros, quem tem acesso mais rapido` | Distâncias mínimas a partir de cada vértice | Inverso da soma das distâncias alcançáveis |
| `pagerank(graph, damping=0.85) - mostra a influencia de um colaborador` | Iteração de potência com fator de amortecimento 0.85 | Nós pendentes distribuem rank; soma total aproxima 1 |

### 5.4 `structure.py`

| Função | Fórmula / comportamento |
|--------|------------------------|
| `density(graph) - indica o quãoo colaborativa é a rede` | `\|E\| / (\|V\| × (\|V\| - 1))` — razão entre arestas existentes e arestas possíveis |
| `clustering_coefficient(graph)` | Calcula coeficiente local por vértice (transitividade dirigida) e coeficiente global. Retorna dicionário com chaves `local` e `global`. |
| `degree_assortativity(graph)` | Correlação de Pearson entre o grau de origem e destino de cada aresta. Positivo = usuários similares conectam-se mais. |

### 5.5 `community.py`

| Função | Comportamento |
|--------|--------------|
| `detect_communities(graph)` | Algoritmo de Louvain para grafos dirigidos. Executa fase local (mover vértice para comunidade que maximize modularidade) e fase de agregação. Pesos zero são tratados como peso unitário. |
| `modularity(graph, partition)` | Calcula a modularidade de Newman para grafos dirigidos dado um particionamento. - remove as arestas que contem o maior numero de menores caminhos, ou seja, retiram os caminhos que ligam as diferentes partes do grafo, sobrando so qs comunidades. |
| `bridging_ties(graph, partition)` | Retorna lista de tuplas `(origem, destino, com_origem, com_destino)` para cada aresta que conecta comunidades diferentes. |

Pesos zero tratados como peso unitário na detecção de comunidades.

### 5.6 Fluxo de `run_analysis()`

Para cada um dos quatro grafos (G1 a G4):

1. Instancia o builder correspondente e chama `build()` para obter `(graph, registry)`
2. Calcula todas as centralidades e adiciona as linhas em `centrality_rows`
3. Calcula densidade, clustering e assortatividade e armazena em `structure_data`
4. Executa Louvain, calcula modularidade e identifica `bridging_ties`
5. Ao final, escreve os três arquivos de saída em `output/reports/`

### 5.7 Schemas de Saída

| Arquivo | Colunas / campos |
|---------|-----------------|
| `centrality.csv` | `login`, `graph`, `degree_in`, `degree_out`, `betweenness`, `closeness`, `pagerank` (uma linha por usuário por grafo, valores com 6 casas decimais) |
| `communities.csv` | `login`, `community_id`, `graph` (uma linha por usuário por grafo) |
| `structure.json` | Por grafo: `density`, `clustering_coefficient_global`, `clustering_coefficient_local` (por login), `degree_assortativity`, `modularity`, `num_communities`, `num_bridging_ties` |

### 5.8 Testes F4

Arquivo: `tests/test_analysis.py` — 88 testes

Grafos de referência: estrela, ciclo, completo, desconectado, caminho. Propriedades conhecidas; PageRank soma ≈ 1; Louvain; bridging ties. Parametrização lista + matriz.

```bash
python -m pytest tests/test_analysis.py -v
python -m pytest tests/test_analysis.py --cov=src.analysis -q
```

Meta: **≥ 98%** em `src/analysis/`

### 5.9 Resumo rápido F4

Responde: *"O que o grafo diz sobre a comunidade?"*

1. Reconstrói G1–G4 dos mesmos CSVs
2. Mede centralidade (grau, intermedição, proximidade, PageRank)
3. Mede estrutura (densidade, clustering, assortatividade)
4. Detecta comunidades (Louvain) e elos entre elas (bridging ties)
5. Exporta CSV/JSON para relatório e GrafoGen

---

# PARTE 5 — F5 Integração e GrafoGen

## 6.1 F5 — `src/app/main.py` (CLI)

**Responsável: Diogo Meireles**

O `main.py` é o ponto de entrada da linha de comando. Orquestra as frentes F1, F3 e F4 sem misturar responsabilidades entre elas. O import da F1 é feito de forma lazy (somente quando `--mine` é usado) para que `--build` e `--analyze` funcionem sem o token da API.

### 6.2 Flags Disponíveis

| Flag | Função chamada | Observação |
|------|---------------|------------|
| `--mine` | `run_mining()` | Precisa de `GITHUB_TOKEN` no ambiente |
| `--build` | `run_build()` | Só precisa dos CSVs em `data/raw/` |
| `--analyze` | `run_analysis()` | Só precisa dos CSVs em `data/raw/` |
| `--all` | `mine → build → analyze` | Executa pipeline completo |

### 6.3 Argumentos Opcionais

| Argumento | Padrão | Afeta |
|-----------|--------|-------|
| `--repo` | `github/spec-kit` | Repositório minerado pela F1 |
| `--output-dir` | `data/raw` | Onde F1 grava e F3/F4 leem os CSVs |
| `--graph-output-dir` | `output/graphs` | Onde F3 grava os GEXF |
| `--report-output-dir` | `output/reports` | Onde F4 grava os relatórios |

---

## 6.4 F5.5 — GrafoGen (`frontend-grafogen/`)

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
