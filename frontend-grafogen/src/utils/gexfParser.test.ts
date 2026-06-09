import { describe, expect, it } from 'vitest'
import { parseCSVCommunities, parseCSVMetrics, parseGEXF } from './gexfParser'

const SAMPLE_GEXF = `<?xml version="1.0"?>
<gexf xmlns="http://www.gexf.net/1.3" version="1.3">
  <graph defaultedgetype="directed">
    <nodes>
      <node id="0" label="alice"/>
      <node id="1" label="bob"/>
    </nodes>
    <edges>
      <edge source="0" target="1">
        <attvalues>
          <attvalue for="0" value="3.5"/>
        </attvalues>
      </edge>
    </edges>
  </graph>
</gexf>`

describe('parseGEXF', () => {
  it('parses nodes and weighted edges for G4', () => {
    const graph = parseGEXF(SAMPLE_GEXF, 'G4')
    expect(graph.nodes).toHaveLength(2)
    expect(graph.nodes[0].label).toBe('alice')
    expect(graph.edges[0].weight).toBe(3.5)
    expect(graph.metadata.weighted).toBe(true)
    expect(graph.edges[0].label).toBe('3.5')
  })

  it('falls back to node id when label is missing', () => {
    const xml = `<?xml version="1.0"?><gexf><graph><nodes><node id="42"/></nodes></graph></gexf>`
    expect(parseGEXF(xml, 'G1').nodes[0].label).toBe('42')
  })

  it('uses default weight 1 for G1 when attribute missing', () => {
    const g1 = `<?xml version="1.0"?><gexf><graph><nodes><node id="0" label="a"/></nodes><edges><edge source="0" target="0"/></edges></graph></gexf>`
    const graph = parseGEXF(g1, 'G1')
    expect(graph.edges[0].weight).toBe(1)
    expect(graph.metadata.weighted).toBe(false)
  })

  it('skips malformed nodes and edges', () => {
    const partial = `<?xml version="1.0"?><gexf><graph><nodes><node label="no-id"/></nodes><edges><edge source="0"/></edges></graph></gexf>`
    const graph = parseGEXF(partial, 'G2')
    expect(graph.nodes).toHaveLength(0)
    expect(graph.edges).toHaveLength(0)
  })

  it('throws on invalid xml', () => {
    expect(() => parseGEXF('<not-gexf>', 'G1')).toThrow('inválido')
  })
})

describe('parseCSVCommunities', () => {
  it('parses community rows', () => {
    const rows = parseCSVCommunities('login,community_id,graph\nalice,1,G1\nbob,0,G2')
    expect(rows).toEqual([
      { login: 'alice', community_id: 1, graph: 'G1' },
      { login: 'bob', community_id: 0, graph: 'G2' },
    ])
  })

  it('returns empty for header only', () => {
    expect(parseCSVCommunities('login,community_id,graph')).toEqual([])
  })
})

describe('parseCSVMetrics', () => {
  it('returns empty for header only', () => {
    expect(parseCSVMetrics('login,graph,degree_in,degree_out,betweenness,closeness,pagerank')).toEqual([])
  })

  it('parses centrality csv', () => {
    const rows = parseCSVMetrics(
      'login,graph,degree_in,degree_out,betweenness,closeness,pagerank\nalice,G1,0.1,0.2,0.3,0.4,0.5',
    )
    expect(rows[0]).toMatchObject({
      login: 'alice',
      graph: 'G1',
      pagerank: 0.5,
      closeness: 0.4,
    })
  })
})
