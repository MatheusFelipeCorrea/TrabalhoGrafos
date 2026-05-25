# [EPIC] 4 - Analysis

## CARD EPIC-4 - Frente 4 - Analysis
Tipo: Epic
Prioridade: 🔺 Highest
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): -
Data Limite: No date

## 📝 Descricao
Implementar metricas de centralidade, estrutura e comunidades, com relatorios para interpretacao da rede.

## ✅ Criterios de Aceite
- Todas as features e stories do epic implementadas.
- Cobertura de testes da frente entre 90% e 95%.
- Integracao com outras frentes sem quebra de contrato.

## 🚫 Regras de Negocio
- Seguir estritamente o enunciado do trabalho e restricoes tecnicas.

---

## CARD FEAT-4.1
Titulo: Metricas de centralidade
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-4
Data Limite: No date

## 📝 Descricao
Implementar degree, betweenness, closeness e pagerank sem bibliotecas prontas de grafos.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/analysis/centrality.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_analysis.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)

## ✅ Criterios de Aceite
- Fluxos da feature implementados com consistencia funcional e tecnica.
- Integracao validada com camadas adjacentes.
- Erros de entrada e falhas transitorias tratados de forma resiliente.

## 🛠️ Implementacao (Alto Nivel)
- Definir contrato publico da feature e metodos internos.
- Integrar com modulos dependentes sem quebrar API existente.
- Escrever testes cobrindo cenario feliz, alternativo e edge case.

## ✅ Definicao de Pronto (DoD)
- [ ] Stories da feature concluidas e revisadas.
- [ ] Cobertura da frente entre 90% e 95%.
- [ ] Documentacao tecnica atualizada.

## 🔗 Dependencias
- Dependencias: FEAT-2.2, FEAT-3.6

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-4.1.1
Titulo: Calcular degree centrality
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.1
Data Limite: No date

## 📝 Descricao
Como analista, eu quero medir centralidade por grau, para identificar atores mais conectados.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### centrality.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/centrality.py
Seguir padrao de: src/analysis/centrality.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> degree_centrality(graph: AbstractGraph) -> dict[int, float]
-> betweenness_centrality(graph: AbstractGraph) -> dict[int, float]
-> pagerank(graph: AbstractGraph, damping: float = 0.85, tol: float = 1e-6) -> dict[int, float]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_1_1_cenario_feliz() - valida cenario 1.
-> test_______4_1_1_cenario_alternativo() - valida cenario 2.
-> test_______4_1_1_edge_case() - valida cenario 3.
-> test_______4_1_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.3]
- Importa de: src/analysis/centrality.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.1.2
Titulo: Implementar betweenness (Brandes)
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.1
Data Limite: No date

## 📝 Descricao
Como analista, eu quero medir intermediacao de vertices, para detectar pontos de passagem da colaboracao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### centrality.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/centrality.py
Seguir padrao de: src/analysis/centrality.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> degree_centrality(graph: AbstractGraph) -> dict[int, float]
-> betweenness_centrality(graph: AbstractGraph) -> dict[int, float]
-> pagerank(graph: AbstractGraph, damping: float = 0.85, tol: float = 1e-6) -> dict[int, float]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_1_2_cenario_feliz() - valida cenario 1.
-> test_______4_1_2_cenario_alternativo() - valida cenario 2.
-> test_______4_1_2_edge_case() - valida cenario 3.
-> test_______4_1_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.1.1]
- Importa de: src/analysis/centrality.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 5
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.1.3
Titulo: Implementar closeness e pagerank
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.1
Data Limite: No date

## 📝 Descricao
Como analista, eu quero medir proximidade e relevancia global, para complementar analise de influencia.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### centrality.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/centrality.py
Seguir padrao de: src/analysis/centrality.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> degree_centrality(graph: AbstractGraph) -> dict[int, float]
-> betweenness_centrality(graph: AbstractGraph) -> dict[int, float]
-> pagerank(graph: AbstractGraph, damping: float = 0.85, tol: float = 1e-6) -> dict[int, float]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_1_3_cenario_feliz() - valida cenario 1.
-> test_______4_1_3_cenario_alternativo() - valida cenario 2.
-> test_______4_1_3_edge_case() - valida cenario 3.
-> test_______4_1_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.1.1]
- Importa de: src/analysis/centrality.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 5
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

---

## CARD FEAT-4.2
Titulo: Metricas de estrutura e coesao
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-4
Data Limite: No date

## 📝 Descricao
Implementar densidade, clustering e assortatividade para redes dirigidas.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/analysis/structure.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_analysis.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)

## ✅ Criterios de Aceite
- Fluxos da feature implementados com consistencia funcional e tecnica.
- Integracao validada com camadas adjacentes.
- Erros de entrada e falhas transitorias tratados de forma resiliente.

