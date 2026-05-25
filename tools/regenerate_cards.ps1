Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$NL = [Environment]::NewLine

function Get-TestFile {
    param([string]$epicId)
    switch ($epicId) {
        '1' { 'tests/test_mining.py' }
        '2' { 'tests/test_graph_matrix.py' }
        '3' { 'tests/test_builder.py' }
        '4' { 'tests/test_analysis.py' }
        '5' { 'tests/test_analysis.py' }
        default { 'tests/test_analysis.py' }
    }
}

function Get-MethodHints {
    param([string]$path)
    switch -Regex ($path) {
        'src/mining/github_client.py' { @('-> get_repo(self, full_name: str) -> Repository','-> request_with_retry(self, op_name: str, operation: callable, max_retries: int = 5, base_delay: float = 0.5) -> object','-> _is_retryable_error(self, error: Exception) -> bool') }
        'src/mining/issue_miner.py' { @('-> mine(self, repo_full_name: str) -> list[Interaction]','-> _extract_issue_interactions(self, issue: object) -> list[Interaction]','-> _should_skip_self_interaction(self, src_login: str, dst_login: str) -> bool') }
        'src/mining/pr_miner.py' { @('-> mine(self, repo_full_name: str) -> list[Interaction]','-> _extract_pr_interactions(self, pr: object) -> list[Interaction]','-> _map_review_type(self, review_state: str) -> str') }
        'src/mining/interaction_model.py' { @('-> dataclass Interaction','-> __post_init__(self) -> None','-> to_row(self) -> dict[str, object]') }
        'src/mining/data_exporter.py' { @('-> export_users_csv(self, users: list[dict], output_path: str) -> str','-> export_interactions_csv(self, interactions: list[Interaction], output_path: str) -> str','-> _ensure_output_dir(self, output_path: str) -> None') }
        'src/graph/exceptions.py' { @('-> class InvalidVertexError(Exception)','-> class SelfLoopError(Exception)','-> class EdgeNotFoundError(Exception)') }
        'src/graph/abstract_graph.py' { @('-> _validate_vertex(self, v: int) -> None','-> add_edge(self, u: int, v: int) -> None','-> remove_edge(self, u: int, v: int) -> None') }
        'src/graph/adjacency_matrix_graph.py' { @('-> add_edge(self, u: int, v: int) -> None','-> has_edge(self, u: int, v: int) -> bool','-> get_edge_weight(self, u: int, v: int) -> float') }
        'src/graph/adjacency_list_graph.py' { @('-> add_edge(self, u: int, v: int) -> None','-> remove_edge(self, u: int, v: int) -> None','-> get_vertex_out_degree(self, u: int) -> int') }
        'src/graph/gephi_exporter.py' { @('-> export(graph: AbstractGraph, path: str) -> str','-> _build_nodes_xml(graph: AbstractGraph) -> str','-> _build_edges_xml(graph: AbstractGraph) -> str') }
        'src/builder/user_registry.py' { @('-> add_user(self, login: str) -> int','-> get_index(self, login: str) -> int','-> get_login(self, index: int) -> str') }
        'src/builder/base_builder.py' { @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]','-> _filter_interactions(self, rows: list[dict]) -> list[dict]','-> _apply_interaction(self, graph: AbstractGraph, row: dict) -> None') }
        'src/builder/graph1_comments_builder.py' { @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]','-> _is_comment_type(self, interaction_type: str) -> bool') }
        'src/builder/graph2_closures_builder.py' { @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]','-> _is_closure_type(self, interaction_type: str) -> bool') }
        'src/builder/graph3_reviews_builder.py' { @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]','-> _is_review_type(self, interaction_type: str) -> bool') }
        'src/builder/graph4_integrated_builder.py' { @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]','-> _sum_weight(self, current: float, increment: float) -> float') }
        'src/analysis/centrality.py' { @('-> degree_centrality(graph: AbstractGraph) -> dict[int, float]','-> betweenness_centrality(graph: AbstractGraph) -> dict[int, float]','-> pagerank(graph: AbstractGraph, damping: float = 0.85, tol: float = 1e-6) -> dict[int, float]') }
        'src/analysis/structure.py' { @('-> density(graph: AbstractGraph) -> float','-> clustering_coefficient(graph: AbstractGraph) -> float','-> degree_assortativity(graph: AbstractGraph) -> float') }
        'src/analysis/community.py' { @('-> detect_communities(graph: AbstractGraph) -> list[set[int]]','-> modularity(graph: AbstractGraph, partition: list[set[int]]) -> float','-> bridging_ties(graph: AbstractGraph, partition: list[set[int]]) -> list[tuple[int,int]]') }
        'src/app/main.py' { @('-> run_mine() -> int','-> run_build() -> int','-> run_analyze() -> int') }
        'src/app/api_demo.py' { @('-> run_demo() -> None','-> _print_operation_result(name: str, result: object) -> None') }
        '.env.example' { @('-> Definir GITHUB_TOKEN= no exemplo de ambiente','-> Incluir comentario sobre nao versionar credenciais reais','-> Manter formato compativel com python-dotenv') }
        'tests/test_mining.py' { @('-> test_cenario_feliz_mining()','-> test_edge_case_mining()','-> test_resiliencia_retry_rate_limit()') }
        'tests/test_graph_matrix.py' { @('-> test_cenario_feliz_graph_matrix()','-> test_idempotencia_add_edge_matrix()','-> test_excecao_indice_invalido_matrix()') }
        'tests/test_graph_list.py' { @('-> test_cenario_feliz_graph_list()','-> test_idempotencia_add_edge_list()','-> test_excecao_self_loop_list()') }
        'tests/test_builder.py' { @('-> test_cenario_feliz_builder()','-> test_filtro_por_tipo_interacao()','-> test_agregacao_pesos_g4()') }
        'tests/test_analysis.py' { @('-> test_cenario_feliz_analysis()','-> test_metricas_em_grafo_canonico()','-> test_edge_case_grafo_vazio()') }
        'report/main.tex' { @('-> section_metodologia() -> str','-> section_resultados() -> str','-> section_conclusao() -> str') }
        default { @('-> metodo_publico_1(parametros) -> tipo_retorno','-> metodo_publico_2(parametros) -> tipo_retorno','-> _metodo_privado(parametros) -> None') }
    }
}

