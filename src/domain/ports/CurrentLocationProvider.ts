import type { Location } from '../models/Location'

export interface CurrentLocationProvider {
  getCurrentLocation(): Promise<Location>
}
