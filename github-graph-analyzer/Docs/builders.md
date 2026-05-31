# Documentacao da Frente 3 - Builders

Este documento descreve a implementacao do **Epic 3 (Builders)** em `src/builder/`, os testes em `tests/test_builder.py` e o comando `--build` em `src/app/main.py`. A Frente 3 transforma os CSVs minerados pela Frente 1 em quatro grafos direcionados simples (G1 a G4) usando a API da Frente 2.

## Visao Geral

Entrada (contrato com F1):

- `data/raw/users.csv` — colunas `login`, `user_id`, `name`
- `data/raw/interactions.csv` — colunas `src_login`, `dst_login`, `type`, `weight`, `timestamp`, `source_id`

Saida (contrato com F4 e Gephi):

- Instancia de `AbstractGraph` + `UserRegistry` por builder
- Arquivos `.gexf` em `output/graphs/`:
  - `graph1_comments.gexf` — G1
  - `graph2_closures.gexf` — G2
  - `graph3_reviews.gexf` — G3
  - `graph4_integrated.gexf` — G4

Comando principal (usa CSVs ja minerados; **nao** chama a API do GitHub):

```bash
cd github-graph-analyzer
python -m src.app.main --build
```

Opcoes:

```bash
python -m src.app.main --build --output-dir data/raw --graph-output-dir output/graphs
```

## Estrutura de Arquivos

```text
src/builder/
├── __init__.py
├── exceptions.py              # Erros de dominio do builder
├── interaction_weights.py     # Tabela oficial de pesos por tipo
├── user_registry.py           # Bijeção login <-> indice
├── base_builder.py            # Template: leitura CSV + build()
├── graph1_comments_builder.py # G1: comentarios
├── graph2_closures_builder.py # G2: fechamentos de issue
├── graph3_reviews_builder.py  # G3: reviews e merges de PR
└── graph4_integrated_builder.py # G4: integrado e ponderado

tests/
├── test_builder.py
└── builder_test_helpers.py
```

## Features e Stories Implementadas (Epic 3)

| Feature | Descricao | Modulos |
|---------|-----------|---------|
| **FEAT-3.1** | Registry de usuarios (`login` ↔ indice estavel) | `user_registry.py` |
| **FEAT-3.2** | Builder base: leitura de CSV, filtro, template `build()` | `base_builder.py` |
| **FEAT-3.3** | Grafo 1 — comentarios em issue/PR | `graph1_comments_builder.py` |
| **FEAT-3.4** | Grafo 2 — fechamento de issue | `graph2_closures_builder.py` |
| **FEAT-3.5** | Grafo 3 — review e merge de PR | `graph3_reviews_builder.py` |
| **FEAT-3.6** | Grafo 4 — todas as interacoes com soma de pesos | `graph4_integrated_builder.py` |
| **FEAT-3.7** | Testes dos builders, filtros, agregacao G4 e exportacao | `tests/test_builder.py` |

## `user_registry.py`

Classe `UserRegistry` — mapeamento deterministico entre logins do GitHub e indices `0 .. n-1`.

| Metodo | Comportamento |
|--------|----------------|
| `add_user(login)` | Registra login; retorna indice existente se ja cadastrado (idempotente) |
| `get_index(login)` | Retorna indice; lanca `UnknownLoginError` se ausente |
| `get_login(index)` | Retorna login; lanca `UnknownIndexError` se indice invalido |

Usuarios sao ordenados na ordem de primeira insercao. O registry e preenchido a partir de `users.csv` e, durante o `build`, logins que aparecem apenas em `interactions.csv` tambem sao registrados.

## `base_builder.py`

Classe abstrata `BaseBuilder` com fluxo template:

1. Carregar e validar `users.csv`
2. Carregar e validar `interactions.csv` (cada linha validada via `Interaction` da F1)
3. Filtrar linhas (`_filter_interactions` — implementado nas subclasses)
4. Registrar todos os logins envolvidos
5. Instanciar grafo (`AdjacencyListGraph` por padrao)
6. Definir rotulo de cada vertice (`set_vertex_label`)
7. Aplicar cada interacao filtrada (`_apply_interaction`)

Metodos publicos:

- `build(interactions_csv, users_csv) -> tuple[AbstractGraph, UserRegistry]`
- `build_and_export(..., output_path) -> tuple[graph, registry, path]` — delega exportacao a `export_to_gephi` (F2)

Fabricas de grafo:

- `BaseBuilder.list_graph_factory(n)` — **preferencia padrao** (`AdjacencyListGraph`)
- `BaseBuilder.matrix_graph_factory(n)` — `AdjacencyMatrixGraph`

O parametro `graph_factory` no construtor permite trocar a representacao (usado nos testes com ambas).

### Regra de arestas repetidas (G1–G3 vs G4)

O grafo e **simples**: no maximo uma aresta `src -> dst`.

