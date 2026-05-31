# Documentacao da Frente 1 - Mineracao

Este documento explica o minerador implementado em `src/mining/` e o ponto de entrada em `src/app/main.py`. A ideia e ajudar o grupo a entender o fluxo, a responsabilidade de cada arquivo, quais dados sao coletados e como os CSVs finais sao montados.

## Visao Geral

O minerador coleta dados do repositorio `github/spec-kit` usando a biblioteca PyGithub. Ele gera tres arquivos em `data/raw/`:

- `users.csv`: lista de usuarios encontrados na mineracao.
- `interactions.csv`: interacoes usuario-usuario usadas pelos builders de grafos.
- `events.csv`: eventos brutos minerados, incluindo eventos que nao viram aresta de grafo diretamente.

O comando principal e:

```bash
python -m src.app.main --mine --repo github/spec-kit
```

Por padrao, se `--repo` nao for informado, o repositorio usado tambem e `github/spec-kit`.

## Configuracao

As dependencias ficam em `requirements.txt`:

```text
PyGithub
python-dotenv
pandas
tqdm
pytest
pytest-cov
```

O token do GitHub deve ficar em um arquivo `.env`, baseado em `.env.example`:

```env
GITHUB_TOKEN=seu_token_aqui
```

O token aumenta bastante o limite de requisicoes da API. Sem token, a mineracao pode funcionar em repositorios pequenos, mas tende a bater rate limit em mineracoes maiores.

Nunca versionar `.env` com token real.

## Fluxo Completo

O fluxo executado por `python -m src.app.main --mine` e:

1. Criar um `GitHubClient`.
2. Criar um `IssueMiner`.
3. Criar um `PRMiner`.
4. Minerar issues reais.
5. Minerar pull requests.
6. Juntar as interacoes dos dois miners.
7. Juntar os eventos brutos dos dois miners.
8. Gerar usuarios a partir de interacoes e eventos.
9. Exportar `users.csv`, `interactions.csv` e `events.csv`.

O arquivo que orquestra isso e `src/app/main.py`, principalmente a funcao `run_mining`.

## `github_client.py`

Arquivo responsavel por encapsular o acesso ao GitHub.

### Classe `GitHubClient`

A classe cria uma instancia do PyGithub e centraliza chamadas resilientes para a API.

Responsabilidades principais:

- Carregar variaveis do `.env` com `load_dotenv()`.
- Ler `GITHUB_TOKEN`.
- Criar o cliente `Github(token)` quando ha token.
- Criar o cliente anonimo `Github()` quando nao ha token.
- Buscar repositorios pelo nome completo.
- Reexecutar chamadas em caso de erro temporario.
- Esperar o reset do rate limit quando possivel.

### `__init__(token=None, sleep=time.sleep)`

Inicializa o cliente.

Se `token` for passado diretamente, usa esse valor. Caso contrario, busca `GITHUB_TOKEN` no ambiente.

O parametro `sleep` existe para facilitar testes. Nos testes, podemos substituir `time.sleep` por uma funcao fake e evitar esperar de verdade.

### `get_repo(full_name)`

Recebe uma string no formato:

```text
owner/repository
```

Exemplo:

```text
github/spec-kit
```

Se o formato nao tiver `/`, lanca `ValueError`. Depois chama a API real via:

```python
self.github.get_repo(repo_name)
```

Essa chamada passa por `request_with_retry`, entao tambem ganha retry e tratamento de falhas transitorias.

### `request_with_retry(op_name, operation, max_retries=5, base_delay=0.5)`

Executa uma operacao de API com retry.

`operation` e uma funcao sem argumentos. Exemplo:

```python
lambda: repo.get_issues(state="all")
```

Logica:

1. Tenta executar a operacao.
2. Se der certo, retorna o resultado.
3. Se falhar, verifica se o erro e retentavel.
4. Se nao for retentavel, relanca o erro.
5. Se for retentavel, calcula um tempo de espera.
6. Espera e tenta de novo.
7. Se exceder o numero maximo de tentativas, relanca o erro.

### `_is_retryable_error(error)`

