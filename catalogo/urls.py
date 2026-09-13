from django.urls import path
from . import views

urlpatterns = [
    path("productos/", views.producto_list, name="producto-list"),
    path("productos/<int:pk>/", views.producto_detail, name="producto-detail"),
    path("categorias/", views.categoria_list, name="categoria-list"),
    path("categorias/<int:pk>/", views.categoria_detail, name="categoria-detail"),
    path("resenas/", views.ResenaListCreateView.as_view(), name="resena-list"),
    path("resenas/<int:pk>/", views.ResenaDetailView.as_view(), name="resena-detail"),
]
