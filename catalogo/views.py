from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from .models import Producto, Categoria, Resena
from .serializers import (
    ProductoSerializer,
    ProductoDetailSerializer,
    CategoriaSerializer,
    ResenaSerializer,
)


# ---------- PRODUCTOS (vistas funcionales, práctico 1) ----------

@api_view(["GET", "POST"])
def producto_list(request):
    """
    GET  -> Lista todos los productos (soporta ?categoria=<id> y ?disponible=true/false)
    POST -> Crea un nuevo producto (requiere estar autenticado)
    """
    if request.method == "GET":
        productos = Producto.objects.all()

        categoria_id = request.query_params.get("categoria")
        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)

        disponible = request.query_params.get("disponible")
        if disponible is not None:
            valor = disponible.lower() in ("true", "1")
            productos = productos.filter(disponible=valor)

        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Se requiere autenticación para crear productos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def producto_detail(request, pk):
    """
    GET    -> Obtiene un producto puntual (público)
    PUT    -> Actualiza (todos los campos) un producto (requiere autenticación)
    PATCH  -> Actualiza parcialmente un producto (requiere autenticación)
    DELETE -> Elimina un producto (requiere autenticación)
    """
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(
            {"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = ProductoDetailSerializer(producto)
        return Response(serializer.data)

    if not request.user or not request.user.is_authenticated:
        return Response(
            {"detail": "Se requiere autenticación para modificar productos."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if request.method == "PUT":
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- CATEGORIAS Y RESEÑAS (ViewSets, práctico 3) ----------
#
# En el práctico 1, Categoria tenía vistas funcionales de CRUD completo.
# En el práctico 2, Resena tenía vistas basadas en clases "concrete generic"
# (ListCreateAPIView / RetrieveUpdateDestroyAPIView).
#
# Ahora reemplazamos esas dos por ViewSets registrados en un router:
#
#   - CategoriaViewSet: ReadOnlyModelViewSet -> solo lectura desde la API
#     (list + retrieve). Las categorías se gestionan desde /admin/; tiene
#     sentido que la API pública solo permita consultarlas, no alterarlas.
#
#   - ResenaViewSet: ModelViewSet -> CRUD completo (list, retrieve, create,
#     update, partial_update, destroy), igual que antes pero con MUCHO menos
#     código gracias al ViewSet.

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet: solo expone list() y retrieve().
    GET /api/categorias/        -> lista
    GET /api/categorias/<id>/   -> detalle
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]


class ResenaViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet: expone el CRUD completo (list, retrieve, create, update,
    partial_update, destroy) automáticamente.

    Permisos: lectura libre para cualquiera, escritura (POST/PUT/PATCH/DELETE)
    solo para usuarios autenticados (JWT o sesión de Django).
    """
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Resena.objects.all()
        producto_id = self.request.query_params.get("producto")
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        return queryset
