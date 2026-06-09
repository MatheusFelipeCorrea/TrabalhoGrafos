import { create } from 'zustand'
import type { Graph, GraphMetrics, GraphType } from '@/types/graph'
import { loadRecentGraphs, saveRecentGraph, type RecentGraphEntry } from '@/utils/recentGraphs'

interface GraphState {
  graphs: Graph[]
  currentGraph: Graph | null
  metrics: GraphMetrics[]
  communities: Record<string, number>
  colorByCommunity: boolean
  minWeight: number
  searchQuery: string
  focusTarget: string | null
  focusToken: number
  recentGraphs: RecentGraphEntry[]
  loadGraph: (graph: Graph, source?: 'api' | 'upload') => void
  setCurrentGraphByType: (type: GraphType) => void
  loadMetrics: (metrics: GraphMetrics[]) => void
  loadCommunities: (map: Record<string, number>) => void
  setColorByCommunity: (value: boolean) => void
  setMinWeight: (value: number) => void
  setSearchQuery: (value: string) => void
  focusOnVertex: (login: string) => void
  refreshRecentGraphs: () => void
}

export const useGraphStore = create<GraphState>((set, get) => ({
  graphs: [],
  currentGraph: null,
  metrics: [],
  communities: {},
  colorByCommunity: false,
  minWeight: 0,
  searchQuery: '',
  focusTarget: null,
  focusToken: 0,
  recentGraphs: [],

  loadGraph: (graph, source = 'api') => {
    set((state) => {
      const others = state.graphs.filter((item) => item.type !== graph.type)
      const recentGraphs = saveRecentGraph({
        type: graph.type,
        name: graph.name,
        vertexCount: graph.metadata.vertexCount,
        edgeCount: graph.metadata.edgeCount,
        source,
      })
      return { graphs: [...others, graph], currentGraph: graph, recentGraphs }
    })
  },

  setCurrentGraphByType: (type) => {
    const graph = get().graphs.find((item) => item.type === type) ?? null
    set({ currentGraph: graph, colorByCommunity: false, minWeight: 0 })
  },

  loadMetrics: (metrics) => set({ metrics }),

  loadCommunities: (communities) => set({ communities }),

  setColorByCommunity: (value) => set({ colorByCommunity: value }),

  setMinWeight: (value) => set({ minWeight: value }),

  setSearchQuery: (value) => set({ searchQuery: value }),

  focusOnVertex: (login) =>
    set((state) => ({
      focusTarget: login,
      focusToken: state.focusToken + 1,
      searchQuery: login,
    })),

  refreshRecentGraphs: () => set({ recentGraphs: loadRecentGraphs() }),
}))
