from xml.dom import minidom
from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET

import requests
from .Lista_Usuarios import ListaEnlazadaSimple, Usuario
from .Pelicula import ListaCircularDoblementeEnlazada, Pelicula, Categoria
from .Lista_Peliculas_Carrusel import construir_lista_doble_enlazada, obtener_titulos_lista, obtener_imagenes_lista
from .Lista_Salas import ListaDobleEnlazada, Salas
from .Lista_Tarjetas import ListaTarjetasEnlazada

global lista_enlazada_simple, lista_circular_doble, lista_peliculas, lista_salas, lista_tarjetas, lista_categorias, ischarged
lista_enlazada_simple = ListaEnlazadaSimple()
lista_circular_doble = ListaCircularDoblementeEnlazada()
lista_salas = ListaDobleEnlazada()
lista_tarjetas = ListaTarjetasEnlazada()
global lista_usuarios
lista_usuarios = []
ischarged = False

def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        
        ll = construir_lista_doble_enlazada()
        
        titulos = obtener_titulos_lista(ll)
        imagenes = obtener_imagenes_lista(ll)


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
            lista_enlazada_simple.add(usuario)

        # Realizar la búsqueda del usuario en la lista enlazada simple
        usuario_encontrado = lista_enlazada_simple.buscar(correo, contrasena)
        
            # Obtener titulos e imagenes desde el XML
        
    # Combinar titulos e imagenes en una lista de tuplas
        peliculas = list(zip(titulos, imagenes))

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
            return render(request, 'login.html', {'peliculas': peliculas})
    else:
        return render(request, 'login.html')
    
def pagina_cliente(request):
    return render(request, 'cliente.html')

def pagina_login(request):
    return render(request, 'login.html')

def pagina_administrador(request):
    return render(request, 'administrador.html')

def gestionar_usuarios(request):
    return render(request, 'gestionar_usuarios.html')
def gestionar_peliculas(request):
    return render(request, 'gestionar_peliculas.html')
def gestionar_salas(request):
    return render(request, 'gestionar_salas.html')

def gestionar_tarjetas(request):
    return render(request, 'gestionar_tarjetas.html')

def cargar_xml(request):
    if request.method == 'POST':
        lista_enlazada_simple.CargarXML(1)
        response = requests.get('http://localhost:5010/getUsuarios')
        u_Api = response.json()
        
        for usuario in u_Api:
            lista_enlazada_simple.add(usuario)
        print(u_Api)
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
        #usuario = Usuario(rol, nombre, apellido, telefono, correo, password)
        # Guardar el usuario en la lista enlazada o en la base de datos
        
        #lista_enlazada_simple.add(usuario)
        lista_enlazada_simple.agregarXML(nombre,apellido,telefono,correo,password)
        lista_enlazada_simple.CargarXML(1)
        return redirect(gestionar_usuarios)
    
def mostrar_usuarios(request):
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
        lista_usuarios.append(usuario)

    return render(request, 'gestionar_usuarios.html', {'usuarios': lista_usuarios})

def modificar_usuario(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        nuevo_rol = request.POST['rol']
        nuevo_nombre = request.POST['nombre']
        nuevo_apellido = request.POST['apellido']
        nuevo_telefono = request.POST['telefono']
        nueva_contrasena = request.POST['contra']

        tree = ET.parse('usuarios.xml')
        root = tree.getroot()

        encontrado = False
        for user in root.findall('usuario'):
            if user.find('correo').text == correo:
                encontrado = True
                lista_enlazada_simple.delete(correo)
                rol = user.find('rol')
                rol.text = nuevo_rol
                nombre = user.find('nombre')
                nombre.text = nuevo_nombre
                apellido = user.find('apellido')
                apellido.text = nuevo_apellido
                telefono = user.find('telefono')
                telefono.text = nuevo_telefono
                contrasena = user.find('contrasena')
                contrasena.text = nueva_contrasena
                break

        if encontrado:
            tree.write('usuarios.xml')
            mensaje = "Usuario modificado exitosamente."
        else:
            mensaje = "Usuario no existente."

        return render(request, 'gestionar_usuarios.html', {'mensaje': mensaje})

    return render(request, 'gestionar_usuarios.html')

def eliminar_usuario(request):
    if request.method == "POST":
        correo = request.POST['correo']
        
        lista_enlazada_simple.delete(correo)
        lista_enlazada_simple.eliminarXML(correo)
        
    return render(request, 'gestionar_usuarios.html')
    
def cargar_peliculas(request):
    if request.method == 'POST':
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()
        


        for categoria_xml in root.findall('categoria'):
            nombre = categoria_xml.find('nombre').text
            nueva_categoria = Categoria(nombre)
            lista_circular_doble.agregar_categoria(nueva_categoria)
            
            peliculas_xml = categoria_xml.find('peliculas')
            for pelicula_xml in peliculas_xml.findall('pelicula'):
                titulo = pelicula_xml.find('titulo').text
                director = pelicula_xml.find('director').text
                anio = pelicula_xml.find('anio').text
                fecha = pelicula_xml.find('fecha').text
                hora = pelicula_xml.find('hora').text
                imagen = pelicula_xml.find('imagen').text
                precio = pelicula_xml.find('precio').text
                nueva_pelicula = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)
                lista_circular_doble.agregar_pelicula(nueva_categoria,titulo,director,anio,fecha,hora,imagen,precio)
        
        
    categorias = lista_circular_doble.obtener_categorias()
    peliculas = lista_circular_doble.obtener_peliculas(categorias)        
                


    return render(request, 'mostrar_peliculas.html', {'categorias': categorias, 'peliculas_por_categoria': peliculas})
