import type { GraphType } from '@/types/graph'

export interface RecentGraphEntry {
  type: GraphType
  name: string
  vertexCount: number
  edgeCount: number
  openedAt: string
  source: 'api' | 'upload'
}

const STORAGE_KEY = 'grafogen-recent-graphs'
const MAX_ENTRIES = 8

export function loadRecentGraphs(): RecentGraphEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw) as RecentGraphEntry[]
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function saveRecentGraph(entry: Omit<RecentGraphEntry, 'openedAt'>): RecentGraphEntry[] {
  const next: RecentGraphEntry = { ...entry, openedAt: new Date().toISOString() }
  const filtered = loadRecentGraphs().filter((item) => item.type !== entry.type)
  const updated = [next, ...filtered].slice(0, MAX_ENTRIES)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
  return updated
}

const uploadKey = (type: GraphType) => `grafogen-upload-gexf-${type}`

export function cacheUploadedGexf(type: GraphType, xml: string): void {
  try {
    localStorage.setItem(uploadKey(type), xml)
  } catch {
    // quota exceeded — recent list still works for API graphs
  }
}

export function loadCachedGexf(type: GraphType): string | null {
  try {
    return localStorage.getItem(uploadKey(type))
  } catch {
    return null
  }
}