function New-StoryBlock {
    param(
        [string]$epicId,
        [string]$featureId,
        [string]$storyId,
        [string]$title,
        [string]$role,
        [string]$want,
        [string]$value,
        [string[]]$files,
        [string[]]$blockedBy,
        [int]$points,
        [string]$frente,
        [string]$area
    )

    $testFile = Get-TestFile $epicId
    $blockedByText = if (@($blockedBy).Count -eq 0) { 'nenhuma' } else { '[' + (@($blockedBy) -join ', ') + ']' }
    $imports = ($files | Where-Object { $_ -like 'src/*' } | Sort-Object -Unique)
    $importsText = if (@($imports).Count -eq 0) { 'N/A' } else { @($imports) -join ', ' }

    $out = New-Object System.Collections.Generic.List[string]
    $out.Add('## CARD '+$storyId)
    $out.Add('Titulo: '+$title)
    $out.Add('Tipo: Story')
    $out.Add('Prioridade: High')
    $out.Add('Numero da Sprint: Choose an iteration')
    $out.Add('Story Points: '+$points)
    $out.Add('Categoria: Choose an option')
    $out.Add('Relator: Matheus Felipe Correa')
    $out.Add('Pai (Epic/Feature): '+$featureId)
    $out.Add('Data Limite: No date')
    $out.Add('')
    $out.Add('## Descricao')
    $out.Add('Como '+$role+', eu quero '+$want+', para '+$value+'.')
    $out.Add('')
    $out.Add('## Criterios de Aceite')
    $out.Add('**Cenario 1 - Fluxo principal**')
    $out.Add('Dado o contexto valido da story, Quando o fluxo principal for executado, Entao o comportamento esperado deve ser atendido sem regressao.')
    $out.Add('')
    $out.Add('**Cenario 2 - Integracao entre modulos**')
    $out.Add('Dado os modulos dependentes disponiveis, Quando a funcionalidade for integrada, Entao os dados devem trafegar no contrato esperado.')
    $out.Add('')
    $out.Add('**Cenario 3 - Edge case de erro**')
    $out.Add('Dado entrada invalida ou falha transitoria, Quando o processamento ocorrer, Entao o sistema deve tratar erro com mensagem clara e sem quebrar pipeline.')
    $out.Add('')
    $out.Add('## Implementacao')

    foreach ($f in $files) {
        $name = [IO.Path]::GetFileName($f)
        $out.Add('')
        $out.Add('#### '+$name+' (EXISTENTE - MODIFICAR)')
        $out.Add('Criar em: '+$f)
        $out.Add('Seguir padrao de: '+$f)
        $out.Add('Logica existente (NAO alterar):')
        $out.Add('-> Contrato atual do modulo e assinatura publica ja definida no backlog.')
        $out.Add('Logica NOVA a adicionar:')
        foreach ($h in (Get-MethodHints $f)) { $out.Add($h) }
    }

    $out.Add('')
    $out.Add('## Testes')
    $sid = ($storyId -replace '[^0-9]','_')
    $out.Add('Arquivo: '+$testFile)
    $out.Add('-> test_'+$sid+'_cenario_feliz() - valida cenario 1.')
    $out.Add('-> test_'+$sid+'_cenario_alternativo() - valida cenario 2.')
    $out.Add('-> test_'+$sid+'_edge_case() - valida cenario 3.')
    $out.Add('-> test_'+$sid+'_idempotencia_ou_invariante() - valida invariante tecnica da story.')
    $out.Add('Fixtures necessarias: mocks de API/IO, dados sinteticos, controle de tempo e grafos canonicos quando aplicavel.')
    $out.Add('Cobertura minima: 90% para modulo alterado e 80% global da frente.')
    $out.Add('')
    $out.Add('## Dependencias')
    $out.Add('- Bloqueia: [A definir no planejamento da sprint]')
    $out.Add('- Bloqueado por: '+$blockedByText)
    $out.Add('- Importa de: '+$importsText)
    $out.Add('- E importado por: camadas da mesma frente e src/app/main.py')
    $out.Add('')
    $out.Add('## Endpoints / CLI / API Publica')
    if ($epicId -eq '1') { $out.Add('- python -m src.app.main --mine - executa mineracao resiliente.') }
    elseif ($epicId -eq '2') { $out.Add('- python -m src.app.api_demo - demonstra API de grafo.') }
    elseif ($epicId -eq '3') { $out.Add('- python -m src.app.main --build - construcao de grafos G1..G4.') }
    elseif ($epicId -eq '4') { $out.Add('- python -m src.app.main --analyze - gera metricas e relatorios.') }
    elseif ($epicId -eq '5') { $out.Add('- python -m src.app.main --all - orquestra pipeline completo.') }
    else { $out.Add('- Documento tecnico em report/main.tex e entrega final da disciplina.') }
    $out.Add('')
    $out.Add('## Edge Cases e Excecoes')
    $out.Add('- Entrada invalida -> lancar excecao de dominio com mensagem acionavel.')
    $out.Add('- Falha transitoria de rede/API -> aplicar retry/backoff e retomar sem quebra abrupta.')
    if ($epicId -eq '2') {
        $out.Add('- Vertice fora de faixa -> InvalidVertexError.')
        $out.Add('- Laco em grafo simples -> SelfLoopError.')
    }
    if ($epicId -eq '1') {
        $out.Add('- O minerador nao pode falhar por erro transitorio; deve continuar com tratamento resiliente.')
    }
    $out.Add('')
    $out.Add('## Estimativa')
    $out.Add('Story Points: '+$points)
    $out.Add('Justificativa: complexidade tecnica, integracao entre modulos e exigencia de testes robustos.')
    $out.Add('')
    $out.Add('## Labels')
    $out.Add($frente+', '+$area+', python, story')
    $out.Add('')

    return ($out -join $NL)
}

function New-FeatureBlock {
    param(
        [string]$featureId,
        [string]$title,
        [string]$desc,
        [string[]]$files,
        [string]$dep,
        [int]$points,
        [string]$frente,
        [string]$area
    )

    $out = New-Object System.Collections.Generic.List[string]
    $out.Add('## CARD '+$featureId)
    $out.Add('Titulo: '+$title)
    $out.Add('Tipo: Feature')
    $out.Add('Prioridade: High')
    $out.Add('Numero da Sprint: Choose an iteration')
    $out.Add('Story Points: '+$points)
    $out.Add('Categoria: Choose an option')
    $out.Add('Relator: Matheus Felipe Correa')
    $parentEpic = 'EPIC-' + ($featureId.Split('-')[1].Split('.')[0])
    $out.Add('Pai (Epic/Feature): '+$parentEpic)
    $out.Add('Data Limite: No date')
    $out.Add('')
    $out.Add('## Descricao')
    $out.Add($desc)
    $out.Add('')
    $out.Add('## Escopo Funcional')
    $out.Add('Arquivos impactados:')
    foreach ($f in $files) { $out.Add('- github-graph-analyzer/'+$f+' (EXISTENTE - MODIFICAR)') }
    $out.Add('')
    $out.Add('## Criterios de Aceite')
    $out.Add('- Fluxos da feature implementados com consistencia funcional e tecnica.')
    $out.Add('- Integracao validada com camadas adjacentes.')
    $out.Add('- Erros de entrada e falhas transitorias tratados de forma resiliente.')
    $out.Add('')
    $out.Add('## Implementacao (Alto Nivel)')
    $out.Add('- Definir contrato publico da feature e metodos internos.')
    $out.Add('- Integrar com modulos dependentes sem quebrar API existente.')
    $out.Add('- Escrever testes cobrindo cenario feliz, alternativo e edge case.')
    $out.Add('')
    $out.Add('## Definicao de Pronto (DoD)')
    $out.Add('- [ ] Stories da feature concluidas e revisadas.')
    $out.Add('- [ ] Cobertura da frente entre 90% e 95%.')
    $out.Add('- [ ] Documentacao tecnica atualizada.')
    $out.Add('')
    $out.Add('## Dependencias')
    $out.Add('- Dependencias: '+$dep)
    $out.Add('')
    $out.Add('## Regras de Negocio')
    $out.Add('- Seguir enunciado da disciplina e contratos entre frentes.')
    if ($featureId -like 'FEAT-1.*') { $out.Add('- O minerador nao pode falhar por erros transitorios.') }
    $out.Add('')
    $out.Add('## Observacoes')
    $out.Add('- Riscos: divergencia de contrato entre frentes ou cobertura insuficiente de testes.')
    $out.Add('')

    return ($out -join $NL)
}

