import { useCallback, useState } from 'react'
import type { Location } from '../../domain/models/Location'

export function useSelectedLocation() {
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null)

  const selectLocation = useCallback((location: Location) => {
    setSelectedLocation(location)
  }, [])

  return { selectedLocation, selectLocation }
}