Define quais erros podem ser tentados novamente.

Hoje considera retentavel:

- `RateLimitExceededException`.
- Status HTTP `403`, `429`, `500`, `502`, `503`, `504`.
- `TimeoutError`.
- `ConnectionError`.

Erros como entrada invalida, repositorio inexistente ou erro de programacao nao devem ser mascarados pelo retry.

### `_rate_limit_delay(error)`

Tenta calcular quanto tempo esperar quando a API informa rate limit.

Primeiro olha headers do erro:

- `x-ratelimit-remaining`
- `x-ratelimit-reset`

Se o GitHub informou que o limite restante e zero, espera ate o horario de reset, com uma folga de 1 segundo.

Se nao conseguir calcular, `request_with_retry` usa backoff exponencial com jitter.

## `interaction_model.py`

Arquivo com os modelos de dados internos da mineracao.

Existem dois modelos:

- `Interaction`: representa uma aresta potencial para os grafos.
- `MiningEvent`: representa um evento bruto coletado da API.

## Classe `Interaction`

Representa uma interacao usuario-usuario.

Campos:

```text
src_login,dst_login,type,weight,timestamp,source_id
```

Exemplo:

```csv
bob,alice,comment_issue,2,2026-01-15T12:00:00Z,42
```

Interpretacao:

- `bob` interagiu com `alice`.
- O tipo da interacao foi comentario em issue.
- Peso da interacao: `2`.
- A interacao veio da issue ou PR de numero `42`.

### Tipos permitidos de `Interaction`

```text
comment_issue
comment_pr
open_issue_commented
review_pr
merge_pr
close_issue
```

### Validacoes

No `__post_init__`, a classe garante:

- `src_login` nao pode ser vazio.
- `dst_login` nao pode ser vazio.
- `type` precisa estar na lista de tipos permitidos.
- `src_login` e `dst_login` nao podem ser iguais.
- `weight` precisa ser positivo.
- `timestamp` precisa existir.

Essa regra remove auto-interacoes, porque os grafos do trabalho nao aceitam lacos.

### `to_row()`

Converte a interacao para um dicionario pronto para virar linha de CSV.

## Classe `MiningEvent`

Representa um evento bruto minerado.

Nem todo evento vira uma aresta de grafo. Por exemplo, abrir um PR nao aponta naturalmente para outro usuario. Mesmo assim, o dado e importante para analise e auditoria da mineracao.

Campos:

```text
event_type,actor_login,target_login,source_kind,source_id,timestamp,state
```

Exemplo:

```csv
pr_opened,alice,,pull_request,120,2026-01-15T12:00:00Z,
```

### Tipos permitidos de `MiningEvent`

```text
issue_comment
issue_closed
pr_opened
pr_comment
pr_review
pr_approval
pr_merged
```

### Diferenca entre `Interaction` e `MiningEvent`

`Interaction` e para grafo:

- Tem origem e destino obrigatorios.
- Nao aceita auto-interacao.
- Tem peso.
- Alimenta `interactions.csv`.

`MiningEvent` e para registro bruto:

- Pode nao ter destino.
- Pode registrar eventos que nao viram aresta.
- Guarda estado de review quando existir.
- Alimenta `events.csv`.

## `issue_miner.py`

Arquivo responsavel por minerar issues.

### Ponto importante: Issues e Pull Requests compartilham a API

No GitHub, pull requests tambem aparecem na API de issues. Isso acontece porque todo PR tambem tem uma issue associada internamente.

Por isso, a chamada:

```python
repo.get_issues(state="all")
```

retorna:

```text
issues reais + pull requests
```

O minerador diferencia usando o atributo `pull_request`:

```python
if getattr(issue, "pull_request", None):
    continue
```

Se o item tem `pull_request`, ele e PR e e ignorado pelo `IssueMiner`.

### Classe `IssueMiner`

Recebe um `GitHubClient` no construtor.

Guarda tambem:

- `events`: lista de `MiningEvent` coletados.
- `stats`: estatisticas da varredura.

### `stats`

As estatisticas sao:

