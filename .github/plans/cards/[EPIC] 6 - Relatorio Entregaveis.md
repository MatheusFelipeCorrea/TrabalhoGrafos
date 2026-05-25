# [EPIC] 6 - Relatorio Entregaveis

## CARD EPIC-6 - Frente 6 - Relatorio Entregaveis
Tipo: Epic
Prioridade: 🔺 Highest
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): -
Data Limite: No date

## 📝 Descricao
Consolidar relatorio, video e preparacao final da apresentacao conforme requisitos da disciplina.

## ✅ Criterios de Aceite
- Todas as features e stories do epic implementadas.
- Cobertura de testes da frente entre 90% e 95%.
- Integracao com outras frentes sem quebra de contrato.

## 🚫 Regras de Negocio
- Seguir estritamente o enunciado do trabalho e restricoes tecnicas.

---

## CARD FEAT-6.1
Titulo: Relatorio SBC em LaTeX
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 8
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-6
Data Limite: No date

## 📝 Descricao
Consolidar metodologia, resultados e discussao no template SBC.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/report/main.tex (EXISTENTE - MODIFICAR)
- github-graph-analyzer/report/refs.bib (EXISTENTE - MODIFICAR)
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
- Dependencias: FEAT-4.4, FEAT-5.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-6.1.1
Titulo: Descrever modelagem dos grafos G1..G4
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.1
Data Limite: No date

## 📝 Descricao
Como autor do relatorio, eu quero explicar vertices, arestas e pesos, para demonstrar aderencia teorica ao trabalho.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.tex (EXISTENTE - MODIFICAR)
Criar em: report/main.tex
Seguir padrao de: report/main.tex
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> section_metodologia() -> str
-> section_resultados() -> str
-> section_conclusao() -> str

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_1_1_cenario_feliz() - valida cenario 1.
-> test_______6_1_1_cenario_alternativo() - valida cenario 2.
-> test_______6_1_1_edge_case() - valida cenario 3.
-> test_______6_1_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-3.6.3]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, relatorio, python, story

## CARD STORY-6.1.2
Titulo: Descrever arquitetura por frentes
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.1
Data Limite: No date

## 📝 Descricao
Como autor do relatorio, eu quero documentar fluxo F1-F4 e app, para evidenciar organizacao e responsabilidades.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.tex (EXISTENTE - MODIFICAR)
Criar em: report/main.tex
Seguir padrao de: report/main.tex
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> section_metodologia() -> str
-> section_resultados() -> str
-> section_conclusao() -> str

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_1_2_cenario_feliz() - valida cenario 1.
-> test_______6_1_2_cenario_alternativo() - valida cenario 2.
-> test_______6_1_2_edge_case() - valida cenario 3.
-> test_______6_1_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-5.2.3]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, relatorio, python, story

## CARD STORY-6.1.3
Titulo: Inserir resultados de centralidade e estrutura
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.1
Data Limite: No date

## 📝 Descricao
Como autor do relatorio, eu quero apresentar tabelas e analise critica, para sustentar conclusoes com dados.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.tex (EXISTENTE - MODIFICAR)
Criar em: report/main.tex
Seguir padrao de: report/main.tex
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> section_metodologia() -> str
-> section_resultados() -> str
-> section_conclusao() -> str

####  (EXISTENTE - MODIFICAR)
Criar em: output/reports/
Seguir padrao de: output/reports/
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> Atualizar a secao correspondente com evidencias tecnicas reais da entrega
-> Referenciar artefatos de saida (graficos, relatorios, video) de forma rastreavel
-> Revisar ortografia, clareza e consistencia terminologica antes da submissao

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_1_3_cenario_feliz() - valida cenario 1.
-> test_______6_1_3_cenario_alternativo() - valida cenario 2.
-> test_______6_1_3_edge_case() - valida cenario 3.
-> test_______6_1_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-4.4.1, STORY-4.4.2]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 3
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, relatorio, python, story

---

## CARD FEAT-6.2
Titulo: Video de demonstracao
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-6
Data Limite: No date

