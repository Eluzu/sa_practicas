"""
Módulo de Dominio

Define las estructuras de datos centrales (modelos) de la aplicación.
"""
from dataclasses import dataclass

@dataclass
class Producto:
    codigo_barras: str
    nombre: str
    precio: float
    stock: int
    categoria: str