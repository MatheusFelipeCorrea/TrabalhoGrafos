import { useCallback, useEffect } from 'react'
import { fetchStatus } from '@/utils/api'
import { usePipelineStore } from '@/stores/pipelineStore'

export function usePipelineStatus(pollMs = 3000) {
  const { setStatus } = usePipelineStore()

  const refresh = useCallback(async () => {
    try {
      const status = await fetchStatus()
      setStatus(status)
    } catch {
      // API offline — status stays null
    }
  }, [setStatus])

  useEffect(() => {
    refresh()
    const interval = window.setInterval(refresh, pollMs)
    return () => window.clearInterval(interval)
  }, [refresh, pollMs])

  return refresh
}
