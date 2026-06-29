import os
import json

ARCHIVO = "datos_inv.json"
IVA_GENERAL = 0.15
IVA_TECNOLOGIA = 0.12

def cargar_datos():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_datos(datos):
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

def calcular_impuesto(precio, categoria):
    return precio * (IVA_TECNOLOGIA if categoria == "Tecnología" else IVA_GENERAL)

# Hemos añadido el parámetro 'codigo_barras' a la función
def p_pro(op, codigo_barras="", x="", p=0.0, c=0, t=""):
    datos = cargar_datos()

    if op == 1:
        # Validación: codigo_barras es ahora un campo obligatorio
        if not codigo_barras or x == "" or p <= 0 or c < 0:
            print("Error: Todos los datos son obligatorios y válidos.")
            return

        iva = calcular_impuesto(p, t)
        p_final = (p + iva) * (0.9 if t == "Tecnología" else 1.0)
        
        nuevo_producto = {
            "codigo_barras": codigo_barras, # Nuevo campo
            "nombre": x,
            "precio": p,
            "stock": c,
            "categoria": t,
            "precio_final": round(p_final, 2)
        }
        
        datos.append(nuevo_producto)
        guardar_datos(datos)
        print(f"Producto '{x}' (Cod: {codigo_barras}) guardado correctamente.")

    elif op == 2:
        print(f"{'CÓDIGO':<12} | {'PROD':<12} | {'PRECIO':<8} | {'STOCK':<6} | {'CAT':<12} | {'P. FINAL'}")
        for prod in datos:
            # Usamos .get() para evitar el error si falta la clave
            codigo = prod.get('codigo_barras', 'N/A') 
            print(f"{codigo:<12} | {prod['nombre']:<12} | ${prod['precio']:<7} | {prod['stock']:<6} | {prod['categoria']:<12} | ${prod['precio_final']}")
            
    elif op == 3:
        total_iva = sum(calcular_impuesto(p['precio'], p['categoria']) for p in datos)
        print(f"Total de IVA acumulado: ${total_iva:.2f}")

# Simulación
if __name__ == "__main__":
    # Ahora enviamos el código de barras como primer argumento
    p_pro(1, "770123", "Laptop", 800.0, 2, "Tecnología")
    p_pro(1, "770456", "Cuaderno", 2.50, 50, "Útiles")
    
    print("\n--- Listado de Inventario con Código de Barras ---")
    p_pro(2)