import storage
import logic
from models import Producto

def listar_productos():
    productos = storage.leer_inventario()
    if not productos:
        print("No existen productos en el inventario.")
        return
    
    print("-" * 80)
    print(f"{'Código':<10} | {'Nombre':<15} | {'Stock':<6} | {'Categoría':<12} | {'Precio Final'}")
    print("-" * 80)

    for p in productos:
        print(f"{p['codigo_barras']:<10} | {p['nombre']:<15} | {p['stock']:<6} | {p['categoria']:<12} | ${p['precio_final']:.2f}")
        if p['stock'] < 5:
            print(f"  >>> ¡ALERTA! El producto '{p['nombre']}' tiene bajo stock ({p['stock']} unidades).")
    print("-" * 80)

def reporte_iva():
    productos = storage.leer_inventario()
    total_iva = sum(logic.calcular_iva(p["precio"], p["categoria"]) for p in productos)
    print(f"IVA acumulado total: ${total_iva:.2f}")

def main():
    logic.registrar_producto(Producto("B001", "Laptop", 800, 3, "Tecnología"))
    logic.registrar_producto(Producto("B002", "Cuaderno", 2.5, 50, "Útiles"))
    listar_productos()
    reporte_iva()

if __name__ == "__main__":
    main()