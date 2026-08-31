from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer


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
        serializer = ProductoSerializer(producto)
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
