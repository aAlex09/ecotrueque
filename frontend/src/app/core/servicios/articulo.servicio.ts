
import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import {
  Articulo,
  ArticuloActualizar,
  ArticuloCrear,
} from '../modelos/articulo.modelo';

@Injectable({
  providedIn: 'root',
})
export class ArticuloService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  listar(q?: string): Observable<Articulo[]> {
    let params = new HttpParams();
    if (q) {
      params = params.set('q', q);
    }
    return this.http.get<Articulo[]>(`${this.apiUrl}/articulos`, { params });
  }

  obtener(id: number): Observable<Articulo> {
    return this.http.get<Articulo>(`${this.apiUrl}/articulos/${id}`);
  }

  crear(datos: ArticuloCrear): Observable<Articulo> {
    return this.http.post<Articulo>(`${this.apiUrl}/articulos`, datos);
  }

  actualizar(id: number, datos: ArticuloActualizar): Observable<Articulo> {
    return this.http.put<Articulo>(`${this.apiUrl}/articulos/${id}`, datos);
  }

  eliminar(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/articulos/${id}`);
  }
}
