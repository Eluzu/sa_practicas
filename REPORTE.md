# Evaluación de Calidad y Potencial de Evolución del Software

**Curso:** Sistemas Ágiles

**Equipo:**
* Jose Daniel Luzuriaga (Líder)
* Samara Puga
* Marcia Guerrero
* Jaqueline Anrango
* William Males

**Fecha:** 02 de Julio del 2026

---
## 1. Análisis de Calidad del Código Base

El código inicial presentaba varios "olores" de diseño que obstaculizan su mantenimiento y evolución. A continuación, se detallan los principales problemas identificados.

1. **Alta Resistencia al Cambio (Rigidez):**
   El sistema demuestra ser rígido, ya que cambios sencillos en la lógica de negocio provocan una reacción en cadena a través de múltiples componentes. Un ejemplo claro fue el requerimiento de ajustar el IVA para la categoría "Tecnología". Esta modificación no solo implicó alterar la función de cálculo (`calcular_iva`), sino que también forzó un cambio en su firma para aceptar la categoría del producto. Esto, a su vez, repercutió en `calcular_precio_final` y `reporte_iva`, que tuvieron que ser adaptados para proporcionar este nuevo parámetro. El problema subyacente era una constante global `IVA` que asumía una regla de negocio única para todos los casos, haciendo el diseño inflexible ante excepciones.

2. **Baja Reutilización y Acoplamiento Excesivo (Inmovilidad):**
   La reutilización de componentes es prácticamente inviable debido al fuerte acoplamiento. Las funciones de persistencia (`guardar_producto`, `leer_productos`) estaban íntimamente ligadas al formato de archivo de texto plano (`.txt`). Intentar usar estas funciones con otro medio de almacenamiento, como un archivo JSON o una base de datos, requeriría una reescritura total. Este acoplamiento se agrava al mezclar la lógica de negocio (cálculos de precios) con la lógica de persistencia, lo que impide aislar y reutilizar funcionalidades de forma independiente.

3. **Comportamiento Impredecible y Falta de Claridad (Fragilidad y Opacidad):**
   *   **Fragilidad:** El sistema es propenso a romperse en lugares inesperados tras un cambio. La dependencia estricta del formato `nombre,precio,stock,...` en el archivo de texto es un punto crítico. Cualquier alteración en el orden o la cantidad de campos en la función `guardar_producto` causaría fallos silenciosos en `leer_productos`, que no podría interpretar correctamente los datos.
   *   **Opacidad:** El flujo de datos es confuso y difícil de rastrear. Un ejemplo notorio es la inconsistencia en los tipos de datos: la función `leer_productos` retornaba una lista de diccionarios genéricos, mientras que el resto de la aplicación estaba diseñada para operar con un `dataclass` `Producto`. Esta discrepancia obliga a realizar conversiones constantes, dificulta la comprensión del código y es una fuente potencial de errores.

---
## 2. Impacto de los Cambios Solicitados (Análisis de Evolución)

A continuación, se documenta el impacto técnico observado al implementar los cambios requeridos por el docente, justificando el esfuerzo en función de las áreas del código afectadas.

1. ### **Tarea 1: Alerta de Stock Bajo**
   *   **Requerimiento:** Mostrar un mensaje de alerta al listar productos si su stock es inferior a 5 unidades.
   *   **Impacto Técnico:** Fue el cambio de menor complejidad. Se añadió una condición `if` dentro de la función `listar_productos`. Afectó a **1 función** con la modificación de aproximadamente **3 líneas de código**.

2. ### **Tarea 2: IVA Diferenciado por Categoría**
   *   **Requerimiento:** Aplicar una tasa de IVA del 12% a "Tecnología" y mantener el 15% para el resto.
   *   **Impacto Técnico:** Este cambio reveló la rigidez estructural del sistema. Fue necesario reemplazar la constante `IVA` por dos nuevas (`IVA_GENERAL`, `IVA_TECNOLOGIA`). La firma de `calcular_iva` tuvo que ser modificada para recibir la categoría, lo que desencadenó cambios en cascada en las funciones que la invocaban, como `calcular_precio_final` y `reporte_iva`. En total, **3 funciones** fueron modificadas, afectando entre **8 y 10 líneas de código**.

3. ### **Tarea 3: Migración de Persistencia a JSON**
   *   **Requerimiento:** Cambiar el formato de almacenamiento de datos de `.txt` a `.json`.
   *   **Impacto Técnico:** Este fue el cambio más disruptivo, evidenciando la inmovilidad del código. Las funciones `guardar_producto` y `leer_productos` tuvieron que ser reescritas casi por completo. Adicionalmente, la lógica de presentación en `listar_productos` se vio afectada, ya que el cálculo del precio final, que antes se almacenaba en el archivo, ahora se realiza en tiempo de ejecución. El impacto se extendió a **3 funciones** clave, con más de **20 líneas de código** reescritas.

4. ### **Tarea 4: Adición del Campo `codigo_barras`**
   *   **Requerimiento:** Incluir un nuevo campo obligatorio `codigo_barras` para cada producto.
   *   **Impacto Técnico:** La introducción de un nuevo campo de datos se propagó por todo el sistema. Fue necesario actualizar la definición del `dataclass Producto`, la función `validar_producto`, las de persistencia (`guardar_producto`, `leer_productos`), la de presentación (`listar_productos`) y la creación de productos en la función `main()`. Este efecto dominó afectó a **6 componentes distintos** del programa, con cerca de **15 líneas modificadas** en múltiples archivos, demostrando un acoplamiento muy alto.

---
## 3. Plan de Refactorización Sugerido

Para mitigar la deuda técnica identificada, proponemos las siguientes tres acciones prioritarias:

