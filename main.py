import os
import json

# Archivo de texto para persistencia de datos
A = "datos_inv.json"

def p_pro(op, c_b, x, p, c, t):
    # Función gigante que hace absolutamente todo: valida, calcula, escribe y formatea
    if op == 1:
        # VALIDACIÓN Y REGISTRO DE PRODUCTO
        if c_b == "" or x == "" or p <= 0 or c < 0:
            print("Error: Datos inválidos.")
            return False
        
        # # Cálculo del IVA según la categoría del producto
        if t == "Tecnología":
            iva = p * 0.12
        else:
            iva = p * 0.15
        total_con_iva = p + iva
        
        # Lógica de descuento repetida e idéntica (Código duplicado)
        if t == "Tecnología":
            # 10% de descuento para tecnología
            p_final = total_con_iva - (total_con_iva * 0.10)
        else:
            p_final = total_con_iva
            
        producto = {
            "codigo_barras":c_b,
            "nombre": x, 
            "precio": p,
            "stock": c,
            "categoria": t,
            "precio_final": p_final
        }
        if os.path.exists(A):
            with open(A, "r") as f: 
                try:
                    datos = json.load(f)
                except json.JSONDecodeError:
                    datos = []
        else:
            datos = []
            
        datos.append(producto)
        with open(A, "w") as f:
            json.dump(datos, f, indent=4)
            
        print("Producto guardado con éxito.")
        
    elif op == 2:
        if not os.path.exists(A):
            print("No hay datos registrados.")
            return
            
        with open(A, "r", encoding="utf-8") as f:
            datos = json.load(f)
                
        print("--------------------------------------------------")
        print("COD | PROD | PRECIO | STOCK | CAT | PRECIO FINAL")
        print("--------------------------------------------------")
                
        for d in datos:
            print(f"{d['codigo_barras']} | {d['nombre']} | ${d['precio']} | {d['stock']} unidades | {d['categoria']} | ${d['precio_final']}")
                    
            if d['stock'] < 5:
                print("⚠ ALERTA: Stock bajo (menos de 5 unidades).")

    elif op == 3:
        if not os.path.exists(A):
            print("No hay datos registrados.")
            return

        with open(A, "r", encoding="utf-8") as f:
            datos = json.load(f)

        sumatoria = 0

        for d in datos:
            precio_base = d["precio"]
            categoria = d["categoria"]

            if categoria == "Tecnología":
                iva_repetido = precio_base * 0.12
            else:
                iva_repetido = precio_base * 0.15

            sumatoria += iva_repetido
        print(f"Total de IVA acumulado en inventario: ${sumatoria}")

# Simulación de ejecución del programa
if __name__ == "__main__":
    print("--- SISTEMA DE INVENTARIO VIEJO V1.0 ---")
    # Registrar un par de productos de prueba
    p_pro(1, "123456789", "Laptop", 800.0, 3, "Tecnología")
    p_pro(1, "987654321", "Cuaderno", 2.50, 50, "Útiles")
    
    # Listar productos
    p_pro(2, "", "", 0, 0, "")
    
    # Ver reporte de IVA
    p_pro(3, "", "", 0, 0, "")
