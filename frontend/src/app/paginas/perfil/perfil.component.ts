import { Component, OnInit } from '@angular/core';

import { Usuario } from '../../core/modelos/usuario.modelo';
import { UsuarioService } from '../../core/servicios/usuario.servicio';

@Component({
  selector: 'app-perfil',
  templateUrl: './perfil.component.html',
  styleUrls: ['./perfil.component.css'],
})
export class PerfilComponent implements OnInit {
  usuario?: Usuario;
  error = '';

  constructor(private usuarioService: UsuarioService) {}

  ngOnInit(): void {
    this.usuarioService.obtenerPerfil().subscribe({
      next: (usuario) => (this.usuario = usuario),
      error: () => (this.error = 'No se pudo cargar el perfil.'),
    });
  }
}