## 📝 Descricao
Produzir roteiro e gravacao da execucao do pipeline e leitura dos resultados.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/report/main.tex (EXISTENTE - MODIFICAR)
- github-graph-analyzer/output/graphs/ (EXISTENTE - MODIFICAR)
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
- Dependencias: FEAT-5.1, FEAT-5.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-6.2.1
Titulo: Definir roteiro de demonstracao
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.2
Data Limite: No date

## 📝 Descricao
Como apresentador, eu quero mostrar fluxo completo em ordem correta, para evitar omissao de requisito na avaliacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.tex (EXISTENTE - MODIFICAR)
Criar em: report/main.tex
Seguir padrao de: report/main.tex
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> section_metodologia() -> str
-> section_resultados() -> str
-> section_conclusao() -> str

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_2_1_cenario_feliz() - valida cenario 1.
-> test_______6_2_1_cenario_alternativo() - valida cenario 2.
-> test_______6_2_1_edge_case() - valida cenario 3.
-> test_______6_2_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-5.1.3, STORY-5.2.3]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, entrega, python, story

## CARD STORY-6.2.2
Titulo: Gravar execucao do pipeline
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 2
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.2
Data Limite: No date

## 📝 Descricao
Como apresentador, eu quero capturar mine, build, analyze e demo, para provar funcionamento ponta a ponta.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

####  (EXISTENTE - MODIFICAR)
Criar em: output/graphs/
Seguir padrao de: output/graphs/
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> Atualizar a secao correspondente com evidencias tecnicas reais da entrega
-> Referenciar artefatos de saida (graficos, relatorios, video) de forma rastreavel
-> Revisar ortografia, clareza e consistencia terminologica antes da submissao

####  (EXISTENTE - MODIFICAR)
Criar em: output/reports/
Seguir padrao de: output/reports/
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> Atualizar a secao correspondente com evidencias tecnicas reais da entrega
-> Referenciar artefatos de saida (graficos, relatorios, video) de forma rastreavel
-> Revisar ortografia, clareza e consistencia terminologica antes da submissao

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_2_2_cenario_feliz() - valida cenario 1.
-> test_______6_2_2_cenario_alternativo() - valida cenario 2.
-> test_______6_2_2_edge_case() - valida cenario 3.
-> test_______6_2_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-5.2.3]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 2
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, entrega, python, story

## CARD STORY-6.2.3
Titulo: Validar legibilidade tecnica do video
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.2
Data Limite: No date

## 📝 Descricao
Como QA de entrega, eu quero confirmar audio, texto e evidencias, para maximizar clareza e pontuacao da apresentacao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.tex (EXISTENTE - MODIFICAR)
Criar em: report/main.tex
Seguir padrao de: report/main.tex
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> section_metodologia() -> str
-> section_resultados() -> str
-> section_conclusao() -> str

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_2_3_cenario_feliz() - valida cenario 1.
-> test_______6_2_3_cenario_alternativo() - valida cenario 2.
-> test_______6_2_3_edge_case() - valida cenario 3.
-> test_______6_2_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-6.2.2]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, entrega, python, story

---

## CARD FEAT-6.3
Titulo: Preparacao para apresentacao presencial
Tipo: Feature
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 3
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): EPIC-6
Data Limite: No date

## 📝 Descricao
Organizar checklist final de entrega, riscos e perguntas esperadas da banca.

## 🎯 Escopo Funcional
Arquivos impactados:
- github-graph-analyzer/report/main.tex (EXISTENTE - MODIFICAR)
- github-graph-analyzer/README.md (EXISTENTE - MODIFICAR)
- github-graph-analyzer/github-graph-analyzer/README.MD (EXISTENTE - MODIFICAR)

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
- Dependencias: FEAT-6.1, FEAT-6.2

## 🚫 Regras de Negocio
- Seguir enunciado da disciplina e contratos entre frentes.

## 📌 Observacoes
- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.

## CARD STORY-6.3.1
Titulo: Montar checklist tecnico final
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.3
Data Limite: No date

