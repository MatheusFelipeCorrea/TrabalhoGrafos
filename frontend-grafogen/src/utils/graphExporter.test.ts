import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { Graph } from '@/types/graph'
import { exportToDOT, exportToPNG, exportToSVG } from './graphExporter'

const graph: Graph = {
  id: 'G1',
  name: 'G1',
  type: 'G1',
  nodes: [
    { id: '0', label: 'alice' },
    { id: '1', label: 'bob' },
  ],
  edges: [{ from: '0', to: '1', weight: 2 }],
  metadata: { vertexCount: 2, edgeCount: 1, directed: true, weighted: false },
}

describe('graphExporter', () => {
  let blobContent = ''
  const realCreateElement = document.createElement.bind(document)

  beforeEach(() => {
    blobContent = ''
    vi.stubGlobal(
      'Blob',
      class {
        parts: BlobPart[]
        constructor(parts: BlobPart[]) {
          this.parts = parts
          blobContent = parts.map((part) => String(part)).join('')
        }
      },
    )
    vi.stubGlobal('URL', {
      createObjectURL: () => 'blob:mock',
      revokeObjectURL: vi.fn(),
    })
    vi.spyOn(document, 'createElement').mockImplementation((tag: string) => {
      if (tag === 'a') {
        return { click: vi.fn(), download: '', href: '' } as unknown as HTMLAnchorElement
      }
      return realCreateElement(tag)
    })
  })

  it('exports DOT with quoted labels', () => {
    exportToDOT(graph, 'test')
    expect(blobContent).toContain('digraph G1')
    expect(blobContent).toContain('"alice" -> "bob"')
    expect(blobContent).toContain('label="2"')
  })

  it('exports SVG with nodes and edges', () => {
    exportToSVG(graph, 'test')
    expect(blobContent).toContain('<svg')
    expect(blobContent).toContain('<circle')
    expect(blobContent).toContain('<line')
    expect(blobContent).toContain('alice')
  })

  it('escapes xml in svg labels', () => {
    const risky: Graph = {
      ...graph,
      nodes: [{ id: '0', label: 'a<b>&"' }],
    }
    exportToSVG(risky, 'test')
    expect(blobContent).toContain('a&lt;b&gt;&amp;&quot;')
  })

  it('exports PNG from vis canvas', async () => {
    const source = document.createElement('canvas')
    const ctx = { fillStyle: '', fillRect: vi.fn(), drawImage: vi.fn() }
    HTMLCanvasElement.prototype.getContext = vi.fn(() => ctx) as typeof HTMLCanvasElement.prototype.getContext
    HTMLCanvasElement.prototype.toDataURL = vi.fn(() => 'data:image/png;base64,abc')
    vi.spyOn(document, 'querySelector').mockReturnValue(source)

    await exportToPNG(true, 'shot', '1920x1080')
    expect(ctx.drawImage).toHaveBeenCalled()

    await exportToPNG(false, 'shot', '1920x1080')
    expect(ctx.fillRect).toHaveBeenCalled()
  })
})