function New-EpicFile {
    param(
        [string]$epicId,
        [string]$epicTitle,
        [string]$epicDesc,
        [string]$filePath,
        [object[]]$features
    )

    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add('# [EPIC] '+$epicId+' - '+$epicTitle)
    $lines.Add('')
    $lines.Add('## CARD EPIC-'+$epicId+' - Frente '+$epicId+' - '+$epicTitle)
    $lines.Add('Tipo: Epic')
    $lines.Add('Prioridade: Highest')
    $lines.Add('Numero da Sprint: Choose an iteration')
    $lines.Add('Story Points: 8')
    $lines.Add('Categoria: Choose an option')
    $lines.Add('Relator: Matheus Felipe Correa')
    $lines.Add('Pai (Epic/Feature): -')
    $lines.Add('Data Limite: No date')
    $lines.Add('')
    $lines.Add('## Descricao')
    $lines.Add($epicDesc)
    $lines.Add('')
    $lines.Add('## Criterios de Aceite')
    $lines.Add('- Todas as features e stories do epic implementadas.')
    $lines.Add('- Cobertura de testes da frente entre 90% e 95%.')
    $lines.Add('- Integracao com outras frentes sem quebra de contrato.')
    $lines.Add('')
    $lines.Add('## Regras de Negocio')
    $lines.Add('- Seguir estritamente o enunciado do trabalho e restricoes tecnicas.')
    if ($epicId -eq '1') { $lines.Add('- O minerador nao pode falhar por erro transitorio; deve ter retry, backoff e retomada segura.') }
    $lines.Add('')
    $lines.Add('---')
    $lines.Add('')

    foreach ($f in $features) {
        $lines.Add((New-FeatureBlock -featureId $f.id -title $f.title -desc $f.desc -files $f.files -dep $f.dep -points $f.points -frente $f.frente -area $f.area))
        foreach ($s in $f.stories) {
            $lines.Add((New-StoryBlock -epicId $epicId -featureId $f.id -storyId $s.id -title $s.title -role $s.role -want $s.want -value $s.value -files $s.files -blockedBy $s.blockedBy -points $s.points -frente $f.frente -area $f.area))
        }
        $lines.Add('---')
        $lines.Add('')
    }

    [System.IO.File]::WriteAllText($filePath, ($lines -join $NL), [System.Text.Encoding]::UTF8)
}

$root = Get-Location
$cardsDir = Join-Path $root '.github/plans/cards'

# EPIC 1
$ep1 = @(
    @{ id='FEAT-1.1'; title='Cliente GitHub autenticado e resiliente'; desc='Implementar cliente de acesso ao GitHub com autenticacao, tratamento de rate limit e retry seguro.'; files=@('src/mining/github_client.py','.env.example','tests/test_mining.py'); dep='nenhuma'; points=5; frente='frente-1'; area='mining'; stories=@(
        @{ id='STORY-1.1.1'; title='Carregar token GitHub via ambiente'; role='desenvolvedor'; want='carregar GITHUB_TOKEN por ambiente'; value='evitar credencial hardcoded e falhas de autenticacao'; files=@('src/mining/github_client.py','.env.example','tests/test_mining.py'); blockedBy=@(); points=2 },
        @{ id='STORY-1.1.2'; title='Tratar rate limit com espera segura'; role='minerador'; want='detectar e esperar reset de limite'; value='evitar quebra do pipeline por limites da API'; files=@('src/mining/github_client.py','tests/test_mining.py'); blockedBy=@('STORY-1.1.1'); points=3 },
        @{ id='STORY-1.1.3'; title='Aplicar retry exponencial com jitter'; role='minerador'; want='retentar falhas transitorias'; value='aumentar estabilidade da mineracao'; files=@('src/mining/github_client.py','tests/test_mining.py'); blockedBy=@('STORY-1.1.1','STORY-1.1.2'); points=3 }
    )},
    @{ id='FEAT-1.2'; title='Modelo padrao de interacao entre usuarios'; desc='Definir contrato unico de interacao para consumo por builders e analise.'; files=@('src/mining/interaction_model.py','tests/test_mining.py'); dep='FEAT-1.1'; points=3; frente='frente-1'; area='mining'; stories=@(
        @{ id='STORY-1.2.1'; title='Criar dataclass Interaction'; role='desenvolvedor'; want='padronizar estrutura de interacao'; value='garantir contrato claro entre frentes'; files=@('src/mining/interaction_model.py','tests/test_mining.py'); blockedBy=@('STORY-1.1.1'); points=2 },
        @{ id='STORY-1.2.2'; title='Validar tipo de interacao permitido'; role='desenvolvedor'; want='aceitar apenas tipos previstos no trabalho'; value='evitar dados inconsistentes no CSV'; files=@('src/mining/interaction_model.py','tests/test_mining.py'); blockedBy=@('STORY-1.2.1'); points=2 },
        @{ id='STORY-1.2.3'; title='Normalizar payload para exportacao'; role='desenvolvedor'; want='converter interacao para linha csv estavel'; value='facilitar build e analise sem transformacoes extras'; files=@('src/mining/interaction_model.py','src/mining/data_exporter.py','tests/test_mining.py'); blockedBy=@('STORY-1.2.1'); points=2 }
    )},
    @{ id='FEAT-1.3'; title='Mineracao de Issues e eventos relacionados'; desc='Coletar issues, comentarios e fechamentos em formato de interacao.'; files=@('src/mining/issue_miner.py','src/mining/github_client.py','tests/test_mining.py'); dep='FEAT-1.1, FEAT-1.2'; points=5; frente='frente-1'; area='mining'; stories=@(
        @{ id='STORY-1.3.1'; title='Coletar autores e comentarios de issues'; role='analista de dados'; want='extrair interacoes de comentarios em issues'; value='alimentar G1 e G4 com dados corretos'; files=@('src/mining/issue_miner.py','tests/test_mining.py'); blockedBy=@('STORY-1.1.1','STORY-1.2.1'); points=3 },
        @{ id='STORY-1.3.2'; title='Coletar eventos de fechamento de issue'; role='analista de dados'; want='mapear quem fechou issue de quem'; value='alimentar G2 corretamente'; files=@('src/mining/issue_miner.py','tests/test_mining.py'); blockedBy=@('STORY-1.3.1'); points=2 },
        @{ id='STORY-1.3.3'; title='Descartar auto interacao em issues'; role='desenvolvedor'; want='ignorar src==dst'; value='respeitar restricao de grafo simples'; files=@('src/mining/issue_miner.py','src/mining/interaction_model.py','tests/test_mining.py'); blockedBy=@('STORY-1.2.1'); points=2 }
    )},
    @{ id='FEAT-1.4'; title='Mineracao de Pull Requests e Reviews'; desc='Coletar PRs, reviews, comentarios e merges para compor G3 e G4.'; files=@('src/mining/pr_miner.py','src/mining/github_client.py','tests/test_mining.py'); dep='FEAT-1.1, FEAT-1.2'; points=5; frente='frente-1'; area='mining'; stories=@(
        @{ id='STORY-1.4.1'; title='Extrair reviews e estados de aprovacao'; role='analista de dados'; want='capturar reviews de PR'; value='calcular peso correto de review no G3/G4'; files=@('src/mining/pr_miner.py','tests/test_mining.py'); blockedBy=@('STORY-1.1.1','STORY-1.2.1'); points=3 },
        @{ id='STORY-1.4.2'; title='Extrair merges e autor de PR'; role='analista de dados'; want='capturar evento de merge'; value='alimentar peso de merge no G3/G4'; files=@('src/mining/pr_miner.py','tests/test_mining.py'); blockedBy=@('STORY-1.4.1'); points=2 },
        @{ id='STORY-1.4.3'; title='Classificar comentario de PR e review'; role='desenvolvedor'; want='diferenciar tipos de interacao'; value='evitar peso incorreto no grafo integrado'; files=@('src/mining/pr_miner.py','src/mining/interaction_model.py','tests/test_mining.py'); blockedBy=@('STORY-1.2.2'); points=2 }
    )},
    @{ id='FEAT-1.5'; title='Exportacao de datasets CSV padronizados'; desc='Exportar users.csv e interactions.csv no schema oficial do projeto.'; files=@('src/mining/data_exporter.py','tests/test_mining.py'); dep='FEAT-1.2, FEAT-1.3, FEAT-1.4'; points=5; frente='frente-1'; area='mining'; stories=@(
        @{ id='STORY-1.5.1'; title='Exportar users.csv com colunas obrigatorias'; role='desenvolvedor'; want='gerar arquivo users.csv estavel'; value='permitir indexacao consistente no builder'; files=@('src/mining/data_exporter.py','tests/test_mining.py'); blockedBy=@('STORY-1.2.1'); points=2 },
        @{ id='STORY-1.5.2'; title='Exportar interactions.csv com schema oficial'; role='desenvolvedor'; want='gerar interactions.csv padrao'; value='evitar quebra de leitura no builder'; files=@('src/mining/data_exporter.py','src/mining/interaction_model.py','tests/test_mining.py'); blockedBy=@('STORY-1.2.3','STORY-1.3.1','STORY-1.4.1'); points=3 },
        @{ id='STORY-1.5.3'; title='Garantir exportacao idempotente de arquivos'; role='desenvolvedor'; want='reexecutar export sem duplicar linhas'; value='assegurar pipeline repetivel'; files=@('src/mining/data_exporter.py','tests/test_mining.py'); blockedBy=@('STORY-1.5.1','STORY-1.5.2'); points=3 }
    )},
    @{ id='FEAT-1.6'; title='Testes da camada de mineracao'; desc='Cobrir mineracao com cenarios de sucesso, erro e resiliencia para 90-95%.'; files=@('tests/test_mining.py','src/mining/github_client.py','src/mining/issue_miner.py','src/mining/pr_miner.py','src/mining/data_exporter.py'); dep='FEAT-1.1, FEAT-1.2, FEAT-1.3, FEAT-1.4, FEAT-1.5'; points=5; frente='frente-1'; area='testes'; stories=@(
        @{ id='STORY-1.6.1'; title='Testar autenticacao e configuracao de ambiente'; role='QA'; want='validar token presente, ausente e invalido'; value='garantir bootstrap confiavel do minerador'; files=@('tests/test_mining.py','src/mining/github_client.py'); blockedBy=@('STORY-1.1.1'); points=2 },
        @{ id='STORY-1.6.2'; title='Testar fluxo de issues e PRs com mocks'; role='QA'; want='simular API do GitHub sem chamadas reais'; value='garantir comportamento deterministico em CI'; files=@('tests/test_mining.py','src/mining/issue_miner.py','src/mining/pr_miner.py'); blockedBy=@('STORY-1.3.1','STORY-1.4.1'); points=3 },
        @{ id='STORY-1.6.3'; title='Testar resiliencia completa do minerador'; role='QA'; want='validar retry e rate limit ponta a ponta'; value='evitar falha em producao por erros transitorios'; files=@('tests/test_mining.py','src/mining/github_client.py'); blockedBy=@('STORY-1.1.2','STORY-1.1.3'); points=3 }
    )}
)

