### 📜 Análisis de Deuda Técnica y Evolutividad del Software

**Asignatura:** Sistemas Ágiles

**Equipo de Desarrollo:**
*   Jose Daniel Luzuriaga (Líder de Equipo)
* Samara Puga
* Marcia Guerrero
* Jaqueline Anrango
* William Males

**Fecha de Emisión:** 25 de Junio del 2026

---
### 1. ախ Diagnóstico de la Calidad del Código Heredado

A continuación, se detallan los tres problemas de diseño más significativos identificados en el archivo `main.py`, interpretados a través de los principios de calidad de software.

1.  **Rigidez Estructural:** La base del código exhibe una rigidez considerable. Cualquier modificación en las reglas de negocio, como ajustar la tasa del IVA, requiere intervenciones en múltiples puntos del código. Esto quedó demostrado al intentar cambiar el IVA para la categoría "Tecnología", lo que nos forzó a alterar la lógica de cálculo tanto en el módulo de registro de productos (`op == 1`) como en el de generación de reportes (`op == 3`). El código, en su estado actual, se opone activamente al cambio.

2.  **Inmovilidad de Componentes:** La lógica de negocio está encapsulada de una manera que impide su reutilización. La función `p_pro` actúa como una "Función Dios", un anti-patrón que consolida responsabilidades dispares como validación de entradas, cálculos fiscales, aplicación de descuentos, persistencia de datos y renderizado en la interfaz. Resulta inviable reutilizar únicamente la lógica de cálculo de impuestos en un nuevo contexto sin arrastrar consigo todo el acoplamiento a la consola y al sistema de archivos.

3.  **Fragilidad y Opacidad:** El sistema es frágil, ya que cambios menores en el formato de los datos de entrada (por ejemplo, una coma mal ubicada en el archivo `.txt` original) podrían causar una falla catastrófica en tiempo de ejecución. Adicionalmente, el código es opaco; el uso de nombres de variables ambiguos y poco descriptivos (`p_pro`, `A`, `l`, `x1`, `p1`) oculta la intención del programador, elevando drásticamente la dificultad para su comprensión y mantenimiento futuro.

---
### 2. 🗺️ Registro de Obstáculos en la Evolución del Software (Basado en Commits)

Se documenta el impacto técnico observado al implementar los cambios solicitados, correlacionando las dificultades con las características de diseño previamente mencionadas.

1.  #### Commit: `Tarea 2`
    *   **Impacto Técnico:** La modificación de la tasa de IVA para "Tecnología" al 12% se complicó innecesariamente debido a la **duplicación de código**. La misma lógica para el cálculo del impuesto estaba replicada en el flujo de registro (`op == 1`) y en el de reporte (`op == 3`). Esto nos obligó a intervenir en **dos bloques de código separados** para aplicar una única regla de negocio, lo que incrementa el riesgo de introducir inconsistencias.

2.  #### Commit: `Tarea 3`
    *   **Impacto Técnico:** La migración del formato de persistencia de `.txt` a `.json` tuvo un impacto masivo y generalizado. El código presentaba un **fuerte acoplamiento** con el formato de texto plano. Fue necesario reescribir por completo los módulos de escritura (`op == 1`), lectura (`op == 2`) y reporte (`op == 3`), afectando a más del 50% del cuerpo de la función `p_pro`. La lógica de negocio estaba intrínsecamente mezclada con la de acceso a datos, lo que impidió una transición limpia y controlada.

3.  #### Commit: `Tarea 4`
    *   **Impacto Técnico:** La adición del campo `codigo_barras` introdujo una fricción significativa en el desarrollo. Este cambio nos obligó a modificar la firma de la función `p_pro`, la lógica de validación de datos, la estructura del objeto a persistir y el formato de la tabla de visualización. Además, fue necesario implementar un acceso condicional con `prod.get()` para mantener la retrocompatibilidad con los registros antiguos, lo que pone de manifiesto la fragilidad del sistema ante la evolución del esquema de datos.

---
### 3. 💡 Propuesta de Refactorización Estratégica

Para abordar la deuda técnica acumulada, proponemos las siguientes tres acciones prioritarias, basadas en los principios de **Clean Code**, a ejecutar en el próximo ciclo de desarrollo:

1.  **Aplicar el Principio de Responsabilidad Única (SRP):** Descomponer la función monolítica `p_pro` en unidades más pequeñas y con un propósito bien definido. Esto implica crear funciones especializadas para `leer_inventario()`, `guardar_inventario()`, `calcular_precio_final()`, y funciones adicionales para gestionar las interacciones con la interfaz de usuario.

2.  **Centralizar Reglas y Eliminar Duplicidad (DRY - Don't Repeat Yourself):** Abstraer y centralizar todas las reglas de negocio. Proponemos crear una estructura de configuración (ej. un diccionario) para gestionar las tasas de IVA y los descuentos, eliminando los "valores mágicos". Se debe crear una única función para el cálculo de impuestos que sea invocada desde todos los puntos necesarios, erradicando la lógica duplicada.

3.  **Desacoplar la Lógica de Negocio de la Persistencia:** Implementar una capa de abstracción de datos (patrón Repositorio). La lógica de negocio no debe tener conocimiento sobre el medio de almacenamiento (JSON, TXT, BBDD). En su lugar, debe interactuar con funciones como `obtener_producto()` o `guardar_producto()`, encapsulando por completo la manipulación de archivos o cualquier otro mecanismo de persistencia.

---
### 4. 🎯 Conclusiones del Equipo

*   **Estimación de Deuda Técnica en el Código Original (0% a 100%):** [**85%**]

*   **Reflexión desde una Perspectiva Ágil:** Un sistema de software con un alto índice de deuda técnica es análogo a intentar correr una maratón con una mochila cargada de rocas. En cada sprint, la capacidad del equipo para entregar nuevas funcionalidades o adaptar las existentes se ve mermada. El esfuerzo se desvía hacia la gestión de la complejidad y la mitigación de riesgos, en lugar de centrarse en la entrega de valor tangible para el cliente, lo que ralentiza el ciclo de desarrollo y eleva los costos a largo plazo.