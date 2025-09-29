from django.shortcuts import render, redirect
from .models import Producto, Categoria, Comentarios, ConfiguracionComentarios
from .form import ConfiguracionComentariosForm, ProductoForm, CategoriaForm, ComentarioForm
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404


def lista_comentarios(request):
    comentarios = Comentarios.objects.all().order_by('-fecha_creacion')
    comentario_form = ComentarioForm()

    # Form para el modal de máximo comentarios
    config = ConfiguracionComentarios.objects.first()
    if not config:
        config = ConfiguracionComentarios.objects.create(max_comentarios=100)
    max_form = ConfiguracionComentariosForm(instance=config)

    return render(request, 'admin/comentarios.html', {
        'comentarios': comentarios,
        'comentario_form': comentario_form,
        'form': comentario_form,  # ya tenías este para agregar comentario
        'max_form': max_form      # nuevo form para el modal
    })


@user_passes_test(lambda u: u.is_superuser)
def gestion_productos(request):
    productos = Producto.objects.select_related('categoria').all()  # Optimiza consultas
    producto_form = ProductoForm()
    categoria_form = CategoriaForm()
    categorias = Categoria.objects.all()
    producto_forms = {p.id: ProductoForm(instance=p) for p in productos}
    comentario_form = ComentarioForm()
    comentarios = Comentarios.objects.all().order_by('-fecha_creacion')

    return render(request, 'admin/gestion.html', {
        'productos': productos,
        'producto_form': producto_form,
        'categoria_form': categoria_form,
        'producto_forms': producto_forms,
        'comentario_form': comentario_form,
        'comentarios': comentarios,
        'categorias': categorias
    })


@user_passes_test(lambda u: u.is_superuser)
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('gestion_productos')


@user_passes_test(lambda u: u.is_superuser)
def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('gestion_productos')



@user_passes_test(lambda u: u.is_superuser)
def eliminar_producto(request, producto_id):
    if request.method == 'POST':
        try:
            producto = get_object_or_404(Producto, id=producto_id)
            producto.delete()
        except Producto.DoesNotExist:
            raise Http404("Producto no encontrado")
    return redirect('gestion_productos')


@user_passes_test(lambda u: u.is_superuser)
def eliminar_categoria(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            categoria.delete()
        except Categoria.DoesNotExist:
            raise Http404("Categoría no encontrada")
    return redirect('gestion_productos')


@user_passes_test(lambda u: u.is_superuser)
def editar_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')
    except Producto.DoesNotExist:
        raise Http404("Producto no encontrado")

    return render(request, 'admin/gestion.html', {'form': form, 'producto': producto})

def ingresar_comentario(request):
    comentarios = Comentarios.objects.all().order_by('-fecha_creacion')

    config = ConfiguracionComentarios.objects.first()
    if not config:
        config = ConfiguracionComentarios.objects.create(max_comentarios=100)
    max_form = ConfiguracionComentariosForm(instance=config)

    max_comentarios = config.max_comentarios
    comentarios_conteo = Comentarios.objects.count()
    error = None

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if comentarios_conteo >= max_comentarios:
            error = f"⚠️ Se ha alcanzado el límite máximo de {max_comentarios} comentarios."
        elif form.is_valid():
            form.save()
            return redirect('lista_comentarios')
    else:
        form = ComentarioForm()

    return render(request, 'admin/comentarios.html', {
        'comentarios': comentarios,
        'form': form,
        'max_form': max_form,
        'error': error
    })



@user_passes_test(lambda u: u.is_superuser)
def eliminar_comentario(request, comentario_id):
    if request.method == 'POST':
        try:
            comentario = Comentarios.objects.get(id=comentario_id)
            comentario.delete()
        except Comentarios.DoesNotExist:
            raise Http404("Comentario no encontrado")
    return redirect('lista_comentarios')

@user_passes_test(lambda u: u.is_superuser)
def configurar_max_comentario(request):
    config = ConfiguracionComentarios.objects.first()
    if not config:
        config = ConfiguracionComentarios.objects.create(max_comentarios=100)

    if request.method == 'POST':
        form = ConfiguracionComentariosForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('lista_comentarios')
    else:
        form = ConfiguracionComentariosForm(instance=config)

    return render(request, 'admin/configurar_max_comentarios.html', {'form': form})

def prueba_navbar(request):
    return render(request, 'base/navbarBase.html')

def prueba_main(request):
    categorias = Categoria.objects.prefetch_related('producto_set').all()
    comentarios = Comentarios.objects.all().order_by('-fecha_creacion')  # 👈 aquí
    form = ComentarioForm()
    return render(request, 'base/main.html', {
        'categorias': categorias,
        'comentarios': comentarios,
        'form': form
    })

def ingresar_comentario_main(request):
    if request.method == "POST":
        form = ComentarioForm(request.POST)

        # Traemos configuración
        config = ConfiguracionComentarios.objects.first()
        if not config:
            config = ConfiguracionComentarios.objects.create(max_comentarios=100)
        max_comentarios = config.max_comentarios
        comentarios_conteo = Comentarios.objects.count()

        if comentarios_conteo >= max_comentarios:
            # Ya está lleno
            categorias = Categoria.objects.prefetch_related('producto_set').all()
            comentarios = Comentarios.objects.all().order_by('-fecha_creacion')
            return render(request, 'base/main.html', {
                'categorias': categorias,
                'comentarios': comentarios,
                'form': form,
                'error': f"⚠️ Se ha alcanzado el límite máximo de {max_comentarios} comentarios."
            })

        elif form.is_valid():
            form.save()
            return redirect('prueba_main')
        else:
            print("❌ Errores en el formulario:", form.errors)  
            categorias = Categoria.objects.prefetch_related('producto_set').all()
            comentarios = Comentarios.objects.all().order_by('-fecha_creacion')
            return render(request, 'base/main.html', {
                'categorias': categorias,
                'comentarios': comentarios,
                'form': form,
                'error': 'Por favor corrige los errores.'
            })

    return redirect('prueba_main')
