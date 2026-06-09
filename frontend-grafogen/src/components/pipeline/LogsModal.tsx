interface LogsModalProps {
  open: boolean
  logs: string[]
  onClose: () => void
}

export default function LogsModal({ open, logs, onClose }: LogsModalProps) {
  if (!open) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-3xl max-h-[80vh] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-bold">Logs do Pipeline</h2>
          <button type="button" onClick={onClose} className="text-2xl text-gray-500">
            ×
          </button>
        </div>
        <pre className="p-4 overflow-auto text-xs font-mono bg-gray-900 text-green-400 flex-1">
          {logs.length ? logs.join('\n') : 'Nenhum log disponível.'}
        </pre>
      </div>
    </div>
  )
}
