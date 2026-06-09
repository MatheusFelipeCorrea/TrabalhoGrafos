# 🕸️ GitHub Graph Analyzer

> Ferramenta de mineração e análise de redes de colaboração em repositórios open-source do GitHub, modelada com Teoria dos Grafos.

---

## 🎓 Sobre o Trabalho

Trabalho prático da disciplina **Teoria dos Grafos e Computabilidade** — Curso de Engenharia de Software / PUC Minas — 2026/1.  
**Professor:** Leonardo V. Cardoso

O objetivo é desenvolver uma ferramenta computacional que **modele as interações entre colaboradores de um repositório open-source como um grafo direcionado**, aplicando algoritmos clássicos da teoria dos grafos e métricas de redes complexas para extrair insights sobre a dinâmica da comunidade.

---

## 🎯 Repositório Analisado

**[github/spec-kit](https://github.com/github/spec-kit)** — escolhido por:

- ⭐ Mais de 5.000 estrelas (atende ao requisito do enunciado)
- 🧑‍🤝‍🧑 Comunidade ativa, com fluxo constante de issues, PRs e revisões
- 🔄 Diversidade de tipos de interação (discussões, reviews, merges)
- 📊 Volume de dados suficiente para análises significativas de centralidade, coesão e comunidades

---

## 🧠 Modelagem em Grafos

Cada **usuário** é um **vértice**. Cada **interação** é uma **aresta direcionada** (de quem agiu para o autor do artefato impactado). Grafos são **simples e direcionados**, com arestas anti-paralelas quando há reciprocidade.

| Grafo | Relação modelada |
|-------|------------------|
| **G1** | Comentários em issues e pull requests |
| **G2** | Fechamento de issue por outro usuário |
| **G3** | Revisões / aprovações / merges de pull requests |
| **G4** | **Integrado e ponderado**, combinando todas as interações |

### Pesos do grafo integrado (G4)

| Interação | Peso |
|-----------|:---:|
| Comentário em issue ou PR | 2 |
| Abertura de issue comentada por outro | 3 |
| Revisão / aprovação de PR | 4 |
| Merge de PR | 5 |

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Por quê? |
|--------|-----------|----------|
| Linguagem | **Python 3.10+** | Permitida pelo enunciado, ecossistema rico para mineração |
| Mineração GitHub | **PyGithub** | Cobre 100% dos endpoints REST necessários (issues, PRs, reviews, eventos), com paginação automática e tratamento nativo de rate-limit |
| Manipulação de dados | **pandas**, **tqdm** | Persistência em CSV e barras de progresso |
| Cálculos numéricos | **numpy** | Matriz de adjacência e operações numéricas |
| Configuração | **python-dotenv** | Carregamento de token GitHub via `.env` |
| Testes | **pytest** | Padrão da comunidade Python |
| Relatório | **LaTeX (template SBC)** | Exigência do enunciado |
| Visualização (desktop) | **Gephi** (externo) | Abre `.gexf` exportado manualmente |
| Visualização (web) | **GrafoGen** — React + Vis-Network | SPA em `frontend-grafogen/` |

> ⚠️ **IMPORTANTE:** Conforme o enunciado, **NÃO usamos** bibliotecas prontas de grafos (como `networkx`, `igraph`, `graph-tool`). A estrutura de grafo (matriz e lista de adjacência), todos os algoritmos da API e os algoritmos de análise (centralidade, comunidades, etc.) são **implementados do zero**.

---

## 🏛️ Arquitetura

```
┌─────────────────────────────────────────────────────┐
│  [F1] MINING       →  Coleta dados via GitHub API   │
│  [F2] GRAPH        →  Estrutura de grafo (do zero)  │
│  [F3] BUILDER      →  Constrói G1, G2, G3, G4       │
│  [F4] ANALYSIS     →  Métricas e algoritmos         │
└─────────────────────────────────────────────────────┘
                   │
                   ▼
          [APP] Pipeline + Demo da API
                   │
                   ▼
          [F5] GRAFOGEN — Visualizador web interativo
```

A estrutura completa de pastas, contratos entre camadas e documentação técnica por frente estão em:

- [`github-graph-analyzer/README.MD`](./github-graph-analyzer/README.MD) — contratos e `src/`
- [`github-graph-analyzer/Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md`](./github-graph-analyzer/Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md) — **F1–F5.5 em um documento** (leitura em grupo)
- [`github-graph-analyzer/Docs/README.md`](./github-graph-analyzer/Docs/README.md) — índice da pasta Docs

---

## 👥 Equipe e Divisão de Responsabilidades

| Frente | Responsável | Descrição |
|--------|-------------|-----------|
| 🟦 **F1 — Mining** | **Arthur Henrique** | Coleta via GitHub API, CSVs em `data/raw/` |
| 🟩 **F2 — Graph Structures** | **Matheus Felipe** | `AbstractGraph`, matriz/lista, GEXF, `api_demo` |
| 🟨 **F3 — Builders** | **Alice Shikida** | G1–G4, `UserRegistry`, exportação `.gexf` |
| 🟥 **F4 — Analysis** | **Diogo Meireles** | Centralidade, estrutura, comunidades |
| 🟪 **F5 — Integração** | **Diogo Meireles** | `main.py` CLI, pipeline `--all` |
| 🟦 **F5.5 — Frontend** | **Matheus Felipe** | GrafoGen (`frontend-grafogen/`) |
| 📄 **F6 — Relatório SBC** | **Alice Shikida**, **Matheus Felipe** | LaTeX, vídeo, entrega final |

> Todos os membros são responsáveis por: **testes da própria frente (meta ≥ 98% de cobertura)**, **commits regulares no Git**, **revisão dos PRs dos colegas** e **contribuição no relatório**.

Diagramas UML: [`github-graph-analyzer/Docs/diagramas/`](./github-graph-analyzer/Docs/diagramas/)

---

## 🚀 Como Executar

### 1. Pré-requisitos
- Python 3.10+
- Node.js 18+ (apenas para o GrafoGen)
- Conta GitHub com [Personal Access Token](https://github.com/settings/tokens) (escopo `public_repo`)

### 2. Instalação (backend Python)

```bash
git clone <url-do-repo>
cd TrabalhoGrafos/github-graph-analyzer
python -m venv .venv
source .venv/bin/activate            # Linux/Mac
# .venv\Scripts\activate              # Windows
pip install -r requirements.txt
```

### 3. Configuração

```bash
cp .env.example .env
# Edite .env e adicione: GITHUB_TOKEN=ghp_seu_token_aqui
```

### 4. Pipeline completo

```bash
# 1) Coleta os dados do repositório (gera CSVs em data/raw/)
python -m src.app.main --mine

# 2) Constrói os 4 grafos (gera .gexf em output/graphs/)
python -m src.app.main --build

# 3) Roda as análises (gera relatórios em output/reports/)
python -m src.app.main --analyze

# OU rodar tudo de uma vez:
python -m src.app.main --all
```

> Se os CSVs e GEXF já existem no repositório, pule `--mine` e use apenas `--build` / `--analyze` conforme necessário.

### 5. Demonstração da API de grafos

```bash
python -m src.app.api_demo
```

### 6. Visualizador web (GrafoGen)

```bash
cd ../frontend-grafogen
npm install
npm run dev
```

- Frontend: http://localhost:5173
- API local: http://localhost:3001

Documentação completa: [`github-graph-analyzer/Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md`](./github-graph-analyzer/Docs/DocumentaçãoTecnica/DocumentacaoTecnica.md) (Parte 5 — GrafoGen)

### 7. Testes

**Backend (Python):**

```bash
cd github-graph-analyzer
pytest tests/ -v          # exige ≥98% em src/ (pytest.ini)
pytest --cov=src tests/   # relatório detalhado
```

**Frontend (GrafoGen — utilitários):**

```bash
cd frontend-grafogen
npm test
npm run test:coverage
```

---

## 📦 Entregáveis

- [x] **Etapa 1** — Modelagem e planejamento (README + relatório inicial)
- [x] **Etapa 2** — Protótipo funcional com testes (F1–F4 implementadas, GrafoGen operacional)
- [ ] **Etapa 3** — Relatório SBC final + vídeo de apresentação

---

## 📑 Relatório

O relatório técnico em LaTeX (template oficial da SBC) será entregue na **Etapa 3** (F6 — Relatório).  
Enunciado: [`github-graph-analyzer/Docs/Orientação Trabalho/tp-es.pdf`](./github-graph-analyzer/Docs/Orientação%20Trabalho/tp-es.pdf).

---

## 🎬 Apresentação em Vídeo

Link disponibilizado na entrega final.

---

## 📜 Licença

Trabalho acadêmico — PUC Minas / 2026-1.
