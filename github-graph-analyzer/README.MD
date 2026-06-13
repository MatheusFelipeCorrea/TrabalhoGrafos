# 🔧 Documentação Técnica — `src/`

Documento interno de desenvolvimento. Descreve **arquitetura**, **contratos entre módulos**, **fluxo de dados** e **responsabilidades de cada frente**.

> Para visão geral do projeto, consulte o [README principal](../README.md).

### Documentação técnica

| Documento | Conteúdo |
|-----------|----------|
| **[`Docs/DocumentacaoTecnica.md`](./Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md)** | **Documento único** — F1–F5.5 (estudo do caso) |
| [`Docs/diagramas/`](./Docs/diagramas/) | UML PlantUML |
| [`Docs/README.md`](./Docs/README.md) | Índice da pasta Docs |

---

## 📂 Estrutura de Diretórios

```
src/
├── mining/                          # 🟦 FRENTE 1
│   ├── __init__.py
│   ├── github_client.py             # Autenticação, rate limit, retry
│   ├── issue_miner.py               # Issues + comentários + eventos de fechamento
│   ├── pr_miner.py                  # PRs + reviews + merges + comentários
│   ├── interaction_model.py         # @dataclass Interaction
│   └── data_exporter.py             # Persistência em CSV
│
├── graph/                           # 🟩 FRENTE 2
│   ├── __init__.py
│   ├── exceptions.py                # InvalidVertexError, SelfLoopError, etc.
│   ├── abstract_graph.py            # ABC com a API obrigatória
│   ├── adjacency_matrix_graph.py    # Implementação por matriz NxN
│   ├── adjacency_list_graph.py      # Implementação por listas
│   └── gephi_exporter.py            # Geração manual de .gexf (XML)
│
├── builder/                         # 🟨 FRENTE 3
│   ├── __init__.py
│   ├── user_registry.py             # Bijeção login ↔ índice
│   ├── base_builder.py              # Lê CSVs e popula grafo
│   ├── graph1_comments_builder.py   # G1: comentários
│   ├── graph2_closures_builder.py   # G2: fechamentos
│   ├── graph3_reviews_builder.py    # G3: reviews/merges
│   └── graph4_integrated_builder.py # G4: ponderado integrado
│
├── analysis/                        # 🟥 FRENTE 4
│   ├── __init__.py
│   ├── centrality.py                # Degree, Betweenness, Closeness, PageRank
│   ├── structure.py                 # Densidade, Clustering, Assortatividade
│   └── community.py                 # Louvain, modularity, Bridging Ties
│
└── app/                             # 🤝 INTEGRAÇÃO
├── __init__.py
├── api_demo.py                  # Demonstra TODAS as operações da AbstractGraph
└── main.py                      # CLI: --mine, --build, --analyze, --all
```

---

## 🟦 Frente 1 — Mining (`src/mining/`)

**Responsável:** Arthur Henrique  
**Objetivo:** Coletar dados do repositório `github/spec-kit` e persistir em CSV padronizado.

### Módulos

| Arquivo | Responsabilidade |
|---------|------------------|
| `github_client.py` | Inicializa cliente PyGithub, gerencia token, trata rate limit (espera quando necessário), implementa retry exponencial |
| `issue_miner.py` | Itera sobre issues do repo, coleta autor, comentários (autor + texto), eventos `closed` (quem fechou) |
| `pr_miner.py` | Itera sobre PRs, coleta autor, reviews (`APPROVED`, `CHANGES_REQUESTED`, `COMMENTED`), comentários e merge (quem mergeou) |
| `interaction_model.py` | `@dataclass Interaction(src_login, dst_login, type, weight, timestamp, source_id)` |
| `data_exporter.py` | Exporta para `data/raw/users.csv` e `data/raw/interactions.csv` |

### 📤 Saída — Schema dos CSVs (CONTRATO COM F3)

**`data/raw/users.csv`**
```csv
login,user_id,name
torvalds,1024025,Linus Torvalds
...
```

**`data/raw/interactions.csv`**
```csv
src_login,dst_login,type,weight,timestamp,source_id
alice,bob,comment_issue,2,2026-01-15T14:32:00Z,42
carol,dave,review_pr,4,2026-01-16T09:11:00Z,87
```

