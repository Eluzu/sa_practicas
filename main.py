import os
import json

# Cambiamos el archivo de persistencia a formato JSON
ARCHIVO_DATOS = "datos_inv.json"

def calcular_iva(precio, categoria):
    """Centraliza la regla de negocio del IVA según la categoría."""
    if categoria == "Tecnología":
        return precio * 0.12  # 12% para Tecnología
    return precio * 0.15      # 15% general para el resto


def leer_datos_json():
    """Función utilitaria para leer de forma segura el archivo JSON."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []  # Si no existe, retornamos una lista vacía
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # Si el archivo está corrupto o vacío, retornamos lista vacía


def guardar_datos_json(datos):
    """Función utilitaria para escribir la estructura completa en el JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def p_pro(op, x, p, c, t):
    # Función que maneja las operaciones del inventario
    if op == 1:
        # VALIDACIÓN Y REGISTRO DE PRODUCTO
        if x == "" or p <= 0 or c < 0:
            print("Error: Datos inválidos.")
            return False
        
        # Aplicamos la regla de IVA
        iva = calcular_iva(p, t)
        total_con_iva = p + iva
        
        # Lógica de descuento
        if t == "Tecnología":
            p_final = total_con_iva - (total_con_iva * 0.10)
        else:
            p_final = total_con_iva
            
        # Creamos una estructura de diccionario limpia para el JSON
        nuevo_producto = {
            "producto": x,
            "precio_base": p,
            "stock": c,
            "categoria": t,
            "precio_final": round(p_final, 2)
        }
        
        # Leemos el estado actual, añadimos el nuevo item y guardamos
        inventario = leer_datos_json()
        inventario.append(nuevo_producto)
        guardar_datos_json(inventario)
        
        print("Producto guardado con éxito en formato JSON.")
        
    elif op == 2:
        # LECTURA Y DESPLIEGUE EN TABLA
        inventario = leer_datos_json()
        if not inventario:
            print("No hay datos registrados.")
            return
        
        print("--------------------------------------------------")
        print("PROD | PRECIO | STOCK | CAT | PRECIO FINAL")
        print("--------------------------------------------------")
        for item in inventario:
            # Ahora accedemos por llaves legibles en lugar de índices numéricos (datos[0])
            if item["stock"] < 5:
                print(f"⚠️ Alerta: Stock de '{item['producto']}' menor a 5 unidades")
                
            print(f"{item['producto']} | ${item['precio_base']} | {item['stock']} unidades | {item['categoria']} | ${item['precio_final']}")
        print("--------------------------------------------------")

    elif op == 3:
        # REPORTES
        inventario = leer_datos_json()
        if not inventario:
            print("No hay datos en el inventario para generar reportes.")
            return
        
        sumatoria = 0
        for item in inventario:
            # Usamos la función de IVA mapeando los datos del JSON
            iva_correcto = calcular_iva(item["precio_base"], item["categoria"])
            sumatoria += iva_correcto
            
        print(f"Total de IVA acumulado en inventario: ${sumatoria:.2f}")

# Simulación de ejecución del programa
if __name__ == "__main__":
    print("--- SISTEMA DE INVENTARIO JSON V1.2 ---")
    
    # Limpieza inicial para propósitos de prueba
    if os.path.exists(ARCHIVO_DATOS):
        os.remove(ARCHIVO_DATOS)

    # Registrar productos de prueba
    p_pro(1, "Laptop", 800.0, 3, "Tecnología")
    p_pro(1, "Cuaderno", 2.50, 50, "Útiles")
    
    # Listar productos
    p_pro(2, "", 0, 0, "")
    
    # Ver reporte de IVA
    p_pro(3, "", 0, 0, "")