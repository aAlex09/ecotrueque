
export interface Intercambio {
  id: number;
  articulo_id: number;
  solicitante_id: number;
  propietario_id: number;
  estado: string;
  creado_en?: string;
  actualizado_en?: string;
}

export interface IntercambioCrear {
  articulo_id: number;
}

export interface IntercambioEstado {
  estado: string;
}
