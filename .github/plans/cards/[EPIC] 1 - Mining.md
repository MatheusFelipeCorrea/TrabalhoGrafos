# [EPIC] 1 - Mining

## CARD EPIC-1 - Frente 1 - Mining
Tipo: Epic
Prioridade: 🔺 Highest
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): -
Data Limite: No date

## 📝 Descricao
Implementar coleta robusta no github/spec-kit com autenticacao, resiliencia e exportacao CSV para as demais frentes.
Stack obrigatoria da mineracao: PyGithub, python-dotenv, pandas e tqdm.

## ✅ Criterios de Aceite
- Todas as features e stories do epic implementadas.
- Cobertura de testes da frente entre 90% e 95%.
- Integracao com outras frentes sem quebra de contrato.

## 🚫 Regras de Negocio
- Seguir estritamente o enunciado do trabalho e restricoes tecnicas.
- O minerador nao pode falhar por erro transitorio; deve ter retry, backoff e retomada segura.

---

## CARD FEAT-1.1
Titulo: Cliente GitHub autenticado e resiliente
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-1
Data Limite: No date

## 📝 Descricao
Implementar cliente de acesso ao GitHub com autenticacao, tratamento de rate limit e retry seguro.
Biblioteca principal desta feature: PyGithub.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/mining/github_client.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/.env.example (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_mining.py (EXISTENTE - MODIFICAR)

## ✅ Criterios de Aceite
- Fluxos da feature implementados com consistencia funcional e tecnica.
- Integracao validada com camadas adjacentes.
- Erros de entrada e falhas transitorias tratados de forma resiliente.

## 🛠️ Implementacao (Alto Nivel)
- Definir contrato publico da feature e metodos internos.
- Integrar com modulos dependentes sem quebrar API existente.
- Escrever testes cobrindo cenario feliz, alternativo e edge case.
- Dependencias Python da frente: `pip install PyGithub python-dotenv pandas tqdm`.

## ✅ Definicao de Pronto (DoD)
- [ ] Stories da feature concluidas e revisadas.
- [ ] Cobertura da frente entre 90% e 95%.
- [ ] Documentacao tecnica atualizada.

## 🔗 Dependencias
- Dependencias: nenhuma

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.
- O minerador nao pode falhar por erros transitorios.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-1.1.1
Titulo: Carregar token GitHub via ambiente
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.1
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero carregar GITHUB_TOKEN por ambiente, para evitar credencial hardcoded e falhas de autenticacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### github_client.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/github_client.py
Seguir padrao de: src/mining/github_client.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> get_repo(self, full_name: str) -> Repository
-> request_with_retry(self, op_name: str, operation: callable, max_retries: int = 5, base_delay: float = 0.5) -> object
-> _is_retryable_error(self, error: Exception) -> bool

#### .env.example (EXISTENTE - MODIFICAR)
Criar em: .env.example
Seguir padrao de: .env.example
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> Definir GITHUB_TOKEN= no exemplo de ambiente
-> Incluir comentario sobre nao versionar credenciais reais
-> Manter formato compativel com python-dotenv

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
Arquivo: tests/test_mining.py
-> test_______1_1_1_cenario_feliz() - valida cenario 1.
-> test_______1_1_1_cenario_alternativo() - valida cenario 2.
-> test_______1_1_1_edge_case() - valida cenario 3.
-> test_______1_1_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: nenhuma
- Importa de: src/mining/github_client.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.1.2
Titulo: Tratar rate limit com espera segura
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.1
Data Limite: No date

## 📝 Descricao
Como minerador, eu quero detectar e esperar reset de limite, para evitar quebra do pipeline por limites da API.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

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
Arquivo: tests/test_mining.py
-> test_______1_1_2_cenario_feliz() - valida cenario 1.
-> test_______1_1_2_cenario_alternativo() - valida cenario 2.
-> test_______1_1_2_edge_case() - valida cenario 3.
-> test_______1_1_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.1.1]
- Importa de: src/mining/github_client.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.1.3
Titulo: Aplicar retry exponencial com jitter
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.1
Data Limite: No date

