import { useEffect, useMemo, useRef, useState } from 'react'
import { Network } from 'vis-network/standalone'
import { useGraphStore } from '@/stores/graphStore'
import { colorForCommunity } from '@/utils/communityColors'
import { getGraphColor, getVisOptions } from '@/utils/graphOptions'
import ZoomControls from '@/components/graph/ZoomControls'

export default function GraphCanvas() {
  const containerRef = useRef<HTMLDivElement>(null)
  const networkRef = useRef<Network | null>(null)
  const {
    currentGraph,
    minWeight,
    searchQuery,
    communities,
    colorByCommunity,
    focusTarget,
    focusToken,
  } = useGraphStore()
  const [zoom, setZoom] = useState(1)

  const visibleEdges = useMemo(() => {
    if (!currentGraph) return []
    return currentGraph.edges.filter((edge) => (edge.weight ?? 0) >= minWeight)
  }, [currentGraph, minWeight])

  const resolveNodeColor = (nodeLabel: string, highlighted: boolean) => {
    if (!currentGraph) return '#3b82f6'
    if (highlighted) return '#f59e0b'
    if (colorByCommunity && communities[nodeLabel] !== undefined) {
      return colorForCommunity(communities[nodeLabel])
    }
    return getGraphColor(currentGraph.type)
  }

  useEffect(() => {
    if (!containerRef.current || !currentGraph) return

    const highlighted = searchQuery.trim().toLowerCase()
    const data = {
      nodes: currentGraph.nodes.map((node) => ({
        id: node.id,
        label: currentGraph.metadata.vertexCount <= 500 ? node.label : undefined,
        title: node.label,
        color: resolveNodeColor(node.label, highlighted.length > 0 && node.label.toLowerCase().includes(highlighted)),
        x: node.x,
        y: node.y,
        fixed: node.fixed ? { x: true, y: true } : false,
      })),
      edges: visibleEdges.map((edge) => ({
        from: edge.from,
        to: edge.to,
        label: edge.label,
        width: edge.weight ? Math.min(6, Math.log(edge.weight + 1) * 1.5) : 1,
        arrows: 'to',
      })),
    }

    const network = new Network(
      containerRef.current,
      data,
      getVisOptions(currentGraph.metadata.vertexCount, currentGraph.type),
    )
    networkRef.current = network

    network.on('zoom', () => setZoom(network.getScale()))
    network.on('dragEnd', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = String(params.nodes[0])
        const positions = network.getPositions([nodeId])
        network.moveNode(nodeId, positions[nodeId].x, positions[nodeId].y)
      }
    })

    network.once('stabilizationIterationsDone', () => {
      network.fit({ animation: { duration: 400, easingFunction: 'easeInOutQuad' } })
    })

    return () => {
      network.destroy()
      networkRef.current = null
    }
  }, [currentGraph, visibleEdges, searchQuery, communities, colorByCommunity])

  useEffect(() => {
    if (!networkRef.current || !currentGraph || !focusTarget) return
    const node = currentGraph.nodes.find(
      (item) => item.label.toLowerCase() === focusTarget.toLowerCase(),
    )
    if (!node) return
    networkRef.current.focus(node.id, { scale: 1.4, animation: { duration: 500, easingFunction: 'easeInOutQuad' } })
    networkRef.current.selectNodes([node.id])
  }, [focusTarget, focusToken, currentGraph])

  if (!currentGraph) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        Selecione um grafo para visualizar
      </div>
    )
  }

  return (
    <div className="relative w-full h-full bg-white">
      <div ref={containerRef} className="w-full h-full" />
      <div className="absolute bottom-4 left-4 bg-white/95 backdrop-blur px-4 py-2 rounded-lg shadow border text-sm font-medium">
        Vértices: {currentGraph.metadata.vertexCount} | Arestas: {visibleEdges.length}
        {colorByCommunity && Object.keys(communities).length > 0 && (
          <span className="ml-2 text-violet-600">· Comunidades</span>
        )}
      </div>
      <ZoomControls
        currentZoom={zoom}
        onZoomIn={() => networkRef.current?.moveTo({ scale: Math.min(5, (networkRef.current?.getScale() ?? 1) * 1.2) })}
        onZoomOut={() => networkRef.current?.moveTo({ scale: Math.max(0.1, (networkRef.current?.getScale() ?? 1) * 0.8) })}
        onReset={() => networkRef.current?.fit({ animation: true })}
      />
    </div>
  )
}
