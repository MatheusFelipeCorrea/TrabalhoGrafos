import type { Graph, GraphEdge, GraphNode, GraphType } from '@/types/graph'

const GRAPH_NAMES: Record<GraphType, string> = {
  G1: 'G1 - Comentários',
  G2: 'G2 - Fechamentos',
  G3: 'G3 - Reviews',
  G4: 'G4 - Integrado Ponderado',
}

export function parseGEXF(xmlString: string, graphType: GraphType): Graph {
  const parser = new DOMParser()
  const xmlDoc = parser.parseFromString(xmlString, 'text/xml')

  if (xmlDoc.getElementsByTagName('parsererror').length > 0) {
    throw new Error('Arquivo GEXF inválido')
  }

  const nodes: GraphNode[] = []
  const nodeElements = xmlDoc.getElementsByTagName('node')
  for (let index = 0; index < nodeElements.length; index += 1) {
    const node = nodeElements[index]
    const id = node.getAttribute('id')
    if (!id) continue
    nodes.push({
      id,
      label: node.getAttribute('label') || id,
    })
  }

  const edges: GraphEdge[] = []
  const edgeElements = xmlDoc.getElementsByTagName('edge')
  for (let index = 0; index < edgeElements.length; index += 1) {
    const edge = edgeElements[index]
    const from = edge.getAttribute('source')
    const to = edge.getAttribute('target')
    if (!from || !to) continue

    let weight = graphType === 'G4' ? 0 : 1
    const attvalues = edge.getElementsByTagName('attvalue')
    for (let j = 0; j < attvalues.length; j += 1) {
      const attvalue = attvalues[j]
      if (attvalue.getAttribute('for') === '0') {
        weight = parseFloat(attvalue.getAttribute('value') || '0')
      }
    }

    edges.push({
      from,
      to,
      weight,
      label: graphType === 'G4' && weight > 0 ? weight.toFixed(1) : undefined,
      arrows: 'to',
    })
  }

  return {
    id: graphType,
    name: GRAPH_NAMES[graphType],
    type: graphType,
    nodes,
    edges,
    metadata: {
      vertexCount: nodes.length,
      edgeCount: edges.length,
      directed: true,
      weighted: graphType === 'G4',
    },
  }
}

export interface CommunityRow {
  login: string
  community_id: number
  graph: string
}

export function parseCSVCommunities(csvString: string): CommunityRow[] {
  const lines = csvString.trim().split('\n')
  if (lines.length <= 1) return []

  return lines.slice(1).map((line) => {
    const [login, community_id, graph] = line.split(',')
    return {
      login,
      community_id: parseInt(community_id, 10),
      graph,
    }
  })
}

export function parseCSVMetrics(csvString: string): import('@/types/graph').GraphMetrics[] {
  const lines = csvString.trim().split('\n')
  if (lines.length <= 1) return []

  return lines.slice(1).map((line) => {
    const [login, graph, degree_in, degree_out, betweenness, closeness, pagerank] = line.split(',')
    return {
      login,
      graph,
      degree_in: parseFloat(degree_in),
      degree_out: parseFloat(degree_out),
      betweenness: parseFloat(betweenness),
      closeness: parseFloat(closeness),
      pagerank: parseFloat(pagerank),
    }
  })
}
