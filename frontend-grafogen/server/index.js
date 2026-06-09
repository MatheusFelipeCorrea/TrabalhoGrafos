import cors from 'cors'
import express from 'express'
import fs from 'fs'
import path from 'path'
import { spawn } from 'child_process'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const BACKEND_ROOT = path.resolve(__dirname, '../../github-graph-analyzer')
const DATA_RAW = path.join(BACKEND_ROOT, 'data/raw')
const GRAPHS_DIR = path.join(BACKEND_ROOT, 'output/graphs')
const REPORTS_DIR = path.join(BACKEND_ROOT, 'output/reports')

const GRAPH_FILES = {
  G1: 'graph1_comments.gexf',
  G2: 'graph2_closures.gexf',
  G3: 'graph3_reviews.gexf',
  G4: 'graph4_integrated.gexf',
}

let activeProcess = null
let activeLogs = []

const app = express()
app.use(cors())
app.use(express.json())

function fileExists(filePath) {
  try {
    return fs.existsSync(filePath)
  } catch {
    return false
  }
}

function countGexfStats(content) {
  return {
    vertexCount: (content.match(/<(?:[\w:]+:)?node\b/g) || []).length,
    edgeCount: (content.match(/<(?:[\w:]+:)?edge\b/g) || []).length,
  }
}

function detectStatus() {
  const stage1Complete =
    fileExists(path.join(DATA_RAW, 'users.csv')) &&
    fileExists(path.join(DATA_RAW, 'interactions.csv'))

  const graphs = Object.entries(GRAPH_FILES).map(([type, filename]) => {
    const fullPath = path.join(GRAPHS_DIR, filename)
    if (!fileExists(fullPath)) {
      return { type, filename, available: false, vertexCount: 0, edgeCount: 0 }
    }
    const content = fs.readFileSync(fullPath, 'utf-8')
    const stats = countGexfStats(content)
    return { type, filename, available: true, path: fullPath, ...stats }
  })

  const stage2Complete = graphs.every((graph) => graph.available)
  const stage3Complete =
    fileExists(path.join(REPORTS_DIR, 'centrality.csv')) &&
    fileExists(path.join(REPORTS_DIR, 'communities.csv'))

  let interactionCount = 0
  if (fileExists(path.join(DATA_RAW, 'interactions.csv'))) {
    const lines = fs.readFileSync(path.join(DATA_RAW, 'interactions.csv'), 'utf-8').trim().split('\n')
    interactionCount = Math.max(0, lines.length - 1)
  }

  return {
    repository: 'github/spec-kit',
    stage1Complete,
    stage2Complete,
    stage3Complete,
    interactionCount,
    graphs,
    metricsAvailable: stage3Complete,
    pipelineRunning: activeProcess !== null,
    logs: activeLogs.slice(-200),
  }
}

app.get('/api/status', (_req, res) => {
  res.json(detectStatus())
})

app.get('/api/graphs/:type', (req, res) => {
  const filename = GRAPH_FILES[req.params.type]
  if (!filename) {
    res.status(404).json({ error: 'Grafo inválido' })
    return
  }
  const fullPath = path.join(GRAPHS_DIR, filename)
  if (!fileExists(fullPath)) {
    res.status(404).json({ error: 'Arquivo GEXF não encontrado' })
    return
  }
  res.type('application/xml').send(fs.readFileSync(fullPath, 'utf-8'))
})

app.get('/api/reports/:name', (req, res) => {
  const allowed = ['centrality.csv', 'communities.csv', 'structure.json']
  if (!allowed.includes(req.params.name)) {
    res.status(404).json({ error: 'Relatório inválido' })
    return
  }
  const fullPath = path.join(REPORTS_DIR, req.params.name)
  if (!fileExists(fullPath)) {
    res.status(404).json({ error: 'Relatório não encontrado' })
    return
  }
  if (req.params.name.endsWith('.json')) {
    res.type('application/json').send(fs.readFileSync(fullPath, 'utf-8'))
  } else {
    res.type('text/csv').send(fs.readFileSync(fullPath, 'utf-8'))
  }
})

app.post('/api/pipeline/:stage', (req, res) => {
  const stage = req.params.stage
  if (!['mine', 'build', 'analyze'].includes(stage)) {
    res.status(400).json({ error: 'Etapa inválida' })
    return
  }
  if (activeProcess) {
    res.status(409).json({ error: 'Já existe uma execução em andamento' })
    return
  }

  activeLogs = [`Iniciando etapa: ${stage}`]
  const args = ['-m', 'src.app.main', `--${stage}`]
  activeProcess = spawn('python', args, {
    cwd: BACKEND_ROOT,
    shell: true,
  })

  activeProcess.stdout?.on('data', (chunk) => {
    activeLogs.push(...chunk.toString().split(/\r?\n/).filter(Boolean))
  })
  activeProcess.stderr?.on('data', (chunk) => {
    activeLogs.push(...chunk.toString().split(/\r?\n/).filter((line) => line).map((line) => `[ERROR] ${line}`))
  })
  activeProcess.on('close', (code) => {
    activeLogs.push(code === 0 ? `Etapa ${stage} concluída com sucesso.` : `Etapa ${stage} falhou (código ${code}).`)
    activeProcess = null
  })

  res.json({ started: true, stage })
})

app.post('/api/pipeline/cancel', (_req, res) => {
  if (!activeProcess) {
    res.status(404).json({ error: 'Nenhuma execução ativa' })
    return
  }
  activeProcess.kill('SIGTERM')
  activeProcess = null
  activeLogs.push('Execução cancelada pelo usuário.')
  res.json({ cancelled: true })
})

const PORT = process.env.API_PORT || 3001
app.listen(PORT, () => {
  console.log(`GrafoGen API em http://localhost:${PORT}`)
  console.log(`Backend Python: ${BACKEND_ROOT}`)
})
