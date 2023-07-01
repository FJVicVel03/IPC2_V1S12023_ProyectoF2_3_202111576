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
from Usuarios.views import login, vista_peliculas, pagina_login
from Usuarios.views import pagina_administrador, eliminar_sala, eliminar_tarjeta
from Usuarios.views import pagina_cliente, crear_pelicula, cargar_peliculas_xml, eliminar_categoria, eliminar_pelicula, modificar_pelicula
from Usuarios.views import mostrar_peliculas, cargar_peliculas, gestionar_peliculas, modificar_categoria
from Usuarios.views import gestionar_usuarios, crear_usuario, mostrar_usuarios, cargar_xml, modificar_usuario, eliminar_usuario
from Usuarios.views import crear_sala, cargar_xml_s, modificar_sala, eliminar_sala, gestionar_salas
from Usuarios.views import crear_tarjeta, cargar_xml_t, modificar_tarjeta, gestionar_tarjetas, eliminar_tarjeta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('pagina_login/', pagina_login, name='pagina_login'),
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
    path('crear_pelicula/', crear_pelicula, name='crear_pelicula'),  # ACÁ EMPIEZA PELICULAS
    path('cargar_peliculas_xml', cargar_peliculas_xml, name='cargar_peliculas_xml'),
    path('modificar_categoria/', modificar_categoria, name="modificar_categoria"),
    path('eliminar_categoria/', eliminar_categoria, name="eliminar_categoria"),
    path('eliminar_pelicula/<str:nombre>', eliminar_pelicula, name="eliminar_pelicula"),
    path('modificar_pelicula/', modificar_pelicula, name="modificar_pelicula"),
    path('vista_peliculas/', vista_peliculas, name='vista_peliculas'),
    path('crear_sala/', crear_sala, name='crear_sala'),
    path('cargar_xml_s/', cargar_xml_s, name='cargar_xml_s'),
    path('modificar_sala/', modificar_sala, name='modificar_sala'),
    path('eliminar_sala/<str:numero>', eliminar_sala, name='eliminar_sala'),
    path('eliminar_sala/', eliminar_sala, name="eliminar_sala"),
    path('gestionar_salas/', gestionar_salas, name='gestionar_salas'),
    path('crear_tarjeta/', crear_tarjeta, name='crear_tarjeta'),
    path('cargar_xml_t/', cargar_xml_t, name='cargar_xml_t'),
    path('modificar_tarjeta/', modificar_tarjeta, name='modificar_tarjeta'),
    path('eliminar_tarjeta/<str:numero>', eliminar_tarjeta, name='eliminar_tarjeta'),
    path('eliminar_tarjeta/', eliminar_tarjeta, name="eliminar_tarjeta"),
    path('gestionar_tarjetas/', gestionar_tarjetas, name='gestionar_tarjetas'),
]