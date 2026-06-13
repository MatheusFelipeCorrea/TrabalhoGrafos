interface ZoomControlsProps {
  currentZoom: number
  onZoomIn: () => void
  onZoomOut: () => void
  onReset: () => void
}

export default function ZoomControls({ currentZoom, onZoomIn, onZoomOut, onReset }: ZoomControlsProps) {
  return (
    <div className="absolute top-4 right-4 flex flex-col gap-2">
      <button type="button" onClick={onZoomIn} className="bg-white p-3 rounded-lg shadow border hover:bg-gray-50 text-xl font-bold">
        +
      </button>
      <button type="button" onClick={onZoomOut} className="bg-white p-3 rounded-lg shadow border hover:bg-gray-50 text-xl font-bold">
        −
      </button>
      <button type="button" onClick={onReset} className="bg-white px-3 py-2 rounded-lg shadow border hover:bg-gray-50 text-sm font-medium">
        Reset
      </button>
      <div className="bg-white px-3 py-1 rounded-lg shadow border text-xs text-center text-gray-600">
        {(currentZoom * 100).toFixed(0)}%
      </div>
    </div>
  )
}
