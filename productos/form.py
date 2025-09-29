from django import forms
from .models import Producto, Categoria, Comentarios
from django.core.exceptions import ValidationError
from .models import ConfiguracionComentarios

PALABRAS_PROHIBIDAS = [
    'idiota', 'estúpido', 'imbécil', 'maldito', 'mierda',
    'cabron', 'puta', 'puto', 'perra', 'pendejo', 'zorra', 'joder',
    'coño', 'chingar', 'culero', 'maricón', 'gay', 'basura',
    'vagina', 'hijueputa', 'pene', 'malparidos', 'hijueputa', 
    'ijueputa', 'cojerme', 'carepicha', 'puchaina', 'verga', 'verg4',
    'pen4', 'fuck','culo','mamapichas', 'mamapich4s', 'anal', 'desgraciado'
]

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "categoria", "estado", "imagen"]
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'categoria': 'Categoría',
            'estado': 'Estado',
            'imagen': 'Imagen del producto'
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre"]
        labels = {
            'nombre': 'Nombre de la categoría',
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ["nombre", "contenido"]
        labels = {
            'nombre': 'Nombre',
            'contenido': 'Comentario',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Escribe tu nombre aquí...'}),
            'contenido': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu comentario aquí...'}),
        }

    def clean_contenido(self):
        contenido = self.cleaned_data.get("contenido", "")
        contenido_lower = contenido.lower()
        for palabra in PALABRAS_PROHIBIDAS:
            if palabra in contenido:
                raise ValidationError("El comentario contiene palabras prohibidas.")
        return contenido
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "")
        nombre_lower = nombre.lower()
        for palabra in PALABRAS_PROHIBIDAS:
            if palabra in nombre:
                raise ValidationError("El nombre contiene palabras prohibidas.")
        return nombre


class ConfiguracionComentariosForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionComentarios
        fields = ['max_comentarios']
        labels = {'max_comentarios': 'Cantidad máxima de comentarios'}
        widgets = {
            'max_comentarios': forms.NumberInput(attrs={'min': 1})
        }
