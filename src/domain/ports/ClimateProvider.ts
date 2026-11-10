import type { ClimateData } from '../models/ClimateData'
import type { Location } from '../models/Location'

export interface ClimateProvider {
  getCurrentClimate(location: Location, signal?: AbortSignal): Promise<ClimateData>
}
