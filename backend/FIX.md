# ✅ ERROR CORREGIDO

## Problema
```
ImportError: cannot import name 'hash_contraseña' from 'app.nucleo.seguridad'
```

## Causa
Dos errores de tipografía en `init_db.py`:

1. Función incorrecta: `hash_contraseña` (con tilde)
   - ✅ Correcto: `hash_contrasena` (sin tilde)

2. Atributo de modelo incorrecto: `contraseña_hash`
   - ✅ Correcto: `hash_contrasena` (en Usuario)

## Solución Aplicada
Actualizado `init_db.py`:
- Línea 15: `hash_contraseña` → `hash_contrasena`
- Líneas 70-98: Todos los `contraseña_hash=` → `hash_contrasena=`

## Resultado
✅ init_db.py está completamente corregido

---

## Ahora ejecuta:

```bash
python init_db.py
```

**Resultado esperado:**
```
==================================================
Inicializando base de datos EcoTrueque
==================================================
Creando tablas...
✓ Tablas creadas

Creando roles...
✓ Roles creados

Creando usuarios de prueba...
✓ Usuarios creados

Creando artículos de prueba...
✓ Artículos creados

==================================================
✓ Base de datos inicializada correctamente
==================================================

👥 Usuarios de prueba:
  - juan@elpoli.edu.co / juan123
  - maria@elpoli.edu.co / maria123
  - carlos@elpoli.edu.co / carlos123
  - ana@elpoli.edu.co / ana123
  - admin@elpoli.edu.co / admin123 (Administrador)

Puedes iniciar el servidor: uvicorn app.main:app --reload
```

---

## Luego ejecuta:

```bash
uvicorn app.main:app --reload
```

**Accede a:** http://localhost:8000/docs

**Logueate con:**
- Email: juan@elpoli.edu.co
- Password: juan123