1.  **Crear una Capa de Acceso a Datos (Principio de Responsabilidad Única):**
    Se debe diseñar una clase `RepositorioInventario` (o similar) que encapsule toda la lógica de lectura y escritura de datos. Esta clase expondrá métodos como `obtener_todos()` o `guardar(producto)` y será la única responsable de interactuar con el medio de almacenamiento (JSON, base de datos, etc.). De este modo, el resto de la aplicación, incluida la lógica de negocio, se vuelve agnóstica al formato de persistencia.

2.  **Externalizar y Centralizar las Reglas de Negocio:**
    Las reglas de negocio, como los porcentajes de IVA o los descuentos, no deben estar codificadas directamente en las funciones (`hardcoded`). Proponemos moverlas a una estructura de configuración externa (ej. un diccionario o un archivo de configuración). Esto permitiría añadir o modificar reglas (ej. "nuevo descuento para la categoría 'Hogar'") sin alterar el código fuente, eliminando la proliferación de sentencias `if/else`.

3.  **Establecer un Modelo de Dominio Unificado:**
    Es fundamental garantizar la consistencia en la representación de los datos. El `dataclass Producto` debe ser el modelo canónico en toda la aplicación. Las funciones de persistencia, como `leer_productos`, deben ser refactorizadas para que devuelvan una lista de objetos `Producto` (`List[Producto]`) en lugar de una lista de diccionarios. Esto no solo mejora la legibilidad y el mantenimiento, sino que también habilita el chequeo de tipos estático y un mejor soporte del IDE.

---
## 4. Implementación de la Refactorización: Separación de Responsabilidades

Siguiendo el plan de refactorización, se procedió a reestructurar la aplicación monolítica (`main.py`) en un proyecto modular, aplicando el **Principio de Responsabilidad Única**. El objetivo principal fue aislar las distintas áreas de la aplicación (datos, lógica de negocio, presentación) para reducir el acoplamiento y aumentar la cohesión, facilitando así su mantenimiento y futura expansión.

La nueva estructura de archivos propuesta es la siguiente:

```
sa_practicas/
├── config.py
├── domain/
│   └── product.py
├── repository/
│   └── product_repository.py
├── services/
│   └── inventory_service.py
├── ui/
│   └── console_ui.py
└── main.py
```

A continuación, se detalla la responsabilidad de cada componente:

*   **`config.py` (Módulo de Configuración):**
    Este archivo centraliza todas las constantes y parámetros que pueden cambiar con el tiempo, como las tasas de IVA, las reglas de descuento o la ubicación del archivo de datos. Al externalizar la configuración, se logra que las modificaciones en las reglas de negocio no requieran alterar el código fuente de la lógica principal.

*   **`domain/product.py` (Capa de Dominio):**
    Contiene la definición del `dataclass Producto`. Este es el corazón del modelo de datos de la aplicación. Aislarlo en su propio módulo asegura que exista una única fuente de verdad sobre la estructura de un producto, eliminando la ambigüedad y la inconsistencia entre capas.

*   **`repository/product_repository.py` (Capa de Repositorio):**
    Implementa el patrón Repositorio. Su única responsabilidad es la persistencia de los objetos `Producto`. Es el único módulo que sabe *cómo* y *dónde* se guardan los datos (en este caso, en un archivo JSON). Abstrae los detalles de lectura y escritura, de modo que el resto de la aplicación solo necesita pedir o enviar listas de objetos `Producto`, sin preocuparse por el formato de almacenamiento.

*   **`services/inventory_service.py` (Capa de Servicios):**
    Aquí reside la lógica de negocio pura. Orquesta las operaciones (ej. registrar un producto), realiza validaciones y ejecuta cálculos (ej. precio final). Depende del repositorio para obtener y guardar datos, pero no sabe nada sobre la persistencia. Tampoco sabe cómo se muestran los datos al usuario. Esta capa es reutilizable y el núcleo funcional del sistema.

*   **`ui/console_ui.py` (Capa de Interfaz de Usuario):**
    Es responsable de toda la interacción con el usuario. Llama a la capa de servicios para obtener los datos que necesita y luego se encarga de formatearlos y presentarlos en la consola. Si en el futuro se deseara una interfaz web, solo habría que crear un nuevo módulo de UI que consuma los mismos servicios, sin tocar la lógica de negocio.

*   **`main.py` (Punto de Entrada):**
    Tras la refactorización, este archivo tiene un rol muy simple y claro: actuar como el "compositor" de la aplicación. Su única tarea es instanciar y conectar los diferentes componentes (Repositorio, Servicio, UI) en un proceso conocido como Inyección de Dependencias, y luego iniciar el flujo principal de la aplicación.

Esta separación de responsabilidades ataca directamente los problemas de **Rigidez**, **Inmovilidad** y **Opacidad** identificados en el análisis inicial, resultando en un sistema más robusto, flexible y fácil de mantener.

---
## 5. Conclusiones Finales

*   **Estimación de Deuda Técnica en el Código Original:** Se estima que el proyecto partió con un **70%** aproximadamente de deuda técnica, considerando el alto costo de modificación frente al bajo costo de desarrollo inicial.
*   **Impacto en la Metodología Ágil:** La alta deuda técnica es un lastre para la agilidad. Un código frágil y rígido como el analizado consume un tiempo desproporcionado en mantenimiento y adaptación, en lugar de dedicarlo a la creación de valor. En un contexto ágil como Scrum, esto se traduce en una velocidad de equipo (velocity) reducida e impredecible. Las estimaciones de las historias de usuario se vuelven poco fiables, lo que dificulta la planificación de los sprints y compromete la capacidad del equipo para entregar incrementos de software funcionales de manera sostenida.
