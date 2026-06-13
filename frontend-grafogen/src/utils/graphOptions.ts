import type { GraphType } from '@/types/graph'

export function getGraphColor(type: GraphType): string {
  const colors: Record<GraphType, string> = {
    G1: '#3b82f6',
    G2: '#10b981',
    G3: '#8b5cf6',
    G4: '#f97316',
  }
  return colors[type]
}

export function getVisOptions(vertexCount: number, graphType: GraphType) {
  const physicsEnabled = vertexCount <= 1000

  return {
    nodes: {
      shape: 'dot',
      size: vertexCount > 500 ? 8 : 16,
      font: {
        size: vertexCount > 500 ? 0 : 14,
        color: '#1f2937',
        face: 'Inter, sans-serif',
        vadjust: vertexCount > 500 ? 0 : -24,
      },
      borderWidth: 2,
      color: {
        background: getGraphColor(graphType),
        border: '#ffffff',
        highlight: { background: '#f59e0b', border: '#ffffff' },
        hover: { background: '#60a5fa', border: '#ffffff' },
      },
      shadow: true,
    },
    edges: {
      width: 1,
      color: { color: '#9ca3af', highlight: getGraphColor(graphType) },
      smooth: { enabled: true, type: 'continuous', roundness: 0.4 },
      arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      font: { size: 10, color: '#6b7280', strokeWidth: 0, align: 'middle' },
    },
    physics: {
      enabled: physicsEnabled,
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -40,
        centralGravity: 0.01,
        springLength: vertexCount > 200 ? 80 : 120,
        springConstant: 0.08,
        damping: 0.45,
        avoidOverlap: 0.8,
      },
      stabilization: { enabled: physicsEnabled, iterations: physicsEnabled ? 150 : 0 },
    },
    interaction: {
      hover: true,
      dragNodes: true,
      dragView: true,
      zoomView: true,
      zoomSpeed: 0.4,
    },
  }
}
