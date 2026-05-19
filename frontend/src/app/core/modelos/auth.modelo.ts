
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface RegistroRequest {
  nombre: string;
  email: string;
  password: string;
}
