import type { ClimateData } from '../../domain/models/ClimateData'
import type { Location } from '../../domain/models/Location'
import type { ClimateProvider } from '../../domain/ports/ClimateProvider'

interface OpenMeteoResponse {
  current?: {
    apparent_temperature?: number
    is_day?: number
    precipitation?: number
    relative_humidity_2m?: number
    temperature_2m?: number
    time?: string
    weather_code?: number
    wind_speed_10m?: number
  }
}

const endpoint = 'https://api.open-meteo.com/v1/forecast'

const weatherDescriptions: Record<number, string> = {
  0: 'Despejado',
  1: 'Mayormente despejado',
  2: 'Parcialmente nublado',
  3: 'Nublado',
  45: 'Neblina',
  48: 'Neblina con escarcha',
  51: 'Llovizna ligera',
  53: 'Llovizna moderada',
  55: 'Llovizna intensa',
  56: 'Llovizna helada ligera',
  57: 'Llovizna helada intensa',
  61: 'Lluvia ligera',
  63: 'Lluvia moderada',
  65: 'Lluvia intensa',
  66: 'Lluvia helada ligera',
  67: 'Lluvia helada intensa',
  71: 'Nieve ligera',
  73: 'Nieve moderada',
  75: 'Nieve intensa',
  77: 'Granizo',
  80: 'Chubascos ligeros',
  81: 'Chubascos moderados',
  82: 'Chubascos intensos',
  85: 'Nevadas ligeras',
  86: 'Nevadas intensas',
  95: 'Tormenta',
  96: 'Tormenta con granizo',
  99: 'Tormenta fuerte con granizo',
}

function isNumber(value: unknown): value is number {
  return typeof value === 'number' && Number.isFinite(value)
}

function mapCurrentWeather(response: OpenMeteoResponse): ClimateData {
  const current = response.current

  if (
    !current ||
    !isNumber(current.temperature_2m) ||
    !isNumber(current.apparent_temperature) ||
    !isNumber(current.relative_humidity_2m) ||
    !isNumber(current.wind_speed_10m) ||
    !isNumber(current.precipitation) ||
    !isNumber(current.weather_code) ||
    typeof current.time !== 'string'
  ) {
    throw new Error('La respuesta meteorológica no tiene el formato esperado.')
  }

  return {
    apparentTemperature: current.apparent_temperature,
    condition: weatherDescriptions[current.weather_code] ?? 'Condición no disponible',
    humidity: current.relative_humidity_2m,
    isDay: current.is_day === 1,
    observedAt: current.time,
    precipitation: current.precipitation,
    temperature: current.temperature_2m,
    windSpeed: current.wind_speed_10m,
  }
}

export class OpenMeteoAdapter implements ClimateProvider {
  async getCurrentClimate(location: Location, signal?: AbortSignal): Promise<ClimateData> {
    const search = new URLSearchParams({
      latitude: String(location.latitude),
      longitude: String(location.longitude),
      current: 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,is_day',
      temperature_unit: 'celsius',
      wind_speed_unit: 'kmh',
      precipitation_unit: 'mm',
      timezone: 'auto',
    })
    const response = await fetch(`${endpoint}?${search}`, { signal })

    if (!response.ok) {
      throw new Error('No fue posible consultar las condiciones actuales.')
    }

    return mapCurrentWeather(await response.json() as OpenMeteoResponse)
  }
}
