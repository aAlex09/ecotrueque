import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../core/servicios/auth.servicio';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  mensaje = '';
  error = '';

  form = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]],
  });

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
  ) {}

  login(): void {
    this.mensaje = '';
    this.error = '';
    if (this.form.invalid) {
      this.error = 'Completa los datos requeridos.';
      return;
    }

    const { email, password } = this.form.getRawValue();
    this.authService.login(email, password).subscribe({
      next: () => {
        this.mensaje = 'Inicio de sesion correcto.';
        this.router.navigate(['/catalogo']);
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo iniciar sesion.';
      },
    });
  }
}
