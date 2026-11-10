import type { Location } from '../../domain/models/Location'
import type { CurrentLocationProvider } from '../../domain/ports/CurrentLocationProvider'

export class LocateUserCommand {
  private readonly provider: CurrentLocationProvider

  constructor(provider: CurrentLocationProvider) {
    this.provider = provider
  }

  execute(): Promise<Location> {
    return this.provider.getCurrentLocation()
  }
}
