from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .Lista_Usuarios import ListaEnlazadaSimple, Usuario
from .Pelicula import ListaCircularDoblementeEnlazada, Pelicula, Categoria

global lista_enlazada_simple, lista_circular_doble
lista_enlazada_simple = ListaEnlazadaSimple()
lista_circular_doble = ListaCircularDoblementeEnlazada()
global lista_usuarios
lista_usuarios = []

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
            lista_enlazada_simple.add(usuario)

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


def mostrar_peliculas(request):
    tree = ET.parse('peliculas.xml')
    root = tree.getroot()

    categorias = []
    peliculas_por_categoria = []

    for categoria_xml in root.findall('categoria'):
        nombre = categoria_xml.find('nombre').text
        categorias.append(nombre)

        peliculas_xml = categoria_xml.find('peliculas')
        peliculas = []
        for pelicula_xml in peliculas_xml.findall('pelicula'):
            titulo = pelicula_xml.find('titulo').text
            director = pelicula_xml.find('director').text
            anio = pelicula_xml.find('anio').text
            fecha = pelicula_xml.find('fecha').text
            hora = pelicula_xml.find('hora').text
            imagen = pelicula_xml.find('imagen').text
            precio = pelicula_xml.find('precio').text
            peliculas.append({
                'titulo': titulo,
                'director': director,
                'anio': anio,
                'fecha': fecha,
                'hora': hora,
                'imagen': imagen,
                'precio': precio
            })

        peliculas_por_categoria.append(peliculas)

    return render(request, 'mostrar_peliculas.html', {'categorias': categorias, 'peliculas_por_categoria': peliculas})


