"""
Enrutamiento automático para los ViewSets de la app catalogo.

DefaultRouter genera solo, a partir de cada ViewSet registrado, todas las
rutas de list/retrieve/create/update/partial_update/destroy que correspondan
según el tipo de ViewSet (ReadOnlyModelViewSet -> solo list/retrieve;
ModelViewSet -> el CRUD completo), además de una vista raíz de la API.
"""
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ResenaViewSet

router = DefaultRouter()
router.register(r"categorias", CategoriaViewSet, basename="categoria-viewset")
router.register(r"resenas", ResenaViewSet, basename="resena-viewset")

urlpatterns = router.urls
