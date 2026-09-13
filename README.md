# Práctico DRF — Catálogo de Productos

Proyecto Django + Django REST Framework para gestionar un **catálogo de productos**
de una tienda.

## Primer práctico (Producto + Categoria)

- **Modelos**: `Producto` y `Categoria` (relación FK).
- **Serializers**: `ProductoSerializer` y `CategoriaSerializer` (con validaciones de precio/stock).
- **Vistas funcionales de CRUD** usando el decorador `@api_view`.

## Segundo práctico

- **Nuevo modelo relacionado**: `Resena` (reseña de un cliente sobre un producto),
  con relación **Foreign Key** hacia `Producto` (`related_name="resenas"`): un producto
  puede tener muchas reseñas.
- **Serializers anidados**:
  - `ProductoDetailSerializer` incluye la lista completa de reseñas de ese producto
    (anidamiento hacia "adentro", relación inversa de la FK). Se usa en el detalle
    (`GET /api/productos/<id>/`).
  - `ResenaSerializer` expone el nombre del producto (`producto_nombre`) además del
    id, para no obligar a pedir el producto por separado.
- **Vistas de CRUD basadas en clases (Generic API Views)** para `Resena`:
  - `ResenaListCreateView` (`generics.ListCreateAPIView`)
  - `ResenaDetailView` (`generics.RetrieveUpdateDestroyAPIView`)

  A diferencia de `Producto`/`Categoria` (vistas funcionales, primer práctico),
  acá se usan class-based views genéricas, como permite la consigna
  ("cualquiera de las API Views basadas en clases").

## Estructura

```
tienda_drf/
├── config/            # Configuración del proyecto (settings, urls)
├── catalogo/          # App con modelos, serializers, vistas y urls
│   ├── models.py       # Categoria, Producto, Resena
│   ├── serializers.py  # incluye los serializers anidados
│   ├── views.py        # vistas funcionales (@api_view) + class-based (generics)
│   ├── urls.py
│   └── admin.py
├── postman/
│   └── tienda_drf.postman_collection.json
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

### Categorías

| Método | URL                          | Descripción                                |
|--------|------------------------------|---------------------------------------------|
| GET    | `/api/categorias/`           | Lista todas las categorías                  |
| POST   | `/api/categorias/`           | Crea una categoría                          |
| GET    | `/api/categorias/<id>/`      | Detalle de una categoría                    |
| PUT    | `/api/categorias/<id>/`      | Actualiza (completo) una categoría          |
| PATCH  | `/api/categorias/<id>/`      | Actualiza parcialmente una categoría        |
| DELETE | `/api/categorias/<id>/`      | Elimina una categoría                       |

### Productos

| Método | URL                                | Descripción                                          |
|--------|------------------------------------|-------------------------------------------------------|
| GET    | `/api/productos/`                  | Lista todos los productos                             |
| GET    | `/api/productos/?categoria=1`      | Filtra productos por categoría                         |
| GET    | `/api/productos/?disponible=true`  | Filtra productos disponibles                           |
| POST   | `/api/productos/`                  | Crea un producto                                       |
| GET    | `/api/productos/<id>/`             | Detalle de un producto **(incluye reseñas anidadas)**  |
| PUT    | `/api/productos/<id>/`             | Actualiza (completo) un producto                        |
| PATCH  | `/api/productos/<id>/`             | Actualiza parcialmente un producto                     |
| DELETE | `/api/productos/<id>/`             | Elimina un producto                                    |

### Reseñas (nuevo — class-based views)

| Método | URL                              | Descripción                                  |
|--------|-----------------------------------|-----------------------------------------------|
| GET    | `/api/resenas/`                  | Lista todas las reseñas                        |
| GET    | `/api/resenas/?producto=1`       | Filtra reseñas de un producto puntual          |
| POST   | `/api/resenas/`                  | Crea una reseña (requiere `producto`, `autor`, `calificacion` 1-5) |
| GET    | `/api/resenas/<id>/`             | Detalle de una reseña                          |
| PUT    | `/api/resenas/<id>/`             | Actualiza (completo) una reseña                |
| PATCH  | `/api/resenas/<id>/`             | Actualiza parcialmente una reseña              |
| DELETE | `/api/resenas/<id>/`             | Elimina una reseña                             |

## Ejemplos de bodies

**Crear un producto (POST /api/productos/):**
```json
{
  "nombre": "Auriculares Bluetooth",
  "descripcion": "Cancelación de ruido, 20hs de batería",
  "precio": "25000.00",
  "stock": 10,
  "categoria": 1
}
```

**Crear una reseña (POST /api/resenas/):**
```json
{
  "producto": 1,
  "autor": "Juan",
  "comentario": "Excelente calidad de sonido",
  "calificacion": 5
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

curl -X POST http://localhost:8000/api/resenas/ \
  -H "Content-Type: application/json" \
  -d '{"producto": 1, "autor": "Juan", "calificacion": 5}'

curl http://localhost:8000/api/productos/1/
```

También se puede probar con **Postman** (hay una colección lista en `postman/tienda_drf.postman_collection.json`),
**Bruno** o **ThunderClient**.

## Autores

- Francisco Ambrogio
- Nicolas Lacroix  


