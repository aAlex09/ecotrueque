"""
=============================================================================
SEED - Datos Iniciales
=============================================================================

Carga datos de prueba en la BD cuando la aplicación inicia.
Se ejecuta una sola vez (verifica si los datos ya existen).

Incluye:
1. Roles: "usuario" y "admin"
2. Usuarios de prueba: 4 usuarios + 1 admin (contraseña: nombre+123)
3. Artículos de prueba: 10 artículos en diferentes categorías

Nota: Los datos se crean con hashes de contraseña correctos (bcrypt),
      por lo que se puede loguear directamente.
"""

from sqlalchemy.orm import Session

from app.modelos.articulo import Articulo
from app.modelos.rol import Rol
from app.modelos.usuario import Usuario
from app.nucleo.seguridad import hash_contrasena, verificar_contrasena
from passlib.exc import UnknownHashError


def seed_data(db: Session) -> None:
    """
    Carga datos iniciales en la base de datos.
    
    Pasos:
    1. Verifica/crea roles
    2. Verifica/crea usuarios (hashea contraseñas si es necesario)
    3. Crea artículos de prueba
    4. Commit único al final (transacción atómica)
    
    Args:
        db: Sesión de base de datos
    """
    
    # =================================================================
    # CREAR ROLES
    # =================================================================
    # Definición de roles disponibles
    roles_def = {
        "usuario": "Usuario normal de la plataforma",
        "admin": "Administrador del sistema",
    }

    # Crear o verificar roles
    roles: dict[str, Rol] = {}
    for nombre, descripcion in roles_def.items():
        # Buscar si el rol ya existe
        rol = db.query(Rol).filter(Rol.nombre == nombre).first()
        if not rol:
            # No existe → crear
            rol = Rol(nombre=nombre, descripcion=descripcion)
            db.add(rol)
            db.flush()  # Flush: guardaen transacción pero no commit
        roles[nombre] = rol

    # =================================================================
    # CREAR USUARIOS DE PRUEBA
    # =================================================================
    # Formato: (nombre, email, password, rol)
    usuarios_def = [
        ("Juan Pérez", "juan@elpoli.edu.co", "juan123", "usuario"),
        ("María García", "maria@elpoli.edu.co", "maria123", "usuario"),
        ("Carlos López", "carlos@elpoli.edu.co", "carlos123", "usuario"),
        ("Ana Martínez", "ana@elpoli.edu.co", "ana123", "usuario"),
        ("Admin Sistema", "admin@elpoli.edu.co", "admin123", "admin"),
    ]

    usuarios: dict[str, Usuario] = {}
    for nombre, email, password, rol_nombre in usuarios_def:
        # Buscar si el usuario ya existe
        usuario = db.query(Usuario).filter(Usuario.email == email.lower()).first()
        if not usuario:
            # No existe → crear con contraseña hasheada
            usuario = Usuario(
                nombre=nombre,
                email=email.lower(),
                hash_contrasena=hash_contrasena(password),
                rol_id=roles[rol_nombre].id,
            )
            db.add(usuario)
            db.flush()
        else:
            # Usuario existe → verificar si credenciales son correctas
            # (por si cambió la contraseña de prueba)
            try:
                cred_ok = verificar_contrasena(password, usuario.hash_contrasena)
            except (UnknownHashError, ValueError):
                cred_ok = False
            
            # Si la contraseña no coincide, actualizar hash
            if not cred_ok:
                usuario.hash_contrasena = hash_contrasena(password)
            
            # Si no tiene rol, asignarlo
            if usuario.rol_id is None:
                usuario.rol_id = roles[rol_nombre].id
        
        usuarios[email] = usuario

    # =================================================================
    # CREAR ARTÍCULOS DE PRUEBA
    # =================================================================
    # Solo crear si la tabla está vacía
    if db.query(Articulo).count() == 0:
        # Formato: (titulo, descripcion, categoria, estado, disponible, owner_email)
        articulos_def = [
            (
                "Libro de Python",
                "Libro de programación Python, edición 2023, en buen estado",
                "Libros",
                "disponible",
                True,
                "juan@elpoli.edu.co",
            ),
            (
                "Chamarra de invierno",
                "Chamarra negra de invierno, talla M, poco uso",
                "Ropa",
                "disponible",
                True,
                "maria@elpoli.edu.co",
            ),
            (
                "Cuadernos de estudio",
                "Pack de 5 cuadernos para tomar notas, nuevos",
                "Materiales de estudio",
                "disponible",
                True,
                "juan@elpoli.edu.co",
            ),
            (
                "Novela de ficción",
                "Novela de ciencia ficción, páginas sin subrayar",
                "Libros",
                "disponible",
                True,
                "carlos@elpoli.edu.co",
            ),
            (
                "Juguete educativo",
                "Juguete armable para niños mayores de 8 años",
                "Juguetes",
                "disponible",
                True,
                "maria@elpoli.edu.co",
            ),
            (
                "Diccionario inglés",
                "Diccionario inglés-español, tapa dura",
                "Libros",
                "disponible",
                True,
                "ana@elpoli.edu.co",
            ),
            (
                "Tenis deportivos",
                "Tenis para correr, marca reconocida, poco uso",
                "Ropa",
                "disponible",
                True,
                "juan@elpoli.edu.co",
            ),
            (
                "Lápices de colores",
                "Juego de 48 lápices de colores, completo",
                "Materiales de estudio",
                "disponible",
                True,
                "carlos@elpoli.edu.co",
            ),
            (
                "Mochila universitaria",
                "Mochila con compartimentos, resistente",
                "Mochilas",
                "disponible",
                True,
                "ana@elpoli.edu.co",
            ),
            (
                "Audífonos Bluetooth",
                "Audífonos inalámbricos, buena batería",
                "Electrónica",
                "disponible",
                True,
                "maria@elpoli.edu.co",
            ),
        ]

        # Crear cada artículo
        for titulo, descripcion, categoria, estado, disponible, owner_email in articulos_def:
            propietario = usuarios[owner_email]
            db.add(
                Articulo(
                    titulo=titulo,
                    descripcion=descripcion,
                    categoria=categoria,
                    estado=estado,
                    disponible=disponible,
                    propietario_id=propietario.id,
                )
            )

    # =================================================================
    # COMMIT ÚNICO
    # =================================================================
    # Guardar todos los cambios en una sola transacción atómica
    db.commit()
