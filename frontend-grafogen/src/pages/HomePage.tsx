import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import GraphTypeCard from '@/components/home/GraphTypeCard'
import Navbar from '@/components/layout/Navbar'
import LogsModal from '@/components/pipeline/LogsModal'
import PipelineCard from '@/components/pipeline/PipelineCard'
import { usePipelineStatus } from '@/hooks/usePipelineStatus'
import { useGraphStore } from '@/stores/graphStore'
import { usePipelineStore } from '@/stores/pipelineStore'
import { cancelPipeline, fetchGraphGexf, fetchReport, runPipelineStage } from '@/utils/api'
import { parseCSVMetrics, parseGEXF } from '@/utils/gexfParser'
import { cacheUploadedGexf } from '@/utils/recentGraphs'
import type { GraphType } from '@/types/graph'

const GRAPH_CARDS = [
  {
    type: 'G1' as GraphType,
    title: 'G1 - Comentários',
    subtitle: 'Grafo Direcionado',
    description: 'Interações via comentários em issues e pull requests.',
    example: 'Peso: 2 por comentário',
    icon: '💬',
    colorClass: 'bg-blue-500',
  },
  {
    type: 'G2' as GraphType,
    title: 'G2 - Fechamentos',
    subtitle: 'Grafo Direcionado',
    description: 'Fechamento de issues por outros colaboradores.',
    example: 'Peso: 3 por fechamento',
    icon: '✔️',
    colorClass: 'bg-emerald-500',
  },
  {
    type: 'G3' as GraphType,
    title: 'G3 - Reviews',
    subtitle: 'Grafo Direcionado',
    description: 'Reviews, aprovações e merges de pull requests.',
    example: 'Peso: 4 (review) / 5 (merge)',
    icon: '👁️',
    colorClass: 'bg-violet-500',
  },
  {
    type: 'G4' as GraphType,
    title: 'G4 - Integrado',
    subtitle: 'Grafo Ponderado',
    description: 'Todas as interações combinadas com pesos acumulados.',
    example: 'Pesos: 2 a 5+',
    icon: '🌐',
    colorClass: 'bg-orange-500',
  },
]

function stageStatus(done: boolean, running: boolean): 'idle' | 'running' | 'done' | 'error' {
  if (running) return 'running'
  return done ? 'done' : 'idle'
}

