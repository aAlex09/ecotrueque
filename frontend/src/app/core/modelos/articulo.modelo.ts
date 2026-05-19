
export interface Articulo {
  id: number;
  titulo: string;
  descripcion?: string;
  categoria: string;
  estado: string;
  disponible: boolean;
  propietario_id: number;
  creado_en?: string;
}

export interface ArticuloCrear {
  titulo: string;
  descripcion?: string;
  categoria: string;
  estado: string;
}

export interface ArticuloActualizar {
  titulo?: string;
  descripcion?: string;
  categoria?: string;
  estado?: string;
  disponible?: boolean;
}
