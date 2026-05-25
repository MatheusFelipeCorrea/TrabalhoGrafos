# [EPIC] 2 - Graph Structures

## CARD EPIC-2 - Frente 2 - Graph Structures
Tipo: Epic
Prioridade: 🔺 Highest
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): -
Data Limite: No date

## 📝 Descricao
Implementar estruturas de grafo direcionado simples do zero, com API completa e exportacao GEXF.

## ✅ Criterios de Aceite
- Todas as features e stories do epic implementadas.
- Cobertura de testes da frente entre 90% e 95%.
- Integracao com outras frentes sem quebra de contrato.

## 🚫 Regras de Negocio
- Seguir estritamente o enunciado do trabalho e restricoes tecnicas.

---

## CARD FEAT-2.1
Titulo: Excecoes customizadas de dominio do grafo
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-2
Data Limite: No date

## 📝 Descricao
Criar excecoes claras para validacao de vertices, lacos e arestas inexistentes.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/graph/exceptions.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_matrix.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_list.py (EXISTENTE - MODIFICAR)

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
- Dependencias: nenhuma

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-2.1.1
Titulo: Criar InvalidVertexError
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero sinalizar indice fora da faixa, para evitar corrupcao de estado do grafo.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### exceptions.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/exceptions.py
Seguir padrao de: src/graph/exceptions.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> class InvalidVertexError(Exception)
-> class SelfLoopError(Exception)
-> class EdgeNotFoundError(Exception)

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_1_1_cenario_feliz() - valida cenario 1.
-> test_______2_1_1_cenario_alternativo() - valida cenario 2.
-> test_______2_1_1_edge_case() - valida cenario 3.
-> test_______2_1_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: nenhuma
- Importa de: src/graph/exceptions.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.1.2
Titulo: Criar SelfLoopError
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero bloquear aresta u para u, para cumprir restricao de grafo simples.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### exceptions.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/exceptions.py
Seguir padrao de: src/graph/exceptions.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> class InvalidVertexError(Exception)
-> class SelfLoopError(Exception)
-> class EdgeNotFoundError(Exception)

#### test_graph_list.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_list.py
Seguir padrao de: tests/test_graph_list.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_list()
-> test_idempotencia_add_edge_list()
-> test_excecao_self_loop_list()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_1_2_cenario_feliz() - valida cenario 1.
-> test_______2_1_2_cenario_alternativo() - valida cenario 2.
-> test_______2_1_2_edge_case() - valida cenario 3.
-> test_______2_1_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: nenhuma
- Importa de: src/graph/exceptions.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.1.3
Titulo: Criar EdgeNotFoundError
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero sinalizar operacao em aresta ausente, para dar feedback tecnico correto em remocao e peso.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### exceptions.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/exceptions.py
Seguir padrao de: src/graph/exceptions.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> class InvalidVertexError(Exception)
-> class SelfLoopError(Exception)
-> class EdgeNotFoundError(Exception)

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_1_3_cenario_feliz() - valida cenario 1.
-> test_______2_1_3_cenario_alternativo() - valida cenario 2.
-> test_______2_1_3_edge_case() - valida cenario 3.
-> test_______2_1_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: nenhuma
- Importa de: src/graph/exceptions.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

---

## CARD FEAT-2.2
Titulo: API abstrata AbstractGraph e validacoes comuns
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-2
Data Limite: No date

## 📝 Descricao
Definir contrato unico das operacoes obrigatorias de grafo e validacoes compartilhadas.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/exceptions.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_matrix.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_list.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-2.1

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-2.2.1
Titulo: Definir metodos obrigatorios da API
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero explicitar assinatura de operacoes, para garantir implementacoes consistentes.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### abstract_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/abstract_graph.py
Seguir padrao de: src/graph/abstract_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> _validate_vertex(self, v: int) -> None
-> add_edge(self, u: int, v: int) -> None
-> remove_edge(self, u: int, v: int) -> None

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_2_1_cenario_feliz() - valida cenario 1.
-> test_______2_2_1_cenario_alternativo() - valida cenario 2.
-> test_______2_2_1_edge_case() - valida cenario 3.
-> test_______2_2_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.1.1]
- Importa de: src/graph/abstract_graph.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.2.2
Titulo: Implementar validacao de vertices
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero validar indice em um unico ponto, para reduzir duplicacao e erro nas classes concretas.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### abstract_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/abstract_graph.py
Seguir padrao de: src/graph/abstract_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> _validate_vertex(self, v: int) -> None
-> add_edge(self, u: int, v: int) -> None
-> remove_edge(self, u: int, v: int) -> None

