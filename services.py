from models import Producto
import config

def validar_producto(producto: Producto) -> bool:
    """
    Valida que los campos de un producto sean correctos.
    """
    return (
        producto.codigo_barras != ""
        and producto.nombre != ""
        and producto.precio > 0
        and producto.stock >= 0
    )

def calcular_iva(precio: float, categoria: str) -> float:
    if categoria == config.CATEGORIA_DESCUENTO:
        return precio * config.IVA_TECNOLOGIA
    return precio * config.IVA_GENERAL

def calcular_precio_final(producto: Producto) -> float:
    precio_con_iva = producto.precio + calcular_iva(producto.precio, producto.categoria)

    if producto.categoria == config.CATEGORIA_DESCUENTO:
        return precio_con_iva * (1 - config.DESCUENTO_TECNOLOGIA)

    return precio_con_iva