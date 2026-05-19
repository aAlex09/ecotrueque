import { Component, OnInit } from '@angular/core';

import { Intercambio } from '../../core/modelos/intercambio.modelo';
import { IntercambioService } from '../../core/servicios/intercambio.servicio';

@Component({
  selector: 'app-intercambios',
  templateUrl: './intercambios.component.html',
  styleUrls: ['./intercambios.component.css'],
})
export class IntercambiosComponent implements OnInit {
  intercambios: Intercambio[] = [];
  mensaje = '';
  error = '';
  estados = ['pendiente', 'aceptado', 'rechazado', 'completado'];

  constructor(private intercambioService: IntercambioService) {}

  ngOnInit(): void {
    this.cargar();
  }

  cargar(): void {
    this.intercambioService.listarMios().subscribe({
      next: (data) => (this.intercambios = data),
      error: () => (this.error = 'No se pudieron cargar los intercambios.'),
    });
  }

  actualizar(intercambio: Intercambio): void {
    this.mensaje = '';
    this.error = '';
    this.intercambioService
      .actualizarEstado(intercambio.id, { estado: intercambio.estado })
      .subscribe({
        next: () => {
          this.mensaje = 'Estado actualizado.';
          this.cargar();
        },
        error: (err) =>
          (this.error = err?.error?.detail || 'No se pudo actualizar.'),
      });
  }
}
