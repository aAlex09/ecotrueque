
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import {
  Intercambio,
  IntercambioCrear,
  IntercambioEstado,
} from '../modelos/intercambio.modelo';

@Injectable({
  providedIn: 'root',
})
export class IntercambioService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  solicitar(datos: IntercambioCrear): Observable<Intercambio> {
    return this.http.post<Intercambio>(`${this.apiUrl}/intercambios`, datos);
  }

  listarMios(): Observable<Intercambio[]> {
    return this.http.get<Intercambio[]>(`${this.apiUrl}/intercambios/mios`);
  }

  actualizarEstado(
    intercambioId: number,
    datos: IntercambioEstado,
  ): Observable<Intercambio> {
    return this.http.put<Intercambio>(
      `${this.apiUrl}/intercambios/${intercambioId}/estado`,
      datos,
    );
  }
}
