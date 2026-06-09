import { useEffect, useMemo } from 'react'
import type { GraphType } from '@/types/graph'
import { useGraphStore } from '@/stores/graphStore'
import { useUIStore } from '@/stores/uiStore'

function maxEdgeWeight(edges: { weight?: number }[]): number {
  const weights = edges.map((edge) => edge.weight ?? 0).filter((value) => value > 0)
  return weights.length ? Math.max(...weights) : 1
}

function weightSliderStep(max: number): number {
  if (max <= 20) return 0.5
  if (max <= 100) return 1
  return Math.max(1, Math.ceil(max / 100))
}

const GRAPH_OPTIONS: { type: GraphType; label: string }[] = [
  { type: 'G1', label: 'G1 - Comentários' },
  { type: 'G2', label: 'G2 - Fechamentos' },
  { type: 'G3', label: 'G3 - Reviews' },
  { type: 'G4', label: 'G4 - Integrado' },
]

export default function GraphSidebar() {
  const { graphs, currentGraph, setCurrentGraphByType, minWeight, setMinWeight, searchQuery, setSearchQuery, focusOnVertex } =
    useGraphStore()
  const { openExportModal, openMetricsPanel } = useUIStore()

  const maxWeight = useMemo(
    () => (currentGraph ? maxEdgeWeight(currentGraph.edges) : 1),
    [currentGraph],
  )
  const sliderStep = weightSliderStep(maxWeight)

  useEffect(() => {
    if (minWeight > maxWeight) setMinWeight(maxWeight)
  }, [maxWeight, minWeight, setMinWeight])

  return (
    <aside className="w-80 bg-white border-r border-gray-200 p-6 overflow-y-auto shrink-0">
      <h2 className="text-xl font-bold text-gray-800 mb-6">Configuração</h2>

      <label className="block text-sm font-medium text-gray-700 mb-2">Selecionar Grafo</label>
      <select
        className="w-full border border-gray-300 rounded-lg px-3 py-2 mb-6 text-sm"
        value={currentGraph?.type ?? ''}
        onChange={(event) => setCurrentGraphByType(event.target.value as GraphType)}
      >
        <option value="">Selecione...</option>
        {GRAPH_OPTIONS.filter((option) => graphs.some((graph) => graph.type === option.type)).map((option) => (
          <option key={option.type} value={option.type}>
            {option.label}
          </option>
        ))}
      </select>

      {currentGraph && (
        <div className="bg-gray-50 rounded-lg p-4 mb-6 text-sm text-gray-600 space-y-1">
          <p>
            <strong>Vértices:</strong> {currentGraph.metadata.vertexCount}
          </p>
          <p>
            <strong>Arestas:</strong> {currentGraph.metadata.edgeCount}
          </p>
          <p>
            <strong>Tipo:</strong> Direcionado
          </p>
          <p>
            <strong>Ponderado:</strong> {currentGraph.metadata.weighted ? 'Sim' : 'Não'}
          </p>
        </div>
      )}

      <label className="block text-sm font-medium text-gray-700 mb-2">Buscar colaborador</label>
      <input
        type="text"
        value={searchQuery}
        onChange={(event) => setSearchQuery(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === 'Enter' && searchQuery.trim()) {
            focusOnVertex(searchQuery.trim())
          }
        }}
        placeholder="login do GitHub..."
        className="w-full border border-gray-300 rounded-lg px-3 py-2 mb-6 text-sm"
      />

      {currentGraph?.metadata.weighted && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Peso mínimo: {minWeight.toLocaleString('pt-BR', { maximumFractionDigits: maxWeight <= 20 ? 1 : 0 })}
            <span className="block text-xs font-normal text-gray-500 mt-0.5">
              Máximo no grafo: {maxWeight.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}
            </span>
          </label>
          <input
            type="range"
            min={0}
            max={maxWeight}
            step={sliderStep}
            value={Math.min(minWeight, maxWeight)}
            onChange={(event) => setMinWeight(parseFloat(event.target.value))}
            className="w-full"
          />
        </div>
      )}

      <div className="space-y-3">
        <button
          type="button"
          onClick={openExportModal}
          className="w-full py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm"
        >
          Exportar Imagem
        </button>
        <button
          type="button"
          onClick={openMetricsPanel}
          className="w-full py-2.5 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium text-sm"
        >
          Métricas e Análises
        </button>
      </div>
    </aside>
  )
}
