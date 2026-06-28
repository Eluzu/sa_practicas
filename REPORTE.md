# Reporte de Deuda Técnica y Adaptabilidad del Software

**Asignatura:** Sistemas Ágiles

**Integrantes del grupo:** 
* Jose Daniel Luzuriaga (Jefe de grupo)
* Samara Puga
* Marcia Guerrero
* Jaqueline Anrango
* William Males

**Fecha:** 25 de Junio del 2026

---
## 1. Diagnóstico de Calidad (Código Legacy)

Identifiquen y describan brevemente los 3 principales problemas de diseño encontrados en el archivo `main.py` utilizando los conceptos de calidad de código vistos en clase:
1. **Rigidez:** El sistema es extremadamente rígido. Un cambio en una regla de negocio, como la tasa de IVA, obliga a modificar el código en múltiples lugares. Esto se evidenció al cambiar el IVA para "Tecnología", lo que requirió alterar la lógica de cálculo tanto en la sección de registro de productos (`op == 1`) como en la de reportes (`op == 3`). El código se resiste al cambio.

2. **Inmovilidad:** La lógica de negocio es inmóvil y no se puede reutilizar. La función `p_pro` es una "God Function" que mezcla validación, cálculo de impuestos, descuentos, acceso a datos y presentación. Es imposible reutilizar solo la lógica de cálculo de impuestos en otro contexto sin arrastrar toda la función y su acoplamiento con la consola y el sistema de archivos.

3. **Fragilidad y Opacidad:** El código es frágil porque cualquier cambio inesperado en el formato del archivo de datos (ej. una coma extra en el `.txt` original) rompería el programa. Además, es opaco debido a nombres de variables crípticos (`p_pro`, `A`, `l`, `x1`, `p1`) que no revelan su intención, haciendo que el código sea muy difícil de entender y mantener.
---
## 2. Mapeo de Dificultades para la Evolución (Evidencia Git)

Expliquen qué sucedió cuando intentaron aplicar los cambios solicitados por el docente en cada uno de los commits. Justifiquen el impacto técnico basándose en cuántas funciones o líneas de código se vieron afectadas.
1. ### Commit: `Tarea 2`
* **Impacto encontrado:** El cambio del IVA para "Tecnología" al 12% fue más complejo de lo necesario debido a la **duplicación de código**. La lógica de cálculo de IVA estaba presente tanto en la sección de registro (`op == 1`) como en la de reporte (`op == 3`). Esto nos obligó a modificar **2 bloques de código distintos** para aplicar una sola regla de negocio, aumentando el riesgo de inconsistencias.
2. ### Commit: `Tarea 3`
* **Impacto encontrado:** Cambiar el formato de persistencia de `.txt` a `.json` tuvo un impacto masivo. El código estaba **fuertemente acoplado** al formato de texto plano. Se tuvieron que reescribir por completo las secciones de escritura (`op == 1`), lectura (`op == 2`) y reporte (`op == 3`), afectando a más del 50% de la función `p_pro`. La lógica de negocio estaba mezclada con la lógica de acceso a datos, impidiendo un cambio limpio.
3. ### Commit: `Tarea 4`
* **Impacto encontrado:** Agregar el campo `codigo_barras` generó una fricción notable. Obligó a cambiar la firma de la función `p_pro`, la lógica de validación, la estructura del objeto a guardar y el formato de la tabla de listado. Además, se tuvo que usar `prod.get()` para no romper la compatibilidad con datos antiguos, evidenciando la fragilidad del sistema ante cambios en el esquema de datos.
---
## 3. Propuesta de Refactorización Inicial
Si tuvieran que rediseñar este módulo en la siguiente clase utilizando principios de **Código Limpio (Clean Code)**, enumeren qué 3 acciones principales tomarían para eliminar la deuda técnica de este sistema:
1. **Aplicar el Principio de Responsabilidad Única (SRP):** Refactorizar la función monolítica `p_pro` en funciones más pequeñas y enfocadas: una para leer los datos (`leer_inventario`), otra para escribirlos (`guardar_inventario`), una para la lógica de negocio (`calcular_precio_final`) y otras para las operaciones de la interfaz de usuario.

2. **Eliminar "Valores Mágicos" y Duplicación (DRY):** Centralizar las reglas de negocio. Crear constantes o un diccionario de configuración para las tasas de IVA (general y por categoría) y los descuentos. Crear una única función de cálculo de impuestos que sea llamada desde donde se necesite, en lugar de duplicar la lógica.

3. **Desacoplar la Lógica de la Persistencia:** Crear una "capa de datos" o repositorio. La lógica de negocio no debería saber si los datos se guardan en JSON, TXT o una base de datos. Debería simplemente llamar a funciones como `obtener_producto()` o `guardar_producto()`, encapsulando completamente la manipulación de archivos.
---
## 4. Conclusiones del Equipo
* **Porcentaje estimado de deuda técnica en el script original (0% al 100%):** [**85%**]

* **Reflexión ágil:** Un software con alta deuda técnica es como correr con una mochila llena de piedras. Cada sprint, agregar nuevas funcionalidades o adaptar las existentes (cambios) se vuelve más lento y costoso porque los desarrolladores pasan más tiempo luchando contra la complejidad y el riesgo de romper algo, que entregando valor real al cliente.