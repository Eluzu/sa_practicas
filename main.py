import os
import json

# Archivo de persistencia JSON
ARCHIVO_DATOS = "datos_inv.json"

def calcular_iva(precio, categoria):
    """Centraliza la regla de negocio del IVA según la categoría."""
    if categoria == "Tecnología":
        return precio * 0.12  # 12% para Tecnología
    return precio * 0.15      # 15% general para el resto


def leer_datos_json():
    """Función utilitaria para leer de forma segura el archivo JSON."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def guardar_datos_json(datos):
    """Función utilitaria para escribir la estructura completa en el JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def p_pro(op, cod, x, p, c, t):
    # Agregamos 'cod' como segundo parámetro para el código de barras
    if op == 1:
        # VALIDACIÓN Y REGISTRO DE PRODUCTO
        # Añadimos la validación obligatoria de 'cod'
        if cod == "" or x == "" or p <= 0 or c < 0:
            print("Error: Datos inválidos. El código de barras y el nombre son obligatorios.")
            return False
        
        # Aplicamos la regla de IVA
        iva = calcular_iva(p, t)
        total_con_iva = p + iva
        
        # Lógica de descuento
        if t == "Tecnología":
            p_final = total_con_iva - (total_con_iva * 0.10)
        else:
            p_final = total_con_iva
            
        # Agregamos "codigo_barras" al inicio de nuestro diccionario estructurado
        nuevo_producto = {
            "codigo_barras": cod,
            "producto": x,
            "precio_base": p,
            "stock": c,
            "categoria": t,
            "precio_final": round(p_final, 2)
        }
        
        inventario = leer_datos_json()
        inventario.append(nuevo_producto)
        guardar_datos_json(inventario)
        
        print(f"Producto '{x}' [Cod: {cod}] guardado con éxito.")
        
    elif op == 2:
        # LECTURA Y DESPLIEGUE EN TABLA
        inventario = leer_datos_json()
        if not inventario:
            print("No hay datos registrados.")
            return
        
        print("----------------------------------------------------------------------")
        print("COD   | PROD | PRECIO | STOCK | CAT | PRECIO FINAL")
        print("----------------------------------------------------------------------")
        for item in inventario:
            if item["stock"] < 5:
                print(f"⚠️ Alerta: Stock de '{item['producto']}' menor a 5 unidades")
                
            # Desplegamos el nuevo campo en la tabla visual
            print(f"{item['codigo_barras']} | {item['producto']} | ${item['precio_base']} | {item['stock']} unidades | {item['categoria']} | ${item['precio_final']}")
        print("----------------------------------------------------------------------")

    elif op == 3:
        # REPORTES
        inventario = leer_datos_json()
        if not inventario:
            print("No hay datos en el inventario para generar reportes.")
            return
        
        sumatoria = 0
        for item in inventario:
            iva_correcto = calcular_iva(item["precio_base"], item["categoria"])
            sumatoria += iva_correcto
            
        print(f"Total de IVA acumulado en inventario: ${sumatoria:.2f}")

# Simulación de ejecución del programa
if __name__ == "__main__":
    print("--- SISTEMA DE INVENTARIO CON CÓDIGO DE BARRAS V1.3 ---")
    
    if os.path.exists(ARCHIVO_DATOS):
        os.remove(ARCHIVO_DATOS)

    # Registrar productos incluyendo el nuevo parámetro 'cod' al inicio de los datos
    p_pro(1, "789101", "Laptop", 800.0, 3, "Tecnología")
    p_pro(1, "789102", "Cuaderno", 2.50, 50, "Útiles")
    
    # Intento de registrar un producto inválido (sin código de barras) -> Debería fallar
    p_pro(1, "", "Producto Fallido", 10.0, 5, "Varios")
    
    # Listar productos (pasamos "" en el campo de código ya que la op 2 no lo usa para registrar)
    p_pro(2, "", "", 0, 0, "")
    
    # Ver reporte de IVA
    p_pro(3, "", "", 0, 0, "")