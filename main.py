import os
import json 
from dataclasses import dataclass

ARCHIVO_INVENTARIO = "datos_inv.json"
IVA = 0.15
IVA_TECNOLOGIA = 0.12
CATEGORIA_DESCUENTO = "Tecnología"
DESCUENTO_TECNOLOGIA = 0.10

@dataclass
class Producto:
    codigo_barras: str
    nombre: str
    precio: float
    stock: int
    categoria: str

def validar_producto(producto: Producto) -> bool:
    return (
        producto.codigo_barras != ""
        and producto.nombre != ""
        and producto.precio > 0
        and producto.stock >= 0
    )

def calcular_iva(producto: Producto) -> float:
    if producto.categoria == "Tecnología":
        return producto.precio * IVA_TECNOLOGIA
    return producto.precio * IVA


def calcular_precio_final(producto: Producto) -> float:

    precio_con_iva = producto.precio + calcular_iva(producto)

    if producto.categoria == CATEGORIA_DESCUENTO:
        return precio_con_iva * (1 - DESCUENTO_TECNOLOGIA)

    return precio_con_iva

def guardar_producto(producto: Producto):

    precio_final = calcular_precio_final(producto)
    
    nuevo_producto = {
        "codigo_barras": producto.codigo_barras,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock,
        "categoria": producto.categoria,
        "precio_final": precio_final
    }

    productos = []

    if os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
            try:
                productos = json.load(archivo)
            except json.JSONDecodeError:
                productos = []

    productos.append(nuevo_producto)

    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, indent=4, ensure_ascii=False)


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
    with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []

def listar_productos():

    productos = leer_productos()

    if not productos:
        print("No existen productos.")
        return

    print("-" * 60)

    for producto in productos:
        print(
            f"{producto['codigo_barras']} | "
            f"{producto['nombre']} | "
            f"${producto['precio']} | "
            f"{producto['stock']} | "
            f"{producto['categoria']} | "
            f"${producto['precio_final']:.2f}"
        )
            
        if producto["stock"] < 5:
            print("⚠️ ALERTA: Stock menor a 5 unidades")


def reporte_iva():

    productos = leer_productos()

    total_iva = 0
    for producto in productos:
        if producto["categoria"] == "Tecnología":
            total_iva += producto["precio"] * IVA_TECNOLOGIA
        else:
            total_iva += producto["precio"] * IVA

    print(f"IVA acumulado: ${total_iva:.2f}")


def main():

    registrar_producto(
        Producto("7501234567890", "Laptop",800, 3, "Tecnología")
    )

    registrar_producto(
        Producto("7509876543210", "Cuaderno", 2.5, 50, "Útiles")
    )

    listar_productos()

    reporte_iva()


if __name__ == "__main__":
    main()