## 🛠️ Implementacao (Alto Nivel)
- Definir contrato publico da feature e metodos internos.
- Integrar com modulos dependentes sem quebrar API existente.
- Escrever testes cobrindo cenario feliz, alternativo e edge case.

## ✅ Definicao de Pronto (DoD)
- [ ] Stories da feature concluidas e revisadas.
- [ ] Cobertura da frente entre 90% e 95%.
- [ ] Documentacao tecnica atualizada.

## 🔗 Dependencias
- Dependencias: FEAT-2.2, FEAT-3.6

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-4.2.1
Titulo: Calcular densidade da rede
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.2
Data Limite: No date

## 📝 Descricao
Como analista, eu quero obter E/(V*(V-1)), para medir nivel de conexao global.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### structure.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/structure.py
Seguir padrao de: src/analysis/structure.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> density(graph: AbstractGraph) -> float
-> clustering_coefficient(graph: AbstractGraph) -> float
-> degree_assortativity(graph: AbstractGraph) -> float

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_2_1_cenario_feliz() - valida cenario 1.
-> test_______4_2_1_cenario_alternativo() - valida cenario 2.
-> test_______4_2_1_edge_case() - valida cenario 3.
-> test_______4_2_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.3]
- Importa de: src/analysis/structure.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.2.2
Titulo: Calcular clustering local e global
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.2
Data Limite: No date

## 📝 Descricao
Como analista, eu quero medir triadizacao da rede, para identificar coesao em grupos.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### structure.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/structure.py
Seguir padrao de: src/analysis/structure.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> density(graph: AbstractGraph) -> float
-> clustering_coefficient(graph: AbstractGraph) -> float
-> degree_assortativity(graph: AbstractGraph) -> float

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_2_2_cenario_feliz() - valida cenario 1.
-> test_______4_2_2_cenario_alternativo() - valida cenario 2.
-> test_______4_2_2_edge_case() - valida cenario 3.
-> test_______4_2_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.2.1]
- Importa de: src/analysis/structure.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.2.3
Titulo: Calcular assortatividade de grau
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.2
Data Limite: No date

## 📝 Descricao
Como analista, eu quero medir correlacao de graus conectados, para entender padrao assortativo ou dissortativo.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### structure.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/structure.py
Seguir padrao de: src/analysis/structure.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> density(graph: AbstractGraph) -> float
-> clustering_coefficient(graph: AbstractGraph) -> float
-> degree_assortativity(graph: AbstractGraph) -> float

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_2_3_cenario_feliz() - valida cenario 1.
-> test_______4_2_3_cenario_alternativo() - valida cenario 2.
-> test_______4_2_3_edge_case() - valida cenario 3.
-> test_______4_2_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.2.1]
- Importa de: src/analysis/structure.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

---

## CARD FEAT-4.3
Titulo: Deteccao de comunidades
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-4
Data Limite: No date

## 📝 Descricao
Implementar deteccao de comunidades, modularidade e arestas de ponte.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/analysis/community.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_analysis.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)

## ✅ Criterios de Aceite
- Fluxos da feature implementados com consistencia funcional e tecnica.
- Integracao validada com camadas adjacentes.
- Erros de entrada e falhas transitorias tratados de forma resiliente.

## 🛠️ Implementacao (Alto Nivel)
- Definir contrato publico da feature e metodos internos.
- Integrar com modulos dependentes sem quebrar API existente.
- Escrever testes cobrindo cenario feliz, alternativo e edge case.

## ✅ Definicao de Pronto (DoD)
- [ ] Stories da feature concluidas e revisadas.
- [ ] Cobertura da frente entre 90% e 95%.
- [ ] Documentacao tecnica atualizada.

## 🔗 Dependencias
- Dependencias: FEAT-2.2, FEAT-3.6

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-4.3.1
Titulo: Detectar comunidades na rede
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.3
Data Limite: No date

## 📝 Descricao
Como analista, eu quero separar vertices em grupos, para interpretar estrutura social do repositorio.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### community.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/community.py
Seguir padrao de: src/analysis/community.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> detect_communities(graph: AbstractGraph) -> list[set[int]]
-> modularity(graph: AbstractGraph, partition: list[set[int]]) -> float
-> bridging_ties(graph: AbstractGraph, partition: list[set[int]]) -> list[tuple[int,int]]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_3_1_cenario_feliz() - valida cenario 1.
-> test_______4_3_1_cenario_alternativo() - valida cenario 2.
-> test_______4_3_1_edge_case() - valida cenario 3.
-> test_______4_3_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.3]
- Importa de: src/analysis/community.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 5
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.3.2
Titulo: Calcular modularidade da particao
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.3
Data Limite: No date

