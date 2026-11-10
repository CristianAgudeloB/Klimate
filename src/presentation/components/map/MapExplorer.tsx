import { divIcon, type LeafletMouseEvent } from 'leaflet'
import { useEffect } from 'react'
import { MapContainer, Marker, TileLayer, useMap, useMapEvents } from 'react-leaflet'
import type { Location } from '../../../domain/models/Location'

interface MapExplorerProps {
  location: Location | null
  onLocationSelect: (location: Location) => void
}

const colombiaCenter: [number, number] = [4.5709, -74.2973]

const locationMarker = divIcon({
  className: '',
  html: '<span class="location-marker" aria-hidden="true"></span>',
  iconSize: [22, 22],
  iconAnchor: [11, 22],
})

function LocationSelector({ onLocationSelect }: Pick<MapExplorerProps, 'onLocationSelect'>) {
  useMapEvents({
    click(event: LeafletMouseEvent) {
      onLocationSelect({
        latitude: event.latlng.lat,
        longitude: event.latlng.lng,
      })
    },
  })

  return null
}

function LocationViewport({ location }: Pick<MapExplorerProps, 'location'>) {
  const map = useMap()

  useEffect(() => {
    if (location) {
      map.flyTo([location.latitude, location.longitude], Math.max(map.getZoom(), 13), {
        duration: 0.7,
      })
    }
  }, [location, map])

  return null
}

export function MapExplorer({ location, onLocationSelect }: MapExplorerProps) {
  const markerPosition: [number, number] | null = location
    ? [location.latitude, location.longitude]
    : null

  return (
    <section className="map-section" aria-label="Mapa interactivo de OpenStreetMap">
      <MapContainer center={colombiaCenter} zoom={6} scrollWheelZoom className="map-canvas">
        <TileLayer
          attribution={'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <LocationSelector onLocationSelect={onLocationSelect} />
        <LocationViewport location={location} />
        {markerPosition && <Marker position={markerPosition} icon={locationMarker} />}
      </MapContainer>
    </section>
  )
}
