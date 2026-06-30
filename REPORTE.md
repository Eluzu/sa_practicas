# Reporte Técnico: Diagnóstico de Calidad y Propuesta de Refactorización Ágil

Este documento presenta un análisis de la deuda técnica identificada en el sistema de inventario base, el impacto cuantitativo de los requerimientos implementados y la estrategia ágil propuesta para evolucionar el software hacia una arquitectura mantenible y escalable.

---

## 1. Diagnóstico de la Calidad del Código (Código Original)

El código inicial presentaba múltiples **"code smells"** (síntomas de mal diseño) que violaban los principios fundamentales de la programación limpia (Clean Code) y el desarrollo ágil:

*   **Función "Dios" (Monolítica):** La función `p_pro` centralizaba absolutamente todas las responsabilidades del sistema (validación, reglas de negocio, persistencia en archivos y formateo de interfaces visuales). Esto rompe directamente el **Principio de Responsabilidad Única (SRP)**.
*   **Código Duplicado (Violación de DRY):** El cálculo de la tasa del IVA ($15\%$) se encontraba duplicado y *hardcoded* (quemado) tanto en el módulo de registro como en el de reportes.
*   **Nombres Crípticos e Inexpresivos:** El uso de variables con nombres de una sola letra o genéricos (`A`, `x`, `p`, `c`, `t`, `datos1`, `x1`) reducía drásticamente la legibilidad y auto-documentación del código.
*   **Acoplamiento de Datos (Firma Compleja):** Para ejecutar acciones simples como listar productos o generar reportes, el cliente del código se veía obligado a enviar argumentos falsos o vacíos (`p_pro(2, "", 0, 0, "")`), incrementando el riesgo de errores en tiempo de ejecución.

---

## 2. Mapeo de Dificultades (Análisis de Impacto)

El siguiente cuadro evalúa la complejidad del mantenimiento basándose en la cantidad de líneas de código alteradas o añadidas para resolver los requerimientos del negocio de forma iterativa:

| Requerimiento (Incremento) | Líneas Alteradas / Añadidas | Nivel de Dificultad | Impacto en la Arquitectura |
| :--- | :---: | :---: | :--- |
| **Cambio de IVA (12% Tecnología)** | ~12 líneas | **Medio** | Alto riesgo de inconsistencia. Al estar duplicado el IVA, se tuvo que intervenir la lógica de registro y la de reportes de forma simultánea. |
| **Persistencia a Formato JSON** | ~25 líneas | **Alto** | Rompió la estructura de parseo basada en índices de texto (`split(",")`). Obligó a reescribir por completo los bloques de lectura y escritura. |
| **Campo Obligatorio `codigo_barras`** | ~15 líneas | **Bajo-Medio** | Alteró la firma global de la función `p_pro`, forzando la actualización en cascada de todas las llamadas simuladas en el bloque principal. |

> 📊 **Lección Aprendida:** En una arquitectura monolítica, una modificación simple en los datos (como un archivo JSON o un nuevo campo) impacta directamente en la lógica visual y de cálculo, incrementando exponencialmente el esfuerzo de mantenimiento.

---

## 3. Propuesta Ágil de Refactorización (Evolución a MVC)

Para eliminar la rigidez del código actual, se propone desacoplar el sistema adoptando el patrón arquitectónico **Modelo-Vista-Controlador (MVC)**, el cual distribuye las responsabilidades en capas independientes y altamente cohesivas:

### Estructura de Capas Propuesta:

1.  **Modelo (`Model`):** Encargado exclusivo de la estructura de los datos del producto (esquema del diccionario) y de los métodos de persistencia física en el archivo `datos_inv.json`.
2.  **Controlador (`Controller`):** Orquesta las reglas de negocio puras. Aquí residen de forma aislada las funciones de validación, el cálculo dinámico del IVA según categoría y la aplicación de descuentos.
3.  **Vista (`View`):** Capa limpia encargada de la salida y formato en consola (tablas, alertas de stock mínimo y mensajes de éxito/error). No realiza cálculos ni escribe archivos.

### Plano del Código Refactorizado:

A continuación se presenta el diseño final sugerido para separar responsabilidades y eliminar definitivamente la función rígida `p_pro`:

```python
import os
import json

# ==========================================
# CAPILLA 1: MODELO (Persistencia y Datos)
# ==========================================
class InventarioModel:
    def __init__(self, ruta_archivo="datos_inv.json"):
        self.ruta = ruta_archivo

    def leer_todos(self):
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def guardar_todos(self, datos):
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)


# ==========================================
# CAPILLA 2: CONTROLADOR (Reglas de Negocio)
# ==========================================
class InventarioController:
    def __init__(self, model):
        self.model = model

    def obtener_tasa_iva(self, categoria):
        return 0.12 if categoria == "Tecnología" else 0.15

    def registrar_producto(self, codigo, nombre, precio, stock, categoria):
        # Validaciones obligatorias
        if not codigo or not nombre or precio <= 0 or stock < 0:
            return False, "Error: Datos inválidos o campos obligatorios vacíos."
        
        # Cálculos financieros
        iva = precio * self.obtener_tasa_iva(categoria)
        total_con_iva = precio + iva
        
        # Descuento comercial
        precio_final = total_con_iva - (total_con_iva * 0.10) if categoria == "Tecnología" else total_con_iva

        nuevo_producto = {
            "codigo_barras": codigo,
            "producto": nombre,
            "precio_base": precio,
            "stock": stock,
            "categoria": categoria,
            "precio_final": round(precio_final, 2)
        }

        inventario = self.model.leer_todos()
        inventario.append(nuevo_producto)
        self.model.guardar_todos(inventario)
        return True, f"Producto '{nombre}' registrado con éxito."

    def calcular_total_iva(self):
        inventario = self.model.leer_todos()
        return sum(item["precio_base"] * self.obtener_tasa_iva(item["categoria"]) for item in inventario)


# ==========================================
# CAPILLA 3: VISTA (Interfaz de Usuario)
# ==========================================
class InventarioView:
    @staticmethod
    def mostrar_tabla_productos(productos):
        if not productos:
            print("No hay datos registrados en el inventario.")
            return
        
        print("\n" + "-" * 70)
        print(f"{'COD':<10} | {'PRODUCTO':<15} | {'PRECIO':<9} | {'STOCK':<8} | {'CATEGORÍA':<12} | {'P. FINAL':<9}")
        print("-" * 70)
        for item in productos:
            if item["stock"] < 5:
                print(f"⚠️ Alerta Stock Bajo: '{item['producto']}' tiene solo {item['stock']} unidades.")
            
            print(f"{item['codigo_barras']:<10} | {item['producto']:<15} | ${item['precio_base']:<8.2f} | {item['stock']:<8} | {item['categoria']:<12} | ${item['precio_final']:<8.2f}")
        print("-" * 70)

    @staticmethod
    def mostrar_reporte_iva(total_iva):
        print(f"\n==================================================")
        print(f" Reporte Financiero - Total IVA en Inventario: ${total_iva:.2f}")
        print(f"==================================================")