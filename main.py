"""
Punto de entrada principal de la aplicación de inventario.

Este script se encarga de:
1. Configurar e instanciar los componentes de la aplicación (repositorio, servicio, UI).
2. Orquestar el flujo principal de ejecución.
"""
from config import ARCHIVO_INVENTARIO
from domain.product import Producto
from repository.product_repository import ProductRepository
from services.inventory_service import InventoryService
from ui.console_ui import ConsoleUI

def main():
    # 1. Composición de la aplicación (Inyección de Dependencias)
    repository = ProductRepository(ARCHIVO_INVENTARIO)
    service = InventoryService(repository)
    ui = ConsoleUI(service)
    
    # 2. Flujo de ejecución
    repository.clear() # Limpiamos el inventario para una ejecución limpia
    
    ui.register_product(Producto("7501055311490", "Laptop", 800, 4, "Tecnología"))
    ui.register_product(Producto("7502234567890", "Cuaderno", 2.5, 50, "Útiles"))
    
    ui.list_products()
    ui.show_iva_report()

# Ejecutamos el programa
if __name__ == "__main__":
    main()