export default function HomePage() {
  const navigate = useNavigate()
  const refresh = usePipelineStatus()
  const { status, logsOpen, setLogsOpen } = usePipelineStore()
  const { loadGraph, loadMetrics, setCurrentGraphByType, recentGraphs, refreshRecentGraphs } = useGraphStore()
  const [busyStage, setBusyStage] = useState<string | null>(null)
  const [uploadType, setUploadType] = useState<GraphType>('G1')
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    refreshRecentGraphs()
  }, [refreshRecentGraphs])

  const openGraph = async (type: GraphType) => {
    const xml = await fetchGraphGexf(type)
    const graph = parseGEXF(xml, type)
    loadGraph(graph, 'api')
    setCurrentGraphByType(type)
    navigate(`/visualize/${type}`)
  }

  const openRecent = (type: GraphType) => {
    navigate(`/visualize/${type}`)
  }

  const handleUpload = async (file: File) => {
    const xml = await file.text()
    const graph = parseGEXF(xml, uploadType)
    cacheUploadedGexf(uploadType, xml)
    loadGraph(graph, 'upload')
    setCurrentGraphByType(uploadType)
    navigate(`/visualize/${uploadType}`)
  }

  const executeStage = async (stage: 'mine' | 'build' | 'analyze') => {
    setBusyStage(stage)
    try {
      await runPipelineStage(stage)
      if (stage === 'analyze') {
        const csv = await fetchReport('centrality.csv')
        loadMetrics(parseCSVMetrics(csv))
      }
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Falha na execução')
    } finally {
      setBusyStage(null)
      await refresh()
    }
  }

  const running = status?.pipelineRunning || busyStage !== null

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <main className="max-w-7xl mx-auto px-6 py-10">
        <section className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-3">
            Bem-vindo ao <span className="text-blue-600">GrafoGen</span>
          </h1>
          <p className="text-lg text-gray-600">Visualização interativa de redes de colaboração GitHub</p>
          <p className="text-sm text-gray-500 mt-2">
            Repositório: {status?.repository ?? 'github/spec-kit'} · Teoria de Grafos — PUC Minas 2026/1
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Pipeline de Execução</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <PipelineCard
              title="Etapa 1: Mineração"
              description="Coleta interações do repositório via API GitHub"
              status={stageStatus(!!status?.stage1Complete, running && busyStage === 'mine')}
              detail={status?.stage1Complete ? `${status.interactionCount.toLocaleString()} interações` : undefined}
              onExecute={() => executeStage('mine')}
              onCancel={() => cancelPipeline()}
              onViewLogs={() => setLogsOpen(true)}
            />
            <PipelineCard
              title="Etapa 2: Construção"
              description="Gera os 4 grafos GEXF a partir dos CSVs"
              status={stageStatus(!!status?.stage2Complete, running && busyStage === 'build')}
              detail={status?.stage2Complete ? '4 grafos gerados' : undefined}
              disabled={!status?.stage1Complete}
              disabledReason="Execute a mineração primeiro"
              onExecute={() => executeStage('build')}
              onCancel={() => cancelPipeline()}
              onViewLogs={() => setLogsOpen(true)}
            />
            <PipelineCard
              title="Etapa 3: Análise"
              description="Calcula centralidade, comunidades e estrutura"
              status={stageStatus(!!status?.stage3Complete, running && busyStage === 'analyze')}
              detail={status?.stage3Complete ? 'Métricas calculadas' : undefined}
              disabled={!status?.stage2Complete}
              disabledReason="Gere os grafos primeiro"
              onExecute={() => executeStage('analyze')}
              onCancel={() => cancelPipeline()}
              onViewLogs={() => setLogsOpen(true)}
            />
          </div>
        </section>

        {!status?.stage2Complete && !status?.stage1Complete && (
          <section className="text-center py-12 mb-12 bg-white rounded-xl shadow-sm border">
            <div className="text-5xl mb-4">🔍</div>
            <h3 className="text-2xl font-bold text-gray-700 mb-2">Dados ainda não processados</h3>
            <p className="text-gray-500 mb-6">Execute o pipeline ou use os arquivos já gerados pelo backend.</p>
          </section>
        )}

        <section className="mb-12 bg-white rounded-xl shadow-sm border p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Importar GEXF</h2>
          <p className="text-sm text-gray-500 mb-4">
            Carregue um arquivo `.gexf` exportado pelo backend ou pelo Gephi. Selecione o tipo correspondente.
          </p>
          <div className="flex flex-wrap items-end gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tipo do grafo</label>
              <select
                value={uploadType}
                onChange={(event) => setUploadType(event.target.value as GraphType)}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="G1">G1 — Comentários</option>
                <option value="G2">G2 — Fechamentos</option>
                <option value="G3">G3 — Reviews</option>
                <option value="G4">G4 — Integrado</option>
              </select>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept=".gexf,application/xml,text/xml"
              className="hidden"
              onChange={(event) => {
                const file = event.target.files?.[0]
                if (file) {
                  handleUpload(file).catch((error) => {
                    alert(error instanceof Error ? error.message : 'Falha ao importar GEXF')
                  })
                }
                event.target.value = ''
              }}
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="px-4 py-2 bg-gray-800 text-white rounded-lg text-sm hover:bg-gray-900"
            >
              Escolher arquivo…
            </button>
          </div>
        </section>

        {recentGraphs.length > 0 && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Grafos recentes</h2>
            <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {recentGraphs.map((entry) => (
                <li key={`${entry.type}-${entry.openedAt}`}>
                  <button
                    type="button"
                    onClick={() => openRecent(entry.type)}
                    className="w-full text-left p-4 bg-white rounded-lg border hover:border-blue-400 hover:shadow-sm transition"
                  >
                    <p className="font-semibold text-gray-800">{entry.name}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {entry.vertexCount} vértices · {entry.edgeCount} arestas
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {entry.source === 'upload' ? 'Importado' : 'Pipeline'} ·{' '}
                      {new Date(entry.openedAt).toLocaleString('pt-BR')}
                    </p>
                  </button>
                </li>
              ))}
            </ul>
          </section>
        )}

        <section>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Grafos do Trabalho</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {GRAPH_CARDS.map((card) => {
              const summary = status?.graphs.find((graph) => graph.type === card.type)
              return (
                <GraphTypeCard
                  key={card.type}
                  type={card.type}
                  title={card.title}
                  subtitle={card.subtitle}
                  description={card.description}
                  example={card.example}
                  icon={card.icon}
                  colorClass={card.colorClass}
                  vertexCount={summary?.vertexCount ?? 0}
                  edgeCount={summary?.edgeCount ?? 0}
                  available={!!summary?.available}
                  onOpen={() => openGraph(card.type)}
                />
              )
            })}
          </div>
        </section>
      </main>

      <LogsModal open={logsOpen} logs={status?.logs ?? []} onClose={() => setLogsOpen(false)} />
    </div>
  )
}
