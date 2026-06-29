import os

# Archivo de texto para persistencia de datos
A = "datos_inv.txt"

def p_pro(op, x, p, c, t):
    # Función gigante que hace absolutamente todo: valida, calcula, escribe y formatea
    if op == 1:
        # VALIDACIÓN Y REGISTRO DE PRODUCTO
        if x == "" or p <= 0 or c < 0:
            print("Error: Datos inválidos.")
            return False
        
        # Hardcoding: IVA del 15% quemado directamente en el bucle/lógica
        iva = p * 0.15
        total_con_iva = p + iva
        
        # Lógica de descuento repetida e idéntica (Código duplicado)
        if t == "Tecnología":
            # 10% de descuento para tecnología
            p_final = total_con_iva - (total_con_iva * 0.10)
        else:
            p_final = total_con_iva
            
        linea = f"{x},{p},{c},{t},{p_final}\n"
        
        # Escritura directa en archivo plano
        with open(A, "a") as f:
            f.write(linea)
        print("Producto guardado con éxito.")
        
    elif op == 2:
        # LECTURA Y DESPLIEGUE EN TABLA
        if not os.path.exists(A):
            print("No hay datos registrados.")
            return
        
        with open(A, "r") as f:
            lineas = f.readlines()
            
        print("--------------------------------------------------")
        print("PROD | PRECIO | STOCK | CAT | PRECIO FINAL")
        print("--------------------------------------------------")
        for l in lineas:
            datos1 = l.strip().split(",")
            # Nombres crípticos de variables (datos1, x1, etc.)
            x1 = datos1[0]
            p1 = float(datos1[1])
            c1 = int(datos1[2])

            if c1 < 5:
               print("Stock menos de 5")

            t1 = datos1[3]
            pf1 = float(datos1[4])
            print(f"{x1} | ${p1} | {c1} unidades | {t1} | ${pf1}")
        print("--------------------------------------------------")

    elif op == 3:
        # SIMULACIÓN DE REPORTES (Código duplicado para recalcular el IVA otra vez)
        if not os.path.exists(A):
            return
        with open(A, "r") as f:
            lineas = f.readlines()
        
        sumatoria = 0
        for l in lineas:
            datos2 = l.strip().split(",")
            precio_base = float(datos2[1])
            # Repetición del cálculo del IVA del 15% (Hardcoded)
            iva_repetido = precio_base * 0.15
            sumatoria += iva_repetido
        print(f"Total de IVA acumulado en inventario: ${sumatoria}")

# Simulación de ejecución del programa
if __name__ == "__main__":
    print("--- SISTEMA DE INVENTARIO VIEJO V1.0 ---")
    # Registrar un par de productos de prueba
    p_pro(1, "Laptop", 800.0, 2, "Tecnología")
    p_pro(1, "Cuaderno", 2.50, 50, "Útiles")
    
    # Listar productos
    p_pro(2, "", 0, 0, "")
    
    # Ver reporte de IVA
    p_pro(3, "", 0, 0, "")
