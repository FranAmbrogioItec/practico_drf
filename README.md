# Primer Práctico DRF — Catálogo de Productos

Proyecto Django + Django REST Framework para gestionar un **catálogo de productos**
de una tienda. Contiene:

- **Modelos**: `Producto` y `Categoria` (relación FK, para enriquecer el práctico).
- **Serializers**: `ProductoSerializer` y `CategoriaSerializer` (con validaciones de precio/stock).
- **Vistas funcionales de CRUD** usando el decorador `@api_view` (sin ViewSets ni generics),
  tal como pide la consigna.

## Estructura

```
tienda_drf/
├── config/            # Configuración del proyecto (settings, urls)
├── catalogo/          # App con modelo, serializers, vistas y urls
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── manage.py
├── requirements.txt
└── README.md
```

## Instalación y ejecución

### Opción recomendada: con `uv`

```bash
uv venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # opcional, para entrar al /admin/
python manage.py runserver
```

### Alternativa: con `venv` + `pip`

```bash
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

La API queda disponible en `http://localhost:8000/api/`.

## Endpoints

| Método | URL                          | Descripción                                |
|--------|------------------------------|---------------------------------------------|
| GET    | `/api/categorias/`           | Lista todas las categorías                  |
| POST   | `/api/categorias/`           | Crea una categoría                          |
| GET    | `/api/categorias/<id>/`      | Detalle de una categoría                    |
| PUT    | `/api/categorias/<id>/`      | Actualiza (completo) una categoría          |
| PATCH  | `/api/categorias/<id>/`      | Actualiza parcialmente una categoría        |
| DELETE | `/api/categorias/<id>/`      | Elimina una categoría                       |
| GET    | `/api/productos/`            | Lista todos los productos                   |
| GET    | `/api/productos/?categoria=1`| Filtra productos por categoría              |
| GET    | `/api/productos/?disponible=true` | Filtra productos disponibles           |
| POST   | `/api/productos/`            | Crea un producto                            |
| GET    | `/api/productos/<id>/`       | Detalle de un producto                      |
| PUT    | `/api/productos/<id>/`       | Actualiza (completo) un producto            |
| PATCH  | `/api/productos/<id>/`       | Actualiza parcialmente un producto          |
| DELETE | `/api/productos/<id>/`       | Elimina un producto                         |

## Ejemplo de body para crear un producto (POST)

```json
{
  "nombre": "Auriculares Bluetooth",
  "descripcion": "Cancelación de ruido, 20hs de batería",
  "precio": "25000.00",
  "stock": 10,
  "categoria": 1
}
```

## Pruebas rápidas con curl

```bash
curl -X POST http://localhost:8000/api/categorias/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Electrónica"}'

curl -X POST http://localhost:8000/api/productos/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Auriculares", "precio": "25000.00", "stock": 10, "categoria": 1}'

curl http://localhost:8000/api/productos/
```

También se puede probar con **Postman**, **Bruno** o **ThunderClient**.

## Autores

- Francisco Ambrogio
- Nicolas Lacroix