## 📝 Descricao
Como minerador, eu quero retentar falhas transitorias, para aumentar estabilidade da mineracao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

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
Arquivo: tests/test_mining.py
-> test_______1_1_3_cenario_feliz() - valida cenario 1.
-> test_______1_1_3_cenario_alternativo() - valida cenario 2.
-> test_______1_1_3_edge_case() - valida cenario 3.
-> test_______1_1_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.1.1, STORY-1.1.2]
- Importa de: src/mining/github_client.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

---

## CARD FEAT-1.2
Titulo: Modelo padrao de interacao entre usuarios
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-1
Data Limite: No date

## 📝 Descricao
Definir contrato unico de interacao para consumo por builders e analise.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/mining/interaction_model.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_mining.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-1.1

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.
- O minerador nao pode falhar por erros transitorios.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-1.2.1
Titulo: Criar dataclass Interaction
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero padronizar estrutura de interacao, para garantir contrato claro entre frentes.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### interaction_model.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/interaction_model.py
Seguir padrao de: src/mining/interaction_model.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> dataclass Interaction
-> __post_init__(self) -> None
-> to_row(self) -> dict[str, object]

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
Arquivo: tests/test_mining.py
-> test_______1_2_1_cenario_feliz() - valida cenario 1.
-> test_______1_2_1_cenario_alternativo() - valida cenario 2.
-> test_______1_2_1_edge_case() - valida cenario 3.
-> test_______1_2_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.1.1]
- Importa de: src/mining/interaction_model.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.2.2
Titulo: Validar tipo de interacao permitido
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero aceitar apenas tipos previstos no trabalho, para evitar dados inconsistentes no CSV.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### interaction_model.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/interaction_model.py
Seguir padrao de: src/mining/interaction_model.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> dataclass Interaction
-> __post_init__(self) -> None
-> to_row(self) -> dict[str, object]

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
Arquivo: tests/test_mining.py
-> test_______1_2_2_cenario_feliz() - valida cenario 1.
-> test_______1_2_2_cenario_alternativo() - valida cenario 2.
-> test_______1_2_2_edge_case() - valida cenario 3.
-> test_______1_2_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.2.1]
- Importa de: src/mining/interaction_model.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.2.3
Titulo: Normalizar payload para exportacao
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.2
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero converter interacao para linha csv estavel, para facilitar build e analise sem transformacoes extras.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### interaction_model.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/interaction_model.py
Seguir padrao de: src/mining/interaction_model.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> dataclass Interaction
-> __post_init__(self) -> None
-> to_row(self) -> dict[str, object]

#### data_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/data_exporter.py
Seguir padrao de: src/mining/data_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export_users_csv(self, users: list[dict], output_path: str) -> str
-> export_interactions_csv(self, interactions: list[Interaction], output_path: str) -> str
-> _ensure_output_dir(self, output_path: str) -> None

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
Arquivo: tests/test_mining.py
-> test_______1_2_3_cenario_feliz() - valida cenario 1.
-> test_______1_2_3_cenario_alternativo() - valida cenario 2.
-> test_______1_2_3_edge_case() - valida cenario 3.
-> test_______1_2_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.2.1]
- Importa de: src/mining/data_exporter.py, src/mining/interaction_model.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

---

## CARD FEAT-1.3
Titulo: Mineracao de Issues e eventos relacionados
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-1
Data Limite: No date

## 📝 Descricao
Coletar issues, comentarios e fechamentos em formato de interacao.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/mining/issue_miner.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/mining/github_client.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_mining.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-1.1, FEAT-1.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.
- O minerador nao pode falhar por erros transitorios.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-1.3.1
Titulo: Coletar autores e comentarios de issues
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.3
Data Limite: No date

## 📝 Descricao
Como analista de dados, eu quero extrair interacoes de comentarios em issues, para alimentar G1 e G4 com dados corretos.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### issue_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/issue_miner.py
Seguir padrao de: src/mining/issue_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_issue_interactions(self, issue: object) -> list[Interaction]
-> _should_skip_self_interaction(self, src_login: str, dst_login: str) -> bool

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
Arquivo: tests/test_mining.py
-> test_______1_3_1_cenario_feliz() - valida cenario 1.
-> test_______1_3_1_cenario_alternativo() - valida cenario 2.
-> test_______1_3_1_edge_case() - valida cenario 3.
-> test_______1_3_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.1.1, STORY-1.2.1]
- Importa de: src/mining/issue_miner.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.3.2
Titulo: Coletar eventos de fechamento de issue
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.3
Data Limite: No date

