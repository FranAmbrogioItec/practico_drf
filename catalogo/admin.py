from django.contrib import admin
from .models import Categoria, Producto, Resena


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre"]
    search_fields = ["nombre"]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "precio", "stock", "categoria", "disponible"]
    list_filter = ["categoria", "disponible"]
    search_fields = ["nombre"]


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ["id", "producto", "autor", "calificacion", "creado"]
    list_filter = ["calificacion"]
    search_fields = ["autor", "comentario"]
