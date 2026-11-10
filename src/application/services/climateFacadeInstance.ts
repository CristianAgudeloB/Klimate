import { OpenMeteoAdapter } from '../../infrastructure/open-meteo/OpenMeteoAdapter'
import { ClimateFacade } from './ClimateFacade'

export const climateFacade = new ClimateFacade(new OpenMeteoAdapter())
