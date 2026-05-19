#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para inicializar la base de datos con datos de prueba y crear usuarios
Ejecutar: python init_db.py
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from app.nucleo.base_datos import Base, engine
from app.nucleo.seguridad import hash_contrasena
from app.modelos.usuario import Usuario
from app.modelos.rol import Rol
from app.modelos.articulo import Articulo
from sqlalchemy.orm import sessionmaker

# Crear sesión
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas")


def crear_roles():
    """Crea los roles por defecto"""
    print("\nCreando roles...")
    
    # Verificar si ya existen
    if db.query(Rol).count() > 0:
        print("✓ Roles ya existen")
        return
    
    roles = [
        Rol(nombre="Usuario"),
        Rol(nombre="Administrador"),
    ]
    
    db.add_all(roles)
    db.commit()
    print("✓ Roles creados")


def crear_usuarios():
    """Crea usuarios de prueba con contraseñas hasheadas"""
    print("\nCreando usuarios de prueba...")
    
    # Verificar si ya existen
    if db.query(Usuario).count() > 0:
        print("✓ Usuarios ya existen")
        return
    
    # Obtener rol de usuario
    rol_usuario = db.query(Rol).filter(Rol.nombre == "Usuario").first()
    rol_admin = db.query(Rol).filter(Rol.nombre == "Administrador").first()
    
    usuarios = [
        Usuario(
            nombre="Juan Pérez",
            email="juan@elpoli.edu.co",
            hash_contrasena=hash_contrasena("juan123"),
            rol_id=rol_usuario.id
        ),
        Usuario(
            nombre="María García",
            email="maria@elpoli.edu.co",
            hash_contrasena=hash_contrasena("maria123"),
            rol_id=rol_usuario.id
        ),
        Usuario(
            nombre="Carlos López",
            email="carlos@elpoli.edu.co",
            hash_contrasena=hash_contrasena("carlos123"),
            rol_id=rol_usuario.id
        ),
        Usuario(
            nombre="Ana Martínez",
            email="ana@elpoli.edu.co",
            hash_contrasena=hash_contrasena("ana123"),
            rol_id=rol_usuario.id
        ),
        Usuario(
            nombre="Admin",
            email="admin@elpoli.edu.co",
            hash_contrasena=hash_contrasena("admin123"),
            rol_id=rol_admin.id
        ),
    ]
    
    db.add_all(usuarios)
    db.commit()
    print("✓ Usuarios creados")


def crear_articulos():
    """Crea artículos de prueba"""
    print("\nCreando artículos de prueba...")
    
    # Verificar si ya existen
    if db.query(Articulo).count() > 0:
        print("✓ Artículos ya existen")
        return
    
    # Obtener usuarios
    juan = db.query(Usuario).filter(Usuario.email == "juan@elpoli.edu.co").first()
    maria = db.query(Usuario).filter(Usuario.email == "maria@elpoli.edu.co").first()
    carlos = db.query(Usuario).filter(Usuario.email == "carlos@elpoli.edu.co").first()
    
    articulos = [
        Articulo(
            titulo="Laptop HP",
            descripcion="Laptop en buen estado, poco usada",
            categoria="Electrónica",
            estado="Como nuevo",
            usuario_id=juan.id
        ),
        Articulo(
            titulo="Libro Python",
            descripcion="Libro de programación en Python",
            categoria="Libros",
            estado="Usado",
            usuario_id=maria.id
        ),
        Articulo(
            titulo="Monitor LG",
            descripcion="Monitor de 24 pulgadas",
            categoria="Electrónica",
            estado="Como nuevo",
            usuario_id=carlos.id
        ),
        Articulo(
            titulo="Micrófono",
            descripcion="Micrófono para streaming",
            categoria="Audio",
            estado="Nuevo",
            usuario_id=juan.id
        ),
        Articulo(
            titulo="Teclado Mecánico",
            descripcion="Teclado RGB",
            categoria="Electrónica",
            estado="Como nuevo",
            usuario_id=maria.id
        ),
    ]
    
    db.add_all(articulos)
    db.commit()
    print("✓ Artículos creados")


def main():
    """Función principal"""
    try:
        print("=" * 50)
        print("Inicializando base de datos EcoTrueque")
        print("=" * 50)
        
        crear_tablas()
        crear_roles()
        crear_usuarios()
        crear_articulos()
        
        print("\n" + "=" * 50)
        print("✓ Base de datos inicializada correctamente")
        print("=" * 50)
        print("\n👥 Usuarios de prueba:")
        print("  - juan@elpoli.edu.co / juan123")
        print("  - maria@elpoli.edu.co / maria123")
        print("  - carlos@elpoli.edu.co / carlos123")
        print("  - ana@elpoli.edu.co / ana123")
        print("  - admin@elpoli.edu.co / admin123 (Administrador)")
        print("\nPuedes iniciar el servidor: uvicorn app.main:app --reload")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
