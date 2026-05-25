# [EPIC] 3 - Builders

## CARD EPIC-3 - Frente 3 - Builders
Tipo: Epic
Prioridade: 🔺 Highest
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): -
Data Limite: No date

## 📝 Descricao
Transformar CSVs minerados em grafos G1, G2, G3 e G4 usando registry de usuarios e regras de peso.

## ✅ Criterios de Aceite
- Todas as features e stories do epic implementadas.
- Cobertura de testes da frente entre 90% e 95%.
- Integracao com outras frentes sem quebra de contrato.

## 🚫 Regras de Negocio
- Seguir estritamente o enunciado do trabalho e restricoes tecnicas.

---

## CARD FEAT-3.1
Titulo: Registry de usuarios login para indice
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-3
Data Limite: No date

## 📝 Descricao
Mapear login para indice e indice para login de forma deterministica.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/builder/user_registry.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_builder.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-1.5

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-3.1.1
Titulo: Adicionar usuario e retornar indice
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero gerar indice estavel por login, para construir arestas com vertices consistentes.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### user_registry.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/user_registry.py
Seguir padrao de: src/builder/user_registry.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_user(self, login: str) -> int
-> get_index(self, login: str) -> int
-> get_login(self, index: int) -> str

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
Arquivo: tests/test_builder.py
-> test_______3_1_1_cenario_feliz() - valida cenario 1.
-> test_______3_1_1_cenario_alternativo() - valida cenario 2.
-> test_______3_1_1_edge_case() - valida cenario 3.
-> test_______3_1_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.5.1]
- Importa de: src/builder/user_registry.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.1.2
Titulo: Consultar indice por login
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero buscar vertice de origem e destino, para evitar duplicacao de vertices.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### user_registry.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/user_registry.py
Seguir padrao de: src/builder/user_registry.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_user(self, login: str) -> int
-> get_index(self, login: str) -> int
-> get_login(self, index: int) -> str

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
Arquivo: tests/test_builder.py
-> test_______3_1_2_cenario_feliz() - valida cenario 1.
-> test_______3_1_2_cenario_alternativo() - valida cenario 2.
-> test_______3_1_2_edge_case() - valida cenario 3.
-> test_______3_1_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.1.1]
- Importa de: src/builder/user_registry.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.1.3
Titulo: Consultar login por indice
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero resolver nome para relatorios, para integrar com camada de analise.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### user_registry.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/user_registry.py
Seguir padrao de: src/builder/user_registry.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_user(self, login: str) -> int
-> get_index(self, login: str) -> int
-> get_login(self, index: int) -> str

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
Arquivo: tests/test_builder.py
-> test_______3_1_3_cenario_feliz() - valida cenario 1.
-> test_______3_1_3_cenario_alternativo() - valida cenario 2.
-> test_______3_1_3_edge_case() - valida cenario 3.
-> test_______3_1_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.1.1]
- Importa de: src/builder/user_registry.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

---

## CARD FEAT-3.2
Titulo: Builder base com template build
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-3
Data Limite: No date

## 📝 Descricao
Criar fluxo comum de leitura de CSV, filtro de interacao e aplicacao no grafo.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/builder/base_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/user_registry.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_builder.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-3.1, FEAT-2.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-3.2.1
Titulo: Ler CSVs com validacao de colunas
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero carregar users e interactions com schema valido, para evitar erro silencioso na construcao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

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
Arquivo: tests/test_builder.py
-> test_______3_2_1_cenario_feliz() - valida cenario 1.
-> test_______3_2_1_cenario_alternativo() - valida cenario 2.
-> test_______3_2_1_edge_case() - valida cenario 3.
-> test_______3_2_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.5.2]
- Importa de: src/builder/base_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.2.2
Titulo: Definir template build reutilizavel
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero padronizar fluxo dos builders concretos, para reduzir codigo duplicado.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

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
Arquivo: tests/test_builder.py
-> test_______3_2_2_cenario_feliz() - valida cenario 1.
-> test_______3_2_2_cenario_alternativo() - valida cenario 2.
-> test_______3_2_2_edge_case() - valida cenario 3.
-> test_______3_2_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.2.1, STORY-3.1.1]
- Importa de: src/builder/base_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.2.3
Titulo: Aplicar interacao no grafo com registry
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero converter login para indice ao adicionar aresta, para integrar F1, F2 e F3 corretamente.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### base_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/base_builder.py
Seguir padrao de: src/builder/base_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _filter_interactions(self, rows: list[dict]) -> list[dict]
-> _apply_interaction(self, graph: AbstractGraph, row: dict) -> None

