import os
from models import Producto
from repository import registrar_producto
import ui
import config

def main():
    # Limpiamos el archivo de inventario para una ejecución limpia
    if os.path.exists(config.ARCHIVO_INVENTARIO):
        os.remove(config.ARCHIVO_INVENTARIO)
        
    registrar_producto(
        Producto("7501055311490", "Laptop", 800, 4, "Tecnología")
    )
    registrar_producto(
        Producto("7502234567890", "Cuaderno", 2.5, 50, "Útiles")
    )

    ui.listar_productos()

    ui.reporte_iva()

if __name__ == "__main__":
    main()