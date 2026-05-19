import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../core/servicios/auth.servicio';

@Component({
  selector: 'app-registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.css'],
})
export class RegistroComponent {
  mensaje = '';
  error = '';

  form = this.fb.nonNullable.group({
    nombre: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
  ) {}

  registrar(): void {
    this.mensaje = '';
    this.error = '';
    if (this.form.invalid) {
      this.error = 'Completa los datos requeridos.';
      return;
    }

    const datos = this.form.getRawValue();
    this.authService.registrar(datos).subscribe({
      next: () => {
        this.mensaje = 'Registro exitoso. Ahora puedes iniciar sesion.';
        this.form.reset({ nombre: '', email: '', password: '' });
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo registrar.';
      },
    });
  }
}
