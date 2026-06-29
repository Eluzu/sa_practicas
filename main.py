import os
import json

# Cambiamos la extensión a .json
ARCHIVO = "datos_inv.json"
IVA_GENERAL = 0.15
IVA_TECNOLOGIA = 0.12

def cargar_datos():
    """Carga los productos desde el archivo JSON."""
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_datos(datos):
    """Guarda la lista completa de productos en el archivo JSON."""
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

def calcular_impuesto(precio, categoria):
    return precio * (IVA_TECNOLOGIA if categoria == "Tecnología" else IVA_GENERAL)

def p_pro(op, x="", p=0.0, c=0, t=""):
    datos = cargar_datos()

    if op == 1:
        if x == "" or p <= 0 or c < 0:
            print("Error: Datos inválidos.")
            return

        # Creamos un diccionario estructurado en lugar de una línea de texto
        iva = calcular_impuesto(p, t)
        p_final = (p + iva) * (0.9 if t == "Tecnología" else 1.0)
        
        nuevo_producto = {
            "nombre": x,
            "precio": p,
            "stock": c,
            "categoria": t,
            "precio_final": round(p_final, 2)
        }
        
        datos.append(nuevo_producto)
        guardar_datos(datos)
        print(f"Producto '{x}' guardado en formato JSON.")

    elif op == 2:
        print(f"{'PROD':<12} | {'PRECIO':<8} | {'STOCK':<8} | {'CAT':<12} | {'P. FINAL'}")
        for prod in datos:
            print(f"{prod['nombre']:<12} | ${prod['precio']:<7} | {prod['stock']:<8} | {prod['categoria']:<12} | ${prod['precio_final']}")

    elif op == 3:
        total_iva = sum(calcular_impuesto(p['precio'], p['categoria']) for p in datos)
        print(f"Total de IVA acumulado: ${total_iva:.2f}")

# Simulación
if __name__ == "__main__":
    p_pro(1, "Laptop", 800.0, 2, "Tecnología")
    p_pro(1, "Cuaderno", 2.50, 50, "Útiles")
    
    print("\n--- Listado de Inventario ---")
    p_pro(2)
    
    print("\n--- Reporte Financiero ---")
    p_pro(3)