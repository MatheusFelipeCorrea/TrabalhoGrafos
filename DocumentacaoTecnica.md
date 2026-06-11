# GitHub Graph Analyzer — Documentação Técnica

> Repositório analisado: `github/spec-kit`

| Frente | Responsável | Pasta |
|--------|-------------|-------|
| F1 — Mining | Arthur Henrique | `src/mining/` |
| F2 — Graph Structures | Matheus Felipe | `src/graph/` |
| F3 — Builders | Alice Shikida | `src/builder/` |
| F4 — Analysis | Diogo Meireles | `src/analysis/` |
| F5 — Integração (CLI) | Diogo Meireles | `src/app/main.py` |
| F5.5 — Frontend GrafoGen | Matheus Felipe | `frontend-grafogen/` |

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

## 2. F1 — Mining (`src/mining/`)

**Responsável: Arthur Henrique**

A frente de mineração é o ponto de entrada do pipeline. Ela acessa a API do GitHub via PyGithub e transforma a atividade do repositório em arquivos CSV estruturados que alimentam as demais frentes.

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

### 2.3 Arquivos e Classes

#### `github_client.py` — `GitHubClient`

Encapsula todo o acesso à API do GitHub, adicionando lógica de retry e controle de rate limit para tornar a mineração resiliente a falhas temporárias.

| Método | O que faz |
|--------|-----------|
| `__init__(token, sleep)` | Usa o token passado ou busca `GITHUB_TOKEN` do ambiente. O parâmetro `sleep` é injetável, facilitando testes unitários sem esperas reais. |
| `get_repo(full_name)` | Recebe uma string no formato `owner/repo` e retorna o objeto repositório. Lança `ValueError` se o formato for inválido. |
| `request_with_retry(op_name, operation, max_retries=5)` | Executa uma operação qualquer com retry exponencial mais jitter aleatório. Aceita até 5 tentativas por padrão. |
| `_is_retryable_error(error)` | Identifica se um erro justifica nova tentativa: rate limit, HTTP 403/429/5xx, timeout e erros de conexão. |
| `_rate_limit_delay(error)` | Quando o GitHub retorna o header `x-ratelimit-reset`, calcula e aguarda exatamente o tempo necessário antes de tentar novamente. |

#### `interaction_model.py` — `Interaction` e `MiningEvent`

Define os dois modelos de dados produzidos pela mineração.

**`Interaction`** representa uma aresta do grafo. Campos: `src_login`, `dst_login`, `type`, `weight`, `timestamp`, `source_id`. As validações no `__post_init__` garantem que os logins não sejam vazios, o tipo seja um dos permitidos, `src` seja diferente de `dst`, `weight` seja positivo e `timestamp` seja obrigatório. O método `to_row()` converte o objeto em dicionário para escrita no CSV.

Tipos permitidos em `Interaction`:
- `comment_issue` — comentário em issue
- `comment_pr` — comentário em PR
- `open_issue_commented` — autor da issue ao receber comentário
- `review_pr` — revisão de PR
- `merge_pr` — merge de PR por terceiro
- `close_issue` — fechamento de issue por terceiro

**`MiningEvent`** é um log bruto de eventos. Campos: `event_type`, `actor_login`, `target_login`, `source_kind`, `source_id`, `timestamp`, `state`. Ao contrário de `Interaction`, o destino pode ser vazio e auto-interações são permitidas no log. `MiningEvent`s vão para `events.csv` (auditoria); `Interaction`s vão para `interactions.csv` (grafo).

#### `issue_miner.py` — `IssueMiner`

> **Particularidade importante:** a API `repo.get_issues(state='all')` do GitHub retorna tanto issues reais quanto pull requests (PRs possuem o campo `pull_request` preenchido). O `IssueMiner` filtra e ignora todos os itens com `pull_request` preenchido, garantindo que apenas issues reais sejam processadas. As estatísticas `scanned_items`, `mined_issues` e `skipped_pull_requests` permitem auditar esse processo.

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

#### `data_exporter.py` — `DataExporter`

| Método | Arquivo gerado | Observação |
|--------|---------------|------------|
| `export_users_csv(users)` | `data/raw/users.csv` | Deduplica por login, ordena alfabeticamente |
| `export_interactions_csv(interactions)` | `data/raw/interactions.csv` | Usa `Interaction.to_row()` em cada objeto |
| `export_events_csv(events)` | `data/raw/events.csv` | Usa `MiningEvent.to_row()` em cada objeto |
| `users_from_interactions(interactions, events)` | (lista em memória) | Extrai todos os logins únicos de interações e eventos |

