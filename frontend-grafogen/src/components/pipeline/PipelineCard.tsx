type StageStatus = 'idle' | 'running' | 'done' | 'error'

interface PipelineCardProps {
  title: string
  description: string
  status: StageStatus
  detail?: string
  disabled?: boolean
  disabledReason?: string
  onExecute: () => void
  onCancel?: () => void
  onViewLogs?: () => void
}

const statusStyles: Record<StageStatus, string> = {
  idle: 'bg-white border-gray-200',
  running: 'bg-amber-50 border-amber-300 animate-pulse',
  done: 'bg-emerald-50 border-emerald-400',
  error: 'bg-red-50 border-red-400',
}

const statusLabel: Record<StageStatus, string> = {
  idle: '❌ Não executado',
  running: '⏳ Executando...',
  done: '✅ Concluído',
  error: '🔴 Erro',
}

export default function PipelineCard({
  title,
  description,
  status,
  detail,
  disabled,
  disabledReason,
  onExecute,
  onCancel,
  onViewLogs,
}: PipelineCardProps) {
  return (
    <div className={`rounded-xl border-2 p-6 shadow-sm ${statusStyles[status]}`}>
      <div className="flex items-start justify-between gap-4 mb-3">
        <div>
          <h3 className="text-lg font-bold text-gray-800">{title}</h3>
          <p className="text-sm text-gray-500 mt-1">{description}</p>
          <p className="text-sm font-medium text-gray-700 mt-2">{statusLabel[status]}</p>
          {detail && <p className="text-sm text-gray-600 mt-1">{detail}</p>}
        </div>
        {status === 'running' && onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-3 py-1.5 bg-red-500 text-white rounded-lg text-sm hover:bg-red-600"
          >
            ⏹️ Cancelar
          </button>
        )}
      </div>

      <div className="flex gap-2">
        {status !== 'running' && (
          <button
            type="button"
            onClick={onExecute}
            disabled={disabled}
            title={disabled ? disabledReason : undefined}
            className={`flex-1 py-2.5 rounded-lg font-medium text-sm ${
              disabled
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            ▶️ Executar
          </button>
        )}
        {onViewLogs && (
          <button
            type="button"
            onClick={onViewLogs}
            className="px-4 py-2.5 border border-gray-300 rounded-lg text-sm hover:bg-gray-50"
          >
            📋 Logs
          </button>
        )}
      </div>
    </div>
  )
}