## 📝 Descricao
Como lider tecnico, eu quero confirmar requisitos e restricoes atendidos, para evitar perda de pontos por item faltante.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### README.md (EXISTENTE - MODIFICAR)
Criar em: README.md
Seguir padrao de: README.md
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> Atualizar a secao correspondente com evidencias tecnicas reais da entrega
-> Referenciar artefatos de saida (graficos, relatorios, video) de forma rastreavel
-> Revisar ortografia, clareza e consistencia terminologica antes da submissao

#### README.MD (EXISTENTE - MODIFICAR)
Criar em: github-graph-analyzer/README.MD
Seguir padrao de: github-graph-analyzer/README.MD
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> Atualizar a secao correspondente com evidencias tecnicas reais da entrega
-> Referenciar artefatos de saida (graficos, relatorios, video) de forma rastreavel
-> Revisar ortografia, clareza e consistencia terminologica antes da submissao

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_3_1_cenario_feliz() - valida cenario 1.
-> test_______6_3_1_cenario_alternativo() - valida cenario 2.
-> test_______6_3_1_edge_case() - valida cenario 3.
-> test_______6_3_1_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-6.1.3]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, entrega, python, story

## CARD STORY-6.3.2
Titulo: Mapear perguntas provaveis e respostas
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.3
Data Limite: No date

## 📝 Descricao
Como lider tecnico, eu quero preparar defesa da implementacao, para melhorar desempenho na arguicao.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.tex (EXISTENTE - MODIFICAR)
Criar em: report/main.tex
Seguir padrao de: report/main.tex
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> section_metodologia() -> str
-> section_resultados() -> str
-> section_conclusao() -> str

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_3_2_cenario_feliz() - valida cenario 1.
-> test_______6_3_2_cenario_alternativo() - valida cenario 2.
-> test_______6_3_2_edge_case() - valida cenario 3.
-> test_______6_3_2_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-6.3.1]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, entrega, python, story

## CARD STORY-6.3.3
Titulo: Executar dry-run da apresentacao
Tipo: Story
Prioridade: 🔼 High
Numero da Sprint: Choose an iteration
Story Points: 1
Categoria: Choose an option
Relator: Matheus Felipe Correa
Pai (Epic/Feature): FEAT-6.3
Data Limite: No date

## 📝 Descricao
Como equipe, eu quero simular tempo e transicoes, para reduzir risco de falha na banca.

## ✅ Criterios de Aceite
**Cenario 1 - Fluxo principal**
Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.

**Cenario 2 - Integracao entre modulos**
Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.

**Cenario 3 - Edge case de erro**
Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.

## 🛠️ Implementacao

#### main.tex (EXISTENTE - MODIFICAR)
Criar em: report/main.tex
Seguir padrao de: report/main.tex
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> section_metodologia() -> str
-> section_resultados() -> str
-> section_conclusao() -> str

#### README.md (EXISTENTE - MODIFICAR)
Criar em: README.md
Seguir padrao de: README.md
Logica existente (NAO alterar):
-> Contrato atual do modulo e assinatura publica ja definida no backlog.
Logica NOVA a adicionar:
-> Atualizar a secao correspondente com evidencias tecnicas reais da entrega
-> Referenciar artefatos de saida (graficos, relatorios, video) de forma rastreavel
-> Revisar ortografia, clareza e consistencia terminologica antes da submissao

## 🧪 Testes
Arquivo: tests/test_analysis.py
-> test_______6_3_3_cenario_feliz() - valida cenario 1.
-> test_______6_3_3_cenario_alternativo() - valida cenario 2.
-> test_______6_3_3_edge_case() - valida cenario 3.
-> test_______6_3_3_idempotencia_ou_invariante() - valida invariante tecnica da story.
Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.
Cobertura minima: 90% para modulo alterado e 80% global da frente.

## 🔗 Dependencias
- Bloqueia: [A definir no planejamento da sprint]
- Bloqueado por: [STORY-6.2.3, STORY-6.3.2]
- Importa de: N/A
- E importado por: camadas da mesma frente e src/app/main.py

## 🛣️ Endpoints / CLI / API Publica
- Documento tecnico em report/main.tex e entrega final da disciplina.

## ⚠️ Edge Cases e Excecoes
- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.
- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.

## ⏱️ Estimativa
Story Points: 1
Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.

## 🏷️ Labels
frente-6, entrega, python, story

---
