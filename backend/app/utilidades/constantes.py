"""
=============================================================================
CONSTANTES
=============================================================================

Constantes globales reutilizadas en la aplicación.
Centralizarlas aquí facilita cambios posteriores.
"""

# =================================================================
# VALIDACIÓN DE USUARIOS
# =================================================================
# Dominio de email institucional permitido
# Solo usuarios con este dominio pueden registrarse
DOMINIO_CORREO = "@elpoli.edu.co"

# =================================================================
# INTERCAMBIOS
# =================================================================
# Estados válidos para un intercambio
# - pendiente: Solicitud nueva, esperando respuesta del propietario
# - aceptado: Propietario aceptó el intercambio
# - rechazado: Propietario rechazó el intercambio  
# - completado: Intercambio finalizado
ESTADOS_INTERCAMBIO = ["pendiente", "aceptado", "rechazado", "completado"]
