
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { environment } from '../../../environments/environment';
import { RegistroRequest, TokenResponse } from '../modelos/auth.modelo';
import { Usuario } from '../modelos/usuario.modelo';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private tokenKey = 'ecotrueque_token';

  constructor(private http: HttpClient) {}

  registrar(datos: RegistroRequest): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.apiUrl}/auth/registro`, datos);
  }

  login(email: string, password: string): Observable<TokenResponse> {
    const body = new HttpParams().set('username', email).set('password', password);
    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
    });

    return this.http
      .post<TokenResponse>(`${this.apiUrl}/auth/login`, body.toString(), { headers })
      .pipe(tap((token) => this.guardarToken(token.access_token)));
  }

  guardarToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  obtenerToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  cerrarSesion(): void {
    localStorage.removeItem(this.tokenKey);
  }

  estaLogueado(): boolean {
    return !!this.obtenerToken();
  }
}
