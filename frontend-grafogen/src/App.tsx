import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import HomePage from '@/pages/HomePage'
import VisualizePage from '@/pages/VisualizePage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/visualize/:graphId" element={<VisualizePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