**Valores válidos para `type`:**
- `comment_issue` — comentou em issue de outro usuário (peso 2)
- `comment_pr` — comentou em PR de outro usuário (peso 2)
- `open_issue_commented` — abriu issue que recebeu comentário (peso 3)
- `review_pr` — fez review/aprovou PR de outro (peso 4)
- `merge_pr` — fez merge de PR de outro usuário (peso 5)
- `close_issue` — fechou issue de outro usuário (peso 3; usado no G2; implementado em `issue_miner.py`)

> ⚠️ Auto-interações (mesmo `src_login` e `dst_login`) **devem ser descartadas** (grafos sem laços).

### Tarefas
- [x] Configurar `GitHubClient` com `.env`
- [x] Implementar `IssueMiner.mine()` → lista de `Interaction`
- [x] Implementar `PRMiner.mine()` → lista de `Interaction`
- [x] Exportar para CSV
- [x] Testes com **mocks** da API (sem chamadas reais)

> Detalhes: [`Docs/DocumentacaoTecnica.md#parte-1--f1-mining`](./Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md#parte-1--f1-mining)

---

## 🟩 Frente 2 — Graph Structures (`src/graph/`)

**Responsável:** Matheus Felipe  
**Objetivo:** Implementar **do zero** estruturas de grafo direcionado simples, com duas representações.

### 🚨 Restrições obrigatórias do enunciado
- Grafos **simples**: sem laços, sem multi-arestas
- `addEdge` deve ser **idempotente**
- Lançar **exceções** para índices inválidos
- **PROIBIDO** uso de bibliotecas prontas (`networkx`, etc.)

### API obrigatória — `AbstractGraph`

```python
class AbstractGraph(ABC):
# Construção
def __init__(self, num_vertices: int): ...

# Consultas básicas
def get_vertex_count(self) -> int
def get_edge_count(self) -> int
def has_edge(self, u: int, v: int) -> bool

# Modificação
def add_edge(self, u: int, v: int) -> None
def remove_edge(self, u: int, v: int) -> None

# Relações entre vértices/arestas
def is_successor(self, u: int, v: int) -> bool
def is_predecessor(self, u: int, v: int) -> bool
def is_divergent(self, u1, v1, u2, v2) -> bool
def is_convergent(self, u1, v1, u2, v2) -> bool
def is_incident(self, u: int, v: int, x: int) -> bool

# Graus
def get_vertex_in_degree(self, u: int) -> int
def get_vertex_out_degree(self, u: int) -> int

# Pesos
def set_vertex_weight(self, v: int, w: float) -> None
def get_vertex_weight(self, v: int) -> float
def set_edge_weight(self, u: int, v: int, w: float) -> None
def get_edge_weight(self, u: int, v: int) -> float

# Propriedades
def is_connected(self) -> bool          # fracamente conectado
def is_empty_graph(self) -> bool
def is_complete_graph(self) -> bool

# Exportação
def export_to_gephi(self, path: str) -> None
```

### Exceções customizadas (`exceptions.py`)
- `InvalidVertexError` — índice fora do intervalo
- `SelfLoopError` — tentativa de adicionar laço
- `EdgeNotFoundError` — operação em aresta inexistente

### Exportação Gephi
Formato `.gexf` (XML) escrito **manualmente**. Spec: <https://gephi.org/gexf/format/>

### Tarefas
- [x] Definir `exceptions.py`
- [x] Implementar `AbstractGraph` (ABC com validações compartilhadas)
- [x] Implementar `AdjacencyMatrixGraph` (matriz `numpy`)
- [x] Implementar `AdjacencyListGraph` (dict por vértice)
- [x] Implementar `gephi_exporter` em XML (GEXF 1.3)
- [x] Testes unitários extensivos (cobertura ~98% em `src/graph`)

> Detalhes: [`Docs/DocumentacaoTecnica.md#parte-2--f2-graph-structures`](./Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md#parte-2--f2-graph-structures)

---

## 🟨 Frente 3 — Builders (`src/builder/`)

**Responsável:** Alice Shikida  
**Objetivo:** Transformar os CSVs minerados (F1) em instâncias de grafo (F2).

### Módulos

| Arquivo | Responsabilidade |
|---------|------------------|
| `user_registry.py` | Mantém bijeção `login ↔ índice`. Persistível em JSON. |
| `base_builder.py` | Classe abstrata: lê CSV, filtra por tipo, popula grafo |
| `graph1_comments_builder.py` | Filtra `comment_issue` + `comment_pr` |
| `graph2_closures_builder.py` | Filtra `close_issue` |
| `graph3_reviews_builder.py` | Filtra `review_pr` + `merge_pr` |
| `graph4_integrated_builder.py` | Usa todas, soma pesos em arestas paralelas |

### Lógica do Grafo Integrado (G4)
Quando há múltiplas interações entre A→B, **soma-se os pesos** na mesma aresta:

```
A → B (comment_pr, peso 2)
A → B (review_pr, peso 4)
A → B (merge_pr, peso 5)
========================
Aresta final A → B com peso 11
```

### 📥 Entrada
CSVs gerados pela Frente 1 + schema documentado acima.

### 📤 Saída (CONTRATO COM F4)
Tupla `(graph: AbstractGraph, registry: UserRegistry)` — registry permite traduzir índices ↔ logins nos relatórios.

### Tarefas
- [x] `UserRegistry` com `add_user`, `get_index`, `get_login`
- [x] `BaseBuilder` com método template `build()`
- [x] 4 builders concretos (G1–G4)
- [x] Exportação `.gexf` de cada grafo para `output/graphs/`
- [x] Testes com CSVs de exemplo (cobertura ≥ 98% em `src/builder`)

> Detalhes: [`Docs/DocumentacaoTecnica.md#parte-3--f3-builders`](./Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md#parte-3--f3-builders)

---

## 🟥 Frente 4 — Analysis (`src/analysis/`)

**Responsável:** Diogo Meireles  
**Objetivo:** Implementar **do zero** as métricas e algoritmos de análise.

### Métricas

#### `centrality.py`
- `degree_centrality(graph)` — grau de entrada e saída normalizados
- `betweenness_centrality(graph)` — algoritmo de **Brandes**
- `closeness_centrality(graph)` — baseado em **Dijkstra/BFS** múltiplo
- `pagerank(graph, damping=0.85, tol=1e-6)` — método das potências

#### `structure.py`
- `density(graph)` — `|E| / (|V| × (|V|-1))`
- `clustering_coefficient(graph)` — local e global
- `degree_assortativity(graph)` — coeficiente de Pearson dos graus

#### `community.py`
- `detect_communities(graph)` — algoritmo de Louvain
- `modularity(graph, partition)` — fórmula de Newman
- `bridging_ties(graph, partition)` — arestas inter-comunidade

### 📥 Entrada
Instância de `AbstractGraph` (qualquer implementação) + `UserRegistry`.

### 📤 Saída
- `output/reports/centrality.csv`
- `output/reports/structure.json`
- `output/reports/communities.csv`

### Tarefas
- [x] Implementar todas as métricas de centralidade
- [x] Implementar métricas estruturais
- [x] Implementar detecção de comunidades (Louvain)
- [x] Gerar relatórios em CSV/JSON
- [x] Testes com grafos de propriedades conhecidas (cobertura ≥ 98% em `src/analysis`)

> Detalhes: [`Docs/DocumentacaoTecnica.md#parte-4--f4-analysis`](./Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md#parte-4--f4-analysis)

---

## 🟪 Frente 5.5 — GrafoGen (`frontend-grafogen/`)

**Responsável:** Matheus Felipe  
**Objetivo:** Visualizador web interativo dos grafos G1–G4 e orquestração do pipeline Python.

### Componentes

| Pasta / arquivo | Responsabilidade |
|-----------------|------------------|
| `src/pages/` | Home (pipeline + cards) e Visualize (canvas) |
| `server/index.js` | API Express: status, GEXF, relatórios, spawn `--mine`/`--build`/`--analyze` |
| `src/utils/gexfParser.ts` | Converte GEXF 1.3 → Vis-Network |

### Como rodar

```bash
cd frontend-grafogen
npm install
npm run dev
```

> Detalhes: [`Docs/DocumentacaoTecnica.md#parte-5--f5-integração-e-grafogen`](./Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md#parte-5--f5-integração-e-grafogen)

---

## 🤝 App / Integração (`src/app/`) — F5

**Responsável:** Diogo Meireles

### `api_demo.py`
> 🚨 **Exigência do enunciado:** "uma aplicação separada deve ser utilizada para consumir a API e demonstrar todas operações disponíveis."

Script que cria um grafo pequeno e chama **TODAS** as 18 operações da `AbstractGraph`, imprimindo os resultados.

### `main.py`
CLI principal:
```bash
python -m src.app.main --mine      # F1
python -m src.app.main --build     # F3 (após F1)
python -m src.app.main --analyze   # F4 (após F3)
python -m src.app.main --all       # pipeline completo
```

---

## 🔄 Fluxo de Dados Entre Frentes

```
┌──────────┐   users.csv       ┌──────────┐   AbstractGraph   ┌──────────┐
│   F1     │   interactions.csv│   F3     │   + Registry      │   F4     │
│ Mining   │ ──────────────────►│ Builder  │ ─────────────────►│ Analysis │
└──────────┘                   └────┬─────┘                   └────┬─────┘
                                │                              │
                                │  usa                         │  usa
                                ▼                              ▼
                          ┌─────────────────────────────────────┐
                          │      F2 — Graph Structures          │
                          │   (AbstractGraph + 2 implementações)│
                          └─────────────────────────────────────┘
```

---

## 📝 Convenções de Código

- **PEP 8** para estilo
- **Type hints** em **toda** assinatura pública
- **Docstrings** no formato Google
- **Nomes em inglês** no código; comentários em português permitidos
- **1 classe por arquivo** (regra de ouro pra paralelizar sem conflito de merge)

---

## 🌿 Convenções de Git

### Branches
- `main` — código estável (apenas via PR)
- `dev` — integração contínua
- `feat/f1-issue-miner`, `feat/f2-matrix-graph`, etc. — features por frente

### Commits (Conventional Commits)
```
feat(mining): adiciona coleta de reviews em PRs
fix(graph): corrige idempotência do addEdge
test(builder): cobre filtragem do graph2
docs(readme): atualiza fluxo de dados
```

### Pull Requests
- Mínimo **1 revisor** de outra frente
- CI passando (testes verdes)
- Descrição com checklist do que foi feito

---

## 🧪 Como Rodar os Testes

```bash
# Todos
pytest tests/ -v

# Por frente
pytest tests/test_mining.py -v
pytest tests/test_graph_matrix.py tests/test_graph_list.py -v
pytest tests/test_builder.py -v
pytest tests/test_analysis.py -v

# Com cobertura
pytest --cov=src tests/

# GrafoGen (frontend)
cd ../frontend-grafogen
npm test
npm run test:coverage
```

**Meta de cobertura:** ≥ **98%** em `src/` (enforced via `pytest.ini`); GrafoGen ≥ **90%** em `frontend-grafogen/src/utils/`.

---

## ✅ Checklist de Definição de Pronto (DoD)

| Frente | Código | Testes | Cobertura | Doc técnica |
|--------|--------|--------|-----------|-------------|
| F1 Mining | ✅ | ✅ | ~100% | `Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md` |
| F2 Graph | ✅ | ✅ | 100% | `Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md` |
| F3 Builders | ✅ | ✅ | 100% | `Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md` |
| F4 Analysis | ✅ | ✅ | ~100% | `Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md` |
| F5 Integração | ✅ | ✅ | ~99% | `src/app/main.py` |
| F5.5 GrafoGen | ✅ | ✅ | ≥90% `src/utils` | `Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md` |

Pendente para entrega final (F6):
- [ ] Relatório SBC completo — **Alice Shikida**, **Matheus Felipe**
- [ ] Vídeo de apresentação

Diagramas UML: [`Docs/diagramas/`](./Docs/diagramas/)

---

## 📅 Cronograma

| Semana | F1 (Mining) | F2 (Graph) | F3 (Builder) | F4 (Analysis) |
|:------:|-------------|------------|--------------|---------------|
| **1** | Auth + esqueleto issue miner | `AbstractGraph` + exceptions | `UserRegistry` + mock CSV | Esqueleto + relatório etapa 1 |
| **2** | PRs + reviews + merges | `MatrixGraph` completo + testes | G1, G2, G3 | Centralidades |
| **3** | Dataset spec-kit completo | `ListGraph` + Gephi exporter | G4 integrado | Estrutura + comunidades |
| **4** | Refinos + edge cases | `api_demo.py` | Integração final | Relatório SBC + vídeo |

---

## 📞 Comunicação do Time

- **Daily assíncrona:** mensagem no grupo até as 22h sobre o progresso
- **Reunião semanal:** [definir dia/hora]
- **Decisões importantes:** registrar em `docs/decisions/`

---

