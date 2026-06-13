import { useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import ExportModal from '@/components/graph/ExportModal'
import GraphCanvas from '@/components/graph/GraphCanvas'
import GraphSidebar from '@/components/graph/GraphSidebar'
import MetricsPanel from '@/components/graph/MetricsPanel'
import Navbar from '@/components/layout/Navbar'
import { useGraphStore } from '@/stores/graphStore'
import { fetchGraphGexf, fetchReport } from '@/utils/api'
import { buildCommunityMap } from '@/utils/communityColors'
import { parseCSVCommunities, parseCSVMetrics, parseGEXF } from '@/utils/gexfParser'
import { loadCachedGexf } from '@/utils/recentGraphs'
import type { GraphType } from '@/types/graph'

export default function VisualizePage() {
  const { graphId } = useParams()
  const navigate = useNavigate()
  const {
    graphs,
    currentGraph,
    loadGraph,
    setCurrentGraphByType,
    loadMetrics,
    loadCommunities,
  } = useGraphStore()

  useEffect(() => {
    const type = graphId as GraphType | undefined
    if (!type) return

    const existing = graphs.find((graph) => graph.type === type)
    if (existing) {
      setCurrentGraphByType(type)
    } else {
      const loadFromXml = (xml: string, source: 'api' | 'upload') => {
        const graph = parseGEXF(xml, type)
        loadGraph(graph, source)
        setCurrentGraphByType(type)
      }

      fetchGraphGexf(type)
        .then((xml) => loadFromXml(xml, 'api'))
        .catch(() => {
          const cached = loadCachedGexf(type)
          if (cached) {
            loadFromXml(cached, 'upload')
          } else {
            navigate('/')
          }
        })
    }

    fetchReport('centrality.csv')
      .then((csv) => loadMetrics(parseCSVMetrics(csv)))
      .catch(() => undefined)

    fetchReport('communities.csv')
      .then((csv) => loadCommunities(buildCommunityMap(parseCSVCommunities(csv), type)))
      .catch(() => loadCommunities({}))
  }, [graphId, graphs, loadGraph, setCurrentGraphByType, loadMetrics, loadCommunities, navigate])

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Navbar />

      <div className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/" className="text-sm text-blue-600 hover:underline">
            ← Voltar
          </Link>
          <h1 className="text-lg font-semibold text-gray-800">
            {currentGraph?.name ?? 'Visualização do Grafo'}
          </h1>
        </div>
        <span className="text-sm text-gray-500">Grafo dirigido · Vis-Network</span>
      </div>

      <div className="flex flex-1 min-h-0">
        <GraphSidebar />
        <main className="flex-1 min-w-0 relative">
          <GraphCanvas />
        </main>
      </div>

      <ExportModal />
      <MetricsPanel />
    </div>
  )
}