```text
scanned_items
mined_issues
skipped_pull_requests
```

Elas existem para evitar confusao entre:

- quantidade de itens retornados pela API de issues;
- quantidade real de issues mineradas;
- quantidade de PRs ignorados nessa etapa.

### `mine(repo_full_name)`

Fluxo:

1. Reseta `events` e `stats`.
2. Busca o repositorio.
3. Chama `repo.get_issues(state="all")` via retry.
4. Para cada item retornado:
   - incrementa `scanned_items`;
   - se for PR, incrementa `skipped_pull_requests` e pula;
   - se for issue real, incrementa `mined_issues`;
   - extrai interacoes e eventos da issue.

Retorna uma lista de `Interaction`.

Os eventos brutos ficam em `issue_miner.events`.

### `_extract_issue_interactions(issue)`

Extrai dados de uma issue real.

Primeiro identifica o autor:

```python
author = issue.user.login
```

Se a issue nao tiver autor, retorna lista vazia.

Depois coleta comentarios:

```python
issue.get_comments()
```

Para cada comentario:

- cria um evento `issue_comment`;
- cria uma interacao `comment_issue` de quem comentou para o autor da issue;
- cria uma interacao `open_issue_commented` do autor da issue para quem comentou.

Exemplo:

```text
alice abriu a issue
bob comentou
```

Eventos:

```text
issue_comment: bob comentou na issue de alice
```

Interacoes:

```text
bob -> alice: comment_issue, peso 2
alice -> bob: open_issue_commented, peso 3
```

Depois coleta eventos da issue:

```python
issue.get_events()
```

Filtra apenas eventos com:

```python
event.event == "closed"
```

Para cada fechamento:

- cria evento `issue_closed`;
- cria interacao `close_issue` de quem fechou para o autor da issue.

### `_should_skip_self_interaction(src_login, dst_login)`

Retorna `True` se:

- origem esta vazia;
- destino esta vazio;
- origem e destino sao o mesmo usuario.

Essa funcao evita criar arestas invalidas para os grafos.

## `pr_miner.py`

Arquivo responsavel por minerar pull requests.

### Classe `PRMiner`

Recebe um `GitHubClient` no construtor.

Guarda:

- `events`: lista de `MiningEvent` coletados em PRs.

### `mine(repo_full_name)`

Fluxo:

1. Reseta `events`.
2. Busca o repositorio.
3. Chama `repo.get_pulls(state="all")` via retry.
4. Para cada PR, chama `_extract_pr_interactions`.
5. Retorna uma lista de `Interaction`.

Os eventos brutos ficam em `pr_miner.events`.

### `_extract_pr_interactions(pr)`

Extrai dados de um PR.

Primeiro identifica o autor:

```python
author = pr.user.login
```

Se nao houver autor, retorna lista vazia.

### Abertura de PR

Assim que o PR e processado, registra:

```text
pr_opened
```

Esse evento vai para `events.csv`.

Ele nao vira `Interaction`, porque abertura de PR nao tem outro usuario como destino.

### Comentarios em PR

O minerador coleta dois tipos de comentarios:

```python
pr.get_issue_comments()
pr.get_review_comments()
```

`get_issue_comments()` pega comentarios gerais da conversa do PR.

`get_review_comments()` pega comentarios feitos em linhas de codigo durante review.

Para cada comentario:

- cria evento `pr_comment`;
- cria interacao `comment_pr` de quem comentou para o autor do PR, se nao for auto-interacao.

### Reviews e aprovacoes

O minerador chama:

```python
pr.get_reviews()
```

Para cada review, olha o estado:

```text
APPROVED
CHANGES_REQUESTED
COMMENTED
```

Esses estados viram interacao `review_pr`, com peso `4`.

Nos eventos brutos:

- `APPROVED` vira `pr_approval`;
- `CHANGES_REQUESTED` e `COMMENTED` viram `pr_review`.

O campo `state` em `events.csv` guarda o estado original da review.

### Merge de PR

O minerador verifica:

```python
pr.merged
pr.merged_by
pr.merged_at
```

