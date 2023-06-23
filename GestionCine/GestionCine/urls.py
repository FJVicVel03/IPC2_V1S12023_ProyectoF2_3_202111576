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
from Usuarios.views import login
from Usuarios.views import pagina_administrador
from Usuarios.views import pagina_cliente
from Usuarios.views import mostrar_peliculas
from Usuarios.views import gestionar_usuarios, crear_usuario, mostrar_usuarios, cargar_xml, modificar_usuario, eliminar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='login'),
    path('administrador/', pagina_administrador, name='administrador'),
    path('cliente/', pagina_cliente , name='cliente'),
    path('peliculas/',mostrar_peliculas, name='mostrar_peliculas'),
    path('gestionar_usuarios/', gestionar_usuarios, name="gestionar_usuarios"),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('mostrar_usuarios/', mostrar_usuarios, name='mostrar_usuarios'),
    path('cargar_xml/',cargar_xml, name='cargar_xml'), 
    path('modificar_usuario/', modificar_usuario, name='modificar_usuario'),
    path('eliminar_usuario/', eliminar_usuario, name='eliminar_usuario'),
]