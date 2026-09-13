from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics

from .models import Producto, Categoria, Resena
from .serializers import (
    ProductoSerializer,
    ProductoDetailSerializer,
    CategoriaSerializer,
    ResenaSerializer,
)


# ---------- PRODUCTOS ----------

@api_view(["GET", "POST"])
def producto_list(request):
    """
    GET  -> Lista todos los productos (soporta ?categoria=<id> y ?disponible=true/false)
    POST -> Crea un nuevo producto
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
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def producto_detail(request, pk):
    """
    GET    -> Obtiene un producto puntual
    PUT    -> Actualiza (todos los campos) un producto
    PATCH  -> Actualiza parcialmente un producto
    DELETE -> Elimina un producto
    """
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(
            {"detail": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        # Usamos el serializer con reseñas anidadas solo en el detalle,
        # para no sobrecargar el listado con datos que no siempre hacen falta.
        serializer = ProductoDetailSerializer(producto)
        return Response(serializer.data)

    elif request.method == "PUT":
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


# ---------- CATEGORIAS ----------

@api_view(["GET", "POST"])
def categoria_list(request):
    """
    GET  -> Lista todas las categorías
    POST -> Crea una nueva categoría
    """
    if request.method == "GET":
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def categoria_detail(request, pk):
    """
    GET    -> Obtiene una categoría puntual
    PUT    -> Actualiza una categoría
    PATCH  -> Actualiza parcialmente una categoría
    DELETE -> Elimina una categoría
    """
    try:
        categoria = Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return Response(
            {"detail": "Categoría no encontrada."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = CategoriaSerializer(categoria, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- RESEÑAS (Class-Based Views genéricas) ----------
#
# A diferencia de Producto/Categoria (vistas funcionales con @api_view,
# práctico anterior), acá usamos Generic API Views: DRF ya resuelve el
# GET/POST y GET/PUT/PATCH/DELETE con muy poco código, delegando en
# queryset + serializer_class.

class ResenaListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/resenas/            -> lista todas las reseñas
    GET  /api/resenas/?producto=1 -> lista las reseñas de un producto puntual
    POST /api/resenas/            -> crea una reseña nueva
    """
    serializer_class = ResenaSerializer

    def get_queryset(self):
        queryset = Resena.objects.all()
        producto_id = self.request.query_params.get("producto")
        if producto_id:
            queryset = queryset.filter(producto_id=producto_id)
        return queryset


class ResenaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/resenas/<id>/ -> detalle de una reseña
    PUT    /api/resenas/<id>/ -> actualiza (completo)
    PATCH  /api/resenas/<id>/ -> actualiza parcialmente
    DELETE /api/resenas/<id>/ -> elimina
    """
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