### 2.4 Schemas dos CSVs (Contrato com F3)

| Arquivo | Colunas |
|---------|---------|
| `users.csv` | `login`, `user_id`, `name` |
| `interactions.csv` | `src_login`, `dst_login`, `type`, `weight`, `timestamp`, `source_id` |
| `events.csv` | `event_type`, `actor_login`, `target_login`, `source_kind`, `source_id`, `timestamp`, `state` |

`interactions.csv` não tem uma linha por issue, mas sim uma linha por interação ocorrida (cada comentário, fechamento etc. gera entradas separadas). O campo `source_id` é o número da issue ou PR, não uma contagem sequencial.

### 2.5 Fluxo Completo de `run_mining()`

1. Criação do `GitHubClient` com o token do ambiente
2. Criação das instâncias de `IssueMiner` e `PRMiner`
3. `issue_miner.mine(repo)` percorre todas as issues e retorna lista de `Interaction`
4. `pr_miner.mine(repo)` percorre todos os PRs e retorna lista de `Interaction`
5. As listas de interações e eventos são combinadas
6. `users_from_interactions()` extrai os logins únicos
7. `DataExporter` grava os três CSVs em `data/raw/`
8. Estatísticas são impressas no terminal

### 2.6 Testes F1

Meta de cobertura: **>= 98%** em `src/mining/`. Cenários cobertos: mineração completa com mocks, filtro de PRs na API de issues, validações de `Interaction` e `MiningEvent`, retry exponencial, exportação CSV e repositório com formato inválido.

```bash
python -m pytest tests/test_mining.py -q
python -m pytest tests/test_mining.py --cov=src.mining --cov-report=term-missing -q
```

---

## 3. F2 — Graph Structures (`src/graph/`)

**Responsável: Matheus Felipe**

A frente de estruturas de grafo é a biblioteca central do projeto. Implementa do zero duas representações de grafos direcionados ponderados (matriz de adjacência e lista de adjacência), sem uso de bibliotecas externas como networkx ou igraph. Toda a F3 (builders) e F4 (análise) usam essa API.

### 3.1 Decisões de Implementação

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

### 3.2 `exceptions.py`

| Exceção | Quando é lançada |
|---------|------------------|
| `InvalidVertexError` | Índice fora do intervalo [0, n-1] |
| `SelfLoopError` | Chamada de `add_edge(u, u)` |
| `EdgeNotFoundError` | `remove_edge` ou consulta de peso em aresta inexistente |

### 3.3 `abstract_graph.py` — `AbstractGraph`

Classe base que centraliza o contrato da API, validações comuns, contagem de vértices e arestas, pesos e rótulos de vértices e exportação GEXF. Ambas as implementações herdam desta classe.

| Método | O que faz |
|--------|-----------|
| `get_vertex_count()` | Retorna `n`, o número de vértices do grafo |
| `get_edge_count()` | Retorna o número de arestas existentes |
| `has_edge(u, v)` | Verifica se existe a aresta `u → v` |
| `add_edge(u, v)` | Cria a aresta `u → v` com peso `0.0`. Idempotente: chamadas repetidas não têm efeito |
| `remove_edge(u, v)` | Remove a aresta `u → v`. Lança `EdgeNotFoundError` se não existir |
| `is_successor(u, v)` | Retorna `True` se existe `u → v` (v é sucessor de u) |
| `is_predecessor(u, v)` | Retorna `True` se existe `u → v` (u é predecessor de v) |
| `is_divergent(u1,v1,u2,v2)` | `True` se `u1 == u2` e ambas as arestas existem (mesma origem) |
| `is_convergent(u1,v1,u2,v2)` | `True` se `v1 == v2` e ambas as arestas existem (mesmo destino) |
| `is_incident(u, v, x)` | `True` se `x` é `u` ou `x` é `v` (x é extremo da aresta u→v) |
| `get_vertex_in_degree(u)` | Retorna quantas arestas chegam em `u` |
| `get_vertex_out_degree(u)` | Retorna quantas arestas saem de `u` |
| `set_vertex_weight(v, w)` | Define o peso do vértice `v` |
| `get_vertex_weight(v)` | Retorna o peso do vértice `v` |
| `set_edge_weight(u, v, w)` | Define o peso da aresta `u → v` |
| `get_edge_weight(u, v)` | Retorna o peso da aresta `u → v`. Lança `EdgeNotFoundError` se não existir |
| `set_vertex_label(v, label)` | Associa um rótulo de texto (ex: login) ao vértice `v` |
| `get_vertex_label(v)` | Retorna o rótulo do vértice `v` |
| `is_connected()` | `True` se o grafo é fracamente conectado (existe caminho ignorando direção) |
| `is_empty_graph()` | `True` se não há arestas |
| `is_complete_graph()` | `True` se todo par ordenado (u,v) com u != v possui aresta |
| `export_to_gephi(path)` | Serializa o grafo como GEXF 1.3 no caminho especificado |

