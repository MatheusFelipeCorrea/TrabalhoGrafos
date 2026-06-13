import { create } from 'zustand'

interface UIState {
  exportModalOpen: boolean
  metricsPanelOpen: boolean
  openExportModal: () => void
  closeExportModal: () => void
  openMetricsPanel: () => void
  closeMetricsPanel: () => void
}

export const useUIStore = create<UIState>((set) => ({
  exportModalOpen: false,
  metricsPanelOpen: false,
  openExportModal: () => set({ exportModalOpen: true }),
  closeExportModal: () => set({ exportModalOpen: false }),
  openMetricsPanel: () => set({ metricsPanelOpen: true }),
  closeMetricsPanel: () => set({ metricsPanelOpen: false }),
}))
