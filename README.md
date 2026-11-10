# Klimate

Prototipo web para seleccionar un punto en OpenStreetMap y consultar sus condiciones meteorológicas actuales con Open-Meteo.

## Requisitos

- Node.js 22 o superior
- npm 10 o superior

## Desarrollo

```bash
npm install
npm run dev
```

Para comprobar calidad y generar la versión de producción:

```bash
npm run lint
npm run build
```

## Arquitectura

```text
src/
  domain/                    Modelos y contratos independientes de proveedores
  application/               Comandos y fachada de clima
  infrastructure/open-meteo/ Adaptador del proveedor meteorológico
  infrastructure/browser/    Adaptador de geolocalización del navegador
  presentation/              Componentes, estado y experiencia de usuario en React
    components/map/          Integración visual del mapa
    components/weather/      Panel de condiciones actuales
    hooks/                   Estado reactivo de la aplicación
```

`useSelectedLocation` concentra el estado de la ubicación. El mapa emite la selección y los componentes consumidores reaccionan a ese cambio, estableciendo la base del patrón Observer.

`OpenMeteoAdapter` transforma la respuesta externa al modelo interno `ClimateData`, aplicando el patrón Adapter. `ClimateFacade` expone una única operación de consulta para la interfaz y oculta el proveedor concreto, aplicando el patrón Facade.

`LocateUserCommand` encapsula la acción de solicitar la ubicación actual. `BrowserLocationProvider` adapta la API de geolocalización del navegador, por lo que el componente de React no depende directamente de ella.

La siguiente etapa puede incorporar datos de calidad del aire y reglas de recomendación según actividad.
