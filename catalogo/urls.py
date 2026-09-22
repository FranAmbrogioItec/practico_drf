from django.urls import path, include
from . import views
from .routers import router

urlpatterns = [
    # Productos: vistas funcionales con @api_view (práctico 1, sin cambios)
    path("productos/", views.producto_list, name="producto-list"),
    path("productos/<int:pk>/", views.producto_detail, name="producto-detail"),

    # Categorias y Resenas: ViewSets registrados en un router (práctico 3)
    # genera automáticamente:
    #   GET  /api/categorias/            (list, ReadOnlyModelViewSet)
    #   GET  /api/categorias/<id>/       (retrieve, ReadOnlyModelViewSet)
    #   GET/POST            /api/resenas/       (list/create, ModelViewSet)
    #   GET/PUT/PATCH/DELETE /api/resenas/<id>/ (retrieve/update/destroy, ModelViewSet)
    path("", include(router.urls)),
]