## 📝 Descricao
Como analista de dados, eu quero mapear quem fechou issue de quem, para alimentar G2 corretamente.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### issue_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/issue_miner.py
Seguir padrao de: src/mining/issue_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_issue_interactions(self, issue: object) -> list[Interaction]
-> _should_skip_self_interaction(self, src_login: str, dst_login: str) -> bool

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
Arquivo: tests/test_mining.py
-> test_______1_3_2_cenario_feliz() - valida cenario 1.
-> test_______1_3_2_cenario_alternativo() - valida cenario 2.
-> test_______1_3_2_edge_case() - valida cenario 3.
-> test_______1_3_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.3.1]
- Importa de: src/mining/issue_miner.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.3.3
Titulo: Descartar auto interacao em issues
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.3
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero ignorar src==dst, para respeitar restricao de grafo simples.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### issue_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/issue_miner.py
Seguir padrao de: src/mining/issue_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_issue_interactions(self, issue: object) -> list[Interaction]
-> _should_skip_self_interaction(self, src_login: str, dst_login: str) -> bool

#### interaction_model.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/interaction_model.py
Seguir padrao de: src/mining/interaction_model.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> dataclass Interaction
-> __post_init__(self) -> None
-> to_row(self) -> dict[str, object]

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
Arquivo: tests/test_mining.py
-> test_______1_3_3_cenario_feliz() - valida cenario 1.
-> test_______1_3_3_cenario_alternativo() - valida cenario 2.
-> test_______1_3_3_edge_case() - valida cenario 3.
-> test_______1_3_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.2.1]
- Importa de: src/mining/interaction_model.py, src/mining/issue_miner.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

---

## CARD FEAT-1.4
Titulo: Mineracao de Pull Requests e Reviews
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-1
Data Limite: No date

## 📝 Descricao
Coletar PRs, reviews, comentarios e merges para compor G3 e G4.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/mining/pr_miner.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/mining/github_client.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_mining.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-1.1, FEAT-1.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.
- O minerador nao pode falhar por erros transitorios.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-1.4.1
Titulo: Extrair reviews e estados de aprovacao
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.4
Data Limite: No date

## 📝 Descricao
Como analista de dados, eu quero capturar reviews de PR, para calcular peso correto de review no G3/G4.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### pr_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/pr_miner.py
Seguir padrao de: src/mining/pr_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_pr_interactions(self, pr: object) -> list[Interaction]
-> _map_review_type(self, review_state: str) -> str

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
Arquivo: tests/test_mining.py
-> test_______1_4_1_cenario_feliz() - valida cenario 1.
-> test_______1_4_1_cenario_alternativo() - valida cenario 2.
-> test_______1_4_1_edge_case() - valida cenario 3.
-> test_______1_4_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.1.1, STORY-1.2.1]
- Importa de: src/mining/pr_miner.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.4.2
Titulo: Extrair merges e autor de PR
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.4
Data Limite: No date

## 📝 Descricao
Como analista de dados, eu quero capturar evento de merge, para alimentar peso de merge no G3/G4.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### pr_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/pr_miner.py
Seguir padrao de: src/mining/pr_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_pr_interactions(self, pr: object) -> list[Interaction]
-> _map_review_type(self, review_state: str) -> str

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
Arquivo: tests/test_mining.py
-> test_______1_4_2_cenario_feliz() - valida cenario 1.
-> test_______1_4_2_cenario_alternativo() - valida cenario 2.
-> test_______1_4_2_edge_case() - valida cenario 3.
-> test_______1_4_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.4.1]
- Importa de: src/mining/pr_miner.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.4.3
Titulo: Classificar comentario de PR e review
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.4
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero diferenciar tipos de interacao, para evitar peso incorreto no grafo integrado.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### pr_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/pr_miner.py
Seguir padrao de: src/mining/pr_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_pr_interactions(self, pr: object) -> list[Interaction]
-> _map_review_type(self, review_state: str) -> str

