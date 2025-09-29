from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path('gestion-productos/', views.gestion_productos, name='gestion_productos'),
    path('', views.prueba_main, name='prueba_main'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('agregar-categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar-categoria/', views.eliminar_categoria, name='eliminar_categoria'),
    path('lista_comentarios/', views.lista_comentarios, name='lista_comentarios'),
    path('ingresar-comentario/', views.ingresar_comentario, name='ingresar_comentario'),
    path('eliminar-comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('prueba-navbar/', views.prueba_navbar, name='prueba_navbar'),
    path('configurar-max-comentario/', views.configurar_max_comentario, name='configurar_max_comentario'),
    path('ingresar-comentario-main/', views.ingresar_comentario_main, name='ingresar_comentario_main'),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)