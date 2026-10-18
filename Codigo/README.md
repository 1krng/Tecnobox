# Tecnobox — Sumativa 3 PRO205

## Requisitos
- Python 3.10 o superior
- pytest para ejecutar las pruebas

## Ejecutar
Desde esta carpeta:

```bash
python main.py
```

El programa crea/actualiza `inventario.json` para mantener el inventario entre ejecuciones.

## Pruebas
```bash
python -m pytest -v
```

## Estructura
- `gestor_defectuoso.py`: versión "antes", intencionalmente monolítica.
- `productos.py`: abstracción Producto y tipos concretos.
- `repositorios.py`: contrato de repositorio y persistencia JSON.
- `salidas.py`: abstracción de salida del ticket.
- `gestor_inventario.py`: coordinación de operaciones con dependencias inyectadas.
- `main.py`: ejecución de demostración.
- `test_inventario.py`: pruebas automatizadas.
