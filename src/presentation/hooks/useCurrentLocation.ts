import { useCallback, useState } from 'react'
import { currentLocationCommand } from '../../infrastructure/browser/currentLocationCommand'
import type { Location } from '../../domain/models/Location'

export function useCurrentLocation(onLocationSelect: (location: Location) => void) {
  const [error, setError] = useState<string | null>(null)
  const [isLocating, setIsLocating] = useState(false)

  const locate = useCallback(async () => {
    setIsLocating(true)
    setError(null)

    try {
      onLocationSelect(await currentLocationCommand.execute())
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'No fue posible obtener tu ubicación.')
    } finally {
      setIsLocating(false)
    }
  }, [onLocationSelect])

  return { error, isLocating, locate }
}