# EPIC 2
$ep2 = @(
    @{ id='FEAT-2.1'; title='Excecoes customizadas de dominio do grafo'; desc='Criar excecoes claras para validacao de vertices, lacos e arestas inexistentes.'; files=@('src/graph/exceptions.py','tests/test_graph_matrix.py','tests/test_graph_list.py'); dep='nenhuma'; points=3; frente='frente-2'; area='graph'; stories=@(
        @{ id='STORY-2.1.1'; title='Criar InvalidVertexError'; role='desenvolvedor'; want='sinalizar indice fora da faixa'; value='evitar corrupcao de estado do grafo'; files=@('src/graph/exceptions.py','tests/test_graph_matrix.py'); blockedBy=@(); points=1 },
        @{ id='STORY-2.1.2'; title='Criar SelfLoopError'; role='desenvolvedor'; want='bloquear aresta u para u'; value='cumprir restricao de grafo simples'; files=@('src/graph/exceptions.py','tests/test_graph_list.py'); blockedBy=@(); points=1 },
        @{ id='STORY-2.1.3'; title='Criar EdgeNotFoundError'; role='desenvolvedor'; want='sinalizar operacao em aresta ausente'; value='dar feedback tecnico correto em remocao e peso'; files=@('src/graph/exceptions.py','tests/test_graph_matrix.py'); blockedBy=@(); points=1 }
    )},
    @{ id='FEAT-2.2'; title='API abstrata AbstractGraph e validacoes comuns'; desc='Definir contrato unico das operacoes obrigatorias de grafo e validacoes compartilhadas.'; files=@('src/graph/abstract_graph.py','src/graph/exceptions.py','tests/test_graph_matrix.py','tests/test_graph_list.py'); dep='FEAT-2.1'; points=5; frente='frente-2'; area='graph'; stories=@(
        @{ id='STORY-2.2.1'; title='Definir metodos obrigatorios da API'; role='desenvolvedor'; want='explicitar assinatura de operacoes'; value='garantir implementacoes consistentes'; files=@('src/graph/abstract_graph.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.1.1'); points=2 },
        @{ id='STORY-2.2.2'; title='Implementar validacao de vertices'; role='desenvolvedor'; want='validar indice em um unico ponto'; value='reduzir duplicacao e erro nas classes concretas'; files=@('src/graph/abstract_graph.py','src/graph/exceptions.py','tests/test_graph_list.py'); blockedBy=@('STORY-2.1.1'); points=2 },
        @{ id='STORY-2.2.3'; title='Documentar contratos de idempotencia'; role='desenvolvedor'; want='especificar add_edge sem duplicacao'; value='garantir comportamento exigido pelo enunciado'; files=@('src/graph/abstract_graph.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.2.1'); points=1 }
    )},
    @{ id='FEAT-2.3'; title='Implementacao por matriz de adjacencia'; desc='Implementar classe de grafo direcionado simples usando matriz NxN.'; files=@('src/graph/adjacency_matrix_graph.py','src/graph/abstract_graph.py','src/graph/exceptions.py','tests/test_graph_matrix.py'); dep='FEAT-2.1, FEAT-2.2'; points=5; frente='frente-2'; area='graph'; stories=@(
        @{ id='STORY-2.3.1'; title='Inicializar matriz e contadores'; role='desenvolvedor'; want='criar estrutura base da classe'; value='suportar operacoes de aresta e grau'; files=@('src/graph/adjacency_matrix_graph.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.2.1'); points=2 },
        @{ id='STORY-2.3.2'; title='Implementar add_edge idempotente sem laco'; role='desenvolvedor'; want='adicionar arestas sem duplicar'; value='cumprir regra de grafo simples'; files=@('src/graph/adjacency_matrix_graph.py','src/graph/exceptions.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.1.1','STORY-2.1.2','STORY-2.2.2'); points=2 },
        @{ id='STORY-2.3.3'; title='Implementar consultas de grau e pesos'; role='desenvolvedor'; want='obter in/out degree e peso de aresta'; value='suportar metodos da API e analise'; files=@('src/graph/adjacency_matrix_graph.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.3.2'); points=3 }
    )},
    @{ id='FEAT-2.4'; title='Implementacao por lista de adjacencia'; desc='Implementar classe de grafo direcionado simples por lista de adjacencia.'; files=@('src/graph/adjacency_list_graph.py','src/graph/abstract_graph.py','src/graph/exceptions.py','tests/test_graph_list.py'); dep='FEAT-2.1, FEAT-2.2'; points=5; frente='frente-2'; area='graph'; stories=@(
        @{ id='STORY-2.4.1'; title='Inicializar lista de adjacencia'; role='desenvolvedor'; want='estruturar armazenamento por vertice'; value='otimizar grafo esparso'; files=@('src/graph/adjacency_list_graph.py','tests/test_graph_list.py'); blockedBy=@('STORY-2.2.1'); points=2 },
        @{ id='STORY-2.4.2'; title='Implementar add_edge idempotente e validacoes'; role='desenvolvedor'; want='adicionar aresta sem duplicar e sem laco'; value='garantir contrato da API abstrata'; files=@('src/graph/adjacency_list_graph.py','src/graph/exceptions.py','tests/test_graph_list.py'); blockedBy=@('STORY-2.1.1','STORY-2.1.2','STORY-2.2.2'); points=2 },
        @{ id='STORY-2.4.3'; title='Implementar remocao, graus e pesos'; role='desenvolvedor'; want='completar operacoes obrigatorias'; value='equivaler comportamento da implementacao em matriz'; files=@('src/graph/adjacency_list_graph.py','tests/test_graph_list.py'); blockedBy=@('STORY-2.4.2'); points=3 }
    )},
    @{ id='FEAT-2.5'; title='Exportador Gephi em formato GEXF'; desc='Gerar arquivo GEXF manualmente sem bibliotecas prontas para visualizacao no Gephi.'; files=@('src/graph/gephi_exporter.py','src/graph/abstract_graph.py','tests/test_graph_matrix.py'); dep='FEAT-2.3, FEAT-2.4'; points=3; frente='frente-2'; area='graph'; stories=@(
        @{ id='STORY-2.5.1'; title='Montar XML de nos e arestas'; role='desenvolvedor'; want='gerar estrutura gexf valida'; value='permitir importacao no gephi'; files=@('src/graph/gephi_exporter.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.3.3'); points=2 },
        @{ id='STORY-2.5.2'; title='Exportar atributos de peso'; role='desenvolvedor'; want='persistir pesos de aresta no gexf'; value='preservar semantica do grafo integrado'; files=@('src/graph/gephi_exporter.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.5.1'); points=2 },
        @{ id='STORY-2.5.3'; title='Validar arquivo gerado no parser XML'; role='QA'; want='garantir xml bem formado'; value='evitar falhas de importacao na apresentacao'; files=@('src/graph/gephi_exporter.py','tests/test_graph_matrix.py'); blockedBy=@('STORY-2.5.1'); points=1 }
    )},
    @{ id='FEAT-2.6'; title='Testes das estruturas de grafo'; desc='Criar suite robusta para validar contratos entre matrix e list.'; files=@('tests/test_graph_matrix.py','tests/test_graph_list.py','src/graph/adjacency_matrix_graph.py','src/graph/adjacency_list_graph.py'); dep='FEAT-2.1, FEAT-2.2, FEAT-2.3, FEAT-2.4, FEAT-2.5'; points=5; frente='frente-2'; area='testes'; stories=@(
        @{ id='STORY-2.6.1'; title='Cobrir cenarios de idempotencia e excecoes'; role='QA'; want='testar contrato de add_edge e validacoes'; value='evitar regressao em regras criticas'; files=@('tests/test_graph_matrix.py','tests/test_graph_list.py'); blockedBy=@('STORY-2.3.2','STORY-2.4.2'); points=2 },
        @{ id='STORY-2.6.2'; title='Comparar consistencia matrix vs list'; role='QA'; want='validar mesmos resultados para mesmos dados'; value='garantir equivalencia de implementacao'; files=@('tests/test_graph_matrix.py','tests/test_graph_list.py'); blockedBy=@('STORY-2.3.3','STORY-2.4.3'); points=3 },
        @{ id='STORY-2.6.3'; title='Validar exportacao gexf em testes'; role='QA'; want='checar geracao de arquivo e conteudo basico'; value='evitar erro em entregavel visual'; files=@('tests/test_graph_matrix.py','src/graph/gephi_exporter.py'); blockedBy=@('STORY-2.5.1'); points=2 }
    )}
)

