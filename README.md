# sa_practicas
Ejemplos prácticos de sistemas ágiles

Estudiante:
Marcia Guerrero

Diagnostico de calidad del código:
El sistema está centralizado en una única función p_pro(op, c_b, x, p, c, t) que controla todas las 
operaciones del inventario (registro, listado y reportes).

Fortalezas:
- Estructura simple y fácil de ejecutar
- Flujo lógico claro por medio de op (1, 2, 3)
- Integración completa con JSON
Debilidades:
- Alto acoplamiento (todo depende de una sola función)
- Baja modularidad
- Difícil mantenimiento a largo plazo

Mapero de dificultades:
1. Alerta de stock bajo: Se modifico la seccion de listado de productos para incluir una validación:
                         Si stock < 5, se imprime mensaje de alerta en consola.
Se modifico las lineas de codigo de op == 2.
Las dificultades se encuentran en integrar una validación sin roper el formato de impresión, mantener la 
estructura de salida tabular y evitar que la alerta afecte al flujo de datos.

2. Cambio de IVA para categiria Tecnologia: Se modifico la logica de calculo de impuestos.
                         Antes: IVA fijo de 15%
                         Despues: 12% solo para tecnologia, 15% para el resto.
Se modigico las lineas de codigo relacionadas con el IVA en registro y reporte.
Las dificultades encontradas fueron el asegurar coherencia entre el cálculo de registro y el cálculo de 
reporte. Ademas, habia que evitar la inconsistencia de doble cálculo del IVA. 

3. Cambiar a almacenamiento .json: Se reemplazo completamente el sistema de persistecia al eliminar el 
archivo .txt e implementar el .json. Se uso json.load() y json.dum().
Se modifico varias lineas de codigo.
Las dificultades encontradas fueron el manejo de JSONDecodeError, la reestructuración completa del modelo
de datos, la adaptación de todas las operaciones a formato estructurado y la depuración de errores de lectura
inical vacía.

4. Codigo de barras: Se añadio un nuevo atributo obligatorio de codigo de barras en los productors. Se 
modifico la estructura del JSON, la firma de función y la impresión del listado. 
Se cambio las lineas de codigo relacionadas con la función, la visualización y la llamada de datos. 
Las dificultades encontradas fueron los errores de ejecución por parámetros faltantes (TypeError), la 
actualización obligatoria de todas las llamadas a la función y el desalineación temporal entre versiones 
del código. 

Propuesta de refactorización: 
La propuesta de refactorización ágil busca transformar el sistema de inventario actual en una 
arquitectura más modular, mantenible y escalable, aplicando principios de desarrollo iterativo. 
Actualmente el sistema presenta una función monolítica con alta responsabilidad, lógica duplicada y 
fuerte acoplamiento entre procesos, lo que dificulta su mantenimiento y evolución. A través de sprints 
progresivos se plantea separar responsabilidades en módulos, introducir programación orientada a objetos, 
centralizar reglas de negocio como el cálculo del IVA y mejorar la gestión de la persistencia de datos en 
JSON.

Con esta estrategia se espera reducir la complejidad del código, mejorar su legibilidad y facilitar la 
incorporación de nuevas funcionalidades sin afectar el sistema completo. Además, el enfoque ágil permite 
realizar mejoras incrementales y controladas, asegurando estabilidad en cada etapa del desarrollo. En 
conjunto, la refactorización no solo optimiza el rendimiento del sistema, sino que también eleva la calidad 
del software y su capacidad de adaptación a futuros requerimientos.