## 📝 Descricao
Como analista, eu quero avaliar qualidade da comunidade detectada, para comparar resultados de estrategia de agrupamento.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### community.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/community.py
Seguir padrao de: src/analysis/community.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> detect_communities(graph: AbstractGraph) -> list[set[int]]
-> modularity(graph: AbstractGraph, partition: list[set[int]]) -> float
-> bridging_ties(graph: AbstractGraph, partition: list[set[int]]) -> list[tuple[int,int]]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_3_2_cenario_feliz() - valida cenario 1.
-> test_______4_3_2_cenario_alternativo() - valida cenario 2.
-> test_______4_3_2_edge_case() - valida cenario 3.
-> test_______4_3_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.3.1]
- Importa de: src/analysis/community.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.3.3
Titulo: Identificar arestas de ponte
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.3
Data Limite: No date

## 📝 Descricao
Como analista, eu quero achar ligacoes entre comunidades, para destacar conexoes criticas entre grupos.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### community.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/community.py
Seguir padrao de: src/analysis/community.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> detect_communities(graph: AbstractGraph) -> list[set[int]]
-> modularity(graph: AbstractGraph, partition: list[set[int]]) -> float
-> bridging_ties(graph: AbstractGraph, partition: list[set[int]]) -> list[tuple[int,int]]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_3_3_cenario_feliz() - valida cenario 1.
-> test_______4_3_3_cenario_alternativo() - valida cenario 2.
-> test_______4_3_3_edge_case() - valida cenario 3.
-> test_______4_3_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.3.1]
- Importa de: src/analysis/community.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

---

## CARD FEAT-4.4
Titulo: Geracao de relatorios de analise
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-4
Data Limite: No date

## 📝 Descricao
Gerar arquivos de saida centrality.csv, structure.json e communities.csv.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/analysis/centrality.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/analysis/structure.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/analysis/community.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/output/reports/ (EXISTENTE - MODIFICAR)

## ✅ Criterios de Aceite
- Fluxos da feature implementados com consistencia funcional e tecnica.
- Integracao validada com camadas adjacentes.
- Erros de entrada e falhas transitorias tratados de forma resiliente.

## 🛠️ Implementacao (Alto Nivel)
- Definir contrato publico da feature e metodos internos.
- Integrar com modulos dependentes sem quebrar API existente.
- Escrever testes cobrindo cenario feliz, alternativo e edge case.

## ✅ Definicao de Pronto (DoD)
- [ ] Stories da feature concluidas e revisadas.
- [ ] Cobertura da frente entre 90% e 95%.
- [ ] Documentacao tecnica atualizada.

## 🔗 Dependencias
- Dependencias: FEAT-4.1, FEAT-4.2, FEAT-4.3

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-4.4.1
Titulo: Gerar centrality.csv
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.4
Data Limite: No date

## 📝 Descricao
Como analista, eu quero exportar metricas de centralidade, para fornecer base para ranking de usuarios.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### centrality.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/centrality.py
Seguir padrao de: src/analysis/centrality.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> degree_centrality(graph: AbstractGraph) -> dict[int, float]
-> betweenness_centrality(graph: AbstractGraph) -> dict[int, float]
-> pagerank(graph: AbstractGraph, damping: float = 0.85, tol: float = 1e-6) -> dict[int, float]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_4_1_cenario_feliz() - valida cenario 1.
-> test_______4_4_1_cenario_alternativo() - valida cenario 2.
-> test_______4_4_1_edge_case() - valida cenario 3.
-> test_______4_4_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.1.1, STORY-4.1.2, STORY-4.1.3]
- Importa de: src/analysis/centrality.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.4.2
Titulo: Gerar structure.json
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.4
Data Limite: No date

## 📝 Descricao
Como analista, eu quero exportar metricas estruturais, para consolidar indicadores globais do grafo.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### structure.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/structure.py
Seguir padrao de: src/analysis/structure.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> density(graph: AbstractGraph) -> float
-> clustering_coefficient(graph: AbstractGraph) -> float
-> degree_assortativity(graph: AbstractGraph) -> float

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_4_2_cenario_feliz() - valida cenario 1.
-> test_______4_4_2_cenario_alternativo() - valida cenario 2.
-> test_______4_4_2_edge_case() - valida cenario 3.
-> test_______4_4_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.2.1, STORY-4.2.2, STORY-4.2.3]
- Importa de: src/analysis/structure.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

## CARD STORY-4.4.3
Titulo: Gerar communities.csv
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.4
Data Limite: No date

