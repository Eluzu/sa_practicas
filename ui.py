import repository
import services
import config

def listar_productos():
    """
    Obtiene los productos del repositorio y los muestra en la consola.
    """
    productos = repository.leer_productos()

    if not productos:
        print("No existen productos.")
        return

    print("-" * 80)
    print(f"{'Código':<15} | {'Nombre':<15} | {'Precio':<10} | {'Stock':<5} | {'Categoría':<12} | {'Precio Final':<12}")
    print("-" * 80)

    for producto in productos:
        precio_final = services.calcular_precio_final(producto)
        
        print(
            f"{producto.codigo_barras:<15} | "
            f"{producto.nombre:<15} | "
            f"${producto.precio:<9.2f} | "
            f"{producto.stock:<5} | "
            f"{producto.categoria:<12} | "
            f"${precio_final:<11.2f}"
        )
        if producto.stock < config.STOCK_MINIMO_ALERTA:
            print(f"  -> ALERTA: ¡Stock bajo! ({producto.stock} unidades restantes)")

def reporte_iva():
    """
    Calcula y muestra el total de IVA acumulado de todos los productos.
    """
    productos = repository.leer_productos()
    total_iva = sum(services.calcular_iva(p.precio, p.categoria) for p in productos)
    print(f"\nIVA acumulado: ${total_iva:.2f}")