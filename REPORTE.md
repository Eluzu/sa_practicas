# Reporte de Diagnóstico y Refactorización del Sistema de Inventario

## 1. Diagnóstico de la Calidad del Código
El código original presentaba un diseño basado en procedimientos simples con acoplamiento fuerte al formato de almacenamiento (`txt` plano). Esto dificultaba la escalabilidad y la mantenibilidad.

*   **Puntos Fuertes:** Uso de `dataclass` para definir la entidad `Producto` y modularización básica de funciones.
*   **Puntos Débiles:** 
    *   **Acoplamiento:** La lógica de persistencia estaba entrelazada con la lógica de negocio.
    *   **Escalabilidad:** La gestión de archivos planos impedía una evolución sencilla hacia estructuras más complejas.
    *   **Mantenibilidad:** El cálculo de impuestos estaba disperso, lo que dificultaba cambios normativos.

## 2. Mapeo de Dificultades (Estimación de Impacto)
Se analiza la magnitud del cambio basado en el alcance de las alteraciones por requerimiento:

| Requerimiento | Líneas Alteradas (Aprox) | Complejidad de Implementación |
| :--- | :---: | :--- |
| **Alerta de Stock (<5)** | 10 | Baja (lógica de presentación) |
| **IVA Diferenciado (Tecnología)** | 15 | Media (lógica de cálculo) |
| **Migración a JSON** | 30 | Alta (cambio de infraestructura) |
| **Campo `codigo_barras`** | 20 | Alta (cambio de modelo de datos) |

*   **Nota:** La migración a JSON fue el punto de mayor fricción, ya que obligó a reconstruir los métodos de lectura y escritura de forma no lineal.

## 3. Propuesta Ágil de Refactorización
Para mejorar la calidad y prevenir "deuda técnica" futura, se propone la siguiente arquitectura:

1.  **Patrón Repositorio:** Separar la lógica de acceso a datos (lectura/escritura) de la lógica de negocio. Esto permitirá cambiar de `JSON` a una `Base de Datos SQL` sin tocar las funciones de cálculo.
2.  **Inyección de Dependencias:** Pasar las reglas de cálculo (IVA, Descuentos) como configuraciones externas en lugar de constantes fijas dentro del código.
3.  **Validación de Esquema:** Implementar `pydantic` o validadores de esquema robustos para asegurar que los nuevos campos (como `codigo_barras`) no corrompan el archivo de datos.
4.  **Testing:** Automatizar pruebas unitarias para `calcular_precio_final`, garantizando que los cambios en las tasas impositivas no rompan la integridad financiera.

---
*Generado automáticamente para el Departamento de Control de Calidad.*