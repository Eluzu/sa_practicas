# Reporte Técnico: Diagnóstico de Calidad, Mapeo de Dificultades y Propuesta Ágile

## 1. Diagnóstico de la Calidad del Código (Code Smell Assessment)
El código inicial presentaba una estructura funcional básica para un Producto Mínimo Viable (MVP). Sin embargo, al enfrentarse a la evolución del negocio, se identificaron varios **"olores de código" (Code Smells)** y violaciones a principios de diseño de software:

* **Violación del Principio de Responsabilidad Única (SRP):** La función `calcular_iva` asumía que el impuesto era global e inmutable ($15\%$). Al no recibir el contexto del producto, impedía que el reporte financiero consolidara métricas reales cuando las reglas de negocio cambiaron por categoría.
* **Acoplamiento Rígido a la Persistencia (Tight Coupling):** El sistema dependía enteramente de un archivo de texto plano separado por comas (`datos_inv.txt`). Cualquier cambio en la estructura (como añadir el código de barras) obligaba a reescribir manualmente los índices de parsing por posición (`linea.strip().split(",")`), aumentando la fragilidad ante errores de ejecución (*IndexError*).
* **Falta de Validación Extensible:** La validación estaba acoplada a campos fijos dentro de un condicional `if` rígido, lo que dificultaba la auditoría o la inyección de nuevas reglas obligatorias por parte de Control de Calidad sin modificar la lógica nuclear.

---

## 2. Mapeo de Dificultades por Iteración (Git / Branch Impact)
Evaluando el impacto del cambio basándonos en la cantidad de líneas de código (LoC) que tuvieron que alterarse, modificarse o añadirse en cada incremento del ciclo de vida ágil:

| Iteración / Requerimiento | Tipo de Cambio | Líneas Alteradas / Añadidas | Nivel de Dificultad | Impacto Arquitectónico |
| :--- | :--- | :--- | :--- | :--- |
| **Hito 1:** Alerta de Stock Crítico (Control de Calidad) | Extensión Visual | ~4 líneas | **Bajo** | Localizado únicamente en la capa de presentación (`listar_productos`). No alteró la persistencia. |
| **Hito 2:** IVA Diferenciado del $12\%$ (Financiero) | Refactorización Lógica | ~15 líneas | **Medio** | Alto. Se tuvo que cambiar la firma de `calcular_iva` y actualizar transversalmente tanto el cálculo del precio final como el bucle acumulador del reporte financiero. |
| **Hito 3:** Migración a Persistencia JSON (Cliente) | Cambio de Infraestructura | ~30 líneas | **Alto** | Crítico. Se eliminó la persistencia lineal y se rediseñaron por completo las funciones de Entrada/Salida (`leer_productos` y `guardar_producto`) adoptando el patrón Read-Modify-Write. |
| **Hito 4:** Campo Obligatorio `codigo_barras` | Modificación de Modelo | ~12 líneas | **Medio** | Medio. Afectó la definición de la Dataclass, la función de validación estructural, los mapeos del diccionario JSON y las máscaras de espaciado en la interfaz de consola. |

### Conclusión del Mapeo:
El incremento que mayor fricción causó fue la **Migración a JSON**, debido a que el código original no utilizaba un patrón de repositorio aislado, lo que obligó a modificar la lógica íntima de persistencia. Esto demuestra que la falta de abstracción inicial eleva el costo del cambio.

---

## 3. Propuesta Ágil de Refactorización Futura
Para maximizar la velocidad de entrega del equipo (*Velocity*) y asegurar que el sistema soporte cambios sin añadir deuda técnica, se propone la adopción de las siguientes prácticas en el próximo Sprint: