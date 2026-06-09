import { useMemo, useState } from 'react'
import { useGraphStore } from '@/stores/graphStore'
import { useUIStore } from '@/stores/uiStore'
import { colorForCommunity } from '@/utils/communityColors'

type MetricTab = 'pagerank' | 'betweenness' | 'degree_in' | 'closeness'

export default function MetricsPanel() {
  const { metricsPanelOpen, closeMetricsPanel } = useUIStore()
  const {
    currentGraph,
    metrics,
    communities,
    colorByCommunity,
    setColorByCommunity,
    focusOnVertex,
  } = useGraphStore()
  const [activeTab, setActiveTab] = useState<MetricTab>('pagerank')

  const graphMetrics = useMemo(
    () => metrics.filter((item) => item.graph === currentGraph?.type),
    [metrics, currentGraph],
  )

  const topVertices = useMemo(() => {
    return [...graphMetrics].sort((a, b) => b[activeTab] - a[activeTab]).slice(0, 10)
  }, [graphMetrics, activeTab])

  const communityLegend = useMemo(() => {
    const ids = new Set<number>()
    if (!currentGraph) return []
    for (const [login, id] of Object.entries(communities)) {
      if (graphMetrics.some((metric) => metric.login === login)) {
        ids.add(id)
      }
    }
    return [...ids].sort((a, b) => a - b).slice(0, 12)
  }, [communities, currentGraph, graphMetrics])

  if (!metricsPanelOpen || !currentGraph) return null

  const weights = currentGraph.edges.map((edge) => edge.weight ?? 0).filter((value) => value > 0)
  const maxWeight = weights.length ? Math.max(...weights) : 0
  const minWeightVal = weights.length ? Math.min(...weights) : 0
  const hasCommunities = Object.keys(communities).length > 0

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl border-l border-gray-200 p-6 overflow-y-auto z-40">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Métricas</h2>
        <button type="button" onClick={closeMetricsPanel} className="text-2xl text-gray-500">
          ×
        </button>
      </div>

      {currentGraph.metadata.weighted && (
        <div className="grid grid-cols-2 gap-3 mb-6">
          <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-3">
            <p className="text-xs text-emerald-700">Maior Peso</p>
            <p className="text-2xl font-bold text-emerald-800">{maxWeight.toFixed(1)}</p>
          </div>
          <div className="bg-red-50 border border-red-200 rounded-lg p-3">
            <p className="text-xs text-red-700">Menor Peso</p>
            <p className="text-2xl font-bold text-red-800">{minWeightVal.toFixed(1)}</p>
          </div>
        </div>
      )}

      {hasCommunities && (
        <div className="mb-6">
          <button
            type="button"
            onClick={() => setColorByCommunity(!colorByCommunity)}
            className={`w-full py-2.5 rounded-lg font-medium text-sm border ${
              colorByCommunity
                ? 'bg-violet-600 text-white border-violet-600'
                : 'border-gray-300 hover:bg-gray-50'
            }`}
          >
            {colorByCommunity ? '✓ Colorindo por comunidade' : 'Colorir por comunidade'}
          </button>
          {colorByCommunity && communityLegend.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-3">
              {communityLegend.map((id) => (
                <span
                  key={id}
                  className="inline-flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-gray-100"
                >
                  <span
                    className="w-3 h-3 rounded-full inline-block"
                    style={{ backgroundColor: colorForCommunity(id) }}
                  />
                  C{id}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {graphMetrics.length === 0 ? (
        <p className="text-sm text-gray-500">Execute a análise (Etapa 3) para carregar métricas.</p>
      ) : (
        <>
          <div className="flex flex-wrap border-b border-gray-200 mb-4 text-xs">
            {(['pagerank', 'betweenness', 'degree_in', 'closeness'] as MetricTab[]).map((tab) => (
              <button
                key={tab}
                type="button"
                onClick={() => setActiveTab(tab)}
                className={`flex-1 min-w-[4.5rem] py-2 capitalize ${
                  activeTab === tab ? 'border-b-2 border-blue-600 text-blue-600 font-medium' : 'text-gray-500'
                }`}
              >
                {tab.replace('_', ' ')}
              </button>
            ))}
          </div>
          <ul className="space-y-2">
            {topVertices.map((vertex, index) => (
              <li key={vertex.login}>
                <button
                  type="button"
                  onClick={() => focusOnVertex(vertex.login)}
                  className="w-full flex justify-between items-center p-2 rounded hover:bg-blue-50 text-sm text-left"
                >
                  <span>
                    <span className="text-gray-400 mr-2">#{index + 1}</span>
                    {vertex.login}
                  </span>
                  <span className="font-semibold text-blue-600">{vertex[activeTab].toFixed(4)}</span>
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  )
}
