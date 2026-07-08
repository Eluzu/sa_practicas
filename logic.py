from dataclasses import asdict
import storage
from models import Producto

IVA_GENERAL = 0.15
IVA_TECNOLOGIA = 0.12
CATEGORIA_TECNOLOGIA = "Tecnología"
DESCUENTO_TECNOLOGIA = 0.10

def validar_producto(producto: Producto) -> bool:
    return (producto.codigo_barras != "" and producto.nombre != "" 
            and producto.precio > 0 and producto.stock >= 0)

def calcular_iva(precio: float, categoria: str) -> float:
    tasa = IVA_TECNOLOGIA if categoria == CATEGORIA_TECNOLOGIA else IVA_GENERAL
    return precio * tasa

def calcular_precio_final(producto: Producto) -> float:
    precio_con_iva = producto.precio + calcular_iva(producto.precio, producto.categoria)
    if producto.categoria == CATEGORIA_TECNOLOGIA:
        return precio_con_iva * (1 - DESCUENTO_TECNOLOGIA)
    return precio_con_iva

def registrar_producto(producto: Producto):
    if not validar_producto(producto):
        print(f"Error: Datos inválidos para el producto {producto.nombre}.")
        return
    producto.precio_final = calcular_precio_final(producto)
    lista = storage.leer_inventario()
    lista.append(asdict(producto))
    storage.guardar_inventario(lista)
    print(f"Producto '{producto.nombre}' registrado exitosamente.")