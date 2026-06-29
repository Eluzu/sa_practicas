import os

# Archivo de texto para persistencia de datos
ARCHIVO_DATOS = "datos_inv.txt"

def calcular_iva(precio, categoria):
    """Centraliza la regla de negocio del IVA según la categoría."""
    if categoria == "Tecnología":
        return precio * 0.12  # 12% para Tecnología
    return precio * 0.15      # 15% general para el resto


def p_pro(op, x, p, c, t):
    # Función que maneja las operaciones del inventario
    if op == 1:
        # VALIDACIÓN Y REGISTRO DE PRODUCTO
        if x == "" or p <= 0 or c < 0:
            print("Error: Datos inválidos.")
            return False
        
        # Aplicamos la nueva regla de IVA centralizada
        iva = calcular_iva(p, t)
        total_con_iva = p + iva
        
        # Lógica de descuento
        if t == "Tecnología":
            # 10% de descuento para tecnología
            p_final = total_con_iva - (total_con_iva * 0.10)
        else:
            p_final = total_con_iva
            
        linea = f"{x},{p},{c},{t},{p_final}\n"
        
        # Escritura directa en archivo plano
        with open(ARCHIVO_DATOS, "a") as f:
            f.write(linea)
        print("Producto guardado con éxito.")
        
    elif op == 2:
        # LECTURA Y DESPLIEGUE EN TABLA
        if not os.path.exists(ARCHIVO_DATOS):
            print("No hay datos registrados.")
            return
        
        with open(ARCHIVO_DATOS, "r") as f:
            lineas = f.readlines()
            
        print("--------------------------------------------------")
        print("PROD | PRECIO | STOCK | CAT | PRECIO FINAL")
        print("--------------------------------------------------")
        for l in lineas:
            datos1 = l.strip().split(",")
            x1 = datos1[0]
            p1 = float(datos1[1])
            c1 = int(datos1[2])

            if c1 < 5:
                print("Stock menor a 5")
            t1 = datos1[3]
            pf1 = float(datos1[4])
            print(f"{x1} | ${p1} | {c1} unidades | {t1} | ${pf1}")
        print("--------------------------------------------------")

    elif op == 3:
        # REPORTES (Usa la misma función centralizada de IVA)
        if not os.path.exists(ARCHIVO_DATOS):
            return
        with open(ARCHIVO_DATOS, "r") as f:
            lineas = f.readlines()
        
        sumatoria = 0
        for l in lineas:
            datos2 = l.strip().split(",")
            precio_base = float(datos2[1])
            categoria = datos2[3]
            
            # Llamamos a la función centralizada para evitar discrepancias
            iva_correcto = calcular_iva(precio_base, categoria)
            sumatoria += iva_correcto
            
        print(f"Total de IVA acumulado en inventario: ${sumatoria:.2f}")

# Simulación de ejecución del programa
if __name__ == "__main__":
    print("--- SISTEMA DE INVENTARIO ACTUALIZADO V1.1 ---")
    
    # IMPORTANTE: Si ya tenías un archivo 'datos_inv.txt' viejo, 
    # es recomendable borrarlo para que las pruebas no mezclen cálculos viejos con nuevos.
    if os.path.exists(ARCHIVO_DATOS):
        os.remove(ARCHIVO_DATOS)

    # Registrar productos de prueba
    p_pro(1, "Laptop", 800.0, 3, "Tecnología") # Debería calcular 12% de IVA ($96)
    p_pro(1, "Cuaderno", 2.50, 50, "Útiles")     # Debería calcular 15% de IVA ($0.375)
    
    # Listar productos
    p_pro(2, "", 0, 0, "")
    
    # Ver reporte de IVA
    p_pro(3, "", 0, 0, "")