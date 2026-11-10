import type { Location } from '../../domain/models/Location'
import type { CurrentLocationProvider } from '../../domain/ports/CurrentLocationProvider'

function locationError(message: string) {
  return new Error(message)
}

export class BrowserLocationProvider implements CurrentLocationProvider {
  getCurrentLocation(): Promise<Location> {
    if (!navigator.geolocation) {
      return Promise.reject(locationError('Tu navegador no permite obtener la ubicación.'))
    }

    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          })
        },
        (error) => {
          const messages: Record<number, string> = {
            [error.PERMISSION_DENIED]: 'Permite el acceso a tu ubicación para continuar.',
            [error.POSITION_UNAVAILABLE]: 'Tu ubicación no está disponible en este momento.',
            [error.TIMEOUT]: 'La ubicación tardó demasiado. Inténtalo de nuevo.',
          }
          reject(locationError(messages[error.code] ?? 'No fue posible obtener tu ubicación.'))
        },
        {
          enableHighAccuracy: true,
          maximumAge: 0,
          timeout: 10_000,
        },
      )
    })
  }
}