###---------------------------------------------------------
def mostrar_peliculas(request):
    
    return render(request, 'gestionar_peliculas.html', {"peliculas": lista_circular_doble}) 
def cargar_peliculas_xml(request):
    if request.method == "POST":
        response = requests.get('http://localhost:5010/getPeliculas')
        p_Api = response.json()

        for peli in p_Api:
            if not ischarged:
                nombre = "Anime"
                categoria = Categoria(nombre)
                pelicula = Pelicula(
                    titulo=peli['titulo'],
                    director=peli['director'],
                    anio=peli['anio'],
                    fecha=peli['fecha'],
                    hora=peli['hora'],
                    imagen=peli['imagen'],
                    precio=peli['precio'],
                )

                lista_circular_doble.agregar(pelicula)

                lista1 = lista_circular_doble.obtener_elementos()
                lista2 = lista_circular_doble.obtener_peliculas_xml()
                lista_combinada = list(zip(lista1,lista2))

        print(lista_combinada)
        return render(request, 'gestionar_peliculas.html', {'peliculas': lista1, 'pelis': lista2})


def crear_pelicula(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        categoria = request.POST.get('categoria')
        titulo = request.POST.get('titulo')
        director = request.POST.get('director')
        anio = request.POST.get('anio')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        imagen = request.POST.get('imagen')
        precio = request.POST.get('precio')

        nueva_pelicula = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)

        # Cargar las películas del archivo XML en la lista circular doble
        lista_circular_doble.cargar_peliculas_xml()

        # Agregar la película a la lista circular doble
        categoria_encontrada = False
        categoria_actual = lista_circular_doble.cabeza
        while True:
            if categoria_actual.data.nombre == categoria:
                categoria_actual.data.agregar_pelicula(nueva_pelicula)
                categoria_encontrada = True
                break
            categoria_actual = categoria_actual.siguiente
            if categoria_actual == lista_circular_doble.cabeza:
                break

        if not categoria_encontrada:
            nueva_categoria = Categoria(categoria)
            nueva_categoria.agregar_pelicula(nueva_pelicula)
            lista_circular_doble.agregar(nueva_categoria)

        # Agregar la película al archivo XML
        lista_circular_doble.agregar_pelicula_xml(categoria, nueva_pelicula)

        return render(request, 'gestionar_peliculas.html')

    return render(request, 'gestionar_peliculas.html')

def modificar_categoria(request):
    if request.method == "POST":
        categoria_anterior = request.POST.get('categoria_anterior')
        categoria_nueva = request.POST.get('categoria_nueva')
        
        lista_circular_doble.modificar_nombre_categoria(categoria_anterior,categoria_nueva)
        lista_circular_doble.actualizar_xml(categoria_anterior,categoria_nueva)
        
        return render(request, 'gestionar_peliculas.html')    
def eliminar_categoria(request):
    if request.method == "POST":
        categoria_eliminar = request.POST.get('categoria_eliminada')
        
        lista_circular_doble.eliminar_categoria(categoria_eliminar)
        lista_circular_doble.eliminar_categoria_xml(categoria_eliminar)
        
        return render(request, 'gestionar_peliculas.html')
