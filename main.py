import os

ARCHIVO = "datos_inv.txt"
IVA_GENERAL = 0.15
IVA_TECNOLOGIA = 0.12  # Requerimiento solicitado por Financiero

def calcular_impuesto(precio, categoria):
    """Retorna el IVA correspondiente según la categoría."""
    if categoria == "Tecnología":
        return precio * IVA_TECNOLOGIA
    return precio * IVA_GENERAL

def p_pro(op, x, p, c, t):
    if op == 1:
        if x == "" or p <= 0 or c < 0:
            print("Error: Datos inválidos.")
            return False
        
        # Uso de la lógica centralizada
        iva = calcular_impuesto(p, t)
        total_con_iva = p + iva
        
        # Lógica de descuento
        descuento = 0.10 if t == "Tecnología" else 0.0
        p_final = total_con_iva * (1 - descuento)
            
        linea = f"{x},{p},{c},{t},{p_final}\n"
        with open(ARCHIVO, "a") as f:
            f.write(linea)
        print(f"Producto '{x}' guardado.")
        
    elif op == 3:
        # Reporte de IVA utilizando la lógica centralizada
        if not os.path.exists(ARCHIVO): return
        with open(ARCHIVO, "r") as f:
            lineas = f.readlines()
        
        total_iva = sum(calcular_impuesto(float(l.split(",")[1]), l.split(",")[3]) for l in lineas)
        print(f"Total de IVA acumulado: ${total_iva:.2f}")

# Simulación
if __name__ == "__main__":
    # Al registrar, Tecnología ahora calcula el 12%
    p_pro(1, "Laptop", 800.0, 2, "Tecnología")
    p_pro(1, "Cuaderno", 2.50, 50, "Útiles")
    
    # Ver reporte de IVA actualizado
    p_pro(3, "", 0, 0, "")