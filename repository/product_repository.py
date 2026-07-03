"""
Módulo de Repositorio

Abstrae el acceso a la capa de datos. Es el único lugar que sabe cómo
y dónde se guardan los datos de los productos.
"""
import os
import json
from typing import List
from domain.product import Producto


class ProductRepository:
    """
    Se encarga de la persistencia de los productos en un archivo JSON.
    Siempre trabaja con objetos `Producto`, no con diccionarios.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path

    def get_all(self) -> List[Producto]:
        if not os.path.exists(self._file_path):
            return []
        
        with open(self._file_path, "r") as archivo:
            try:
                data = json.load(archivo)
                # Convierte la lista de diccionarios a una lista de objetos Producto
                return [Producto(**p) for p in data]
            except (json.JSONDecodeError, TypeError):
                return []

    def save_all(self, productos: List[Producto]):
        # Convierte la lista de objetos Producto a una lista de diccionarios
        productos_dict = [p.__dict__ for p in productos]
        with open(self._file_path, "w") as archivo:
            json.dump(productos_dict, archivo, indent=4)

    def clear(self):
        if os.path.exists(self._file_path):
            os.remove(self._file_path)