def eliminar_pelicula(request, nombre):
    lista_circular_doble.eliminar_pelicula_xml(nombre)
    
    return render(request, 'gestionar_peliculas.html')
        
def modificar_pelicula(request):
    if request.method == "POST":
        titulo_actual = request.POST.get('titulo_actual')
        titulo_nuevo = request.POST.get('titulo_nuevo')
        director = request.POST.get('director')
        anio = request.POST.get('anio')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        imagen = request.POST.get('imagen')
        precio = request.POST.get('precio')
        print("Si recibe datos")
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()
        
        for categoria in root.findall('categoria'):
            peliculas = categoria.find('peliculas')
            print("Busca en categorias")
            for pelicula in peliculas.findall('pelicula'):
                if pelicula.find('titulo').text == titulo_actual:
                    print("pelicula encontrada")
                    pelicula.find('titulo').text = titulo_nuevo
                    pelicula.find('director').text = director
                    pelicula.find('anio').text = anio
                    pelicula.find('fecha').text = fecha
                    pelicula.find('hora').text = hora
                    pelicula.find('imagen').text = imagen
                    pelicula.find('precio').text = precio
        
        tree.write('peliculas.xml')
        
    return render(request, 'gestionar_peliculas.html')


###-----------------------------------------------------------------------------------

def vista_peliculas(request):
    
    lista = construir_lista_doble_enlazada()
    titulos = obtener_titulos_lista(lista)
    imagenes = obtener_imagenes_lista(lista)

    peliculas = list(zip(titulos, imagenes))

    return render(request, 'login.html', {'peliculas': peliculas})

def mostrar_sala(request):
    return render(request, 'gestionar_salas.html', {'Salas': lista_salas})

def cargar_xml_s(request):
    if request.method == "POST":
        lista_salas.CargarXML_LED(1)
        response = requests.get('http://localhost:5010/getSalas')
        s_Api = response.json()
        for sala in s_Api[0]['cines']['cine']['salas']['sala']:
            lista_salas.add(Salas('Cine ABC', sala['numero'], sala['asientos']))
        print(s_Api)    
        
    return render(request, 'gestionar_salas.html', {'Salas': lista_salas})

def crear_sala(request):
    if request.method == 'POST':
        cine = 'Cine ABC'
        sala = request.POST.get('sala')
        asiento = request.POST.get('asiento')
        lista_salas.agregarXML_LED(sala, asiento)
        return redirect('cargar_xml_s')
    return render(request, 'gestionar_salas.html')

def modificar_sala(request):
    if request.method == 'POST':
        sala = request.POST['sala']
        asientos = request.POST['asiento']
        nueva_sala = request.POST['nueva_sala']

        lista_salas.editarXML_LED(sala, asientos, nueva_sala)

        return render(request, 'gestionar_salas.html')

    return render(request, 'gestionar_salas.html')

def eliminar_sala(request, numero):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        lista_salas.eliminar_LED(numero)
        return render(request, 'gestionar_salas.html')
    return redirect('cargar_xml_s')


def mostrar_tarjeta(request):
    return render(request, 'gestionar_tarjetas.html', {'Tarjetas': lista_tarjetas})

def cargar_xml_t(request):
    if request.method == "POST":
        lista_tarjetas.CargarXML_TAR(1)
        response = requests.get('http://localhost:5010/getTarjetas')
        tarjetas_API = response.json()
        print(tarjetas_API)

        for tarj in tarjetas_API:
            lista_tarjetas.add(tarj)
    return render(request, 'gestionar_tarjetas.html', {'Tarjetas': lista_tarjetas})

def crear_tarjeta(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        numero = request.POST.get('numero')
        titular = request.POST.get('titular')
        fechaexp = request.POST.get('fecha_expiracion')
        lista_tarjetas.agregarXML_TAR(tipo, numero, titular, fechaexp)
        return redirect('cargar_xml_t')
    return render(request, 'gestionar_tarjetas.html')

def modificar_tarjeta(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        numero = request.POST['numero']
        titular = request.POST['titular']
        fechaexp = request.POST['fecha_expiracion']

        lista_tarjetas.editarXML_TAR(tipo, numero, titular, fechaexp)

        return render(request, 'gestionar_tarjetas.html')

    return render(request, 'gestionar_tarjetas.html')

def eliminar_tarjeta(request, numero):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        lista_tarjetas.eliminar_TAR(numero)
    return redirect('cargar_xml_t')