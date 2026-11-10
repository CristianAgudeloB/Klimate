import { MapExplorer } from './presentation/components/map/MapExplorer'
import { WeatherPanel } from './presentation/components/weather/WeatherPanel'
import { useClimate } from './presentation/hooks/useClimate'
import { useCurrentLocation } from './presentation/hooks/useCurrentLocation'
import { useSelectedLocation } from './presentation/hooks/useSelectedLocation'
import './App.css'

function App() {
  const { selectedLocation, selectLocation } = useSelectedLocation()
  const { climate, error, isLoading, refresh } = useClimate(selectedLocation)
  const { error: locationError, isLocating, locate } = useCurrentLocation(selectLocation)

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Klimate, inicio">
          <span className="brand-mark" aria-hidden="true">K</span>
          <span>Klimate</span>
        </a>
      </header>

      <section className="workspace" aria-label="Clima por ubicación">
        <aside className="sidebar">
          <h1>Clima actual</h1>
          <div className="location-action">
            <button className="locate-button" type="button" onClick={locate} disabled={isLocating}>
              <span aria-hidden="true">⌖</span>
              {isLocating ? 'Buscando ubicación…' : 'Usar mi ubicación'}
            </button>
            {locationError && <p className="location-error" role="alert">{locationError}</p>}
          </div>
          <WeatherPanel
            climate={climate}
            error={error}
            isLoading={isLoading}
            location={selectedLocation}
            onRetry={refresh}
          />
        </aside>

        <MapExplorer location={selectedLocation} onLocationSelect={selectLocation} />
      </section>
    </main>
  )
}

export default App
