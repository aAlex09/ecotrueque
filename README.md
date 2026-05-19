# 🌱 EcoTrueque - Plataforma de Intercambio Comunitario

Proyecto web para intercambiar artículos entre estudiantes de forma comunitaria y sostenible.

## 📂 Estructura del Proyecto

```
ecotrueque/
├── backend/                     # API REST (FastAPI + PostgreSQL)
│   ├── app/
│   │   ├── rutas/              # Endpoints HTTP
│   │   ├── modelos/            # Modelos de base de datos
│   │   ├── esquemas/           # Validación Pydantic
│   │   ├── servicios/          # Lógica de negocio
│   │   ├── nucleo/             # Configuración y seguridad
│   │   ├── utilidades/         # Constantes y helpers
│   │   └── main.py             # Entrada principal
│   ├── pruebas/                # Tests
│   ├── init_db.py              # Inicializar BD con datos
│   ├── requirements.txt        # Dependencias
│   ├── .env                    # Variables de entorno
│   └── README.md
│
├── frontend/                    # Web App (Angular)
│   ├── src/app/
│   │   ├── core/               # Servicios, guards, modelos
│   │   ├── compartido/         # Componentes reutilizables
│   │   ├── paginas/            # Componentes de página
│   │   ├── app-routing.module.ts
│   │   └── app.component.ts
│   └── README.md
│
├── docs/                        # Documentación
│   ├── arquitectura.md
│   ├── bd.md
│   ├── endpoints.md
│   ├── flujo.md
│   ├── modulos.md
│   └── backlog.md
│
├── .gitignore
└── README.md
```

## 🚀 Inicio Rápido

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Inicializar base de datos
python init_db.py

# Ejecutar servidor
uvicorn app.main:app --reload
```

✅ **Backend en:** http://localhost:8000/docs

### Frontend

```bash
cd frontend

npm install
npm start
```

✅ **Frontend en:** http://localhost:4200

## 👥 Usuarios de Prueba

| Email | Contraseña |
|-------|-----------|
| juan@elpoli.edu.co | juan123 |
| maria@elpoli.edu.co | maria123 |
| carlos@elpoli.edu.co | carlos123 |
| ana@elpoli.edu.co | ana123 |
| admin@elpoli.edu.co | admin123 |

## 📚 Documentación

- **[Backend README](./backend/README.md)**
- **[Frontend README](./frontend/README.md)**
- **[Documentación General](./docs/)**

## 🛠️ Tecnologías

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** Angular, TypeScript
- **Autenticación:** JWT + Bcrypt

## 🔐 Características

- ✅ Autenticación segura
- ✅ CRUD de artículos
- ✅ Sistema de intercambios
- ✅ Datos de prueba automáticos
- ✅ API documentada

## 📝 Licencia

Proyecto educativo. Libre para usar y modificar.

---

¡Bienvenido a EcoTrueque! 🌍♻️