**Idempotência de `add_edge`:**
- Primeira chamada: cria a aresta com peso `0.0` e incrementa o contador interno
- Chamadas repetidas: não alteram o peso nem incrementam o contador
- Para definir o peso: usar `set_edge_weight(u, v, peso)` após o `add_edge`

### 3.4 `AdjacencyMatrixGraph`

Mantém duas matrizes numpy de tamanho n×n: `_adjacency` (booleana, indica existência) e `_weights` (float, armazena pesos).

| Operação | Complexidade |
|----------|-------------|
| `has_edge`, `add_edge`, `remove_edge` | O(1) |
| `get_vertex_in_degree`, `get_vertex_out_degree` | O(n) — percorre linha ou coluna |
| Iterar todas as arestas | O(n²) |

Indicada para grafos densos. No contexto do projeto, é usada principalmente nos testes de equivalência com a lista de adjacência.

### 3.5 `AdjacencyListGraph`

Mantém `_adjacency[u]` como um dicionário que mapeia `v → peso` para cada vizinho `v` do vértice `u`.

| Operação | Complexidade |
|----------|-------------|
| `has_edge`, `add_edge`, `remove_edge` | O(1) amortizado |
| `get_vertex_out_degree(u)` | O(1) — apenas `len(dict)` |
| `get_vertex_in_degree(u)` | O(n) no pior caso — precisa checar todos os dicts |
| Iterar todas as arestas | O(n + m) — proporcional a vértices + arestas |

É a implementação padrão usada pelos builders (F3) porque os grafos de colaboração no GitHub são esparsos. As duas implementações produzem resultados idênticos em todos os testes de equivalência.

### 3.6 `gephi_exporter.py`

Gera arquivos GEXF versão 1.3 manualmente (sem dependências externas). O grafo é marcado como `directed` e `static`. Cada nó recebe `id` (índice numérico) e `label` (login do usuário). Cada aresta recebe o atributo `weight`.

```python
graph.export_to_gephi("output/graphs/exemplo.gexf")
```

### 3.7 Testes F2

46 testes cobrindo: fluxo feliz, idempotência de `add_edge`, exceções para operações inválidas, equivalência entre matriz e lista, GEXF válido e grafos especiais (vazio, unitário, completo, desconectado).

```bash
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py -v
python -m pytest tests/test_graph_matrix.py tests/test_graph_list.py --cov=src.graph -q
```

### 3.8 `api_demo.py`

Aplicação separada que executa todas as operações da API em um grafo de 3 vértices (nas duas implementações) e exporta `output/demo/graph_demo.gexf`. É a demonstração exigida pela Etapa 2 do enunciado.

```bash
python -m src.app.api_demo
```

---

## 4. F3 — Builders (`src/builder/`)

**Responsável: Alice Shikida**

A frente de builders é a ponte entre os CSVs gerados pela mineração (F1) e os grafos em memória/GEXF. Ela lê os arquivos CSV, registra os usuários como vértices, filtra as interações por tipo e popula os grafos G1 a G4 usando a API da F2.

### 4.1 Execução

```bash
python -m src.app.main --build
python -m src.app.main --build --output-dir data/raw --graph-output-dir output/graphs
```

O `--build` não precisa de token nem acessa a API do GitHub. Funciona apenas com os CSVs já existentes em `data/raw/`.