#### exceptions.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/exceptions.py
Seguir padrao de: src/graph/exceptions.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> class InvalidVertexError(Exception)
-> class SelfLoopError(Exception)
-> class EdgeNotFoundError(Exception)

#### test_graph_list.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_list.py
Seguir padrao de: tests/test_graph_list.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_list()
-> test_idempotencia_add_edge_list()
-> test_excecao_self_loop_list()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_2_2_cenario_feliz() - valida cenario 1.
-> test_______2_2_2_cenario_alternativo() - valida cenario 2.
-> test_______2_2_2_edge_case() - valida cenario 3.
-> test_______2_2_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.1.1]
- Importa de: src/graph/abstract_graph.py, src/graph/exceptions.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.2.3
Titulo: Documentar contratos de idempotencia
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero especificar add_edge sem duplicacao, para garantir comportamento exigido pelo enunciado.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### abstract_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/abstract_graph.py
Seguir padrao de: src/graph/abstract_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> _validate_vertex(self, v: int) -> None
-> add_edge(self, u: int, v: int) -> None
-> remove_edge(self, u: int, v: int) -> None

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_2_3_cenario_feliz() - valida cenario 1.
-> test_______2_2_3_cenario_alternativo() - valida cenario 2.
-> test_______2_2_3_edge_case() - valida cenario 3.
-> test_______2_2_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.2.1]
- Importa de: src/graph/abstract_graph.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

---

## CARD FEAT-2.3
Titulo: Implementacao por matriz de adjacencia
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-2
Data Limite: No date

## 📝 Descricao
Implementar classe de grafo direcionado simples usando matriz NxN.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/graph/adjacency_matrix_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/exceptions.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_matrix.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-2.1, FEAT-2.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-2.3.1
Titulo: Inicializar matriz e contadores
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.3
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero criar estrutura base da classe, para suportar operacoes de aresta e grau.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### adjacency_matrix_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_matrix_graph.py
Seguir padrao de: src/graph/adjacency_matrix_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> has_edge(self, u: int, v: int) -> bool
-> get_edge_weight(self, u: int, v: int) -> float

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_3_1_cenario_feliz() - valida cenario 1.
-> test_______2_3_1_cenario_alternativo() - valida cenario 2.
-> test_______2_3_1_edge_case() - valida cenario 3.
-> test_______2_3_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.2.1]
- Importa de: src/graph/adjacency_matrix_graph.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.3.2
Titulo: Implementar add_edge idempotente sem laco
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.3
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero adicionar arestas sem duplicar, para cumprir regra de grafo simples.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### adjacency_matrix_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_matrix_graph.py
Seguir padrao de: src/graph/adjacency_matrix_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> has_edge(self, u: int, v: int) -> bool
-> get_edge_weight(self, u: int, v: int) -> float

#### exceptions.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/exceptions.py
Seguir padrao de: src/graph/exceptions.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> class InvalidVertexError(Exception)
-> class SelfLoopError(Exception)
-> class EdgeNotFoundError(Exception)

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_3_2_cenario_feliz() - valida cenario 1.
-> test_______2_3_2_cenario_alternativo() - valida cenario 2.
-> test_______2_3_2_edge_case() - valida cenario 3.
-> test_______2_3_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.1.1, STORY-2.1.2, STORY-2.2.2]
- Importa de: src/graph/adjacency_matrix_graph.py, src/graph/exceptions.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.3.3
Titulo: Implementar consultas de grau e pesos
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.3
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero obter in/out degree e peso de aresta, para suportar metodos da API e analise.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### adjacency_matrix_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_matrix_graph.py
Seguir padrao de: src/graph/adjacency_matrix_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> has_edge(self, u: int, v: int) -> bool
-> get_edge_weight(self, u: int, v: int) -> float

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_3_3_cenario_feliz() - valida cenario 1.
-> test_______2_3_3_cenario_alternativo() - valida cenario 2.
-> test_______2_3_3_edge_case() - valida cenario 3.
-> test_______2_3_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.2]
- Importa de: src/graph/adjacency_matrix_graph.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

---

## CARD FEAT-2.4
Titulo: Implementacao por lista de adjacencia
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-2
Data Limite: No date

