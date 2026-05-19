# 🌱 EcoTrueque - Backend API

API REST para la plataforma de intercambio comunitario.

## ⚡ Inicio Rápido

### 1️⃣ Instalación

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate
# O (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Configurar Base de Datos

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus datos PostgreSQL
# DATABASE_URL=postgresql://usuario:password@localhost:5432/ecotrueque
```

### 3️⃣ Inicializar Base de Datos

```bash
python init_db.py
```

### 4️⃣ Ejecutar Servidor

```bash
uvicorn app.main:app --reload
```

✅ API en: http://localhost:8000/docs

## 👥 Usuarios de Prueba

Después de `python init_db.py`:

| Email | Contraseña |
|-------|-----------|
| juan@elpoli.edu.co | juan123 |
| maria@elpoli.edu.co | maria123 |
| carlos@elpoli.edu.co | carlos123 |
| ana@elpoli.edu.co | ana123 |
| admin@elpoli.edu.co | admin123 |

## 📂 Estructura

```
app/
├── rutas/          # Endpoints HTTP
├── modelos/        # Base de datos
├── esquemas/       # Validación
├── servicios/      # Lógica
├── nucleo/         # Config
├── utilidades/     # Helpers
└── main.py         # Entrada
```

## 🔐 Tecnologías

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT + Bcrypt

## 📚 Documentación

| Documento | Descripción |
|-----------|-----------|
| [API_ENDPOINTS.md](./API_ENDPOINTS.md) | Todos los endpoints disponibles |
| [ARQUITECTURA.md](./ARQUITECTURA.md) | Diseño y estructura del proyecto |

---

## 👥 Usuarios de Prueba

Los usuarios se cargan automáticamente al iniciar.

| Email | Contraseña | Rol |
|-------|-----------|-----|
| juan@elpoli.edu.co | juan123 | Usuario |
| maria@elpoli.edu.co | maria123 | Usuario |
| carlos@elpoli.edu.co | carlos123 | Usuario |
| ana@elpoli.edu.co | ana123 | Usuario |
| admin@elpoli.edu.co | admin123 | Admin |

---

## 🏗️ Estructura del Proyecto

```
app/
├── nucleo/              # Configuración, DB, seguridad
├── modelos/             # Definición de tablas (ORM)
├── esquemas/            # Validación de datos (Pydantic)
├── servicios/           # Lógica de negocio
├── rutas/               # Endpoints HTTP
├── utilidades/          # Constantes
├── main.py              # Punto de entrada
└── seed.py              # Datos iniciales
```

---

## 🔐 Flujo de Autenticación

```
1. Cliente hace POST /auth/login (email, password)
2. Servidor autentica y retorna JWT token
3. Cliente guarda token y lo envía en cada petición:
   Authorization: Bearer <token>
4. Servidor valida token en dependencias
5. Si es válido: procesa la petición
   Si no: retorna 401 Unauthorized
```

---

## 📦 Dependencias Principales

- **FastAPI**: Framework web
- **SQLAlchemy**: ORM para BD
- **PostgreSQL**: Base de datos
- **Pydantic**: Validación de datos
- **JWT**: Autenticación sin estado
- **Bcrypt**: Hash de contraseñas

---

## 🚀 Variables de Entorno (.env)

```bash
# Base de Datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/ecotrueque

# Seguridad
SECRET_KEY=tuclavesecretsuperlargarandomizada

# JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS (URLs del frontend)
CORS_ORIGINS=http://localhost:4200,http://localhost:3000
```

---

## 🧪 Probar Endpoints

### Registro de Usuario

```bash
curl -X POST "http://localhost:8000/auth/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Tu Nombre",
    "email": "tu@elpoli.edu.co",
    "password": "TuContraseña123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan@elpoli.edu.co&password=juan123"
```

### Obtener Mi Perfil

```bash
curl -X GET "http://localhost:8000/usuarios/me" \
  -H "Authorization: Bearer <tu_token_aqui>"
```

---

## 📋 Estructura de Datos

### Usuario
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@elpoli.edu.co",
  "creado_en": "2024-01-15T10:30:00"
}
```

### Artículo
```json
{
  "id": 1,
  "titulo": "Laptop HP",
  "descripcion": "Laptop poco usada",
  "categoria": "Electrónica",
  "estado": "Como nuevo",
  "disponible": true,
  "propietario_id": 1,
  "creado_en": "2024-01-15T10:30:00"
}
```

### Intercambio
```json
{
  "id": 1,
  "articulo_id": 1,
  "solicitante_id": 2,
  "propietario_id": 1,
  "estado": "pendiente",
  "creado_en": "2024-01-15T10:40:00",
  "actualizado_en": null
}
```

---

## 🤝 Contribuir

1. Hacer fork del proyecto
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am "Agrega nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

---

## 📝 Licencia

Este proyecto está bajo licencia MIT.

---

## 👨‍💻 Autor

EcoTrueque - Plataforma de Intercambio Comunitario