### 4.2 Estrutura de Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `exceptions.py` | `BuilderError`, `UnknownLoginError`, `UnknownIndexError`, `InvalidCsvError` |
| `interaction_weights.py` | Função `official_weight(tipo)` com a tabela de pesos do enunciado |
| `user_registry.py` | Mapeamento bidirecional `login ↔ índice inteiro` |
| `base_builder.py` | Lógica comum de build: leitura de CSV, registro de usuários, população do grafo |
| `graph1_comments_builder.py` | Builder do G1 — filtra `comment_issue` e `comment_pr` |
| `graph2_closures_builder.py` | Builder do G2 — filtra `close_issue` |
| `graph3_reviews_builder.py` | Builder do G3 — filtra `review_pr` e `merge_pr` |
| `graph4_integrated_builder.py` | Builder do G4 — usa todos os tipos, somando pesos |

### 4.3 `user_registry.py` — `UserRegistry`

Mantém um mapeamento bidirecional entre logins (strings) e índices inteiros (0 a n-1). A ordem de inserção define os índices, que são usados como identificadores de vértice no `AbstractGraph`.

| Método | Comportamento |
|--------|--------------|
| `add_user(login)` | Registra o login e retorna seu índice. Se o login já existe, retorna o índice já atribuído sem duplicar. |
| `get_index(login)` | Retorna o índice do login. Lança `UnknownLoginError` se o login não foi registrado. |
| `get_login(index)` | Retorna o login do índice. Lança `UnknownIndexError` se o índice não existe. |

O `UserRegistry` é preenchido a partir de `users.csv` primeiro e depois com logins adicionais que apareçam somente em `interactions.csv`.

### 4.4 `base_builder.py` — `BaseBuilder`

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

### 4.5 `interaction_weights.py`

Centraliza a tabela de pesos oficiais do enunciado. A função `official_weight(tipo)` é usada pelo G4 para garantir que o peso somado seja sempre o peso canônico do tipo, independente do valor que vier no campo `weight` do CSV.

### 4.6 `exceptions.py` (builder)

| Exceção | Quando é lançada |
|---------|------------------|
| `BuilderError` | Classe base para erros da frente de builders |
| `UnknownLoginError` | Tentativa de acessar índice de login não registrado no `UserRegistry` |
| `UnknownIndexError` | Tentativa de acessar login de índice inexistente no `UserRegistry` |
| `InvalidCsvError` | Arquivo ausente, coluna faltando ou linha com dados inválidos |

### 4.7 Saída dos Builders

| Grafo | Arquivo GEXF gerado |
|-------|---------------------|
| G1 | `output/graphs/graph1_comments.gexf` |
| G2 | `output/graphs/graph2_closures.gexf` |
| G3 | `output/graphs/graph3_reviews.gexf` |
| G4 | `output/graphs/graph4_integrated.gexf` |

### 4.8 Testes F3

Meta de cobertura: **>= 98%** em `src/builder/`. Cenários: filtro por tipo de interação, acumulação de pesos no G4, exportação GEXF, parametrização com lista e matriz, e testes opcionais com os CSVs reais de `data/raw/`.

```bash
python -m pytest tests/test_builder.py -v
python -m pytest tests/test_builder.py --cov=src.builder --cov-report=term-missing
```

---

## 5. F4 — Analysis (`src/analysis/`)

**Responsável: Diogo Meireles**

A frente de análise calcula métricas de centralidade, estrutura e comunidade sobre os grafos G1 a G4. Ela não lê os arquivos `.gexf` — reconstrói os grafos em memória chamando os próprios builders (F3) sobre os CSVs.

### 5.1 Execução

```bash
python -m src.app.main --analyze
python -m src.app.main --analyze --output-dir data/raw --report-output-dir output/reports
```

### 5.2 `centrality.py`

| Função | Algoritmo | Normalização |
|--------|-----------|-------------|
| `degree_centrality(graph)` | Grau de entrada e saída de cada vértice | Dividido por (n - 1) |
| `betweenness_centrality(graph)` | Algoritmo de Brandes — BFS se pesos zero, Dijkstra se ponderado | Dividido por (n-1)(n-2) para grafos dirigidos |
| `closeness_centrality(graph)` | Distâncias mínimas a partir de cada vértice | Inverso da soma das distâncias alcançáveis |
| `pagerank(graph, damping=0.85)` | Iteração de potência com fator de amortecimento 0.85 | Nós pendentes distribuem rank; soma total aproxima 1 |

### 5.3 `structure.py`

