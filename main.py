import os
import json
from dataclasses import dataclass

# Definimos las variables globales
ARCHIVO_INVENTARIO = "inventario.json"
IVA_GENERAL = 0.15
IVA_TECNOLOGIA = 0.12
CATEGORIA_DESCUENTO = "Tecnología"
DESCUENTO_TECNOLOGIA = 0.10
STOCK_MINIMO_ALERTA = 5

# Definimos la clase Producto
@dataclass
class Producto:
    codigo_barras: str
    nombre: str
    precio: float
    stock: int
    categoria: str

# Definimos la funcion para validar el producto
def validar_producto(producto: Producto) -> bool:
    return (
        producto.codigo_barras != ""
        and producto.nombre != ""
        and producto.precio > 0
        and producto.stock >= 0
    )

# Definimos la funcion para calcular el IVA
def calcular_iva(precio: float, categoria: str) -> float:
    if categoria == "Tecnología":
        return precio * IVA_TECNOLOGIA
    return precio * IVA_GENERAL

# Definimos la funcion para calcular el precio final
def calcular_precio_final(producto: Producto) -> float:
    precio_con_iva = producto.precio + calcular_iva(producto.precio, producto.categoria)

    if producto.categoria == CATEGORIA_DESCUENTO:
        return precio_con_iva * (1 - DESCUENTO_TECNOLOGIA)

    return precio_con_iva

# Definimos la funcion para guardar el producto
def guardar_producto(producto: Producto):
    productos = leer_productos()
    
    producto_dict = {
        "codigo_barras": producto.codigo_barras,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock,
        "categoria": producto.categoria,
    }
    productos.append(producto_dict)
    
    with open(ARCHIVO_INVENTARIO, "w") as archivo:
        json.dump(productos, archivo, indent=4)

# Definimos la funcion para registrar el producto
def registrar_producto(producto: Producto):
    if not validar_producto(producto):
        print("Datos inválidos.")
        return

    guardar_producto(producto)
    print(f"Producto '{producto.nombre}' registrado.")

# Definimos la funcion para leer los productos
def leer_productos():
    if not os.path.exists(ARCHIVO_INVENTARIO):
        return []
    
    with open(ARCHIVO_INVENTARIO) as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return []

# Definimos la funcion para listar los productos
def listar_productos():
    productos = leer_productos()

    if not productos:
        print("No existen productos.")
        return

    print("-" * 80)
    print(f"{'Código':<15} | {'Nombre':<15} | {'Precio':<10} | {'Stock':<5} | {'Categoría':<12} | {'Precio Final':<12}")
    print("-" * 80)

    for producto in productos:
        # Recreamos una instancia de Producto para usar los métodos de cálculo
        prod_obj = Producto(**producto)
        precio_final = calcular_precio_final(prod_obj)
        
        print(
            f"{producto['codigo_barras']:<15} | "
            f"{producto['nombre']:<15} | "
            f"${producto['precio']:<9.2f} | "
            f"{producto['stock']:<5} | "
            f"{producto['categoria']:<12} | "
            f"${precio_final:<11.2f}"
        )
        if producto['stock'] < STOCK_MINIMO_ALERTA:
            print(f"  -> ALERTA: ¡Stock bajo! ({producto['stock']} unidades restantes)")

# Definimos la funcion que sirve para calcular el IVA
# La diferencia con la anterior es que ahora usamos la instancia de Producto
def reporte_iva():

    productos = leer_productos()

    total_iva = sum(
        calcular_iva(producto["precio"], producto["categoria"])
        for producto in productos
    )

    print(f"IVA acumulado: ${total_iva:.2f}")

# Definimos la funcion principal
def main():
    # Limpiamos el archivo de inventario para una ejecución limpia
    if os.path.exists(ARCHIVO_INVENTARIO):
        os.remove(ARCHIVO_INVENTARIO)
        
    registrar_producto(
        Producto("7501055311490", "Laptop", 800, 4, "Tecnología")
    )
    registrar_producto(
        Producto("7502234567890", "Cuaderno", 2.5, 50, "Útiles")
    )

    listar_productos()

    reporte_iva()

# Ejecutamos el programa
if __name__ == "__main__":
    main()