# EPIC 3
$ep3 = @(
    @{ id='FEAT-3.1'; title='Registry de usuarios login para indice'; desc='Mapear login para indice e indice para login de forma deterministica.'; files=@('src/builder/user_registry.py','tests/test_builder.py'); dep='FEAT-1.5'; points=3; frente='frente-3'; area='builder'; stories=@(
        @{ id='STORY-3.1.1'; title='Adicionar usuario e retornar indice'; role='desenvolvedor'; want='gerar indice estavel por login'; value='construir arestas com vertices consistentes'; files=@('src/builder/user_registry.py','tests/test_builder.py'); blockedBy=@('STORY-1.5.1'); points=2 },
        @{ id='STORY-3.1.2'; title='Consultar indice por login'; role='desenvolvedor'; want='buscar vertice de origem e destino'; value='evitar duplicacao de vertices'; files=@('src/builder/user_registry.py','tests/test_builder.py'); blockedBy=@('STORY-3.1.1'); points=1 },
        @{ id='STORY-3.1.3'; title='Consultar login por indice'; role='desenvolvedor'; want='resolver nome para relatorios'; value='integrar com camada de analise'; files=@('src/builder/user_registry.py','tests/test_builder.py'); blockedBy=@('STORY-3.1.1'); points=1 }
    )},
    @{ id='FEAT-3.2'; title='Builder base com template build'; desc='Criar fluxo comum de leitura de CSV, filtro de interacao e aplicacao no grafo.'; files=@('src/builder/base_builder.py','src/builder/user_registry.py','tests/test_builder.py'); dep='FEAT-3.1, FEAT-2.2'; points=5; frente='frente-3'; area='builder'; stories=@(
        @{ id='STORY-3.2.1'; title='Ler CSVs com validacao de colunas'; role='desenvolvedor'; want='carregar users e interactions com schema valido'; value='evitar erro silencioso na construcao'; files=@('src/builder/base_builder.py','tests/test_builder.py'); blockedBy=@('STORY-1.5.2'); points=2 },
        @{ id='STORY-3.2.2'; title='Definir template build reutilizavel'; role='desenvolvedor'; want='padronizar fluxo dos builders concretos'; value='reduzir codigo duplicado'; files=@('src/builder/base_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.2.1','STORY-3.1.1'); points=2 },
        @{ id='STORY-3.2.3'; title='Aplicar interacao no grafo com registry'; role='desenvolvedor'; want='converter login para indice ao adicionar aresta'; value='integrar F1, F2 e F3 corretamente'; files=@('src/builder/base_builder.py','src/builder/user_registry.py','tests/test_builder.py'); blockedBy=@('STORY-3.1.1','STORY-2.3.2'); points=3 }
    )},
    @{ id='FEAT-3.3'; title='Grafo 1 de comentarios'; desc='Construir G1 com comment_issue e comment_pr.'; files=@('src/builder/graph1_comments_builder.py','src/builder/base_builder.py','tests/test_builder.py'); dep='FEAT-3.2'; points=3; frente='frente-3'; area='builder'; stories=@(
        @{ id='STORY-3.3.1'; title='Filtrar tipos de comentario'; role='desenvolvedor'; want='considerar apenas comment_issue e comment_pr'; value='garantir semantica correta de G1'; files=@('src/builder/graph1_comments_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.2.2'); points=1 },
        @{ id='STORY-3.3.2'; title='Criar arestas comentador para autor'; role='desenvolvedor'; want='adicionar relacao direcionada correta'; value='representar colaboracao entre usuarios'; files=@('src/builder/graph1_comments_builder.py','src/builder/base_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.3.1','STORY-3.2.3'); points=2 },
        @{ id='STORY-3.3.3'; title='Exportar graph1_comments.gexf'; role='desenvolvedor'; want='persistir G1 para visualizacao'; value='dar suporte ao relatorio e demonstracao'; files=@('src/builder/graph1_comments_builder.py','src/graph/gephi_exporter.py','tests/test_builder.py'); blockedBy=@('STORY-2.5.1','STORY-3.3.2'); points=1 }
    )},
    @{ id='FEAT-3.4'; title='Grafo 2 de fechamentos de issue'; desc='Construir G2 com close_issue.'; files=@('src/builder/graph2_closures_builder.py','src/builder/base_builder.py','tests/test_builder.py'); dep='FEAT-3.2'; points=3; frente='frente-3'; area='builder'; stories=@(
        @{ id='STORY-3.4.1'; title='Filtrar tipo close_issue'; role='desenvolvedor'; want='considerar somente eventos de fechamento'; value='evitar contaminacao com outras interacoes'; files=@('src/builder/graph2_closures_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.2.2'); points=1 },
        @{ id='STORY-3.4.2'; title='Aplicar direcao fechador para autor'; role='desenvolvedor'; want='modelar aresta src fechador dst autor'; value='capturar poder de resolucao de issues'; files=@('src/builder/graph2_closures_builder.py','src/builder/base_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.4.1','STORY-3.2.3'); points=2 },
        @{ id='STORY-3.4.3'; title='Exportar graph2_closures.gexf'; role='desenvolvedor'; want='gerar artefato visual de G2'; value='suportar analise comparativa'; files=@('src/builder/graph2_closures_builder.py','src/graph/gephi_exporter.py','tests/test_builder.py'); blockedBy=@('STORY-2.5.1','STORY-3.4.2'); points=1 }
    )},
    @{ id='FEAT-3.5'; title='Grafo 3 de reviews e merges'; desc='Construir G3 com review_pr e merge_pr.'; files=@('src/builder/graph3_reviews_builder.py','src/builder/base_builder.py','tests/test_builder.py'); dep='FEAT-3.2'; points=3; frente='frente-3'; area='builder'; stories=@(
        @{ id='STORY-3.5.1'; title='Filtrar tipos review_pr e merge_pr'; role='desenvolvedor'; want='processar apenas eventos de review e merge'; value='garantir semantica correta de G3'; files=@('src/builder/graph3_reviews_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.2.2'); points=1 },
        @{ id='STORY-3.5.2'; title='Aplicar arestas de revisor e merger'; role='desenvolvedor'; want='criar relacao para autor da PR'; value='medir influencia tecnica na rede'; files=@('src/builder/graph3_reviews_builder.py','src/builder/base_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.5.1','STORY-3.2.3'); points=2 },
        @{ id='STORY-3.5.3'; title='Exportar graph3_reviews.gexf'; role='desenvolvedor'; want='persistir G3'; value='habilitar visualizacao e comparacao com G1/G2'; files=@('src/builder/graph3_reviews_builder.py','src/graph/gephi_exporter.py','tests/test_builder.py'); blockedBy=@('STORY-2.5.1','STORY-3.5.2'); points=1 }
    )},
    @{ id='FEAT-3.6'; title='Grafo 4 integrado e ponderado'; desc='Construir G4 unificando todos os tipos de interacao e somando pesos por aresta.'; files=@('src/builder/graph4_integrated_builder.py','src/builder/base_builder.py','tests/test_builder.py'); dep='FEAT-3.2, FEAT-3.3, FEAT-3.4, FEAT-3.5'; points=5; frente='frente-3'; area='builder'; stories=@(
        @{ id='STORY-3.6.1'; title='Combinar todos os tipos de interacao'; role='desenvolvedor'; want='agregar eventos elegiveis no G4'; value='obter visao integrada da colaboracao'; files=@('src/builder/graph4_integrated_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.3.1','STORY-3.4.1','STORY-3.5.1'); points=2 },
        @{ id='STORY-3.6.2'; title='Somar pesos em arestas repetidas'; role='desenvolvedor'; want='acumular peso por par src,dst'; value='representar intensidade de interacao'; files=@('src/builder/graph4_integrated_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.6.1'); points=3 },
        @{ id='STORY-3.6.3'; title='Aplicar tabela oficial de pesos'; role='desenvolvedor'; want='mapear tipo para peso definido no README'; value='manter coerencia com criterios do trabalho'; files=@('src/builder/graph4_integrated_builder.py','src/mining/interaction_model.py','tests/test_builder.py'); blockedBy=@('STORY-1.2.2','STORY-3.6.1'); points=2 }
    )},
    @{ id='FEAT-3.7'; title='Testes dos builders'; desc='Cobrir construcoes de G1, G2, G3 e G4 com fixtures sinteticas e validacao de contrato.'; files=@('tests/test_builder.py','src/builder/graph1_comments_builder.py','src/builder/graph2_closures_builder.py','src/builder/graph3_reviews_builder.py','src/builder/graph4_integrated_builder.py'); dep='FEAT-3.3, FEAT-3.4, FEAT-3.5, FEAT-3.6'; points=5; frente='frente-3'; area='testes'; stories=@(
        @{ id='STORY-3.7.1'; title='Testar filtros por tipo em cada builder'; role='QA'; want='validar entrada correta por builder'; value='evitar arestas indevidas nos grafos'; files=@('tests/test_builder.py'); blockedBy=@('STORY-3.3.1','STORY-3.4.1','STORY-3.5.1'); points=2 },
        @{ id='STORY-3.7.2'; title='Testar pesos e agregacao do G4'; role='QA'; want='validar soma e mapa de pesos'; value='garantir fidelidade da analise integrada'; files=@('tests/test_builder.py','src/builder/graph4_integrated_builder.py'); blockedBy=@('STORY-3.6.2','STORY-3.6.3'); points=3 },
        @{ id='STORY-3.7.3'; title='Testar exportacao de todos os grafos'; role='QA'; want='verificar arquivos gexf de G1 a G4'; value='garantir entregavel visual pronto'; files=@('tests/test_builder.py','src/graph/gephi_exporter.py'); blockedBy=@('STORY-2.5.1','STORY-3.3.3','STORY-3.4.3','STORY-3.5.3'); points=2 }
    )}
)

