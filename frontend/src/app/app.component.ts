
import { Component } from '@angular/core';

import { AuthService } from './core/servicios/auth.servicio';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  constructor(public authService: AuthService) {}

  cerrarSesion(): void {
    this.authService.cerrarSesion();
  }
}