#### interaction_model.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/interaction_model.py
Seguir padrao de: src/mining/interaction_model.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> dataclass Interaction
-> __post_init__(self) -> None
-> to_row(self) -> dict[str, object]

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
Arquivo: tests/test_mining.py
-> test_______1_4_3_cenario_feliz() - valida cenario 1.
-> test_______1_4_3_cenario_alternativo() - valida cenario 2.
-> test_______1_4_3_edge_case() - valida cenario 3.
-> test_______1_4_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.2.2]
- Importa de: src/mining/interaction_model.py, src/mining/pr_miner.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

---

## CARD FEAT-1.5
Titulo: Exportacao de datasets CSV padronizados
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-1
Data Limite: No date

## 📝 Descricao
Exportar users.csv e interactions.csv no schema oficial do projeto.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/src/mining/data_exporter.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/tests/test_mining.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-1.2, FEAT-1.3, FEAT-1.4

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.
- O minerador nao pode falhar por erros transitorios.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-1.5.1
Titulo: Exportar users.csv com colunas obrigatorias
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero gerar arquivo users.csv estavel, para permitir indexacao consistente no builder.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### data_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/data_exporter.py
Seguir padrao de: src/mining/data_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export_users_csv(self, users: list[dict], output_path: str) -> str
-> export_interactions_csv(self, interactions: list[Interaction], output_path: str) -> str
-> _ensure_output_dir(self, output_path: str) -> None

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
Arquivo: tests/test_mining.py
-> test_______1_5_1_cenario_feliz() - valida cenario 1.
-> test_______1_5_1_cenario_alternativo() - valida cenario 2.
-> test_______1_5_1_edge_case() - valida cenario 3.
-> test_______1_5_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.2.1]
- Importa de: src/mining/data_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.5.2
Titulo: Exportar interactions.csv com schema oficial
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero gerar interactions.csv padrao, para evitar quebra de leitura no builder.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### data_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/data_exporter.py
Seguir padrao de: src/mining/data_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export_users_csv(self, users: list[dict], output_path: str) -> str
-> export_interactions_csv(self, interactions: list[Interaction], output_path: str) -> str
-> _ensure_output_dir(self, output_path: str) -> None

#### interaction_model.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/interaction_model.py
Seguir padrao de: src/mining/interaction_model.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> dataclass Interaction
-> __post_init__(self) -> None
-> to_row(self) -> dict[str, object]

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
Arquivo: tests/test_mining.py
-> test_______1_5_2_cenario_feliz() - valida cenario 1.
-> test_______1_5_2_cenario_alternativo() - valida cenario 2.
-> test_______1_5_2_edge_case() - valida cenario 3.
-> test_______1_5_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.2.3, STORY-1.3.1, STORY-1.4.1]
- Importa de: src/mining/data_exporter.py, src/mining/interaction_model.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

## CARD STORY-1.5.3
Titulo: Garantir exportacao idempotente de arquivos
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.5
Data Limite: No date

## 📝 Descricao
Como desenvolvedor, eu quero reexecutar export sem duplicar linhas, para assegurar pipeline repetivel.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### data_exporter.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/data_exporter.py
Seguir padrao de: src/mining/data_exporter.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> export_users_csv(self, users: list[dict], output_path: str) -> str
-> export_interactions_csv(self, interactions: list[Interaction], output_path: str) -> str
-> _ensure_output_dir(self, output_path: str) -> None

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
Arquivo: tests/test_mining.py
-> test_______1_5_3_cenario_feliz() - valida cenario 1.
-> test_______1_5_3_cenario_alternativo() - valida cenario 2.
-> test_______1_5_3_edge_case() - valida cenario 3.
-> test_______1_5_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.5.1, STORY-1.5.2]
- Importa de: src/mining/data_exporter.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, mining, python, story

---

## CARD FEAT-1.6
Titulo: Testes da camada de mineracao
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 5
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-1
Data Limite: No date

