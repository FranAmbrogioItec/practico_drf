# Práctico DRF — Catálogo de Productos

Proyecto Django + Django REST Framework para gestionar un **catálogo de productos**
de una tienda. Se fue armando en tres entregas sucesivas:

## Primer práctico (Producto + Categoria)

- **Modelos**: `Producto` y `Categoria` (relación FK).
- **Serializers**: `ProductoSerializer` y `CategoriaSerializer` (con validaciones de precio/stock).
- **Vistas funcionales de CRUD** para `Producto` usando el decorador `@api_view`.

## Segundo práctico (agregado sobre el anterior)

- **Nuevo modelo relacionado**: `Resena` (reseña de un cliente sobre un producto),
  con relación **Foreign Key** hacia `Producto` (`related_name="resenas"`).
- **Serializers anidados**: `ProductoDetailSerializer` incluye la lista completa de
  reseñas de ese producto (relación inversa de la FK) en el detalle
  (`GET /api/productos/<id>/`).
- Vistas de CRUD para `Resena` con Concrete Generic Views (`ListCreateAPIView` /
  `RetrieveUpdateDestroyAPIView`) — **reemplazadas en el tercer práctico**.

## Tercer práctico (agregado sobre el anterior)

- **ViewSets en reemplazo de las Concrete Generic Views**:
  - `CategoriaViewSet` (`ReadOnlyModelViewSet`): solo expone `list()` y
    `retrieve()`. Las categorías ahora se gestionan desde `/admin/`; la API
    pública solo permite consultarlas, no crearlas/editarlas/borrarlas
    (`POST/PUT/PATCH/DELETE` devuelven `405 Method Not Allowed`). Reemplaza las
    vistas funcionales de Categoria del primer práctico.
  - `ResenaViewSet` (`ModelViewSet`): CRUD completo (list, retrieve, create,
    update, partial_update, destroy) con mucho menos código que las generics
    anteriores. Reemplaza `ResenaListCreateView` / `ResenaDetailView` del
    segundo práctico.
- **Enrutamiento con router**: ambos ViewSets se registran en
  `catalogo/routers.py` con un `DefaultRouter`, que genera solo todas las
  rutas necesarias.
- **`permission_classes` por viewset**:
  - `CategoriaViewSet` → `AllowAny` (lectura pública, no hay escritura).
  - `ResenaViewSet` → `IsAuthenticatedOrReadOnly` (cualquiera puede leer;
    crear/editar/borrar requiere estar autenticado).
  - Las vistas funcionales de `Producto` (`@api_view`) también fueron
    actualizadas: `GET` es público, `POST/PUT/PATCH/DELETE` devuelven
    `401 Unauthorized` sin un token válido.
- **Autenticación con `djangorestframework-simplejwt`** (JWT) como método
  principal, más `SessionAuthentication` de DRF como método opcional (para
  poder loguearse y probar desde la interfaz navegable de DRF con el usuario
  de `/admin/`, vía `/api-auth/login/`).

## Estructura

```
tienda_drf/
├── config/                # Configuración del proyecto (settings, urls)
│   ├── settings.py         # INSTALLED_APPS, REST_FRAMEWORK, SIMPLE_JWT
│   └── urls.py             # incluye catalogo.urls + endpoints de JWT
├── catalogo/               # App con modelos, serializers, vistas, router
│   ├── models.py            # Categoria, Producto, Resena
│   ├── serializers.py       # incluye los serializers anidados
│   ├── views.py             # @api_view (Producto) + ViewSets (Categoria, Resena)
│   ├── routers.py           # DefaultRouter con los ViewSets registrados
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
python manage.py createsuperuser  # necesario para poder pedir un token JWT
python manage.py runserver
```

### Alternativa: con `venv` + `pip`

```bash
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La API queda disponible en `http://localhost:8000/api/`.

## Autenticación (JWT)

1. Pedir un par de tokens con las credenciales del superusuario:

   ```bash
   curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "tu_contraseña"}'
   ```

   Devuelve `{"refresh": "...", "access": "..."}`.

2. Usar el `access` token en el header `Authorization` de cada request que
   necesite autenticación:

   ```bash
   curl -X POST http://localhost:8000/api/productos/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <access_token>" \
     -d '{"nombre": "Auriculares", "precio": "25000.00", "stock": 10}'
   ```

3. Cuando el `access` token expira (30 min), se renueva sin volver a loguearse:

   ```bash
   curl -X POST http://localhost:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "<refresh_token>"}'
   ```