| Builder | `accumulate_edge_weights` | Comportamento em repeticoes do mesmo par |
|---------|---------------------------|------------------------------------------|
| G1, G2, G3 | `False` | Primeira interacao cria aresta e define peso; demais linhas **ignoradas** |
| G4 | `True` | Cada linha **soma** o peso oficial do tipo na aresta existente |

Exemplo: tres comentarios `alice -> bob` no G1 geram **uma** aresta com peso **2**. No G4, os tres comentarios geram peso **6** (2+2+2).

Auto-interacoes (`src_login == dst_login`) sao descartadas na validacao do CSV e ignoradas em `_apply_interaction`.

## Builders Concretos

### G1 — `Graph1CommentsBuilder`

- **Filtro:** `comment_issue`, `comment_pr`
- **Semantica:** comentador (`src`) -> autor do conteudo (`dst`)
- **Arquivo GEXF:** `graph1_comments.gexf`

### G2 — `Graph2ClosuresBuilder`

- **Filtro:** `close_issue`
- **Semantica:** quem fechou (`src`) -> autor da issue (`dst`)
- **Arquivo GEXF:** `graph2_closures.gexf`

### G3 — `Graph3ReviewsBuilder`

- **Filtro:** `review_pr`, `merge_pr`
- **Semantica:** revisor ou quem fez merge (`src`) -> autor da PR (`dst`)
- **Arquivo GEXF:** `graph3_reviews.gexf`

### G4 — `Graph4IntegratedBuilder`

- **Filtro:** todos os tipos validos de `Interaction.ALLOWED_TYPES`
- **Pesos:** tabela oficial em `interaction_weights.py` (nao apenas o campo `weight` do CSV)
- **Agregacao:** soma de pesos por par `(src, dst)`
- **Arquivo GEXF:** `graph4_integrated.gexf`

## Tabela Oficial de Pesos

Definida em `interaction_weights.py` (alinhada ao PDF e ao README):

| Tipo | Peso |
|------|------|
| `comment_issue` | 2 |
| `comment_pr` | 2 |
| `open_issue_commented` | 3 |
| `close_issue` | 3 |
| `review_pr` | 4 |
| `merge_pr` | 5 |

Funcao `official_weight(tipo)` centraliza o valor usado no G4.

## `exceptions.py`

| Excecao | Quando |
|---------|--------|
| `BuilderError` | Base para erros do builder |
| `UnknownLoginError` | `get_index` com login nao registrado |
| `UnknownIndexError` | `get_login` com indice invalido |
| `InvalidCsvError` | Arquivo ausente, colunas faltando ou linha invalida no CSV |

## Integracao com Outras Frentes

```text
F1 (Mining)     --users.csv, interactions.csv-->  F3 (Builders)
F2 (Graph)      <--AbstractGraph, export_to_gephi--  F3
F3              --graph + UserRegistry-->           F4 (Analysis, futuro)
```

Dependencias atendidas antes deste epic:

- **FEAT-1.5** — exportacao CSV da mineracao
- **FEAT-2.2** — `AbstractGraph`, matriz e lista
- **FEAT-2.5.1** — exportacao GEXF

## `src/app/main.py`

- `run_build()` — executa os quatro builders com `AdjacencyListGraph` e grava os `.gexf`
- `--build` — flag da CLI; importa apenas modulos de builder (nao exige token GitHub)
- `--mine` — continua na F1; imports de mining sao lazy para nao exigir `dotenv` no build

## Testes e Cobertura

Arquivo principal: `tests/test_builder.py`

- Cenarios por story do backlog (`test_3_X_Y_*`)
- Testes agregados: `test_cenario_feliz_builder`, `test_filtro_por_tipo_interacao`, `test_agregacao_pesos_g4`
- Parametrizacao **lista + matriz** (`GRAPH_FACTORIES`)
- Fixtures sinteticas em `tests/builder_test_helpers.py`
- Testes opcionais com dados reais minerados (`data/raw/`) quando os arquivos existem no repo

Comando:

```bash
python -m pytest tests/test_builder.py -v
```

Cobertura da frente (meta do epic: **> 95%**):

```bash
python -m pytest tests/test_builder.py --cov=src.builder --cov-report=term-missing
```

O modulo `src/builder` deve manter cobertura de linhas **acima de 95%** (implementacao atual validada com `pytest-cov`).

## Checklist de Entrega do Epic 3

- [x] `UserRegistry` com `add_user`, `get_index`, `get_login`
- [x] `BaseBuilder` com `build`, `_filter_interactions`, `_apply_interaction`
- [x] Quatro builders concretos (G1–G4)
- [x] Exportacao GEXF para `output/graphs/`
- [x] CLI `--build` sem reexecutar mineracao
- [x] Testes com cobertura > 95% em `src/builder`
- [x] Documentacao tecnica (`Docs/builders.md`)

## Referencias

- Enunciado: `Docs/tp-es.pdf` (modelagem G1–G4 e pesos)
- Contrato CSV: `Docs/mining.md`, `README.MD` (secao Frente 1)
- API de grafo: `Docs/GraphStructures.md`
- Backlog: `.github/plans/cards/[EPIC] 3 - Builders.md`