| Função | Fórmula / comportamento |
|--------|------------------------|
| `density(graph)` | `\|E\| / (\|V\| × (\|V\| - 1))` — razão entre arestas existentes e arestas possíveis |
| `clustering_coefficient(graph)` | Calcula coeficiente local por vértice (transitividade dirigida) e coeficiente global. Retorna dicionário com chaves `local` e `global`. |
| `degree_assortativity(graph)` | Correlação de Pearson entre o grau de origem e destino de cada aresta. Positivo = usuários similares conectam-se mais. |

### 5.4 `community.py`

| Função | Comportamento |
|--------|--------------|
| `detect_communities(graph)` | Algoritmo de Louvain para grafos dirigidos. Executa fase local (mover vértice para comunidade que maximize modularidade) e fase de agregação. Pesos zero são tratados como peso unitário. |
| `modularity(graph, partition)` | Calcula a modularidade de Newman para grafos dirigidos dado um particionamento. |
| `bridging_ties(graph, partition)` | Retorna lista de tuplas `(origem, destino, com_origem, com_destino)` para cada aresta que conecta comunidades diferentes. |

### 5.5 Fluxo de `run_analysis()`

Para cada um dos quatro grafos (G1 a G4):

1. Instancia o builder correspondente e chama `build()` para obter `(graph, registry)`
2. Calcula todas as centralidades e adiciona as linhas em `centrality_rows`
3. Calcula densidade, clustering e assortatividade e armazena em `structure_data`
4. Executa Louvain, calcula modularidade e identifica `bridging_ties`
5. Ao final, escreve os três arquivos de saída em `output/reports/`

### 5.6 Schemas de Saída

| Arquivo | Colunas / campos |
|---------|-----------------|
| `centrality.csv` | `login`, `graph`, `degree_in`, `degree_out`, `betweenness`, `closeness`, `pagerank` (uma linha por usuário por grafo, valores com 6 casas decimais) |
| `communities.csv` | `login`, `community_id`, `graph` (uma linha por usuário por grafo) |
| `structure.json` | Por grafo: `density`, `clustering_coefficient_global`, `clustering_coefficient_local` (por login), `degree_assortativity`, `modularity`, `num_communities`, `num_bridging_ties` |

### 5.7 Testes F4

88 testes usando grafos de referência com propriedades conhecidas: estrela, ciclo, completo, desconectado, caminho. Verificações: PageRank soma aproxima 1, Louvain retorna partição válida, bridging ties corretos. Parametrizados com lista e matriz.

```bash
python -m pytest tests/test_analysis.py -v
python -m pytest tests/test_analysis.py --cov=src.analysis -q
```

---

## 6. F5 — Integração CLI (`src/app/main.py`)

**Responsável: Diogo Meireles**

O `main.py` é o ponto de entrada da linha de comando. Orquestra as frentes F1, F3 e F4 sem misturar responsabilidades entre elas. O import da F1 é feito de forma lazy (somente quando `--mine` é usado) para que `--build` e `--analyze` funcionem sem o token da API.

### 6.1 Flags Disponíveis

| Flag | Função chamada | Observação |
|------|---------------|------------|
| `--mine` | `run_mining()` | Precisa de `GITHUB_TOKEN` no ambiente |
| `--build` | `run_build()` | Só precisa dos CSVs em `data/raw/` |
| `--analyze` | `run_analysis()` | Só precisa dos CSVs em `data/raw/` |
| `--all` | `mine → build → analyze` | Executa pipeline completo |

### 6.2 Argumentos Opcionais

| Argumento | Padrão | Afeta |
|-----------|--------|-------|
| `--repo` | `github/spec-kit` | Repositório minerado pela F1 |
| `--output-dir` | `data/raw` | Onde F1 grava e F3/F4 leem os CSVs |
| `--graph-output-dir` | `output/graphs` | Onde F3 grava os GEXF |
| `--report-output-dir` | `output/reports` | Onde F4 grava os relatórios |

---

## 7. F5.5 — GrafoGen Frontend (`frontend-grafogen/`)

**Responsável: Matheus Felipe**

SPA que detecta o estado atual do pipeline, permite executar cada etapa Python via browser, visualiza os quatro grafos de forma interativa e exibe métricas de centralidade.

