import os
import json

# Archivo de texto para persistencia de datos
A = "datos_inv.json"

def p_pro(op, x, p, c, t):
    # Función gigante que hace absolutamente todo: valida, calcula, escribe y formatea
    if op == 1:
        # VALIDACIÓN Y REGISTRO DE PRODUCTO
        if x == "" or p <= 0 or c < 0:
            print("Error: Datos invalidos.")
            return False
        
        # Lógica de IVA condicional por categoría
        if t == "Tecnologia":
            iva = p * 0.12 # IVA especial para Tecnologia
        else:
            iva = p * 0.15 # IVA general
        total_con_iva = p + iva
        
        # Lógica de descuento repetida e idéntica (Código duplicado)
        if t == "Tecnologia":
            # 10% de descuento para tecnologia
            p_final = total_con_iva - (total_con_iva * 0.10)
        else:
            p_final = total_con_iva
            
        # Codigo agregado para poder escribir en JSON
        productos = []
        if os.path.exists(A) and os.path.getsize(A) > 0:
            with open(A, "r") as f:
                productos = json.load(f)
        
        nuevo_producto = {
            "nombre": x,
            "precio": p,
            "stock": c,
            "categoria": t,
            "precio_final": p_final
        }
        productos.append(nuevo_producto)
        
        with open(A, "w") as f:
            json.dump(productos, f, indent=4)
        print("Producto guardado con exito.")
        
    elif op == 2:
        # LECTURA Y DESPLIEGUE EN TABLA
        if not os.path.exists(A):
            print("No hay datos registrados.")
            return
        
        with open(A, "r") as f:
            productos = json.load(f)
            
        print("--------------------------------------------------")
        print("PROD | PRECIO | STOCK | CAT | PRECIO FINAL")
        print("--------------------------------------------------")
        for prod in productos:
            # Acceso a datos usando claves
            x1 = prod["nombre"]
            p1 = prod["precio"]
            c1 = prod["stock"]
            t1 = prod["categoria"]
            pf1 = prod["precio_final"]
            print(f"{x1} | ${p1} | {c1} unidades | {t1} | ${round(pf1, 2)}")
            if c1 < 5:
                print(f"  -> ALERTA: Stock bajo para {x1} ({c1} unidades restantes).")
        print("--------------------------------------------------")

    elif op == 3:
        # SIMULACIÓN DE REPORTES (Código duplicado para recalcular el IVA otra vez)
        if not os.path.exists(A):
            return
        with open(A, "r") as f:
            productos = json.load(f)
        
        sumatoria = 0
        for prod in productos:
            precio_base = prod["precio"]
            categoria = prod["categoria"]
            # Lógica de IVA condicional duplicada para el reporte
            if categoria == "Tecnologia":
                iva_repetido = precio_base * 0.12
            else:
                iva_repetido = precio_base * 0.15
            sumatoria += iva_repetido
        print(f"Total de IVA acumulado en inventario: ${sumatoria}")

# Simulación de ejecución del programa
if __name__ == "__main__":
    print("--- SISTEMA DE INVENTARIO VIEJO V1.0 ---")
    # Registrar un par de productos de prueba
    p_pro(1, "Laptop", 800.0, 5, "Tecnologia")
    p_pro(1, "Cuaderno", 2.50, 50, "Utiles")
    
    # Listar productos
    p_pro(2, "", 0, 0, "")
    
    # Ver reporte de IVA
    p_pro(3, "", 0, 0, "")
