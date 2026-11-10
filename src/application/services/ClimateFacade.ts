import type { ClimateData } from '../../domain/models/ClimateData'
import type { Location } from '../../domain/models/Location'
import type { ClimateProvider } from '../../domain/ports/ClimateProvider'

export class ClimateFacade {
  private readonly provider: ClimateProvider

  constructor(provider: ClimateProvider) {
    this.provider = provider
  }

  getCurrentClimate(location: Location, signal?: AbortSignal): Promise<ClimateData> {
    return this.provider.getCurrentClimate(location, signal)
  }
}
