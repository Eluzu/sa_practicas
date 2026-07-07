from producto import Producto
from inventario import registrar_producto, listar_productos, reporte_iva


def main():

    registrar_producto(
        Producto(
            "7501234567890",
            "Laptop",
            800,
            3,
            "Tecnología"
        )
    )

    registrar_producto(
        Producto(
            "7509876543210",
            "Cuaderno",
            2.5,
            50,
            "Útiles"
        )
    )

    listar_productos()
    reporte_iva()


if __name__ == "__main__":
    main()