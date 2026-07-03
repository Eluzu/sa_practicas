# Reporte de Deuda Técnica y Adaptabilidad del Software

**Asignatura:** Sistemas Ágiles

**Integrantes del grupo:** 
* Jose Daniel Luzuriaga (Jefe de grupo)
* Samara Puga
* Marcia Guerrero
* Jaqueline Anrango
* William Males

**Fecha:** 02 de Julio del 2026

---
## 1. Diagnóstico de Calidad (Código Legacy)

Identifiquen y describan brevemente los 3 principales problemas de diseño encontrados en el archivo `main.py` utilizando los conceptos de calidad de código vistos en clase:
1. **Rigidez:** 
El sistema es rígido porque un cambio conceptual simple provoca modificaciones en cascada. Por ejemplo, cambiar el cálculo del IVA para una categoría específica (`Tecnología`) no solo afectó a la función `calcular_iva`, sino que obligó a pasar la categoría como parámetro, impactando también a `calcular_precio_final` y `reporte_iva`. El uso de una constante global `IVA` centralizaba una regla de negocio que no era universal, haciendo el sistema frágil a excepciones.

2. **Inmovilidad:** 
El código es inmóvil debido al alto acoplamiento entre sus componentes. Las funciones `guardar_producto` y `leer_productos` están fuertemente acopladas al formato de archivo de texto plano (`.txt`). Reutilizar estas funciones para otro formato de almacenamiento (como JSON o una base de datos) es imposible sin una reescritura completa. Además, la lógica de negocio (cálculo de precio) está mezclada con la lógica de persistencia, dificultando la extracción de componentes para su reutilización.

3. **Fragilidad y Opacidad:** 
*   **Fragilidad:** El sistema es frágil porque un cambio en una parte puede romper otras de forma inesperada. La dependencia del formato `nombre,precio,stock,...` en el archivo `.txt` es un claro ejemplo. Si el orden o número de campos en `guardar_producto` cambiaba, `leer_productos` se rompía sin previo aviso.
*   **Opacidad:** El código es opaco. La función `leer_productos` devolvía una lista de diccionarios, mientras que el resto del sistema usaba un `dataclass` `Producto`. Esta inconsistencia en las estructuras de datos hace que el flujo de información sea difícil de seguir y propenso a errores.
---
## 2. Mapeo de Dificultades para la Evolución (Evidencia Git)

Explica qué sucedió cuando intentaron aplicar los cambios solicitados por el docente en cada una de las actividades requeridas (Abordar todas las 5 actividades  a excepcion de la elaboracion de este reporte que en este caso es la quinta). Justifiquen el impacto técnico basándose en cuántas funciones o líneas de código se vieron afectadas.
1. ### `Tarea 1`
* **Requerimiento:** Imprimir una alerta de stock bajo (< 5 unidades) al listar productos.
* **Impacto encontrado:** Este cambio fue relativamente simple, pero aun así requirió modificar la función `listar_productos` para añadir una estructura condicional (`if`). Se vieron afectadas aproximadamente **3 líneas de código** dentro de **1 función**.
2. ### `Tarea 2`
* **Requerimiento:** Aplicar un IVA del 12% para "Tecnología" en lugar del 15% general.
* **Impacto encontrado:** Este cambio expuso la rigidez del sistema. Se modificó la constante `IVA` por dos nuevas (`IVA_GENERAL`, `IVA_TECNOLOGIA`). La función `calcular_iva` necesitó recibir la categoría del producto, lo que generó un cambio en su firma. Esto obligó a modificar las llamadas en `calcular_precio_final` y `reporte_iva`. En total, se vieron afectadas **3 funciones** y alrededor de **8-10 líneas de código**.
3. ### `Tarea 3`
* **Requerimiento:** Cambiar el almacenamiento de `.txt` a `.json`.
* **Impacto encontrado:** Este fue uno de los cambios más impactantes debido a la inmovilidad del código. Se tuvieron que reescribir por completo las funciones `guardar_producto` y `leer_productos`. Además, el cálculo del `precio_final`, que antes se guardaba en el archivo, ahora se realiza al momento de listar, lo que también afectó a `listar_productos`. Se vieron afectadas **3 funciones** con una reescritura casi total, modificando más de **20 líneas**.
4. ### `Tarea 4`
* **Requerimiento:** Agregar un campo obligatorio `codigo_barras`.
* **Impacto encontrado:** Este cambio se propagó por todo el sistema. Hubo que modificar el `dataclass Producto`, la función de validación (`validar_producto`), las funciones de persistencia (`guardar_producto`, `leer_productos`), la función de presentación (`listar_productos`) y la creación de instancias en `main()`. En total, se vieron afectadas **6 áreas/funciones del código**, demostrando un alto acoplamiento. Se modificaron aproximadamente **15 líneas** en múltiples lugares.
---
## 3. Propuesta de Refactorización Inicial