### 7.1 Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| UI | React 19 + TypeScript + Vite 8 |
| Estilo | Tailwind CSS 4 |
| Visualização de grafo | vis-network (canvas WebGL) |
| Gerenciamento de estado | Zustand 5 |
| Roteamento | React Router 7 |
| API local | Express 5 (Node.js) |
| Orquestração Python | `spawn('python', ['-m', 'src.app.main', '--{stage}'])` |

### 7.2 Como Rodar

```bash
cd frontend-grafogen
npm install
npm run dev   # inicia API Express (3001) + Vite (5173) em paralelo
```

Pré-requisitos: Node 18+, Python 3.10+ com `requirements.txt` instalado. Os dados de `data/raw/` e `output/` são opcionais — o frontend detecta automaticamente quais etapas já foram executadas.

### 7.3 API Express (`/api`)

| Método | Rota | Comportamento |
|--------|------|--------------|
| `GET` | `/status` | Estado do pipeline. Verificado a cada 3s pela Home via polling. Indica quais etapas foram concluídas. |
| `GET` | `/graphs/:type` | Retorna o GEXF XML. `:type` aceita `G1`, `G2`, `G3` ou `G4`. |
| `GET` | `/reports/:name` | Retorna `centrality.csv`, `communities.csv` ou `structure.json`. |
| `POST` | `/pipeline/:stage` | Dispara `mine`, `build` ou `analyze`. Retorna 409 se já há processo rodando. |
| `POST` | `/pipeline/cancel` | Envia SIGTERM para o processo Python ativo. |

**Detecção de Status do Pipeline:**

| Campo em `/status` | Critério de verificação |
|--------------------|------------------------|
| `stage1Complete` | Existem `data/raw/users.csv` e `data/raw/interactions.csv` |
| `stage2Complete` | Os 4 arquivos GEXF existem em `output/graphs/` |
| `stage3Complete` | Existem `centrality.csv` e `communities.csv` em `output/reports/` |
| `interactionCount` | Número de linhas de `interactions.csv` menos o cabeçalho |

### 7.4 Rotas React

| Rota | Componente | Função |
|------|-----------|--------|
| `/` | `HomePage` | Cards do pipeline (mine → build → analyze), logs de execução, cards G1–G4 disponíveis |
| `/visualize/:graphId` | `VisualizePage` | Visualização interativa do grafo. `graphId` aceita `G1`, `G2`, `G3` ou `G4`. |

### 7.5 Componentes Principais

| Componente | Função |
|-----------|--------|
| `GraphCanvas` | Renderiza o grafo com vis-network. Suporta filtro por peso mínimo (`minWeight`), destaque de nós na busca, coloração por comunidade e foco animado em vértice específico. |
| `GraphSidebar` | Troca de grafo, campo de busca por login (foco ao pressionar Enter), slider de peso mínimo (G4), botões de exportar e métricas. |
| `MetricsPanel` | Exibe top 10 usuários por pagerank, betweenness, degree_in ou closeness. Permite toggle de coloração por comunidade. |
| `ExportModal` | Exporta o grafo como PNG (1920x1080 ou 3840x2160), SVG vetorial ou formato DOT. |
| `ZoomControls` | Botões de zoom in, zoom out e fit (centraliza o grafo na tela). |
| `PipelineCard + LogsModal` | Dispara cada etapa do pipeline Python e exibe os logs de execução em tempo real. |

### 7.6 `gexfParser.ts`

Converte o GEXF 1.3 gerado por `gephi_exporter.py` (F2) para o modelo interno do frontend. Cada nó vira um objeto com `id` (índice) e `label` (login). Cada aresta vira um objeto com `source`, `target` e `weight`. Para G1–G3, o peso padrão é 1 se o atributo estiver ausente; para G4, é 0 até a leitura do atributo.

A função `parseCSVMetrics(csv)` converte o `centrality.csv` em uma lista de objetos com os campos `login`, `graph`, `degree_in`, `degree_out`, `betweenness`, `closeness` e `pagerank`, armazenados no `graphStore`.

### 7.7 Regras de Performance (`graphOptions.ts`)

| Condição | Comportamento aplicado |
|----------|----------------------|
| <= 500 vértices | Labels visíveis diretamente no canvas |
| > 500 vértices | Labels ocultos; exibidos como tooltip no hover |
| <= 1000 vértices | Física vis-network habilitada (forceAtlas2Based) |
| > 1000 vértices | Física desligada (layout estático para performance) |
| Tamanho do nó | 16px com <= 500 vértices; 8px com > 500 |
| Largura da aresta | Proporcional a `log(weight + 1)` |