## 📝 Descricao
Como analista, eu quero exportar particao e pontes, para apoiar interpretacao de comunidades no relatorio.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### community.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/community.py
Seguir padrao de: src/analysis/community.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> detect_communities(graph: AbstractGraph) -> list[set[int]]
-> modularity(graph: AbstractGraph, partition: list[set[int]]) -> float
-> bridging_ties(graph: AbstractGraph, partition: list[set[int]]) -> list[tuple[int,int]]

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_4_3_cenario_feliz() - valida cenario 1.
-> test_______4_4_3_cenario_alternativo() - valida cenario 2.
-> test_______4_4_3_edge_case() - valida cenario 3.
-> test_______4_4_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.3.1, STORY-4.3.2, STORY-4.3.3]
- Importa de: src/analysis/community.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, analysis, python, story

---

## CARD FEAT-4.5
Titulo: Testes da camada de analise
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-4
Data Limite: No date

## 📝 Descricao
Cobrir algoritmos com grafos canonicos: vazio, estrela, ciclo e completo.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/tests/test_analysis.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/analysis/centrality.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/analysis/structure.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/analysis/community.py (EXISTENTE - MODIFICAR)

## ✅ Criterios de Aceite
- Fluxos da feature implementados com consistencia funcional e tecnica.
- Integracao validada com camadas adjacentes.
- Erros de entrada e falhas transitorias tratados de forma resiliente.

## 🛠️ Implementacao (Alto Nivel)
- Definir contrato publico da feature e metodos internos.
- Integrar com modulos dependentes sem quebrar API existente.
- Escrever testes cobrindo cenario feliz, alternativo e edge case.

## ✅ Definicao de Pronto (DoD)
- [ ] Stories da feature concluidas e revisadas.
- [ ] Cobertura da frente entre 90% e 95%.
- [ ] Documentacao tecnica atualizada.

## 🔗 Dependencias
- Dependencias: FEAT-4.1, FEAT-4.2, FEAT-4.3, FEAT-4.4

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-4.5.1
Titulo: Criar fixtures de grafos canonicos
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.5
Data Limite: No date

## 📝 Descricao
Como QA, eu quero reutilizar cenarios de teste deterministas, para aumentar confiabilidade dos testes.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_5_1_cenario_feliz() - valida cenario 1.
-> test_______4_5_1_cenario_alternativo() - valida cenario 2.
-> test_______4_5_1_edge_case() - valida cenario 3.
-> test_______4_5_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.2, STORY-2.4.2]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, testes, python, story

## CARD STORY-4.5.2
Titulo: Validar resultados esperados das metricas
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.5
Data Limite: No date

## 📝 Descricao
Como QA, eu quero comparar metricas com valores conhecidos, para evitar erro matematico na implementacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

#### centrality.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/centrality.py
Seguir padrao de: src/analysis/centrality.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> degree_centrality(graph: AbstractGraph) -> dict[int, float]
-> betweenness_centrality(graph: AbstractGraph) -> dict[int, float]
-> pagerank(graph: AbstractGraph, damping: float = 0.85, tol: float = 1e-6) -> dict[int, float]

#### structure.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/structure.py
Seguir padrao de: src/analysis/structure.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> density(graph: AbstractGraph) -> float
-> clustering_coefficient(graph: AbstractGraph) -> float
-> degree_assortativity(graph: AbstractGraph) -> float

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_5_2_cenario_feliz() - valida cenario 1.
-> test_______4_5_2_cenario_alternativo() - valida cenario 2.
-> test_______4_5_2_edge_case() - valida cenario 3.
-> test_______4_5_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.1.1, STORY-4.2.1]
- Importa de: src/analysis/centrality.py, src/analysis/structure.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, testes, python, story

## CARD STORY-4.5.3
Titulo: Validar robustez em edge cases
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-4.5
Data Limite: No date

## 📝 Descricao
Como QA, eu quero testar grafo vazio e desconexo, para evitar quebra em entrada limite na apresentacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_analysis.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_analysis.py
Seguir padrao de: tests/test_analysis.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_analysis()
-> test_metricas_em_grafo_canonico()
-> test_edge_case_grafo_vazio()

#### community.py (EXISTENTE - MODIFICAR)
Criar em: src/analysis/community.py
Seguir padrao de: src/analysis/community.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> detect_communities(graph: AbstractGraph) -> list[set[int]]
-> modularity(graph: AbstractGraph, partition: list[set[int]]) -> float
-> bridging_ties(graph: AbstractGraph, partition: list[set[int]]) -> list[tuple[int,int]]

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______4_5_3_cenario_feliz() - valida cenario 1.
-> test_______4_5_3_cenario_alternativo() - valida cenario 2.
-> test_______4_5_3_edge_case() - valida cenario 3.
-> test_______4_5_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.3.1]
- Importa de: src/analysis/community.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --analyze - gera metricas e relatorios.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-4, testes, python, story

---