## 📝 Descricao
Implementar classe de grafo direcionado simples por lista de adjacencia.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/graph/adjacency_list_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/exceptions.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_list.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-2.1, FEAT-2.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-2.4.1
Titulo: Inicializar lista de adjacencia
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.4
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero estruturar armazenamento por vertice, para otimizar grafo esparso.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### adjacency_list_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_list_graph.py
Seguir padrao de: src/graph/adjacency_list_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> remove_edge(self, u: int, v: int) -> None
-> get_vertex_out_degree(self, u: int) -> int

#### test_graph_list.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_list.py
Seguir padrao de: tests/test_graph_list.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_list()
-> test_idempotencia_add_edge_list()
-> test_excecao_self_loop_list()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_4_1_cenario_feliz() - valida cenario 1.
-> test_______2_4_1_cenario_alternativo() - valida cenario 2.
-> test_______2_4_1_edge_case() - valida cenario 3.
-> test_______2_4_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.2.1]
- Importa de: src/graph/adjacency_list_graph.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.4.2
Titulo: Implementar add_edge idempotente e validacoes
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.4
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero adicionar aresta sem duplicar e sem laco, para garantir contrato da API abstrata.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### adjacency_list_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_list_graph.py
Seguir padrao de: src/graph/adjacency_list_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> remove_edge(self, u: int, v: int) -> None
-> get_vertex_out_degree(self, u: int) -> int

#### exceptions.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/exceptions.py
Seguir padrao de: src/graph/exceptions.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> class InvalidVertexError(Exception)
-> class SelfLoopError(Exception)
-> class EdgeNotFoundError(Exception)

#### test_graph_list.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_list.py
Seguir padrao de: tests/test_graph_list.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_list()
-> test_idempotencia_add_edge_list()
-> test_excecao_self_loop_list()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_4_2_cenario_feliz() - valida cenario 1.
-> test_______2_4_2_cenario_alternativo() - valida cenario 2.
-> test_______2_4_2_edge_case() - valida cenario 3.
-> test_______2_4_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.1.1, STORY-2.1.2, STORY-2.2.2]
- Importa de: src/graph/adjacency_list_graph.py, src/graph/exceptions.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.4.3
Titulo: Implementar remocao, graus e pesos
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.4
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero completar operacoes obrigatorias, para equivaler comportamento da implementacao em matriz.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### adjacency_list_graph.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/adjacency_list_graph.py
Seguir padrao de: src/graph/adjacency_list_graph.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_edge(self, u: int, v: int) -> None
-> remove_edge(self, u: int, v: int) -> None
-> get_vertex_out_degree(self, u: int) -> int

#### test_graph_list.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_list.py
Seguir padrao de: tests/test_graph_list.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_list()
-> test_idempotencia_add_edge_list()
-> test_excecao_self_loop_list()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_4_3_cenario_feliz() - valida cenario 1.
-> test_______2_4_3_cenario_alternativo() - valida cenario 2.
-> test_______2_4_3_edge_case() - valida cenario 3.
-> test_______2_4_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.4.2]
- Importa de: src/graph/adjacency_list_graph.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

---

## CARD FEAT-2.5
Titulo: Exportador Gephi em formato GEXF
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-2
Data Limite: No date

## 📝 Descricao
Gerar arquivo GEXF manualmente sem bibliotecas prontas para visualizacao no Gephi.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/graph/gephi_exporter.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/graph/abstract_graph.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_matrix.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-2.3, FEAT-2.4

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-2.5.1
Titulo: Montar XML de nos e arestas
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero gerar estrutura gexf valida, para permitir importacao no gephi.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### gephi_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/gephi_exporter.py
Seguir padrao de: src/graph/gephi_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export(graph: AbstractGraph, path: str) -> str
-> _build_nodes_xml(graph: AbstractGraph) -> str
-> _build_edges_xml(graph: AbstractGraph) -> str

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_5_1_cenario_feliz() - valida cenario 1.
-> test_______2_5_1_cenario_alternativo() - valida cenario 2.
-> test_______2_5_1_edge_case() - valida cenario 3.
-> test_______2_5_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.3]
- Importa de: src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.5.2
Titulo: Exportar atributos de peso
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero persistir pesos de aresta no gexf, para preservar semantica do grafo integrado.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### gephi_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/gephi_exporter.py
Seguir padrao de: src/graph/gephi_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export(graph: AbstractGraph, path: str) -> str
-> _build_nodes_xml(graph: AbstractGraph) -> str
-> _build_edges_xml(graph: AbstractGraph) -> str

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_5_2_cenario_feliz() - valida cenario 1.
-> test_______2_5_2_cenario_alternativo() - valida cenario 2.
-> test_______2_5_2_edge_case() - valida cenario 3.
-> test_______2_5_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.5.1]
- Importa de: src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

