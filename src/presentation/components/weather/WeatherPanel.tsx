import type { ClimateData } from '../../../domain/models/ClimateData'
import type { Location } from '../../../domain/models/Location'

interface WeatherPanelProps {
  climate: ClimateData | null
  error: string | null
  isLoading: boolean
  location: Location | null
  onRetry: () => void
}

function formatNumber(value: number) {
  return new Intl.NumberFormat('es-CO', { maximumFractionDigits: 1 }).format(value)
}

function formatCoordinates(location: Location) {
  return `${location.latitude.toFixed(3)}, ${location.longitude.toFixed(3)}`
}

function Metrics({ climate }: Pick<WeatherPanelProps, 'climate'>) {
  if (!climate) {
    return null
  }

  return (
    <dl className="metrics">
      <div>
        <dt>Sensación</dt>
        <dd>{formatNumber(climate.apparentTemperature)} °C</dd>
      </div>
      <div>
        <dt>Humedad</dt>
        <dd>{formatNumber(climate.humidity)}%</dd>
      </div>
      <div>
        <dt>Viento</dt>
        <dd>{formatNumber(climate.windSpeed)} km/h</dd>
      </div>
      <div>
        <dt>Precipitación</dt>
        <dd>{formatNumber(climate.precipitation)} mm</dd>
      </div>
    </dl>
  )
}

export function WeatherPanel({ climate, error, isLoading, location, onRetry }: WeatherPanelProps) {
  if (!location) {
    return <section className="weather-panel empty-state">Selecciona un punto en el mapa.</section>
  }

  if (isLoading) {
    return <section className="weather-panel loading-state" aria-live="polite">Consultando condiciones…</section>
  }

  if (error) {
    return (
      <section className="weather-panel error-state" aria-live="polite">
        <p>{error}</p>
        <button type="button" onClick={onRetry}>Reintentar</button>
      </section>
    )
  }

  if (!climate) {
    return null
  }

  return (
    <section className="weather-panel" aria-live="polite">
      <div className="condition-line">
        <span className={climate.isDay ? 'sun-indicator' : 'moon-indicator'} aria-hidden="true" />
        {climate.condition}
      </div>
      <p className="temperature">{formatNumber(climate.temperature)}<span>°C</span></p>
      <Metrics climate={climate} />
      <p className="coordinates">{formatCoordinates(location)}</p>
    </section>
  )
}
