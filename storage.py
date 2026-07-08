import json
import os

ARCHIVO_INVENTARIO = "datos_inv.json"

def leer_inventario() -> list:
    if not os.path.exists(ARCHIVO_INVENTARIO):
        return []
    with open(ARCHIVO_INVENTARIO, "r") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []

def guardar_inventario(productos: list):
    with open(ARCHIVO_INVENTARIO, "w") as archivo:
        json.dump(productos, archivo, indent=4)