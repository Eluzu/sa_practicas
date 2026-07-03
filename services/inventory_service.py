"""
Módulo de Servicios

Contiene la lógica de negocio principal de la aplicación. Orquesta las
operaciones, valida datos y realiza cálculos.
"""
from typing import List
from domain.product import Producto
from repository.product_repository import ProductRepository
from config import IVA_RATES, DISCOUNT_RULES


class InventoryService:
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def register_product(self, producto: Producto) -> bool:
        if not self._is_valid(producto):
            return False
        
        productos = self._repository.get_all()
        productos.append(producto)
        self._repository.save_all(productos)
        return True

    def get_all_products(self) -> List[Producto]:
        return self._repository.get_all()

    def calculate_final_price(self, producto: Producto) -> float:
        iva_rate = IVA_RATES.get(producto.categoria, IVA_RATES["default"])
        precio_con_iva = producto.precio * (1 + iva_rate)

        if producto.categoria in DISCOUNT_RULES:
            discount = DISCOUNT_RULES[producto.categoria]
            return precio_con_iva * (1 - discount)
        
        return precio_con_iva

    def calculate_total_iva(self) -> float:
        productos = self.get_all_products()
        total_iva = 0.0
        for p in productos:
            iva_rate = IVA_RATES.get(p.categoria, IVA_RATES["default"])
            total_iva += p.precio * iva_rate
        return total_iva

    def _is_valid(self, producto: Producto) -> bool:
        return (producto.codigo_barras != "" and producto.nombre != "" and
                producto.precio > 0 and producto.stock >= 0)