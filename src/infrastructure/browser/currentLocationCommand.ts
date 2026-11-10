import { LocateUserCommand } from '../../application/commands/LocateUserCommand'
import { BrowserLocationProvider } from './BrowserLocationProvider'

export const currentLocationCommand = new LocateUserCommand(new BrowserLocationProvider())
