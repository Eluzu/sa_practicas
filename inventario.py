from persistencia import guardar_producto, leer_productos
from impuestos import IVA, IVA_TECNOLOGIA


def validar_producto(producto) -> bool:
    return (
        producto.codigo_barras != ""
        and producto.nombre != ""
        and producto.precio > 0
        and producto.stock >= 0
    )


def registrar_producto(producto):

    if not validar_producto(producto):
        print("Datos inválidos.")
        return

    guardar_producto(producto)
    print("Producto registrado.")


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