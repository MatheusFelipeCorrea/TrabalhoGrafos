import { useState } from 'react'
import { useGraphStore } from '@/stores/graphStore'
import { useUIStore } from '@/stores/uiStore'
import { exportToDOT, exportToPNG, exportToSVG } from '@/utils/graphExporter'

export default function ExportModal() {
  const { exportModalOpen, closeExportModal } = useUIStore()
  const { currentGraph } = useGraphStore()
  const [format, setFormat] = useState<'png' | 'svg' | 'dot'>('png')
  const [resolution, setResolution] = useState<'1920x1080' | '3840x2160'>('1920x1080')
  const [transparentBg, setTransparentBg] = useState(false)
  const [loading, setLoading] = useState(false)

  if (!exportModalOpen || !currentGraph) return null

  const filename = `grafo-${currentGraph.type}-${new Date().toISOString().slice(0, 10)}`

  const handleExport = async () => {
    setLoading(true)
    try {
      if (format === 'png') {
        await exportToPNG(transparentBg, filename, resolution)
      } else if (format === 'svg') {
        exportToSVG(currentGraph, filename)
      } else {
        exportToDOT(currentGraph, filename)
      }
      closeExportModal()
    } catch (error) {
      alert(error instanceof Error ? error.message : 'Falha ao exportar')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-800">Exportar Grafo</h2>
          <button type="button" onClick={closeExportModal} className="text-2xl text-gray-500 hover:text-gray-700">
            ×
          </button>
        </div>

        <div className="mb-4">
          <p className="text-sm font-medium text-gray-700 mb-2">Formato</p>
          <div className="flex flex-wrap gap-4 text-sm">
            <label className="flex items-center gap-2">
              <input type="radio" checked={format === 'png'} onChange={() => setFormat('png')} />
              PNG
            </label>
            <label className="flex items-center gap-2">
              <input type="radio" checked={format === 'svg'} onChange={() => setFormat('svg')} />
              SVG
            </label>
            <label className="flex items-center gap-2">
              <input type="radio" checked={format === 'dot'} onChange={() => setFormat('dot')} />
              Código DOT
            </label>
          </div>
        </div>

        {format === 'png' && (
          <>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Resolução</label>
              <select
                value={resolution}
                onChange={(event) => setResolution(event.target.value as typeof resolution)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="1920x1080">1920x1080 (Full HD)</option>
                <option value="3840x2160">3840x2160 (4K)</option>
              </select>
            </div>
            <label className="flex items-center gap-2 mb-6 text-sm text-gray-700">
              <input type="checkbox" checked={transparentBg} onChange={(event) => setTransparentBg(event.target.checked)} />
              Ativar fundo transparente
            </label>
          </>
        )}

        {format === 'svg' && (
          <p className="text-sm text-gray-500 mb-6">
            SVG vetorial com layout circular (escalável para relatório).
          </p>
        )}

        <div className="flex gap-3">
          <button type="button" onClick={closeExportModal} className="flex-1 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            Cancelar
          </button>
          <button
            type="button"
            onClick={handleExport}
            disabled={loading}
            className="flex-1 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Exportando...' : 'Baixar'}
          </button>
        </div>
      </div>
    </div>
  )
}