#### user_registry.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/user_registry.py
Seguir padrao de: src/builder/user_registry.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> add_user(self, login: str) -> int
-> get_index(self, login: str) -> int
-> get_login(self, index: int) -> str

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
Arquivo: tests/test_builder.py
-> test_______3_2_3_cenario_feliz() - valida cenario 1.
-> test_______3_2_3_cenario_alternativo() - valida cenario 2.
-> test_______3_2_3_edge_case() - valida cenario 3.
-> test_______3_2_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.1.1, STORY-2.3.2]
- Importa de: src/builder/base_builder.py, src/builder/user_registry.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

---

## CARD FEAT-3.3
Titulo: Grafo 1 de comentarios
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-3
Data Limite: No date

## 📝 Descricao
Construir G1 com comment_issue e comment_pr.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/builder/graph1_comments_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/base_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_builder.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-3.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-3.3.1
Titulo: Filtrar tipos de comentario
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.3
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero considerar apenas comment_issue e comment_pr, para garantir semantica correta de G1.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph1_comments_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph1_comments_builder.py
Seguir padrao de: src/builder/graph1_comments_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_comment_type(self, interaction_type: str) -> bool

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
Arquivo: tests/test_builder.py
-> test_______3_3_1_cenario_feliz() - valida cenario 1.
-> test_______3_3_1_cenario_alternativo() - valida cenario 2.
-> test_______3_3_1_edge_case() - valida cenario 3.
-> test_______3_3_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.2.2]
- Importa de: src/builder/graph1_comments_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.3.2
Titulo: Criar arestas comentador para autor
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.3
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero adicionar relacao direcionada correta, para representar colaboracao entre usuarios.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph1_comments_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph1_comments_builder.py
Seguir padrao de: src/builder/graph1_comments_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_comment_type(self, interaction_type: str) -> bool

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
Arquivo: tests/test_builder.py
-> test_______3_3_2_cenario_feliz() - valida cenario 1.
-> test_______3_3_2_cenario_alternativo() - valida cenario 2.
-> test_______3_3_2_edge_case() - valida cenario 3.
-> test_______3_3_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.3.1, STORY-3.2.3]
- Importa de: src/builder/base_builder.py, src/builder/graph1_comments_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.3.3
Titulo: Exportar graph1_comments.gexf
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.3
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero persistir G1 para visualizacao, para dar suporte ao relatorio e demonstracao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph1_comments_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph1_comments_builder.py
Seguir padrao de: src/builder/graph1_comments_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_comment_type(self, interaction_type: str) -> bool

#### gephi_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/gephi_exporter.py
Seguir padrao de: src/graph/gephi_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export(graph: AbstractGraph, path: str) -> str
-> _build_nodes_xml(graph: AbstractGraph) -> str
-> _build_edges_xml(graph: AbstractGraph) -> str

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
Arquivo: tests/test_builder.py
-> test_______3_3_3_cenario_feliz() - valida cenario 1.
-> test_______3_3_3_cenario_alternativo() - valida cenario 2.
-> test_______3_3_3_edge_case() - valida cenario 3.
-> test_______3_3_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.5.1, STORY-3.3.2]
- Importa de: src/builder/graph1_comments_builder.py, src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

---

## CARD FEAT-3.4
Titulo: Grafo 2 de fechamentos de issue
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-3
Data Limite: No date

## 📝 Descricao
Construir G2 com close_issue.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/builder/graph2_closures_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/base_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_builder.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-3.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-3.4.1
Titulo: Filtrar tipo close_issue
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.4
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero considerar somente eventos de fechamento, para evitar contaminacao com outras interacoes.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph2_closures_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph2_closures_builder.py
Seguir padrao de: src/builder/graph2_closures_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_closure_type(self, interaction_type: str) -> bool

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
Arquivo: tests/test_builder.py
-> test_______3_4_1_cenario_feliz() - valida cenario 1.
-> test_______3_4_1_cenario_alternativo() - valida cenario 2.
-> test_______3_4_1_edge_case() - valida cenario 3.
-> test_______3_4_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.2.2]
- Importa de: src/builder/graph2_closures_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.4.2
Titulo: Aplicar direcao fechador para autor
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.4
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero modelar aresta src fechador dst autor, para capturar poder de resolucao de issues.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph2_closures_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph2_closures_builder.py
Seguir padrao de: src/builder/graph2_closures_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_closure_type(self, interaction_type: str) -> bool

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
Arquivo: tests/test_builder.py
-> test_______3_4_2_cenario_feliz() - valida cenario 1.
-> test_______3_4_2_cenario_alternativo() - valida cenario 2.
-> test_______3_4_2_edge_case() - valida cenario 3.
-> test_______3_4_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.4.1, STORY-3.2.3]
- Importa de: src/builder/base_builder.py, src/builder/graph2_closures_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.4.3
Titulo: Exportar graph2_closures.gexf
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.4
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero gerar artefato visual de G2, para suportar analise comparativa.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph2_closures_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph2_closures_builder.py
Seguir padrao de: src/builder/graph2_closures_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_closure_type(self, interaction_type: str) -> bool

