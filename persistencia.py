import json
import os
from impuestos import calcular_precio_final

ARCHIVO_INVENTARIO = "datos_inv.json"


def guardar_producto(producto):

    precio_final = calcular_precio_final(producto)

    nuevo_producto = {
        "codigo_barras": producto.codigo_barras,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock,
        "categoria": producto.categoria,
        "precio_final": precio_final
    }

    productos = []

    if os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
            try:
                productos = json.load(archivo)
            except json.JSONDecodeError:
                productos = []

    productos.append(nuevo_producto)

    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4, ensure_ascii=False)


def leer_productos():

    if not os.path.exists(ARCHIVO_INVENTARIO):
        return []

    with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []