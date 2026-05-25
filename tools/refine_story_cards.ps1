Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$NL = [Environment]::NewLine

function Method-Hints {
    param([string]$path)
    switch -Regex ($path) {
        'src/mining/github_client.py' { return @('-> request_with_retry(self, op_name: str, operation: callable, max_retries: int = 5, base_delay: float = 0.5) -> object','-> get_repo(self, full_name: str) -> Repository','-> _is_retryable_error(self, error: Exception) -> bool') }
        'src/mining/issue_miner.py' { return @('-> mine(self, repo_full_name: str) -> list[Interaction]','-> _extract_issue_interactions(self, issue: object) -> list[Interaction]','-> _should_skip_self_interaction(self, src_login: str, dst_login: str) -> bool') }
        'src/mining/pr_miner.py' { return @('-> mine(self, repo_full_name: str) -> list[Interaction]','-> _extract_pr_interactions(self, pr: object) -> list[Interaction]','-> _map_review_type(self, review_state: str) -> str') }
        'src/mining/interaction_model.py' { return @('-> dataclass Interaction','-> __post_init__(self) -> None') }
        'src/mining/data_exporter.py' { return @('-> export_users_csv(self, users: list[dict], output_path: str) -> str','-> export_interactions_csv(self, interactions: list[Interaction], output_path: str) -> str','-> _ensure_output_dir(self, output_path: str) -> None') }
        'src/graph/exceptions.py' { return @('-> class InvalidVertexError(Exception)','-> class SelfLoopError(Exception)','-> class EdgeNotFoundError(Exception)') }
        'src/graph/abstract_graph.py' { return @('-> _validate_vertex(self, v: int) -> None','-> add_edge(self, u: int, v: int) -> None','-> export_to_gephi(self, path: str) -> None') }
        'src/graph/adjacency_matrix_graph.py' { return @('-> add_edge(self, u: int, v: int) -> None','-> remove_edge(self, u: int, v: int) -> None','-> has_edge(self, u: int, v: int) -> bool') }
        'src/graph/adjacency_list_graph.py' { return @('-> add_edge(self, u: int, v: int) -> None','-> remove_edge(self, u: int, v: int) -> None','-> get_vertex_out_degree(self, u: int) -> int') }
        'src/graph/gephi_exporter.py' { return @('-> export(graph: AbstractGraph, path: str) -> str','-> _build_nodes_xml(graph: AbstractGraph) -> str','-> _build_edges_xml(graph: AbstractGraph) -> str') }
        'src/builder/user_registry.py' { return @('-> add_user(self, login: str) -> int','-> get_index(self, login: str) -> int','-> get_login(self, index: int) -> str') }
        'src/builder/base_builder.py' { return @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]','-> _filter_interactions(self, rows: list[dict]) -> list[dict]','-> _apply_interaction(self, graph: AbstractGraph, row: dict) -> None') }
        'src/builder/graph1_comments_builder.py' { return @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]') }
        'src/builder/graph2_closures_builder.py' { return @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]') }
        'src/builder/graph3_reviews_builder.py' { return @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]') }
        'src/builder/graph4_integrated_builder.py' { return @('-> build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]','-> _sum_weight(self, current: float, inc: float) -> float') }
        'src/analysis/centrality.py' { return @('-> degree_centrality(graph: AbstractGraph) -> dict[int, float]','-> betweenness_centrality(graph: AbstractGraph) -> dict[int, float]','-> pagerank(graph: AbstractGraph, damping: float = 0.85, tol: float = 1e-6) -> dict[int, float]') }
        'src/analysis/structure.py' { return @('-> density(graph: AbstractGraph) -> float','-> clustering_coefficient(graph: AbstractGraph) -> float','-> degree_assortativity(graph: AbstractGraph) -> float') }
        'src/analysis/community.py' { return @('-> detect_communities(graph: AbstractGraph) -> list[set[int]]','-> modularity(graph: AbstractGraph, partition: list[set[int]]) -> float','-> bridging_ties(graph: AbstractGraph, partition: list[set[int]]) -> list[tuple[int,int]]') }
        'src/app/main.py' { return @('-> run_mine() -> int','-> run_build() -> int','-> run_analyze() -> int') }
        'src/app/api_demo.py' { return @('-> run_demo() -> None') }
        default { return @('-> metodo_publico_1(parametros) -> tipo_retorno','-> _metodo_privado_auxiliar(parametros) -> None') }
    }
}

