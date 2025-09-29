from django.db import models #import

class Categoria(models.Model):#class destinada a representar las categorias
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):#metodo que devuelve el nombre de la categoria
        return self.nombre

class Producto(models.Model):#clase que estructura los productos
    estado_choices = [#opciones para el estado del producto
        ('disponible', 'Disponible'),
        ('agotado', 'Agotado'),
        ('promocion', 'Promoción'),
        ('nuevo', 'Nuevo'),
        ('nada', 'Nada'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        null=True,      
        blank=True      
    )
    estado = models.CharField(max_length=20, choices=estado_choices, default='disponible')
    imagen = models.ImageField(upload_to='productos/media', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Comentarios(models.Model):
    nombre = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.nombre}"
    
class ConfiguracionComentarios(models.Model):
    max_comentarios = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Configuración: {self.max_comentarios} comentarios máximos"