Enumera qué 3 acciones principales tomarían para eliminar la deuda técnica de este sistema:
1.  **Separar Responsabilidades (Single Responsibility Principle):** Crear una clase `Inventario` que encapsule toda la lógica de persistencia (lectura y escritura de datos), independientemente del formato (JSON, DB, etc.). Las funciones de negocio como `calcular_precio_final` no deberían saber cómo se guardan los datos.
2.  **Abstracción de Reglas de Negocio:** Externalizar las reglas de negocio complejas, como los tipos de IVA o descuentos por categoría, a una estructura de configuración más flexible (por ejemplo, un diccionario de configuración o un motor de reglas simple). Esto evitaría tener `if/else` anidados en el código a medida que se añaden nuevas reglas.
3.  **Uso Consistente de Tipos de Datos:** Mantener el uso del `dataclass Producto` a lo largo de todo el ciclo de vida de los datos. La función `leer_productos` debería devolver una lista de objetos `Producto` (`List[Producto]`), no una lista de diccionarios. Esto mejora la legibilidad, la seguridad de tipos y el autocompletado del editor.
---
## 4. Conclusiones del Equipo
* **Porcentaje estimado de deuda técnica en el script original (0% al 100%):** [**70%**]
* **Reflexión ágil:** Un software rígido con alta deuda técnica obliga a los desarrolladores a invertir más tiempo en entender y modificar código frágil que en entregar nuevas funcionalidades. En un marco ágil como Scrum, esto reduce drásticamente la velocidad del equipo, ya que el esfuerzo para completar una historia de usuario aumenta inesperadamente, impidiendo cumplir con los objetivos del sprint y entregar valor de forma continua.
---
## 5. Alternativa para separar en diferentes archivos el programa implementado (respetado siempre los principio de código limpio)

Siguiendo esta propuesta, se ha reestructurado el proyecto aplicando el **Principio de Responsabilidad Única (SRP)**. El monolítico `main.py` fue dividido en módulos cohesivos, donde cada uno tiene una única y bien definida razón para cambiar.

Esta separación no solo elimina la deuda técnica, sino que también crea un sistema más mantenible, escalable y fácil de probar. A continuación, se detalla la arquitectura y la responsabilidad de cada archivo:

### `main.py` - El Orquestador
*   **Responsabilidad:** Ser el punto de entrada y coordinar el flujo principal de la aplicación.
*   **Guía:** Este archivo no contiene lógica de negocio, persistencia o presentación. Su única tarea es iniciar la aplicación y llamar a las funciones de alto nivel de los otros módulos en el orden correcto. Para añadir un nuevo paso en el flujo principal, este es el lugar para hacerlo.

### `config.py` - El Centro de Configuración
*   **Responsabilidad:** Centralizar todas las constantes y parámetros de configuración.
*   **Guía:** Si necesitas cambiar una tasa de IVA, el nombre del archivo de inventario, el umbral de stock o cualquier otro "número mágico", este es el único lugar que debes modificar. Esto evita tener que buscar valores hardcodeados por todo el código.

### `models.py` - Los Planos de Datos
*   **Responsabilidad:** Definir las estructuras de datos de la aplicación, como la clase `Producto`.
*   **Guía:** Si se requiere añadir o modificar un campo en los productos (ej. agregar `descripcion`), se debe empezar por actualizar la `dataclass` en este archivo.

### `services.py` - El Cerebro del Negocio
*   **Responsabilidad:** Contener toda la lógica de negocio pura.
*   **Guía:** Las funciones aquí (`calcular_iva`, `calcular_precio_final`, etc.) realizan los cálculos y validaciones. No dependen de cómo se guardan los datos ni de cómo se muestran. Si una regla de negocio cambia, este es el módulo a modificar. Gracias a su desacoplamiento, es el candidato ideal para las pruebas unitarias.

### `repository.py` - El Guardián de los Datos
*   **Responsabilidad:** Encapsular toda la lógica de persistencia (lectura y escritura de datos).
*   **Guía:** Este módulo actúa como una capa de abstracción sobre el almacenamiento. Actualmente usa un archivo JSON, pero si en el futuro se decide migrar a una base de datos SQL o a un servicio en la nube, **este es el único archivo que necesitaría cambiar**. El resto de la aplicación seguiría funcionando sin modificaciones.

### `ui.py` - La Cara Visible
*   **Responsabilidad:** Manejar toda la interacción con el usuario (la capa de presentación).
*   **Guía:** Todas las funciones que imprimen en consola (`print`) están aquí. Si se desea cambiar el formato de la tabla de productos, añadir colores o incluso crear una interfaz gráfica en el futuro, este es el módulo que se debe evolucionar.

### Conclusión de la Arquitectura

Esta estructura modular permite que los desarrolladores trabajen en diferentes aspectos de la aplicación de forma independiente. Un cambio en la base de datos (`repository.py`) no afectará a quien esté ajustando la interfaz de usuario (`ui.py`), y viceversa. Esto no solo reduce el riesgo de introducir errores, sino que acelera drásticamente el desarrollo y la adaptación a nuevos requerimientos, alineándose perfectamente con los principios de un desarrollo ágil.