Se o PR foi mergeado e existe usuario em `merged_by`, cria evento:

```text
pr_merged
```

Se quem mergeou nao e o proprio autor, cria tambem uma interacao:

```text
merge_pr
```

Peso da interacao: `5`.

Se o autor fez merge do proprio PR, o evento bruto ainda e registrado, mas a interacao nao e criada para evitar laco no grafo.

### `_map_review_type(review_state)`

Mapeia estados de review para tipo de interacao.

Retorna `review_pr` se o estado for:

```text
APPROVED
CHANGES_REQUESTED
COMMENTED
```

Caso contrario, retorna string vazia e nao gera interacao.

## `data_exporter.py`

Arquivo responsavel por exportar dados para CSV.

Usa `pandas` para criar os arquivos.

### Classe `DataExporter`

Define tres schemas oficiais.

### `USER_COLUMNS`

```text
login,user_id,name
```

Hoje `user_id` e `name` podem sair vazios, porque o minerador monta usuarios a partir dos logins vistos em interacoes e eventos.

### `INTERACTION_COLUMNS`

```text
src_login,dst_login,type,weight,timestamp,source_id
```

Esse CSV e o principal contrato com a frente de builders de grafos.

### `EVENT_COLUMNS`

```text
event_type,actor_login,target_login,source_kind,source_id,timestamp,state
```

Esse CSV guarda os eventos brutos adicionais da mineracao.

### `export_users_csv(users, output_path)`

Recebe lista de dicionarios de usuarios.

Logica:

1. Garante que o diretorio de saida existe.
2. Remove usuarios sem login.
3. Monta DataFrame.
4. Remove duplicatas por `login`.
5. Ordena por `login`.
6. Salva CSV sem indice.

### `export_interactions_csv(interactions, output_path)`

Recebe lista de `Interaction`.

Logica:

1. Converte cada `Interaction` com `to_row()`.
2. Monta DataFrame no schema oficial.
3. Remove linhas duplicadas.
4. Ordena por `source_id`, `type`, `src_login`, `dst_login`, `timestamp`.
5. Salva CSV.

### `export_events_csv(events, output_path)`

Recebe lista de `MiningEvent`.

Logica:

1. Converte cada evento com `to_row()`.
2. Monta DataFrame no schema oficial.
3. Remove duplicatas.
4. Ordena por `source_kind`, `source_id`, `event_type`, `timestamp`.
5. Salva CSV.

### `_ensure_output_dir(output_path)`

Cria o diretorio pai do CSV caso ele ainda nao exista.

Exemplo:

```text
data/raw
```

### `users_from_interactions(interactions, events=None)`

Cria uma lista minima de usuarios a partir de:

- origem e destino das interacoes;
- autores dos eventos;
- destinos dos eventos, quando existem.

Isso garante que usuarios que aparecem apenas em eventos brutos tambem entrem em `users.csv`.

## `main.py`

Arquivo de entrada da aplicacao.

### Constantes

```python
DEFAULT_REPOSITORY = "github/spec-kit"
DEFAULT_OUTPUT_DIR = Path("data/raw")
```

### `run_mining(repo, output_dir)`

Orquestra a mineracao inteira.

Passo a passo:

1. Cria `GitHubClient`.
2. Cria `IssueMiner`.
3. Cria `PRMiner`.
4. Executa `issue_miner.mine(repo)`.
5. Executa `pr_miner.mine(repo)`.
6. Junta interacoes.
7. Junta eventos.
8. Cria `DataExporter`.
9. Exporta `users.csv`.
10. Exporta `interactions.csv`.
11. Exporta `events.csv`.
12. Imprime estatisticas da varredura de issues.
13. Retorna os caminhos dos tres arquivos.

### `build_parser()`

Configura argumentos de linha de comando:

```text
--mine
--repo
--output-dir
```

### `main()`

Le argumentos.

Se `--mine` foi informado, roda a mineracao.

Se nao foi informado, mostra ajuda no terminal.

## CSVs Gerados

## `users.csv`

Schema:

```csv
login,user_id,name
```

Uso:

