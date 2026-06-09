export type GraphType = 'G1' | 'G2' | 'G3' | 'G4'

export interface GraphNode {
  id: string
  label: string
  x?: number
  y?: number
  color?: string
  fixed?: boolean
}

export interface GraphEdge {
  from: string
  to: string
  weight?: number
  label?: string
  arrows?: string
}

export interface Graph {
  id: string
  name: string
  type: GraphType
  nodes: GraphNode[]
  edges: GraphEdge[]
  metadata: {
    vertexCount: number
    edgeCount: number
    directed: boolean
    weighted: boolean
  }
}

export interface GraphMetrics {
  login: string
  graph: string
  degree_in: number
  degree_out: number
  betweenness: number
  closeness: number
  pagerank: number
}

export interface GraphSummary {
  type: GraphType
  filename: string
  available: boolean
  vertexCount: number
  edgeCount: number
}

export interface PipelineStatus {
  repository: string
  stage1Complete: boolean
  stage2Complete: boolean
  stage3Complete: boolean
  interactionCount: number
  graphs: GraphSummary[]
  metricsAvailable: boolean
  pipelineRunning: boolean
  logs: string[]
}
