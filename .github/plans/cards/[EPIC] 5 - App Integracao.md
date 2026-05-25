# [EPIC] 5 - App Integracao

## CARD EPIC-5 - Frente 5 - App Integracao
Tipo: Epic
Prioridade: 🔺 Highest
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): -
Data Limite: No date

## 📝 Descricao
Integrar pipeline de execucao e demonstracao da API de grafos para validacao de ponta a ponta.

## ✅ Criterios de Aceite
- Todas as features e stories do epic implementadas.
- Cobertura de testes da frente entre 90% e 95%.
- Integracao com outras frentes sem quebra de contrato.

## 🚫 Regras de Negocio
- Seguir estritamente o enunciado do trabalho e restricoes tecnicas.

---

## CARD FEAT-5.1
Titulo: Demo completa da API de grafos
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-5
Data Limite: No date

## 📝 Descricao
Criar aplicacao separada para demonstrar todas operacoes da API de grafo.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/app/api_demo.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/adjacency_matrix_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/adjacency_list_graph.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-2.2, FEAT-2.3, FEAT-2.4

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-5.1.1
Titulo: Montar roteiro das operacoes obrigatorias
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-5.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero cobrir 18 operacoes da API, para atender exigencia explicita do enunciado.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### api_demo.py (EXISTENTE - MODIFICAR)
Criar em: src/app/api_demo.py
Seguir padrao de: src/app/api_demo.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> run_demo() -> None
-> _print_operation_result(name: str, result: object) -> None

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______5_1_1_cenario_feliz() - valida cenario 1.
-> test_______5_1_1_cenario_alternativo() - valida cenario 2.
-> test_______5_1_1_edge_case() - valida cenario 3.
-> test_______5_1_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.2.1]
- Importa de: src/app/api_demo.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --all - orquestra pipeline completo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-5, app, python, story

## CARD STORY-5.1.2
Titulo: Executar demo em matrix e list
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-5.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero mostrar consistencia entre implementacoes, para aumentar confianca na corretude da API.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### api_demo.py (EXISTENTE - MODIFICAR)
Criar em: src/app/api_demo.py
Seguir padrao de: src/app/api_demo.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> run_demo() -> None
-> _print_operation_result(name: str, result: object) -> None

#### adjacency_matrix_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_matrix_graph.py
Seguir padrao de: src/graph/adjacency_matrix_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> has_edge(self, u: int, v: int) -> bool
-> get_edge_weight(self, u: int, v: int) -> float

#### adjacency_list_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_list_graph.py
Seguir padrao de: src/graph/adjacency_list_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> remove_edge(self, u: int, v: int) -> None
-> get_vertex_out_degree(self, u: int) -> int

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______5_1_2_cenario_feliz() - valida cenario 1.
-> test_______5_1_2_cenario_alternativo() - valida cenario 2.
-> test_______5_1_2_edge_case() - valida cenario 3.
-> test_______5_1_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.3, STORY-2.4.3]
- Importa de: src/app/api_demo.py, src/graph/adjacency_list_graph.py, src/graph/adjacency_matrix_graph.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --all - orquestra pipeline completo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-5, app, python, story

## CARD STORY-5.1.3
Titulo: Melhorar saida da demo para avaliacao
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-5.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero imprimir resultados claros por operacao, para facilitar validacao na banca.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### api_demo.py (EXISTENTE - MODIFICAR)
Criar em: src/app/api_demo.py
Seguir padrao de: src/app/api_demo.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> run_demo() -> None
-> _print_operation_result(name: str, result: object) -> None

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______5_1_3_cenario_feliz() - valida cenario 1.
-> test_______5_1_3_cenario_alternativo() - valida cenario 2.
-> test_______5_1_3_edge_case() - valida cenario 3.
-> test_______5_1_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-5.1.1]
- Importa de: src/app/api_demo.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --all - orquestra pipeline completo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-5, app, python, story

---

## CARD FEAT-5.2
Titulo: CLI principal para pipeline completo
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-5
Data Limite: No date

## 📝 Descricao
Implementar comandos --mine, --build, --analyze e --all com tratamento de erro.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/app/main.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/mining/ (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/ (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/analysis/ (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-1.6, FEAT-3.7, FEAT-4.5

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-5.2.1
Titulo: Implementar flag --mine
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-5.2
Data Limite: No date

## 📝 Descricao
Como usuario do sistema, eu quero executar somente mineracao, para depurar coleta de dados isoladamente.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.py (EXISTENTE - MODIFICAR)
Criar em: src/app/main.py
Seguir padrao de: src/app/main.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> run_mine() -> int
-> run_build() -> int
-> run_analyze() -> int

#### github_client.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/github_client.py
Seguir padrao de: src/mining/github_client.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> get_repo(self, full_name: str) -> Repository
-> request_with_retry(self, op_name: str, operation: callable, max_retries: int = 5, base_delay: float = 0.5) -> object
-> _is_retryable_error(self, error: Exception) -> bool

#### test_mining.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_mining.py
Seguir padrao de: tests/test_mining.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_mining()
-> test_edge_case_mining()
-> test_resiliencia_retry_rate_limit()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______5_2_1_cenario_feliz() - valida cenario 1.
-> test_______5_2_1_cenario_alternativo() - valida cenario 2.
-> test_______5_2_1_edge_case() - valida cenario 3.
-> test_______5_2_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.6.3]
- Importa de: src/app/main.py, src/mining/github_client.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --all - orquestra pipeline completo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-5, app, python, story

## CARD STORY-5.2.2
Titulo: Implementar flag --build
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-5.2
Data Limite: No date

## 📝 Descricao
Como usuario do sistema, eu quero construir grafos a partir dos CSVs, para validar F3 sem rerodar mineracao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.py (EXISTENTE - MODIFICAR)
Criar em: src/app/main.py
Seguir padrao de: src/app/main.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> run_mine() -> int
-> run_build() -> int
-> run_analyze() -> int

#### base_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/base_builder.py
Seguir padrao de: src/builder/base_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _filter_interactions(self, rows: list[dict]) -> list[dict]
-> _apply_interaction(self, graph: AbstractGraph, row: dict) -> None

#### test_builder.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_builder.py
Seguir padrao de: tests/test_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_builder()
-> test_filtro_por_tipo_interacao()
-> test_agregacao_pesos_g4()

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______5_2_2_cenario_feliz() - valida cenario 1.
-> test_______5_2_2_cenario_alternativo() - valida cenario 2.
-> test_______5_2_2_edge_case() - valida cenario 3.
-> test_______5_2_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.7.2]
- Importa de: src/app/main.py, src/builder/base_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --all - orquestra pipeline completo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-5, app, python, story

## CARD STORY-5.2.3
Titulo: Implementar flag --analyze
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-5.2
Data Limite: No date

## 📝 Descricao
Como usuario do sistema, eu quero gerar metricas dos grafos prontos, para inspecionar resultados da analise isoladamente.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.py (EXISTENTE - MODIFICAR)
Criar em: src/app/main.py
Seguir padrao de: src/app/main.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> run_mine() -> int
-> run_build() -> int
-> run_analyze() -> int

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
-> test_______5_2_3_cenario_feliz() - valida cenario 1.
-> test_______5_2_3_cenario_alternativo() - valida cenario 2.
-> test_______5_2_3_edge_case() - valida cenario 3.
-> test_______5_2_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.5.2]
- Importa de: src/analysis/centrality.py, src/app/main.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --all - orquestra pipeline completo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-5, app, python, story

---