## CARD STORY-2.5.3
Titulo: Validar arquivo gerado no parser XML
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.5
Data Limite: No date

## 📝 Descricao
Como QA, eu quero garantir xml bem formado, para evitar falhas de importacao na apresentacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### gephi_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/gephi_exporter.py
Seguir padrao de: src/graph/gephi_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export(graph: AbstractGraph, path: str) -> str
-> _build_nodes_xml(graph: AbstractGraph) -> str
-> _build_edges_xml(graph: AbstractGraph) -> str

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_5_3_cenario_feliz() - valida cenario 1.
-> test_______2_5_3_cenario_alternativo() - valida cenario 2.
-> test_______2_5_3_edge_case() - valida cenario 3.
-> test_______2_5_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.5.1]
- Importa de: src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, graph, python, story

---

## CARD FEAT-2.6
Titulo: Testes das estruturas de grafo
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-2
Data Limite: No date

## 📝 Descricao
Criar suite robusta para validar contratos entre matrix e list.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/tests/test_graph_matrix.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_graph_list.py (EXISTENTE - MODIFICAR)
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
- Dependencias: FEAT-2.1, FEAT-2.2, FEAT-2.3, FEAT-2.4, FEAT-2.5

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-2.6.1
Titulo: Cobrir cenarios de idempotencia e excecoes
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.6
Data Limite: No date

## 📝 Descricao
Como QA, eu quero testar contrato de add_edge e validacoes, para evitar regressao em regras criticas.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

#### test_graph_list.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_list.py
Seguir padrao de: tests/test_graph_list.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_list()
-> test_idempotencia_add_edge_list()
-> test_excecao_self_loop_list()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_6_1_cenario_feliz() - valida cenario 1.
-> test_______2_6_1_cenario_alternativo() - valida cenario 2.
-> test_______2_6_1_edge_case() - valida cenario 3.
-> test_______2_6_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.2, STORY-2.4.2]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, testes, python, story

## CARD STORY-2.6.2
Titulo: Comparar consistencia matrix vs list
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.6
Data Limite: No date

## 📝 Descricao
Como QA, eu quero validar mesmos resultados para mesmos dados, para garantir equivalencia de implementacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

#### test_graph_list.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_list.py
Seguir padrao de: tests/test_graph_list.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_list()
-> test_idempotencia_add_edge_list()
-> test_excecao_self_loop_list()

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_6_2_cenario_feliz() - valida cenario 1.
-> test_______2_6_2_cenario_alternativo() - valida cenario 2.
-> test_______2_6_2_edge_case() - valida cenario 3.
-> test_______2_6_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.3.3, STORY-2.4.3]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, testes, python, story

## CARD STORY-2.6.3
Titulo: Validar exportacao gexf em testes
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-2.6
Data Limite: No date

## 📝 Descricao
Como QA, eu quero checar geracao de arquivo e conteudo basico, para evitar erro em entregavel visual.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_graph_matrix.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_graph_matrix.py
Seguir padrao de: tests/test_graph_matrix.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_graph_matrix()
-> test_idempotencia_add_edge_matrix()
-> test_excecao_indice_invalido_matrix()

#### gephi_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/gephi_exporter.py
Seguir padrao de: src/graph/gephi_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export(graph: AbstractGraph, path: str) -> str
-> _build_nodes_xml(graph: AbstractGraph) -> str
-> _build_edges_xml(graph: AbstractGraph) -> str

## 🧪 Testes
Arquivo: tests/test_graph_matrix.py
-> test_______2_6_3_cenario_feliz() - valida cenario 1.
-> test_______2_6_3_cenario_alternativo() - valida cenario 2.
-> test_______2_6_3_edge_case() - valida cenario 3.
-> test_______2_6_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.5.1]
- Importa de: src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.api_demo - demonstra API de grafo.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- Vertice fora de faixa -> InvalidVertexError.
- Laco em grafo simples -> SelfLoopError.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-2, testes, python, story

---
