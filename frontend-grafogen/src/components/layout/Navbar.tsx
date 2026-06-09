import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="bg-blue-600 text-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3">
          <span className="text-2xl" aria-hidden>
            📊
          </span>
          <span className="text-2xl font-bold tracking-tight">GrafoGen</span>
        </Link>

        <div className="flex items-center gap-8 text-sm font-medium">
          <Link to="/" className={location.pathname === '/' ? 'text-white' : 'text-blue-100 hover:text-white'}>
            Home
          </Link>
          <span className="text-blue-100">github/spec-kit</span>
        </div>
      </div>
    </nav>
  )
}
