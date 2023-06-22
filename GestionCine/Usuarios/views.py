from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .Lista_Usuarios import ListaEnlazadaSimple, Usuario
from .Pelicula import ListaDoblementeEnlazadaCircular, Pelicula

global lista_enlazada_simple
lista_enlazada_simple = ListaEnlazadaSimple()

def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        # Cargar los usuarios del archivo XML en una lista enlazada simple
        
        tree = ET.parse('usuarios.xml')
        root = tree.getroot()

        for usuario_xml in root.findall('usuario'):
            rol = usuario_xml.find('rol').text
            nombre = usuario_xml.find('nombre').text
            apellido = usuario_xml.find('apellido').text
            telefono = usuario_xml.find('telefono').text
            correo_xml = usuario_xml.find('correo').text
            contrasena_xml = usuario_xml.find('contrasena').text

            usuario = Usuario(rol, nombre, apellido, telefono, correo_xml, contrasena_xml)
            lista_enlazada_simple.insertar(usuario)

        # Realizar la búsqueda del usuario en la lista enlazada simple
        usuario_encontrado = lista_enlazada_simple.buscar(correo, contrasena)

        if usuario_encontrado:
            if usuario_encontrado.rol == 'cliente':
                # Redireccionar al perfil de cliente
                return redirect(pagina_cliente)
            elif usuario_encontrado.rol == 'administrador':
                # Redireccionar al perfil de administrador
                return redirect(pagina_administrador)
        else:
            # Usuario no encontrado, mostrar mensaje de error
            error_message = 'Correo o contraseña incorrectos'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def pagina_cliente(request):
    return render(request, 'cliente.html')

def pagina_administrador(request):
    return render(request, 'administrador.html')

def gestionar_usuarios(request):
    return render(request, 'gestionar_usuarios.html')

def cargar_xml(request):
    if request.method == 'POST':
        lista_enlazada_simple.CargarXML(1)
    return render(request, 'gestionar_usuarios.html', {'usuarios': lista_enlazada_simple})

def crear_usuario(request):
    
    if request.method == 'POST':
        # Obtener los datos del formulario de creación
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        rol = 'cliente'
        password = request.POST.get('contra')

        # Crear el nuevo usuario
        usuario = Usuario(rol, nombre, apellido, telefono, correo, password)
        # Guardar el usuario en la lista enlazada o en la base de datos
        
        lista_enlazada_simple.insertar(usuario)

        return redirect(gestionar_usuarios)
    
def mostrar_usuarios(request):
    # Cargar los usuarios del archivo XML en una lista enlazada simple

    tree = ET.parse('usuarios.xml')
    root = tree.getroot()

    lista_usuarios = []
    for usuario_xml in root.findall('usuario'):
        rol = usuario_xml.find('rol').text
        nombre = usuario_xml.find('nombre').text
        apellido = usuario_xml.find('apellido').text
        telefono = usuario_xml.find('telefono').text
        correo_xml = usuario_xml.find('correo').text
        contrasena_xml = usuario_xml.find('contrasena').text

        usuario = Usuario(rol, nombre, apellido, telefono, correo_xml, contrasena_xml)
        lista_usuarios.append(usuario)

    return render(request, 'gestionar_usuarios.html', {'usuarios': lista_usuarios})

    


















def cargar_peliculas():
    lista_peliculas = ListaDoblementeEnlazadaCircular()

    # Cargar datos del XML en la lista
    tree = ET.parse("peliculas.xml")
    root = tree.getroot()

    for categoria in root.findall('categoria'):
        nombre_categoria = categoria.find('nombre').text

        for pelicula in categoria.find('peliculas').findall('pelicula'):
            titulo = pelicula.find('titulo').text
            director = pelicula.find('director').text
            anio = pelicula.find('anio').text
            fecha = pelicula.find('fecha').text
            hora = pelicula.find('hora').text
            imagen_element = pelicula.find('imagen')
            imagen = imagen_element.text if imagen_element is not None else 'vacio'
            precio_element = pelicula.find('precio')
            precio = precio_element.text if precio_element is not None else 'vacio'

            pelicula_obj = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)
            pelicula_obj.categoria = nombre_categoria
            lista_peliculas.agregar_pelicula(pelicula_obj)

    return lista_peliculas


def mostrar_peliculas(request):
    lista_peliculas = cargar_peliculas()

    # Obtener y mostrar las categorías
    categorias = lista_peliculas.obtener_categorias()

    peliculas_por_categoria = {}
    for categoria in categorias:
        peliculas_por_categoria[categoria] = lista_peliculas.obtener_peliculas_por_categoria(categoria)

    return render(request, 'mostrar_peliculas.html', {'categorias': categorias, 'peliculas_por_categoria': peliculas_por_categoria})

