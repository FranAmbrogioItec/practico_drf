from rest_framework import serializers
from .models import Categoria, Producto, Resena


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]


# ---------- RESEÑAS ----------

class ResenaSerializer(serializers.ModelSerializer):
    """
    Serializer "plano" de Resena: se usa para crear/listar/editar reseñas
    directamente desde /api/resenas/. Expone el producto como PK (para poder
    asignarlo al crear) y además su nombre de solo lectura.
    """
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)

    class Meta:
        model = Resena
        fields = [
            "id",
            "producto",
            "producto_nombre",
            "autor",
            "comentario",
            "calificacion",
            "creado",
        ]
        read_only_fields = ["creado"]

    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5.")
        return value


class ResenaNestedSerializer(serializers.ModelSerializer):
    """
    Serializer anidado de Resena: se usa DENTRO de ProductoDetailSerializer.
    """
    class Meta:
        model = Resena
        fields = ["id", "autor", "comentario", "calificacion", "creado"]
        read_only_fields = ["creado"]


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer liviano de Producto, para listar y para crear/editar.
    """
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    cantidad_resenas = serializers.IntegerField(source="resenas.count", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id",
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "categoria",
            "categoria_nombre",
            "disponible",
            "cantidad_resenas",
            "creado",
            "actualizado",
        ]
        read_only_fields = ["creado", "actualizado"]

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value


class ProductoDetailSerializer(ProductoSerializer):
    """
    Serializer de Producto con SERIALIZERS ANIDADOS: incluye la lista completa
    de reseñas del producto (relación inversa de la FK).
    """
    resenas = ResenaNestedSerializer(many=True, read_only=True)

    class Meta(ProductoSerializer.Meta):
        fields = ProductoSerializer.Meta.fields + ["resenas"]
