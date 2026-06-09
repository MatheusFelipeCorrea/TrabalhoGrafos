import { create } from 'zustand'
import type { PipelineStatus } from '@/types/graph'

interface PipelineState {
  status: PipelineStatus | null
  logsOpen: boolean
  setStatus: (status: PipelineStatus) => void
  setLogsOpen: (open: boolean) => void
}

export const usePipelineStore = create<PipelineState>((set) => ({
  status: null,
  logsOpen: false,
  setStatus: (status) => set({ status }),
  setLogsOpen: (open) => set({ logsOpen: open }),
}))
