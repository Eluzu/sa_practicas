IVA = 0.15
IVA_TECNOLOGIA = 0.12
CATEGORIA_DESCUENTO = "Tecnología"
DESCUENTO_TECNOLOGIA = 0.10


def calcular_iva(producto):

    if producto.categoria == "Tecnología":
        return producto.precio * IVA_TECNOLOGIA

    return producto.precio * IVA


def calcular_precio_final(producto):

    precio_con_iva = producto.precio + calcular_iva(producto)

    if producto.categoria == CATEGORIA_DESCUENTO:
        return precio_con_iva * (1 - DESCUENTO_TECNOLOGIA)

    return precio_con_iva