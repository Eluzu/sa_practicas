# Reporte de Calidad y Refactorización: Sistema de Inventario

## 1. Diagnóstico de la Calidad del Código (Estado Inicial)
El código original presentaba los siguientes "code smells" o vicios de programación:
- **Hardcoding:** Valores constantes (como el IVA del 15%) estaban dispersos en la lógica de negocio, dificultando actualizaciones.
- **Acoplamiento fuerte:** La lógica de cálculo, la validación y la persistencia de datos estaban mezcladas en una sola función gigante.
- **Duplicidad de lógica:** Los cálculos se repetían tanto al escribir como al leer, violando el principio DRY (*Don't Repeat Yourself*).
- **Formato ineficiente:** El uso de archivos `.txt` con manejo manual de cadenas (`split`, `strip`) era propenso a errores ante cambios en la estructura de los datos.

## 2. Mapeo de Dificultades y Evolución
La siguiente tabla detalla el impacto de los cambios requeridos:

| Iteración | Cambio Realizado | Dificultad | Impacto en Líneas |
| :--- | :--- | :--- | :--- |
| **Refactorización IVA** | Cambio de 15% a 12% para Tecnología | Baja | Mínimo (Centralización) |
| **Migración JSON** | Cambio de .txt a formato estructurado | Media | Alto (Rediseño de lectura/escritura) |
| **Campo Obligatorio** | Inserción de `codigo_barras` | Baja/Media | Moderado (Requiere validación) |

*Nota: La mayor dificultad técnica ocurrió en la migración a JSON, ya que implicó cambiar la forma en que el programa interactúa con el disco (de lectura por línea a carga de objeto completo).*

## 3. Propuesta Ágil de Refactorización
Para mantener el sistema escalable y sostenible, se propone:

1.  **Patrón de Repositorio:** Separar la lógica de persistencia (guardar/cargar) de la lógica de negocio (cálculos financieros). Actualmente, `p_pro` hace demasiadas cosas.
2.  **Uso de Clases (POO):** Crear una clase `Producto` en lugar de manejar diccionarios planos. Esto permitiría validar el `codigo_barras` y los tipos de datos desde el momento de la creación del objeto.
3.  **Manejo de Excepciones:** Implementar bloques `try-except` más robustos para evitar que cambios en la estructura del archivo (como agregar campos nuevos) rompan la ejecución del programa (como ocurrió con el `KeyError`).
4.  **Validación de Esquema:** Utilizar librerías como `pydantic` o `marshmallow` si el sistema crece, para asegurar que los datos en el JSON siempre sigan el formato esperado.

## 4. Conclusión
El proceso demostró que la agilidad no solo consiste en programar rápido, sino en **diseñar código adaptable**. La transición a JSON y la centralización de constantes como el IVA permiten ahora responder a solicitudes financieras en minutos, en lugar de horas de depuración de código heredado.