#### gephi_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/gephi_exporter.py
Seguir padrao de: src/graph/gephi_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export(graph: AbstractGraph, path: str) -> str
-> _build_nodes_xml(graph: AbstractGraph) -> str
-> _build_edges_xml(graph: AbstractGraph) -> str

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
Arquivo: tests/test_builder.py
-> test_______3_4_3_cenario_feliz() - valida cenario 1.
-> test_______3_4_3_cenario_alternativo() - valida cenario 2.
-> test_______3_4_3_edge_case() - valida cenario 3.
-> test_______3_4_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.5.1, STORY-3.4.2]
- Importa de: src/builder/graph2_closures_builder.py, src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

---

## CARD FEAT-3.5
Titulo: Grafo 3 de reviews e merges
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-3
Data Limite: No date

## 📝 Descricao
Construir G3 com review_pr e merge_pr.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/builder/graph3_reviews_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/base_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_builder.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-3.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-3.5.1
Titulo: Filtrar tipos review_pr e merge_pr
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero processar apenas eventos de review e merge, para garantir semantica correta de G3.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph3_reviews_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph3_reviews_builder.py
Seguir padrao de: src/builder/graph3_reviews_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_review_type(self, interaction_type: str) -> bool

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
Arquivo: tests/test_builder.py
-> test_______3_5_1_cenario_feliz() - valida cenario 1.
-> test_______3_5_1_cenario_alternativo() - valida cenario 2.
-> test_______3_5_1_edge_case() - valida cenario 3.
-> test_______3_5_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.2.2]
- Importa de: src/builder/graph3_reviews_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.5.2
Titulo: Aplicar arestas de revisor e merger
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero criar relacao para autor da PR, para medir influencia tecnica na rede.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph3_reviews_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph3_reviews_builder.py
Seguir padrao de: src/builder/graph3_reviews_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_review_type(self, interaction_type: str) -> bool

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
Arquivo: tests/test_builder.py
-> test_______3_5_2_cenario_feliz() - valida cenario 1.
-> test_______3_5_2_cenario_alternativo() - valida cenario 2.
-> test_______3_5_2_edge_case() - valida cenario 3.
-> test_______3_5_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.5.1, STORY-3.2.3]
- Importa de: src/builder/base_builder.py, src/builder/graph3_reviews_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.5.3
Titulo: Exportar graph3_reviews.gexf
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero persistir G3, para habilitar visualizacao e comparacao com G1/G2.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph3_reviews_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph3_reviews_builder.py
Seguir padrao de: src/builder/graph3_reviews_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _is_review_type(self, interaction_type: str) -> bool

#### gephi_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/graph/gephi_exporter.py
Seguir padrao de: src/graph/gephi_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export(graph: AbstractGraph, path: str) -> str
-> _build_nodes_xml(graph: AbstractGraph) -> str
-> _build_edges_xml(graph: AbstractGraph) -> str

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
Arquivo: tests/test_builder.py
-> test_______3_5_3_cenario_feliz() - valida cenario 1.
-> test_______3_5_3_cenario_alternativo() - valida cenario 2.
-> test_______3_5_3_edge_case() - valida cenario 3.
-> test_______3_5_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.5.1, STORY-3.5.2]
- Importa de: src/builder/graph3_reviews_builder.py, src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

---

## CARD FEAT-3.6
Titulo: Grafo 4 integrado e ponderado
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-3
Data Limite: No date

## 📝 Descricao
Construir G4 unificando todos os tipos de interacao e somando pesos por aresta.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/builder/graph4_integrated_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/base_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_builder.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-3.2, FEAT-3.3, FEAT-3.4, FEAT-3.5

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-3.6.1
Titulo: Combinar todos os tipos de interacao
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.6
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero agregar eventos elegiveis no G4, para obter visao integrada da colaboracao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph4_integrated_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph4_integrated_builder.py
Seguir padrao de: src/builder/graph4_integrated_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _sum_weight(self, current: float, increment: float) -> float

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
Arquivo: tests/test_builder.py
-> test_______3_6_1_cenario_feliz() - valida cenario 1.
-> test_______3_6_1_cenario_alternativo() - valida cenario 2.
-> test_______3_6_1_edge_case() - valida cenario 3.
-> test_______3_6_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.3.1, STORY-3.4.1, STORY-3.5.1]
- Importa de: src/builder/graph4_integrated_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.6.2
Titulo: Somar pesos em arestas repetidas
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.6
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero acumular peso por par src,dst, para representar intensidade de interacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph4_integrated_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph4_integrated_builder.py
Seguir padrao de: src/builder/graph4_integrated_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _sum_weight(self, current: float, increment: float) -> float

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
Arquivo: tests/test_builder.py
-> test_______3_6_2_cenario_feliz() - valida cenario 1.
-> test_______3_6_2_cenario_alternativo() - valida cenario 2.
-> test_______3_6_2_edge_case() - valida cenario 3.
-> test_______3_6_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.6.1]
- Importa de: src/builder/graph4_integrated_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

## CARD STORY-3.6.3
Titulo: Aplicar tabela oficial de pesos
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.6
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero mapear tipo para peso definido no README, para manter coerencia com criterios do trabalho.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### graph4_integrated_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph4_integrated_builder.py
Seguir padrao de: src/builder/graph4_integrated_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _sum_weight(self, current: float, increment: float) -> float

#### interaction_model.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/interaction_model.py
Seguir padrao de: src/mining/interaction_model.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> dataclass Interaction
-> __post_init__(self) -> None
-> to_row(self) -> dict[str, object]

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
Arquivo: tests/test_builder.py
-> test_______3_6_3_cenario_feliz() - valida cenario 1.
-> test_______3_6_3_cenario_alternativo() - valida cenario 2.
-> test_______3_6_3_edge_case() - valida cenario 3.
-> test_______3_6_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.2.2, STORY-3.6.1]
- Importa de: src/builder/graph4_integrated_builder.py, src/mining/interaction_model.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, builder, python, story

---

## CARD FEAT-3.7
Titulo: Testes dos builders
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-3
Data Limite: No date

## 📝 Descricao
Cobrir construcoes de G1, G2, G3 e G4 com fixtures sinteticas e validacao de contrato.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/tests/test_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/graph1_comments_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/graph2_closures_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/graph3_reviews_builder.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/builder/graph4_integrated_builder.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-3.3, FEAT-3.4, FEAT-3.5, FEAT-3.6

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-3.7.1
Titulo: Testar filtros por tipo em cada builder
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.7
Data Limite: No date

## 📝 Descricao
Como QA, eu quero validar entrada correta por builder, para evitar arestas indevidas nos grafos.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

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
Arquivo: tests/test_builder.py
-> test_______3_7_1_cenario_feliz() - valida cenario 1.
-> test_______3_7_1_cenario_alternativo() - valida cenario 2.
-> test_______3_7_1_edge_case() - valida cenario 3.
-> test_______3_7_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.3.1, STORY-3.4.1, STORY-3.5.1]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, testes, python, story

## CARD STORY-3.7.2
Titulo: Testar pesos e agregacao do G4
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.7
Data Limite: No date

## 📝 Descricao
Como QA, eu quero validar soma e mapa de pesos, para garantir fidelidade da analise integrada.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_builder.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_builder.py
Seguir padrao de: tests/test_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_builder()
-> test_filtro_por_tipo_interacao()
-> test_agregacao_pesos_g4()

#### graph4_integrated_builder.py (EXISTENTE - MODIFICAR)
Criar em: src/builder/graph4_integrated_builder.py
Seguir padrao de: src/builder/graph4_integrated_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]
-> _sum_weight(self, current: float, increment: float) -> float

## 🧪 Testes
Arquivo: tests/test_builder.py
-> test_______3_7_2_cenario_feliz() - valida cenario 1.
-> test_______3_7_2_cenario_alternativo() - valida cenario 2.
-> test_______3_7_2_edge_case() - valida cenario 3.
-> test_______3_7_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.6.2, STORY-3.6.3]
- Importa de: src/builder/graph4_integrated_builder.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, testes, python, story

## CARD STORY-3.7.3
Titulo: Testar exportacao de todos os grafos
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-3.7
Data Limite: No date

## 📝 Descricao
Como QA, eu quero verificar arquivos gexf de G1 a G4, para garantir entregavel visual pronto.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_builder.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_builder.py
Seguir padrao de: tests/test_builder.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_builder()
-> test_filtro_por_tipo_interacao()
-> test_agregacao_pesos_g4()

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
Arquivo: tests/test_builder.py
-> test_______3_7_3_cenario_feliz() - valida cenario 1.
-> test_______3_7_3_cenario_alternativo() - valida cenario 2.
-> test_______3_7_3_edge_case() - valida cenario 3.
-> test_______3_7_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-2.5.1, STORY-3.3.3, STORY-3.4.3, STORY-3.5.3]
- Importa de: src/graph/gephi_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --build - construcao de grafos G1..G4.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-3, testes, python, story

---
