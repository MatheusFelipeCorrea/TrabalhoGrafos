import type { Graph } from '@/types/graph'

export async function exportToPNG(
  transparent: boolean,
  filename: string,
  resolution: '1920x1080' | '3840x2160',
): Promise<void> {
  const source = document.querySelector('.vis-network canvas') as HTMLCanvasElement | null
  if (!source) throw new Error('Canvas não encontrado')

  const [width, height] = resolution.split('x').map(Number)
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d')
  if (!ctx) throw new Error('Contexto 2D indisponível')

  if (!transparent) {
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, width, height)
  }

  ctx.drawImage(source, 0, 0, width, height)
  downloadDataUrl(canvas.toDataURL('image/png'), `${filename}.png`)
}

export function exportToSVG(graph: Graph, filename: string): void {
  const nodes = graph.nodes
  const radius = 220
  const centerX = 400
  const centerY = 300
  const nodeRadius = Math.max(4, Math.min(12, 600 / Math.max(nodes.length, 1)))

  const positions = new Map<string, { x: number; y: number }>()
  nodes.forEach((node, index) => {
    const angle = (2 * Math.PI * index) / Math.max(nodes.length, 1)
    positions.set(node.id, {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    })
  })

  let svg = `<?xml version="1.0" encoding="UTF-8"?>\n`
  svg += `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">\n`
  svg += `<defs><marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#9ca3af"/></marker></defs>\n`
  svg += `<rect width="100%" height="100%" fill="#ffffff"/>\n`

  for (const edge of graph.edges) {
    const from = positions.get(edge.from)
    const to = positions.get(edge.to)
    if (!from || !to) continue
    svg += `<line x1="${from.x}" y1="${from.y}" x2="${to.x}" y2="${to.y}" stroke="#9ca3af" stroke-width="1" marker-end="url(#arrow)"/>\n`
  }

  for (const node of nodes) {
    const pos = positions.get(node.id)
    if (!pos) continue
    const fill = node.color ?? '#3b82f6'
    svg += `<circle cx="${pos.x}" cy="${pos.y}" r="${nodeRadius}" fill="${fill}" stroke="#ffffff" stroke-width="2"/>\n`
    if (nodes.length <= 80) {
      svg += `<text x="${pos.x}" y="${pos.y - nodeRadius - 4}" text-anchor="middle" font-size="10" fill="#374151">${escapeXml(node.label)}</text>\n`
    }
  }

  svg += '</svg>'
  downloadBlob(new Blob([svg], { type: 'image/svg+xml' }), `${filename}.svg`)
}

function escapeXml(value: string): string {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}

export function exportToDOT(graph: Graph, filename: string): void {
  let dot = `digraph ${graph.type} {\n`
  for (const edge of graph.edges) {
    const from = graph.nodes.find((node) => node.id === edge.from)?.label ?? edge.from
    const to = graph.nodes.find((node) => node.id === edge.to)?.label ?? edge.to
    const weight = edge.weight ? ` [label="${edge.weight}"]` : ''
    dot += `  "${from}" -> "${to}"${weight};\n`
  }
  dot += '}\n'
  downloadBlob(new Blob([dot], { type: 'text/plain' }), `${filename}.dot`)
}

function downloadDataUrl(dataUrl: string, name: string) {
  const link = document.createElement('a')
  link.download = name
  link.href = dataUrl
  link.click()
}

function downloadBlob(blob: Blob, name: string) {
  const link = document.createElement('a')
  link.download = name
  link.href = URL.createObjectURL(blob)
  link.click()
  URL.revokeObjectURL(link.href)
}
