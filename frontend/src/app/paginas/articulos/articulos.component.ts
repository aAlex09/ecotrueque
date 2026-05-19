import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import {
  Articulo,
  ArticuloActualizar,
  ArticuloCrear,
} from '../../core/modelos/articulo.modelo';
import { ArticuloService } from '../../core/servicios/articulo.servicio';
import { UsuarioService } from '../../core/servicios/usuario.servicio';

@Component({
  selector: 'app-articulos',
  templateUrl: './articulos.component.html',
  styleUrls: ['./articulos.component.css'],
})
export class ArticulosComponent implements OnInit {
  articulos: Articulo[] = [];
  usuarioId?: number;
  mensaje = '';
  error = '';
  editandoId?: number;

  form = this.fb.nonNullable.group({
    titulo: ['', Validators.required],
    descripcion: [''],
    categoria: ['', Validators.required],
    estado: ['', Validators.required],
  });

  constructor(
    private fb: FormBuilder,
    private articuloService: ArticuloService,
    private usuarioService: UsuarioService,
  ) {}

  ngOnInit(): void {
    this.usuarioService.obtenerPerfil().subscribe({
      next: (usuario) => {
        this.usuarioId = usuario.id;
        this.cargar();
      },
      error: () => (this.error = 'No se pudo cargar el perfil.'),
    });
  }

  cargar(): void {
    this.articuloService.listar().subscribe({
      next: (data) => {
        this.articulos = this.usuarioId
          ? data.filter((a) => a.propietario_id === this.usuarioId)
          : data;
      },
      error: () => (this.error = 'No se pudieron cargar los articulos.'),
    });
  }

  guardar(): void {
    this.mensaje = '';
    this.error = '';
    if (this.form.invalid) {
      this.error = 'Completa los datos requeridos.';
      return;
    }

    const datos = this.form.getRawValue();
    if (this.editandoId) {
      const update: ArticuloActualizar = { ...datos };
      this.articuloService.actualizar(this.editandoId, update).subscribe({
        next: () => {
          this.mensaje = 'Articulo actualizado.';
          this.editandoId = undefined;
          this.form.reset({
            titulo: '',
            descripcion: '',
            categoria: '',
            estado: '',
          });
          this.cargar();
        },
        error: (err) =>
          (this.error = err?.error?.detail || 'No se pudo actualizar.'),
      });
      return;
    }

    this.articuloService.crear(datos).subscribe({
      next: () => {
        this.mensaje = 'Articulo creado.';
        this.form.reset({
          titulo: '',
          descripcion: '',
          categoria: '',
          estado: '',
        });
        this.cargar();
      },
      error: (err) => (this.error = err?.error?.detail || 'No se pudo crear.'),
    });
  }

  editar(articulo: Articulo): void {
    this.editandoId = articulo.id;
    this.form.patchValue({
      titulo: articulo.titulo,
      descripcion: articulo.descripcion || '',
      categoria: articulo.categoria,
      estado: articulo.estado,
    });
  }

  eliminar(articulo: Articulo): void {
    if (!confirm('Deseas eliminar este articulo?')) {
      return;
    }
    this.articuloService.eliminar(articulo.id).subscribe({
      next: () => {
        this.mensaje = 'Articulo eliminado.';
        this.cargar();
      },
      error: (err) => (this.error = err?.error?.detail || 'No se pudo eliminar.'),
    });
  }
}
