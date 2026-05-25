# 🕸️ GitHub Graph Analyzer

> Ferramenta de mineração e análise de redes de colaboração em repositórios open-source do GitHub, modelada com Teoria dos Grafos.

[](https://www.python.org/)
[](#)
[](#)

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
| Cálculos numéricos | **numpy** | Suporte a operações de matriz nas análises |
| Configuração | **python-dotenv** | Carregamento de token GitHub via `.env` |
| Testes | **pytest** | Padrão da comunidade Python |
| Relatório | **LaTeX (template SBC)** | Exigência do enunciado |
| Visualização | **Gephi** (externo) | Exportamos `.gexf` gerado manualmente |

> ⚠️ **IMPORTANTE:** Conforme o enunciado, **NÃO usamos** bibliotecas prontas de grafos (como `networkx`, `igraph`, `graph-tool`). A estrutura de grafo (matriz e lista de adjacência), todos os algoritmos da API e os algoritmos de análise (centralidade, comunidades, etc.) são **implementados do zero**.

---

## 🏛️ Arquitetura em 4 Camadas

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
```

A estrutura completa de pastas e os contratos entre as camadas estão documentados em [`src/README.md`](./src/README.md).

---

## 👥 Equipe e Divisão de Responsabilidades

| Membro | Frente Principal | Apoio Secundário |
|--------|------------------|------------------|
| **[Nome A]** | 🟦 F1 — Mining (coleta da API) | F3 — Builders |
| **[Nome B]** | 🟩 F2 — Graph Structures (Matrix + List + API + Gephi) | App Demo |
| **[Nome C]** | 🟨 F3 — Builders dos 4 grafos + UserRegistry | F1 — Mining |
| **[Nome D]** | 🟥 F4 — Análises e métricas + Relatório SBC | Vídeo / apresentação |

> Todos os membros são responsáveis por: **testes da própria frente**, **commits regulares no Git**, **revisão dos PRs dos colegas** e **contribuição no relatório**.

---

## 🚀 Como Executar

### 1. Pré-requisitos
- Python 3.10+
- Conta GitHub com [Personal Access Token](https://github.com/settings/tokens) (escopo `public_repo`)

### 2. Instalação

```bash
git clone <url-do-repo>
cd github-graph-analyzer
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

### 5. Demonstração da API de grafos

```bash
python -m src.app.api_demo
```

### 6. Testes

```bash
pytest tests/ -v
```

---

## 📦 Entregáveis

- [x] **Etapa 1** — Modelagem e planejamento (este README + relatório inicial)
- [ ] **Etapa 2** — Protótipo funcional com testes
- [ ] **Etapa 3** — Análises completas + relatório SBC + vídeo

---

## 📑 Relatório

O relatório técnico em LaTeX (template oficial da SBC) está em [`report/main.tex`](./report/main.tex).  
A versão compilada em PDF: [`report/main.pdf`](./report/main.pdf).

---

## 🎬 Apresentação em Vídeo

Link disponibilizado na entrega final.

---

## 📜 Licença

Trabalho acadêmico — PUC Minas / 2026-1.