## 📝 Descricao
Cobrir mineracao com cenarios de sucesso, erro e resiliencia para 90-95%.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/tests/test_mining.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/mining/github_client.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/mining/issue_miner.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/mining/pr_miner.py (EXISTENTE - MODIFICAR)
- github-graph-analyzer/src/mining/data_exporter.py (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-1.1, FEAT-1.2, FEAT-1.3, FEAT-1.4, FEAT-1.5

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.
- O minerador nao pode falhar por erros transitorios.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-1.6.1
Titulo: Testar autenticacao e configuracao de ambiente
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.6
Data Limite: No date

## 📝 Descricao
Como QA, eu quero validar token presente, ausente e invalido, para garantir bootstrap confiavel do minerador.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_mining.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_mining.py
Seguir padrao de: tests/test_mining.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_mining()
-> test_edge_case_mining()
-> test_resiliencia_retry_rate_limit()

#### github_client.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/github_client.py
Seguir padrao de: src/mining/github_client.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> get_repo(self, full_name: str) -> Repository
-> request_with_retry(self, op_name: str, operation: callable, max_retries: int = 5, base_delay: float = 0.5) -> object
-> _is_retryable_error(self, error: Exception) -> bool

## 🧪 Testes
Arquivo: tests/test_mining.py
-> test_______1_6_1_cenario_feliz() - valida cenario 1.
-> test_______1_6_1_cenario_alternativo() - valida cenario 2.
-> test_______1_6_1_edge_case() - valida cenario 3.
-> test_______1_6_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.1.1]
- Importa de: src/mining/github_client.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, testes, python, story

## CARD STORY-1.6.2
Titulo: Testar fluxo de issues e PRs com mocks
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.6
Data Limite: No date

## 📝 Descricao
Como QA, eu quero simular API do GitHub sem chamadas reais, para garantir comportamento deterministico em CI.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_mining.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_mining.py
Seguir padrao de: tests/test_mining.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_mining()
-> test_edge_case_mining()
-> test_resiliencia_retry_rate_limit()

#### issue_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/issue_miner.py
Seguir padrao de: src/mining/issue_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_issue_interactions(self, issue: object) -> list[Interaction]
-> _should_skip_self_interaction(self, src_login: str, dst_login: str) -> bool

#### pr_miner.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/pr_miner.py
Seguir padrao de: src/mining/pr_miner.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> mine(self, repo_full_name: str) -> list[Interaction]
-> _extract_pr_interactions(self, pr: object) -> list[Interaction]
-> _map_review_type(self, review_state: str) -> str

## 🧪 Testes
Arquivo: tests/test_mining.py
-> test_______1_6_2_cenario_feliz() - valida cenario 1.
-> test_______1_6_2_cenario_alternativo() - valida cenario 2.
-> test_______1_6_2_edge_case() - valida cenario 3.
-> test_______1_6_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.3.1, STORY-1.4.1]
- Importa de: src/mining/issue_miner.py, src/mining/pr_miner.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, testes, python, story

## CARD STORY-1.6.3
Titulo: Testar resiliencia completa do minerador
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-1.6
Data Limite: No date

## 📝 Descricao
Como QA, eu quero validar retry e rate limit ponta a ponta, para evitar falha em producao por erros transitorios.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### test_mining.py (EXISTENTE - MODIFICAR)
Criar em: tests/test_mining.py
Seguir padrao de: tests/test_mining.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> test_cenario_feliz_mining()
-> test_edge_case_mining()
-> test_resiliencia_retry_rate_limit()

#### github_client.py (EXISTENTE - MODIFICAR)
Criar em: src/mining/github_client.py
Seguir padrao de: src/mining/github_client.py
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> get_repo(self, full_name: str) -> Repository
-> request_with_retry(self, op_name: str, operation: callable, max_retries: int = 5, base_delay: float = 0.5) -> object
-> _is_retryable_error(self, error: Exception) -> bool

## 🧪 Testes
Arquivo: tests/test_mining.py
-> test_______1_6_3_cenario_feliz() - valida cenario 1.
-> test_______1_6_3_cenario_alternativo() - valida cenario 2.
-> test_______1_6_3_edge_case() - valida cenario 3.
-> test_______1_6_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-1.1.2, STORY-1.1.3]
- Importa de: src/mining/github_client.py
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- python -m src.app.main --mine - executa mineracao resiliente.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.
- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-1, testes, python, story

---