También se puede usar `SessionAuthentication`: entrando a
`http://localhost:8000/api-auth/login/` con el usuario de `/admin/`, la
interfaz navegable de DRF (y Postman con las cookies del navegador) queda
autenticada por sesión.

## Endpoints

### Productos (vistas funcionales — `@api_view`)

| Método | URL                                | Auth requerida | Descripción                                          |
|--------|-------------------------------------|:--------------:|--------------------------------------------------------|
| GET    | `/api/productos/`                  | No             | Lista todos los productos                              |
| GET    | `/api/productos/?categoria=1`      | No             | Filtra productos por categoría                          |
| GET    | `/api/productos/?disponible=true`  | No             | Filtra productos disponibles                            |
| POST   | `/api/productos/`                  | **Sí**         | Crea un producto                                        |
| GET    | `/api/productos/<id>/`             | No             | Detalle de un producto (incluye reseñas anidadas)       |
| PUT    | `/api/productos/<id>/`             | **Sí**         | Actualiza (completo) un producto                        |
| PATCH  | `/api/productos/<id>/`             | **Sí**         | Actualiza parcialmente un producto                      |
| DELETE | `/api/productos/<id>/`             | **Sí**         | Elimina un producto                                     |

### Categorías (`CategoriaViewSet` — `ReadOnlyModelViewSet`)

| Método | URL                          | Auth requerida | Descripción                     |
|--------|-------------------------------|:--------------:|-----------------------------------|
| GET    | `/api/categorias/`           | No             | Lista todas las categorías         |
| GET    | `/api/categorias/<id>/`      | No             | Detalle de una categoría           |
| POST/PUT/PATCH/DELETE | `/api/categorias/...` | —      | **405 Method Not Allowed** (de solo lectura) |

### Reseñas (`ResenaViewSet` — `ModelViewSet`)

| Método | URL                              | Auth requerida | Descripción                                  |
|--------|-----------------------------------|:--------------:|-----------------------------------------------|
| GET    | `/api/resenas/`                  | No             | Lista todas las reseñas                        |
| GET    | `/api/resenas/?producto=1`       | No             | Filtra reseñas de un producto puntual          |
| POST   | `/api/resenas/`                  | **Sí**         | Crea una reseña (`producto`, `autor`, `calificacion` 1-5) |
| GET    | `/api/resenas/<id>/`             | No             | Detalle de una reseña                          |
| PUT    | `/api/resenas/<id>/`             | **Sí**         | Actualiza (completo) una reseña                |
| PATCH  | `/api/resenas/<id>/`             | **Sí**         | Actualiza parcialmente una reseña              |
| DELETE | `/api/resenas/<id>/`             | **Sí**         | Elimina una reseña                             |

### Autenticación (simplejwt)

| Método | URL                      | Descripción                                  |
|--------|---------------------------|-----------------------------------------------|
| POST   | `/api/token/`             | Login: devuelve `access` + `refresh` token    |
| POST   | `/api/token/refresh/`     | Renueva el `access` token con el `refresh`    |
| POST   | `/api/token/verify/`      | Verifica si un token sigue siendo válido      |
| GET/POST | `/api-auth/login/` `/api-auth/logout/` | Login/logout de sesión (SessionAuthentication) |

## Ejemplos de bodies

**Login (POST /api/token/):**
```json
{
  "username": "admin",
  "password": "tu_contraseña"
}
```

**Crear un producto (POST /api/productos/, requiere header Authorization):**
```json
{
  "nombre": "Auriculares Bluetooth",
  "descripcion": "Cancelación de ruido, 20hs de batería",
  "precio": "25000.00",
  "stock": 10,
  "categoria": 1
}
```

**Crear una reseña (POST /api/resenas/, requiere header Authorization):**
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
# 1. Login
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu_contraseña"}'

# 2. Guardar el access token en una variable y usarlo
ACCESS="<pegar el access token acá>"

curl -X POST http://localhost:8000/api/productos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS" \
  -d '{"nombre": "Auriculares", "precio": "25000.00", "stock": 10}'

curl http://localhost:8000/api/productos/
curl http://localhost:8000/api/categorias/
```

También se puede probar con **Postman** (hay una colección lista en
`postman/tienda_drf.postman_collection.json`, con las requests de login y
refresh incluidas), **Bruno** o **ThunderClient**.

## Autores

- Francisco Ambrogio
- Nicolas Lacroix
