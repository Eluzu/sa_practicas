import os
from dataclasses import dataclass

ARCHIVO_INVENTARIO = "datos_inv.txt"
IVA = 0.15
CATEGORIA_DESCUENTO = "Tecnología"
DESCUENTO_TECNOLOGIA = 0.10

@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int
    categoria: str

def validar_producto(producto: Producto) -> bool:
    return (
        producto.nombre != ""
        and producto.precio > 0
        and producto.stock >= 0
    )

def calcular_iva(precio: float) -> float:
    return precio * IVA

def calcular_precio_final(producto: Producto) -> float:

    precio_con_iva = producto.precio + calcular_iva(producto.precio)

    if producto.categoria == CATEGORIA_DESCUENTO:
        return precio_con_iva * (1 - DESCUENTO_TECNOLOGIA)

    return precio_con_iva

def guardar_producto(producto: Producto):

    precio_final = calcular_precio_final(producto)

    with open(ARCHIVO_INVENTARIO, "a") as archivo:
        archivo.write(
            f"{producto.nombre},"
            f"{producto.precio},"
            f"{producto.stock},"
            f"{producto.categoria},"
            f"{precio_final}\n"
        )

def registrar_producto(producto: Producto):

    if not validar_producto(producto):
        print("Datos inválidos.")
        return

    guardar_producto(producto)
    print("Producto registrado.")

def leer_productos():

    if not os.path.exists(ARCHIVO_INVENTARIO):
        return []

    productos = []

    with open(ARCHIVO_INVENTARIO) as archivo:

        for linea in archivo:

            nombre, precio, stock, categoria, precio_final = linea.strip().split(",")

            productos.append({
                "nombre": nombre,
                "precio": float(precio),
                "stock": int(stock),
                "categoria": categoria,
                "precio_final": float(precio_final)
            })

    return productos

def listar_productos():

    productos = leer_productos()

    if not productos:
        print("No existen productos.")
        return

    print("-" * 60)

    for producto in productos:
        print(
            f"{producto['nombre']} | "
            f"${producto['precio']} | "
            f"{producto['stock']} | "
            f"{producto['categoria']} | "
            f"${producto['precio_final']:.2f}"
        )

def reporte_iva():

    productos = leer_productos()

    total_iva = sum(
        calcular_iva(producto["precio"])
        for producto in productos
    )

    print(f"IVA acumulado: ${total_iva:.2f}")

def main():

    registrar_producto(
        Producto("Laptop",800, 5, "Tecnología")
    )

    registrar_producto(
        Producto("Cuaderno", 2.5, 50, "Útiles")
    )

    listar_productos()

    reporte_iva()

if __name__ == "__main__":
    main()