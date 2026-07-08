from dataclasses import dataclass

@dataclass
class Producto:
    codigo_barras: str
    nombre: str
    precio: float
    stock: int
    categoria: str
    precio_final: float = 0