from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
    )
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["-creado"]


class Resena(models.Model):
    """
    Reseña de un cliente sobre un producto.
    Relación Foreign Key: un Producto puede tener muchas Reseñas.
    """

    CALIFICACIONES = [
        (1, "1 - Muy malo"),
        (2, "2 - Malo"),
        (3, "3 - Regular"),
        (4, "4 - Bueno"),
        (5, "5 - Excelente"),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="resenas",
    )
    autor = models.CharField(max_length=100)
    comentario = models.TextField(blank=True)
    calificacion = models.PositiveSmallIntegerField(choices=CALIFICACIONES)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor} → {self.producto.nombre} ({self.calificacion}/5)"

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-creado"]