# EPIC 4
$ep4 = @(
    @{ id='FEAT-4.1'; title='Metricas de centralidade'; desc='Implementar degree, betweenness, closeness e pagerank sem bibliotecas prontas de grafos.'; files=@('src/analysis/centrality.py','tests/test_analysis.py','src/graph/abstract_graph.py'); dep='FEAT-2.2, FEAT-3.6'; points=8; frente='frente-4'; area='analysis'; stories=@(
        @{ id='STORY-4.1.1'; title='Calcular degree centrality'; role='analista'; want='medir centralidade por grau'; value='identificar atores mais conectados'; files=@('src/analysis/centrality.py','tests/test_analysis.py'); blockedBy=@('STORY-2.3.3'); points=2 },
        @{ id='STORY-4.1.2'; title='Implementar betweenness (Brandes)'; role='analista'; want='medir intermediacao de vertices'; value='detectar pontos de passagem da colaboracao'; files=@('src/analysis/centrality.py','tests/test_analysis.py'); blockedBy=@('STORY-4.1.1'); points=5 },
        @{ id='STORY-4.1.3'; title='Implementar closeness e pagerank'; role='analista'; want='medir proximidade e relevancia global'; value='complementar analise de influencia'; files=@('src/analysis/centrality.py','tests/test_analysis.py'); blockedBy=@('STORY-4.1.1'); points=5 }
    )},
    @{ id='FEAT-4.2'; title='Metricas de estrutura e coesao'; desc='Implementar densidade, clustering e assortatividade para redes dirigidas.'; files=@('src/analysis/structure.py','tests/test_analysis.py','src/graph/abstract_graph.py'); dep='FEAT-2.2, FEAT-3.6'; points=5; frente='frente-4'; area='analysis'; stories=@(
        @{ id='STORY-4.2.1'; title='Calcular densidade da rede'; role='analista'; want='obter E/(V*(V-1))'; value='medir nivel de conexao global'; files=@('src/analysis/structure.py','tests/test_analysis.py'); blockedBy=@('STORY-2.3.3'); points=2 },
        @{ id='STORY-4.2.2'; title='Calcular clustering local e global'; role='analista'; want='medir triadizacao da rede'; value='identificar coesao em grupos'; files=@('src/analysis/structure.py','tests/test_analysis.py'); blockedBy=@('STORY-4.2.1'); points=3 },
        @{ id='STORY-4.2.3'; title='Calcular assortatividade de grau'; role='analista'; want='medir correlacao de graus conectados'; value='entender padrao assortativo ou dissortativo'; files=@('src/analysis/structure.py','tests/test_analysis.py'); blockedBy=@('STORY-4.2.1'); points=3 }
    )},
    @{ id='FEAT-4.3'; title='Deteccao de comunidades'; desc='Implementar deteccao de comunidades, modularidade e arestas de ponte.'; files=@('src/analysis/community.py','tests/test_analysis.py','src/graph/abstract_graph.py'); dep='FEAT-2.2, FEAT-3.6'; points=8; frente='frente-4'; area='analysis'; stories=@(
        @{ id='STORY-4.3.1'; title='Detectar comunidades na rede'; role='analista'; want='separar vertices em grupos'; value='interpretar estrutura social do repositorio'; files=@('src/analysis/community.py','tests/test_analysis.py'); blockedBy=@('STORY-2.3.3'); points=5 },
        @{ id='STORY-4.3.2'; title='Calcular modularidade da particao'; role='analista'; want='avaliar qualidade da comunidade detectada'; value='comparar resultados de estrategia de agrupamento'; files=@('src/analysis/community.py','tests/test_analysis.py'); blockedBy=@('STORY-4.3.1'); points=3 },
        @{ id='STORY-4.3.3'; title='Identificar arestas de ponte'; role='analista'; want='achar ligacoes entre comunidades'; value='destacar conexoes criticas entre grupos'; files=@('src/analysis/community.py','tests/test_analysis.py'); blockedBy=@('STORY-4.3.1'); points=3 }
    )},
    @{ id='FEAT-4.4'; title='Geracao de relatorios de analise'; desc='Gerar arquivos de saida centrality.csv, structure.json e communities.csv.'; files=@('src/analysis/centrality.py','src/analysis/structure.py','src/analysis/community.py','output/reports/'); dep='FEAT-4.1, FEAT-4.2, FEAT-4.3'; points=3; frente='frente-4'; area='analysis'; stories=@(
        @{ id='STORY-4.4.1'; title='Gerar centrality.csv'; role='analista'; want='exportar metricas de centralidade'; value='fornecer base para ranking de usuarios'; files=@('src/analysis/centrality.py','tests/test_analysis.py'); blockedBy=@('STORY-4.1.1','STORY-4.1.2','STORY-4.1.3'); points=2 },
        @{ id='STORY-4.4.2'; title='Gerar structure.json'; role='analista'; want='exportar metricas estruturais'; value='consolidar indicadores globais do grafo'; files=@('src/analysis/structure.py','tests/test_analysis.py'); blockedBy=@('STORY-4.2.1','STORY-4.2.2','STORY-4.2.3'); points=2 },
        @{ id='STORY-4.4.3'; title='Gerar communities.csv'; role='analista'; want='exportar particao e pontes'; value='apoiar interpretacao de comunidades no relatorio'; files=@('src/analysis/community.py','tests/test_analysis.py'); blockedBy=@('STORY-4.3.1','STORY-4.3.2','STORY-4.3.3'); points=2 }
    )},
    @{ id='FEAT-4.5'; title='Testes da camada de analise'; desc='Cobrir algoritmos com grafos canonicos: vazio, estrela, ciclo e completo.'; files=@('tests/test_analysis.py','src/analysis/centrality.py','src/analysis/structure.py','src/analysis/community.py'); dep='FEAT-4.1, FEAT-4.2, FEAT-4.3, FEAT-4.4'; points=5; frente='frente-4'; area='testes'; stories=@(
        @{ id='STORY-4.5.1'; title='Criar fixtures de grafos canonicos'; role='QA'; want='reutilizar cenarios de teste deterministas'; value='aumentar confiabilidade dos testes'; files=@('tests/test_analysis.py'); blockedBy=@('STORY-2.3.2','STORY-2.4.2'); points=2 },
        @{ id='STORY-4.5.2'; title='Validar resultados esperados das metricas'; role='QA'; want='comparar metricas com valores conhecidos'; value='evitar erro matematico na implementacao'; files=@('tests/test_analysis.py','src/analysis/centrality.py','src/analysis/structure.py'); blockedBy=@('STORY-4.1.1','STORY-4.2.1'); points=3 },
        @{ id='STORY-4.5.3'; title='Validar robustez em edge cases'; role='QA'; want='testar grafo vazio e desconexo'; value='evitar quebra em entrada limite na apresentacao'; files=@('tests/test_analysis.py','src/analysis/community.py'); blockedBy=@('STORY-4.3.1'); points=2 }
    )}
)

