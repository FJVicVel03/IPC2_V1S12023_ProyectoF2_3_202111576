"""
URL configuration for GestionCine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Usuarios.views import login, vista_peliculas
from Usuarios.views import pagina_administrador, eliminar_pelicula
from Usuarios.views import pagina_cliente, modificar_categoria, modificar_peliculas, eliminar_categoria
from Usuarios.views import mostrar_peliculas, cargar_peliculas, gestionar_peliculas, agregar_categoria, agregar_pelicula
from Usuarios.views import gestionar_usuarios, crear_usuario, mostrar_usuarios, cargar_xml, modificar_usuario, eliminar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('administrador/', pagina_administrador, name='administrador'),
    path('cliente/', pagina_cliente , name='cliente'),
    path('peliculas/',mostrar_peliculas, name='mostrar_peliculas'),
    path('gestionar_usuarios/', gestionar_usuarios, name="gestionar_usuarios"),
    path('gestionar_peliculas/', gestionar_peliculas, name = 'gestionar_peliculas'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('mostrar_usuarios/', mostrar_usuarios, name='mostrar_usuarios'),
    path('cargar_xml/',cargar_xml, name='cargar_xml'), 
    path('modificar_usuario/', modificar_usuario, name='modificar_usuario'),
    path('eliminar_usuario/', eliminar_usuario, name='eliminar_usuario'),
    path('cargar_peliculas/', cargar_peliculas, name='cargar_peliculas' ),
    path('agregar_categorias/', agregar_categoria, name='agregar_categoria'),
    path('agregar_pelicula/', agregar_pelicula, name='agregar_pelicula'),
    path('modificar_categoria/', modificar_categoria, name="modificar_categoria"),
    path('modificar_peliculas/', modificar_peliculas, name='modificar_peliculas'),
    path('eliminar_categoria/', eliminar_categoria, name="eliminar_categoria"),
    path('eliminar_pelicula/', eliminar_pelicula, name="eliminar_pelicula"),
    path('vista_peliculas/', vista_peliculas, name='vista_peliculas'),
]