- Registrar usuarios vistos na mineracao.
- Servir de base para registry dos builders.

Observacao:

- `user_id` e `name` podem ficar vazios na versao atual.

## `interactions.csv`

Schema:

```csv
src_login,dst_login,type,weight,timestamp,source_id
```

Uso:

- Alimentar os grafos.
- Cada linha representa uma aresta dirigida potencial.

Tipos e pesos atuais:

```text
comment_issue           peso 2
comment_pr              peso 2
open_issue_commented    peso 3
review_pr               peso 4
merge_pr                peso 5
close_issue             peso 3
```

## `events.csv`

Schema:

```csv
event_type,actor_login,target_login,source_kind,source_id,timestamp,state
```

Uso:

- Guardar eventos brutos de mineracao.
- Permitir conferencias e analises que nao cabem diretamente no grafo.

Tipos atuais:

```text
issue_comment
issue_closed
pr_opened
pr_comment
pr_review
pr_approval
pr_merged
```

## Diferenca Entre Contar Issues e Contar Linhas

Um ponto importante: `interactions.csv` nao deve ser usado diretamente como "quantidade de issues".

Uma unica issue pode gerar varias linhas:

- comentario de usuario A;
- comentario de usuario B;
- interacao reversa `open_issue_commented`;
- fechamento.

Entao, para contar issues distintas a partir de `interactions.csv`, e preciso contar `source_id` unico apenas para tipos relacionados a issues:

```text
comment_issue
open_issue_commented
close_issue
```

Mesmo assim, a contagem mais confiavel de issues reais durante a execucao fica em:

```text
Issue scan: X issue-API items, Y real issues, Z pull requests skipped
```

Onde:

- `X` = itens retornados pela API de issues, incluindo PRs.
- `Y` = issues reais mineradas.
- `Z` = pull requests ignorados pelo `IssueMiner`.

## Por Que PRs Aparecem na API de Issues

No GitHub, issues e pull requests compartilham a sequencia de numeros.

Exemplo:

```text
Issue #120
Pull Request #121
Issue #122
```

Por isso, o numero da issue nao e uma contagem real de issues. Ele e apenas o identificador dentro da sequencia combinada de issues e PRs.

O minerador nao usa o numero para distinguir issue de PR. Ele usa o campo:

```python
pull_request
```

Se o item tem esse campo, e PR e nao deve ser minerado como issue.

## Testes

Os testes ficam em:

```text
tests/test_mining.py
```

Eles validam:

- cenario feliz de mineracao com mocks;
- filtro de PRs retornados pela API de issues;
- validacoes de `Interaction`;
- validacoes de `MiningEvent`;
- retry em erro temporario;
- exportacao idempotente dos CSVs;
- formato invalido de repositorio.

Comando:

```bash
python -m pytest tests/test_mining.py -q
```

Com cobertura:

```bash
python -m pytest tests/test_mining.py --cov=src.mining --cov-report=term-missing -q
```

## Pontos de Atencao

- `events.csv` e mais completo para auditoria da mineracao.
- `interactions.csv` e mais adequado para construir grafos.
- Auto-interacoes sao descartadas em `interactions.csv`, mas podem aparecer como eventos brutos quando fizer sentido registrar o acontecimento.
- O token do GitHub deve ficar apenas no `.env`.
- A API do GitHub pode retornar muitos itens; o retry ajuda, mas a mineracao ainda depende dos limites da conta/token.
- `source_id` e o numero da issue ou PR, nao uma contagem sequencial separada por tipo.

## Como Explicar Rapidamente Para a Turma

O minerador tem tres camadas:

1. `GitHubClient`: fala com o GitHub de forma autenticada e resiliente.
2. `IssueMiner` e `PRMiner`: transformam objetos da API em dados padronizados.
3. `DataExporter`: salva os dados finais em CSV.

O resultado tambem tem duas naturezas:

1. `interactions.csv`: dados prontos para virar grafo.
2. `events.csv`: log estruturado dos eventos minerados.

Essa separacao evita forcar todo evento do GitHub a virar uma aresta de grafo, mas ainda preserva os dados importantes para analise.
