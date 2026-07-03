import os
import json
from typing import List
from models import Producto
import config
import services

def leer_productos() -> List[Producto]:
    if not os.path.exists(config.ARCHIVO_INVENTARIO):
        return []
    
    with open(config.ARCHIVO_INVENTARIO, 'r') as archivo:
        try:
            datos = json.load(archivo)
            # Convertir lista de diccionarios a lista de objetos Producto
            return [Producto(**dato) for dato in datos]
        except json.JSONDecodeError:
            return []

def guardar_productos(productos: List[Producto]):
    # Convertir lista de objetos Producto a lista de diccionarios
    datos = [prod.__dict__ for prod in productos]
    with open(config.ARCHIVO_INVENTARIO, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

def registrar_producto(producto: Producto):
    """
    Añade un nuevo producto al repositorio.
    """
    if not services.validar_producto(producto):
        print(f"Error: Datos inválidos para el producto '{producto.nombre}'.")
        return

    productos = leer_productos()
    productos.append(producto)
    guardar_productos(productos)
    print(f"Producto '{producto.nombre}' registrado.")