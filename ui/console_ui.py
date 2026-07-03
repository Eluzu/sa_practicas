"""
Módulo de Interfaz de Usuario (UI)

Gestiona toda la interacción con el usuario a través de la consola.
"""
from services.inventory_service import InventoryService
from domain.product import Producto
from config import STOCK_MINIMO_ALERTA


class ConsoleUI:
    def __init__(self, service: InventoryService):
        self._service = service

    def register_product(self, producto: Producto):
        if self._service.register_product(producto):
            print(f"Producto '{producto.nombre}' registrado.")
        else:
            print("Datos inválidos.")

    def list_products(self):
        productos = self._service.get_all_products()
        if not productos:
            print("No existen productos.")
            return

        print("-" * 80)
        print(f"{'Código':<15} | {'Nombre':<15} | {'Precio':<10} | {'Stock':<5} | {'Categoría':<12} | {'Precio Final':<12}")
        print("-" * 80)

        for producto in productos:
            precio_final = self._service.calculate_final_price(producto)
            print(f"{producto.codigo_barras:<15} | {producto.nombre:<15} | "
                  f"${producto.precio:<9.2f} | {producto.stock:<5} | "
                  f"{producto.categoria:<12} | ${precio_final:<11.2f}")
            if producto.stock < STOCK_MINIMO_ALERTA:
                print(f"  -> ALERTA: ¡Stock bajo! ({producto.stock} unidades restantes)")

    def show_iva_report(self):
        total_iva = self._service.calculate_total_iva()
        print(f"IVA acumulado: ${total_iva:.2f}")