### 7.8 Integração com as Frentes

| Frente | Artefato consumido pelo GrafoGen |
|--------|----------------------------------|
| F1 | `users.csv` e `interactions.csv` (para verificar `stage1Complete`) |
| F3 | `output/graphs/*.gexf` (visualização dos grafos) |
| F4 | `centrality.csv` (métricas), `communities.csv` (coloração por comunidade), `structure.json` |

---

## 8. Fluxo Completo: da API ao Grafo

### Etapa 1 — Mineração (F1)

1. `GitHubClient` autentica com o token do `.env`
2. `IssueMiner` percorre todas as issues via `get_issues(state='all')`, filtrando PRs
3. Para cada issue: extrai comentários (`comment_issue` + `open_issue_commented`) e fechamentos (`close_issue`)
4. `PRMiner` percorre todos os PRs via `get_pulls(state='all')`
5. Para cada PR: extrai comentários gerais, comentários em linha de código, reviews e merges
6. Cada interação entre usuários distintos vira um objeto `Interaction`
7. `DataExporter` grava `users.csv`, `interactions.csv` e `events.csv` em `data/raw/`

### Etapa 2 — Build dos Grafos (F3)

1. `BaseBuilder` carrega `users.csv` → `UserRegistry` atribui índice `0..n-1` a cada login
2. `interactions.csv` é lido linha por linha
3. Cada builder filtra as linhas pelo campo `type`
4. Para cada interação filtrada: `add_edge(src_idx, dst_idx)` + `set_edge_weight(src_idx, dst_idx, peso)`
5. G4 acumula pesos; G1–G3 usam apenas a primeira ocorrência de cada par
6. `export_to_gephi()` serializa cada grafo como GEXF 1.3 em `output/graphs/`

### Etapa 3 — Análise (F4)

1. `run_analysis()` reconstrói cada grafo em memória chamando os builders novamente
2. Para cada grafo: `degree_centrality`, `betweenness_centrality`, `closeness_centrality` e `pagerank`
3. Para cada grafo: `density`, `clustering_coefficient` e `degree_assortativity`
4. Para cada grafo: `detect_communities` (Louvain), `modularity` e `bridging_ties`
5. Resultados salvos em `output/reports/`

### Etapa 4 — Visualização (F5.5)

1. Frontend detecta `stage1Complete`, `stage2Complete` e `stage3Complete` via polling em `/api/status`
2. Usuário clica em um card de grafo → `fetchGraphGexf(G1)` busca o GEXF via `/api/graphs/G1`
3. `gexfParser.ts` converte o GEXF em nós e arestas para o vis-network
4. Se `stage3Complete`, `centrality.csv` é carregado e métricas ficam disponíveis no `MetricsPanel`
5. `communities.csv` habilita a coloração por comunidade no `GraphCanvas`
6. Usuário pode filtrar arestas por peso mínimo, buscar usuários, exportar o grafo e navegar entre G1–G4

---

## 9. Comandos de Referência

### Pipeline

```bash
python -m src.app.main --mine                    # Mineração
python -m src.app.main --build                   # Build dos grafos
python -m src.app.main --analyze                 # Análise
python -m src.app.main --all                     # Pipeline completo
python -m src.app.api_demo                       # Demo da API de grafos (F2)
cd frontend-grafogen && npm run dev              # GrafoGen em localhost:5173
```

### Testes

```bash
pytest tests/test_mining.py -q                                            # F1
pytest tests/test_graph_matrix.py tests/test_graph_list.py -q            # F2
pytest tests/test_builder.py -q                                           # F3
pytest tests/test_analysis.py -q                                          # F4
pytest tests/ -q                                                          # Todos (~290 testes)
pytest --cov=src tests/                                                   # Cobertura geral (~99%)
npm test            # (em frontend-grafogen/) Vitest
npm run test:coverage                                                     # Cobertura frontend
```

### Metas de Cobertura

| Frente | Meta |
|--------|------|
| F1 — `src/mining/` | >= 98% |
| F2 — `src/graph/` | >= 98% |
| F3 — `src/builder/` | >= 98% |
| F4 — `src/analysis/` | >= 98% |
| F5.5 — `src/utils/` (frontend) | >= 90% |
