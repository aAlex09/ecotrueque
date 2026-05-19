import { Component, OnInit } from '@angular/core';

import { Articulo } from '../../core/modelos/articulo.modelo';
import { ArticuloService } from '../../core/servicios/articulo.servicio';
import { AuthService } from '../../core/servicios/auth.servicio';
import { IntercambioService } from '../../core/servicios/intercambio.servicio';

@Component({
  selector: 'app-catalogo',
  templateUrl: './catalogo.component.html',
  styleUrls: ['./catalogo.component.css'],
})
export class CatalogoComponent implements OnInit {
  articulos: Articulo[] = [];
  busqueda = '';
  mensaje = '';
  error = '';

  constructor(
    private articuloService: ArticuloService,
    private intercambioService: IntercambioService,
    public authService: AuthService,
  ) {}

  ngOnInit(): void {
    this.cargar();
  }

  cargar(): void {
    this.articuloService.listar(this.busqueda).subscribe({
      next: (data) => (this.articulos = data),
      error: () => (this.error = 'No se pudo cargar el catalogo.'),
    });
  }

  solicitarIntercambio(articuloId: number): void {
    this.mensaje = '';
    this.error = '';
    this.intercambioService.solicitar({ articulo_id: articuloId }).subscribe({
      next: () => (this.mensaje = 'Solicitud enviada.'),
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo solicitar el intercambio.';
      },
    });
  }
}