function Section-Body {
    param([string]$block,[string]$headingKeyword)
    $m=[regex]::Match($block,'(?ms)^## .*'+[regex]::Escape($headingKeyword)+'.*\r?\n(.*?)(?=^## [^\r\n]+|\z)')
    if($m.Success){ return $m.Groups[1].Value.TrimEnd() }
    return ''
}

function Refine-Story {
    param([string]$block)
    if($block -notmatch '(?m)^## CARD STORY-'){ return $block }
    if($block -match '(?m)^## .*Testes'){ return $block }

    $storyId=[regex]::Match($block,'(?m)^## CARD (STORY-[0-9.]+)').Groups[1].Value
    $sp=[regex]::Match($block,'(?m)^Story Points:\s*(.+)$').Groups[1].Value.Trim()
    if(-not $sp){ $sp='3' }

    $esc=Section-Body $block 'Escopo Funcional'
    $rel=@()
    foreach($l in ($esc -split '\r?\n')){
        if($l -match 'github-graph-analyzer/(.+?)(?:\s*\(|$)'){ $rel += $Matches[1].Trim() }
    }
    $rel=$rel | Select-Object -Unique

    $impl = New-Object System.Collections.Generic.List[string]
    $impl.Add('## 🛠️ Implementação (Alto Nível)'); $impl.Add('')
    foreach($p in $rel){
        if($p -like 'tests/*'){ continue }
        $name=[IO.Path]::GetFileName($p)
        $impl.Add('#### '+$name+' (EXISTENTE — MODIFICAR)')
        $impl.Add('Criar em: '+$p)
        $impl.Add('Seguir padrão de: '+$p)
        $impl.Add('')
        $impl.Add('Lógica existente (NÃO alterar):')
        $impl.Add('-> Estrutura base já planejada no card e no README técnico da frente.')
        $impl.Add('')
        $impl.Add('Lógica NOVA a adicionar:')
        foreach($h in (Method-Hints $p)){ $impl.Add($h) }
        $impl.Add('')
    }
    if(@($rel | Where-Object { $_ -like 'src/*' }).Count -eq 0){
        $impl.Add('#### src/modulo/arquivo.py (NOVO — CRIAR)')
        $impl.Add('Criar em: src/modulo/arquivo.py')
        $impl.Add('Seguir padrão de: src/modulo/__init__.py')
        $impl.Add('-> metodo_publico_1(parametros) -> tipo_retorno')
        $impl.Add('-> _metodo_privado_auxiliar(parametros) -> None')
        $impl.Add('')
    }

    $testsFile=($rel | Where-Object { $_ -like 'tests/test_*.py' } | Select-Object -First 1)
    if(-not $testsFile){
        if($storyId -like 'STORY-1*'){ $testsFile='tests/test_mining.py' }
        elseif($storyId -like 'STORY-2*'){ $testsFile='tests/test_graph_matrix.py' }
        elseif($storyId -like 'STORY-3*'){ $testsFile='tests/test_builder.py' }
        elseif($storyId -like 'STORY-4*'){ $testsFile='tests/test_analysis.py' }
        else { $testsFile='tests/test_app.py' }
    }

    $safe=($storyId -replace '[^0-9]','_')
    $tests=@(
        '## Testes','',
        'Arquivo: '+$testsFile,'',
        '-> test_'+$safe+'_cenario_feliz() — valida cenário principal.',
        '-> test_'+$safe+'_cenario_alternativo() — valida cenário alternativo.',
        '-> test_'+$safe+'_edge_case_erro() — valida cenário de erro.',
        '-> test_'+$safe+'_idempotencia_ou_invariante() — valida invariante relevante.','',
        'Fixtures necessárias: mocks da API/IO, dados sintéticos e controle de tempo quando aplicável.',
        'Cobertura mínima: 80%.'
    )

    $depRaw=[regex]::Match($block,'(?m)^-\s*Dependencias:\s*(.+)$').Groups[1].Value.Trim()
    if(-not $depRaw){ $depRaw='nenhuma' }
    $blockedBy = if($depRaw -eq 'nenhuma'){ 'nenhuma' } else { '['+(($depRaw -split ',') | ForEach-Object { $_.Trim() } | Where-Object { $_ } ) -join ', '+']' }
    $importFrom=($rel | Where-Object { $_ -like 'src/*' }) -join ', '
    if(-not $importFrom){ $importFrom='N/A' }

    $cli='python -m src.app.main --all'
    if($storyId -like 'STORY-1*'){ $cli='python -m src.app.main --mine' }
    elseif($storyId -like 'STORY-2*'){ $cli='python -m src.app.api_demo' }
    elseif($storyId -like 'STORY-3*'){ $cli='python -m src.app.main --build' }
    elseif($storyId -like 'STORY-4*'){ $cli='python -m src.app.main --analyze' }

    $edge=@(
        '## Edge Cases e Excecoes','',
        '- Entrada inválida/ausente -> lançar exceção clara de domínio com mensagem acionável.',
        '- Dado inexistente no dataset/API -> logar warning e continuar quando seguro.',
        '- Falha transitória (rede/rate limit) -> aplicar retry/backoff e retomar sem quebra abrupta.'
    )
    if($storyId -like 'STORY-2*'){
        $edge += '- Índice de vértice fora do intervalo -> lançar InvalidVertexError.'
        $edge += '- Tentativa de laço em grafo simples -> lançar SelfLoopError.'
    }

    $labels='frente, python, story'
    if($storyId -like 'STORY-1*'){ $labels='frente-1, mining, python, story' }
    elseif($storyId -like 'STORY-2*'){ $labels='frente-2, graph, python, story' }
    elseif($storyId -like 'STORY-3*'){ $labels='frente-3, builder, python, story' }
    elseif($storyId -like 'STORY-4*'){ $labels='frente-4, analysis, python, story' }
    elseif($storyId -like 'STORY-5*'){ $labels='frente-5, app, python, story' }
    elseif($storyId -like 'STORY-6*'){ $labels='frente-6, report, docs, story' }

    $dod=Section-Body $block 'Defin'
    if(-not $dod){ $dod='- [ ] Implementação concluída com testes e documentação mínima.' }

    $new=@()
    $new += $impl
    $new += ''
    $new += '## Definicao de Pronto (DoD)'; $new += ''; $new += $dod
    $new += ''
    $new += $tests
    $new += ''
    $new += @('## Dependencias','',
        '- Bloqueia: [A definir durante planejamento fino da sprint]',
        '- Bloqueado por: '+$blockedBy,
        '- Importa de: '+$importFrom,
        '- É importado por: módulos da mesma frente e orquestração em src/app/main.py.')
    $new += ''
    $new += @('## Endpoints / CLI / API Publica','',
        '- '+$cli+' — entrada pública da frente.')
    $new += ''
    $new += $edge
    $new += ''
    $new += @('## Estimativa','',
        'Story Points: '+$sp,
        'Justificativa: complexidade compatível com regras de negócio, integração entre módulos e cobertura de testes exigida.')
    $new += ''
    $new += @('## Labels','',$labels)

    $replacement = ($new -join $NL)
    return [regex]::Replace($block,'(?ms)## .*Implement.*\r?\n.*?(?=\r?\n## .*Regras)',$replacement,1)
}

$cards = Get-ChildItem '.github/plans/cards' -File | Where-Object { $_.Name -like '[[]EPIC[]]*.md' }
foreach($f in $cards){
    $txt=[System.IO.File]::ReadAllText($f.FullName)
    $matches=[regex]::Matches($txt,'(?ms)^## CARD STORY-.*?(?=^## CARD |\z)')
    if($matches.Count -eq 0){ continue }
    $sb=New-Object Text.StringBuilder
    $cursor=0
    foreach($m in $matches){
        $null=$sb.Append($txt.Substring($cursor,$m.Index-$cursor))
        $null=$sb.Append((Refine-Story $m.Value))
        $cursor=$m.Index+$m.Length
    }
    if($cursor -lt $txt.Length){ $null=$sb.Append($txt.Substring($cursor)) }
    [System.IO.File]::WriteAllText($f.FullName,$sb.ToString(),[Text.Encoding]::UTF8)
}

Write-Output ('Refinement completed for '+$cards.Count+' EPIC files.')
