# REPORTE DE CALIDAD DEL CÓDIGO

## Diagnóstico

Se realizaron mejoras al sistema de inventario aplicando principios de código limpio. Las funciones mantienen una única responsabilidad, se utilizaron nombres descriptivos y se incorporaron nuevos requerimientos sin modificar el propósito general del programa.

## Mapeo de dificultades

| Requerimiento | Dificultad | Líneas modificadas |
|---------------|------------|--------------------|
| Alerta de stock menor a 5 | Baja | 3 |
| IVA del 12% para Tecnología | Media | 10 |
| Cambio de TXT a JSON | Alta | 25 |
| Agregar código de barras | Media | 10 |
| Elaboración del reporte | Baja | Archivo nuevo |

## Propuesta ágil de refactorización

Para mejorar el mantenimiento y facilitar futuras modificaciones, se propone dividir el proyecto en varios módulos:

- `main.py`: punto de entrada del programa.
- `producto.py`: definición de la clase `Producto`.
- `inventario.py`: funciones para registrar, leer y listar productos.
- `impuestos.py`: cálculo de IVA y precio final.
- `persistencia.py`: lectura y escritura de archivos JSON.

Esta organización sigue el principio de responsabilidad única, facilita las pruebas y hace que el código sea más fácil de mantener.