# EPIC 5
$ep5 = @(
    @{ id='FEAT-5.1'; title='Demo completa da API de grafos'; desc='Criar aplicacao separada para demonstrar todas operacoes da API de grafo.'; files=@('src/app/api_demo.py','src/graph/abstract_graph.py','src/graph/adjacency_matrix_graph.py','src/graph/adjacency_list_graph.py'); dep='FEAT-2.2, FEAT-2.3, FEAT-2.4'; points=5; frente='frente-5'; area='app'; stories=@(
        @{ id='STORY-5.1.1'; title='Montar roteiro das operacoes obrigatorias'; role='desenvolvedor'; want='cobrir 18 operacoes da API'; value='atender exigencia explicita do enunciado'; files=@('src/app/api_demo.py'); blockedBy=@('STORY-2.2.1'); points=2 },
        @{ id='STORY-5.1.2'; title='Executar demo em matrix e list'; role='desenvolvedor'; want='mostrar consistencia entre implementacoes'; value='aumentar confianca na corretude da API'; files=@('src/app/api_demo.py','src/graph/adjacency_matrix_graph.py','src/graph/adjacency_list_graph.py'); blockedBy=@('STORY-2.3.3','STORY-2.4.3'); points=3 },
        @{ id='STORY-5.1.3'; title='Melhorar saida da demo para avaliacao'; role='desenvolvedor'; want='imprimir resultados claros por operacao'; value='facilitar validacao na banca'; files=@('src/app/api_demo.py'); blockedBy=@('STORY-5.1.1'); points=1 }
    )},
    @{ id='FEAT-5.2'; title='CLI principal para pipeline completo'; desc='Implementar comandos --mine, --build, --analyze e --all com tratamento de erro.'; files=@('src/app/main.py','src/mining/','src/builder/','src/analysis/'); dep='FEAT-1.6, FEAT-3.7, FEAT-4.5'; points=5; frente='frente-5'; area='app'; stories=@(
        @{ id='STORY-5.2.1'; title='Implementar flag --mine'; role='usuario do sistema'; want='executar somente mineracao'; value='depurar coleta de dados isoladamente'; files=@('src/app/main.py','src/mining/github_client.py','tests/test_mining.py'); blockedBy=@('STORY-1.6.3'); points=2 },
        @{ id='STORY-5.2.2'; title='Implementar flag --build'; role='usuario do sistema'; want='construir grafos a partir dos CSVs'; value='validar F3 sem rerodar mineracao'; files=@('src/app/main.py','src/builder/base_builder.py','tests/test_builder.py'); blockedBy=@('STORY-3.7.2'); points=2 },
        @{ id='STORY-5.2.3'; title='Implementar flag --analyze'; role='usuario do sistema'; want='gerar metricas dos grafos prontos'; value='inspecionar resultados da analise isoladamente'; files=@('src/app/main.py','src/analysis/centrality.py','tests/test_analysis.py'); blockedBy=@('STORY-4.5.2'); points=2 }
    )}
)

