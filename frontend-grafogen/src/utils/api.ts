import type { GraphType, PipelineStatus } from '@/types/graph'

export async function fetchStatus(): Promise<PipelineStatus> {
  const response = await fetch('/api/status')
  if (!response.ok) throw new Error('Falha ao consultar status')
  return response.json()
}

export async function fetchGraphGexf(type: GraphType): Promise<string> {
  const response = await fetch(`/api/graphs/${type}`)
  if (!response.ok) throw new Error(`Grafo ${type} não disponível`)
  return response.text()
}

export async function fetchReport(name: 'centrality.csv' | 'communities.csv' | 'structure.json'): Promise<string> {
  const response = await fetch(`/api/reports/${name}`)
  if (!response.ok) throw new Error(`Relatório ${name} não disponível`)
  return response.text()
}

export async function runPipelineStage(stage: 'mine' | 'build' | 'analyze'): Promise<void> {
  const response = await fetch(`/api/pipeline/${stage}`, { method: 'POST' })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.error || `Falha ao executar ${stage}`)
  }
}

export async function cancelPipeline(): Promise<void> {
  await fetch('/api/pipeline/cancel', { method: 'POST' })
}
