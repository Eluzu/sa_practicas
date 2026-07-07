import json
import os
from dataclasses import dataclass

ARCHIVO_INVENTARIO = "datos_inv.json"
IVA_GENERAL = 0.15
IVA_TECNOLOGIA = 0.12
CATEGORIA_TECNOLOGIA = "Tecnología"
DESCUENTO_TECNOLOGIA = 0.10

@dataclass
class Producto:
    codigo_barras: str  # Requerimiento: Campo obligatorio al inicio
    nombre: str
    precio: float
    stock: int
    categoria: str

def validar_producto(producto: Producto) -> bool:
    return (
        producto.codigo_barras != ""  # Validación del nuevo campo obligatorio
        and producto.nombre != ""
        and producto.precio > 0
        and producto.stock >= 0
    )

def obtener_tasa_iva(categoria: str) -> float:
    if categoria == CATEGORIA_TECNOLOGIA:
        return IVA_TECNOLOGIA
    return IVA_GENERAL

def calcular_iva(precio: float, categoria: str) -> float:
    tasa = obtener_tasa_iva(categoria)
    return precio * tasa

def calcular_precio_final(producto: Producto) -> float:
    iva_producto = calcular_iva(producto.precio, producto.categoria)
    precio_con_iva = producto.precio + iva_producto

    if producto.categoria == CATEGORIA_TECNOLOGIA:
        return precio_con_iva * (1 - DESCUENTO_TECNOLOGIA)

    return precio_con_iva

def leer_productos() -> list:
    if not os.path.exists(ARCHIVO_INVENTARIO):
        return []

    try:
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        return []

def guardar_producto(producto: Producto):
    precio_final = calcular_precio_final(producto)
    productos = leer_productos()

    # Estructuramos el diccionario poniendo el código de barras al inicio
    nuevo_producto = {
        "codigo_barras": producto.codigo_barras,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock,
        "categoria": producto.categoria,
        "precio_final": round(precio_final, 2)
    }

    productos.append(nuevo_producto)

    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4, ensure_ascii=False)

def registrar_producto(producto: Producto):
    if not validar_producto(producto):
        print(f"Error: Datos inválidos para el producto con código '{producto.codigo_barras}'.")
        return

    guardar_producto(producto)
    print(f"Producto [{producto.codigo_barras}] '{producto.nombre}' registrado con éxito.")

def listar_productos():
    productos = leer_productos()

    if not productos:
        print("No existen productos en el inventario.")
        return

    print("-" * 95)
    print(f"{'Código Barras':<15} | {'Nombre':<20} | {'Precio':<8} | {'Stock':<5} | {'Categoría':<12} | {'Precio Final':<12}")
    print("-" * 95)

    for prod in productos:
        alerta_stock = " -> [¡ALERTA! STOCK CRÍTICO]" if prod['stock'] < 5 else ""
        
        print(
            f"{prod['codigo_barras']:<15} | "
            f"{prod['nombre']:<20} | "
            f"${prod['precio']:<7.2f} | "
            f"{prod['stock']:<5} | "
            f"{prod['categoria']:<12} | "
            f"${prod['precio_final']:<11.2f}"
            f"{alerta_stock}"
        )
    print("-" * 95)

def reporte_iva():
    productos = leer_productos()

    total_iva = sum(
        calcular_iva(prod["precio"], prod["categoria"])
        for prod in productos
    )

    print(f"IVA acumulado total: ${total_iva:.2f}")


def main():
    # Limpieza del archivo JSON para pruebas limpias
    if os.path.exists(ARCHIVO_INVENTARIO):
        os.remove(ARCHIVO_INVENTARIO)

    # El código de barras ahora es el primer parámetro obligatorio
    registrar_producto(Producto("789101112", "Laptop Pro", 1200.0, 3, "Tecnología"))
    registrar_producto(Producto("978012345", "Enciclopedia", 45.0, 15, "Libros"))
    registrar_producto(Producto("789101115", "Mouse Óptico", 25.0, 10, "Tecnología"))

    print("\n--- INVENTARIO ACTUAL DESDE ARCHIVO JSON ---")
    listar_productos()

    print("--- INFORME FINANCIERO DE IMPUESTOS ---")
    reporte_iva()


if __name__ == "__main__":
    main()