# EPIC 6
$ep6 = @(
    @{ id='FEAT-6.1'; title='Relatorio SBC em LaTeX'; desc='Consolidar metodologia, resultados e discussao no template SBC.'; files=@('report/main.tex','report/refs.bib','output/reports/'); dep='FEAT-4.4, FEAT-5.2'; points=8; frente='frente-6'; area='relatorio'; stories=@(
        @{ id='STORY-6.1.1'; title='Descrever modelagem dos grafos G1..G4'; role='autor do relatorio'; want='explicar vertices, arestas e pesos'; value='demonstrar aderencia teorica ao trabalho'; files=@('report/main.tex'); blockedBy=@('STORY-3.6.3'); points=2 },
        @{ id='STORY-6.1.2'; title='Descrever arquitetura por frentes'; role='autor do relatorio'; want='documentar fluxo F1-F4 e app'; value='evidenciar organizacao e responsabilidades'; files=@('report/main.tex'); blockedBy=@('STORY-5.2.3'); points=2 },
        @{ id='STORY-6.1.3'; title='Inserir resultados de centralidade e estrutura'; role='autor do relatorio'; want='apresentar tabelas e analise critica'; value='sustentar conclusoes com dados'; files=@('report/main.tex','output/reports/'); blockedBy=@('STORY-4.4.1','STORY-4.4.2'); points=3 }
    )},
    @{ id='FEAT-6.2'; title='Video de demonstracao'; desc='Produzir roteiro e gravacao da execucao do pipeline e leitura dos resultados.'; files=@('report/main.tex','output/graphs/','output/reports/'); dep='FEAT-5.1, FEAT-5.2'; points=3; frente='frente-6'; area='entrega'; stories=@(
        @{ id='STORY-6.2.1'; title='Definir roteiro de demonstracao'; role='apresentador'; want='mostrar fluxo completo em ordem correta'; value='evitar omissao de requisito na avaliacao'; files=@('report/main.tex'); blockedBy=@('STORY-5.1.3','STORY-5.2.3'); points=1 },
        @{ id='STORY-6.2.2'; title='Gravar execucao do pipeline'; role='apresentador'; want='capturar mine, build, analyze e demo'; value='provar funcionamento ponta a ponta'; files=@('output/graphs/','output/reports/'); blockedBy=@('STORY-5.2.3'); points=2 },
        @{ id='STORY-6.2.3'; title='Validar legibilidade tecnica do video'; role='QA de entrega'; want='confirmar audio, texto e evidencias'; value='maximizar clareza e pontuacao da apresentacao'; files=@('report/main.tex'); blockedBy=@('STORY-6.2.2'); points=1 }
    )},
    @{ id='FEAT-6.3'; title='Preparacao para apresentacao presencial'; desc='Organizar checklist final de entrega, riscos e perguntas esperadas da banca.'; files=@('report/main.tex','README.md','github-graph-analyzer/README.MD'); dep='FEAT-6.1, FEAT-6.2'; points=3; frente='frente-6'; area='entrega'; stories=@(
        @{ id='STORY-6.3.1'; title='Montar checklist tecnico final'; role='lider tecnico'; want='confirmar requisitos e restricoes atendidos'; value='evitar perda de pontos por item faltante'; files=@('README.md','github-graph-analyzer/README.MD'); blockedBy=@('STORY-6.1.3'); points=1 },
        @{ id='STORY-6.3.2'; title='Mapear perguntas provaveis e respostas'; role='lider tecnico'; want='preparar defesa da implementacao'; value='melhorar desempenho na arguicao'; files=@('report/main.tex'); blockedBy=@('STORY-6.3.1'); points=1 },
        @{ id='STORY-6.3.3'; title='Executar dry-run da apresentacao'; role='equipe'; want='simular tempo e transicoes'; value='reduzir risco de falha na banca'; files=@('report/main.tex','README.md'); blockedBy=@('STORY-6.2.3','STORY-6.3.2'); points=1 }
    )}
)

New-EpicFile -epicId '1' -epicTitle 'Mining' -epicDesc 'Implementar coleta robusta no github/spec-kit com autenticacao, resiliencia e exportacao CSV para as demais frentes.' -filePath (Join-Path $cardsDir '[EPIC] 1 - Mining.md') -features $ep1
New-EpicFile -epicId '2' -epicTitle 'Graph Structures' -epicDesc 'Implementar estruturas de grafo direcionado simples do zero, com API completa e exportacao GEXF.' -filePath (Join-Path $cardsDir '[EPIC] 2 - Graph Structures.md') -features $ep2
New-EpicFile -epicId '3' -epicTitle 'Builders' -epicDesc 'Transformar CSVs minerados em grafos G1, G2, G3 e G4 usando registry de usuarios e regras de peso.' -filePath (Join-Path $cardsDir '[EPIC] 3 - Builders.md') -features $ep3
New-EpicFile -epicId '4' -epicTitle 'Analysis' -epicDesc 'Implementar metricas de centralidade, estrutura e comunidades, com relatorios para interpretacao da rede.' -filePath (Join-Path $cardsDir '[EPIC] 4 - Analysis.md') -features $ep4
New-EpicFile -epicId '5' -epicTitle 'App Integracao' -epicDesc 'Integrar pipeline de execucao e demonstracao da API de grafos para validacao de ponta a ponta.' -filePath (Join-Path $cardsDir '[EPIC] 5 - App Integracao.md') -features $ep5
New-EpicFile -epicId '6' -epicTitle 'Relatorio Entregaveis' -epicDesc 'Consolidar relatorio, video e preparacao final da apresentacao conforme requisitos da disciplina.' -filePath (Join-Path $cardsDir '[EPIC] 6 - Relatorio Entregaveis.md') -features $ep6

Write-Output 'Epic card files regenerated successfully.'
