
def texto_no_vacio(valor: str) -> str:
    valor = valor.strip()
    if not valor:
        raise ValueError("El texto no puede estar vacio")
    return valor
