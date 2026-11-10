import { useCallback, useEffect, useState } from 'react'
import { climateFacade } from '../../application/services/climateFacadeInstance'
import type { ClimateData } from '../../domain/models/ClimateData'
import type { Location } from '../../domain/models/Location'

export function useClimate(location: Location | null) {
  const [climate, setClimate] = useState<ClimateData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [requestVersion, setRequestVersion] = useState(0)

  const refresh = useCallback(() => {
    setRequestVersion((version) => version + 1)
  }, [])

  useEffect(() => {
    if (!location) {
      return undefined
    }

    const selectedLocation = location
    const controller = new AbortController()

    async function loadClimate() {
      setIsLoading(true)
      setError(null)

      try {
        setClimate(await climateFacade.getCurrentClimate(selectedLocation, controller.signal))
      } catch (reason) {
        if (!controller.signal.aborted) {
          setClimate(null)
          setError(reason instanceof Error ? reason.message : 'No fue posible consultar el clima.')
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false)
        }
      }
    }

    void loadClimate()

    return () => controller.abort()
  }, [location, requestVersion])

  return { climate, error, isLoading, refresh }
}
