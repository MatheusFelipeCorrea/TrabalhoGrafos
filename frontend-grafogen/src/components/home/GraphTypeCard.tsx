import type { GraphType } from '@/types/graph'

interface GraphTypeCardProps {
  type: GraphType
  title: string
  subtitle: string
  description: string
  example: string
  icon: string
  colorClass: string
  vertexCount: number
  edgeCount: number
  available: boolean
  onOpen: () => void
}

export default function GraphTypeCard({
  title,
  subtitle,
  description,
  example,
  icon,
  colorClass,
  vertexCount,
  edgeCount,
  available,
  onOpen,
}: GraphTypeCardProps) {
  return (
    <div
      className={`rounded-xl shadow-lg p-6 text-white transition transform ${
        available ? `${colorClass} hover:scale-[1.02] cursor-pointer` : 'bg-gray-300 cursor-not-allowed'
      }`}
      onClick={available ? onOpen : undefined}
      onKeyDown={available ? (event) => event.key === 'Enter' && onOpen() : undefined}
      role="button"
      tabIndex={available ? 0 : -1}
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-1">{title}</h3>
      <p className="text-sm opacity-90 mb-3">{subtitle}</p>
      <p className="text-sm mb-4 leading-relaxed">{description}</p>
      <p className="text-xs bg-white/20 rounded px-2 py-1 inline-block mb-4">{example}</p>
      {available ? (
        <p className="text-sm font-medium mb-4">
          {vertexCount.toLocaleString()} vértices · {edgeCount.toLocaleString()} arestas
        </p>
      ) : (
        <p className="text-sm font-medium mb-4 opacity-80">Aguardando construção dos grafos</p>
      )}
      <button
        type="button"
        disabled={!available}
        className="w-full py-2 rounded-lg bg-white/20 hover:bg-white/30 font-medium disabled:opacity-60"
      >
        {available ? 'Visualizar' : 'Indisponível'}
      </button>
    </div>
  )
}
