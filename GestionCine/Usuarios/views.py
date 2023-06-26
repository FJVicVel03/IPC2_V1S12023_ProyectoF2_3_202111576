from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from .Lista_Usuarios import ListaEnlazadaSimple, Usuario
from .Pelicula import ListaCircularDoblementeEnlazada, Pelicula, Categoria
from .Lista_Peliculas_Carrusel import construir_lista_doble_enlazada, obtener_titulos_lista, obtener_imagenes_lista

global lista_enlazada_simple, lista_circular_doble, lista_peliculas
lista_enlazada_simple = ListaEnlazadaSimple()
lista_circular_doble = ListaCircularDoblementeEnlazada()
global lista_usuarios
lista_usuarios = []

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

def pagina_administrador(request):
    return render(request, 'administrador.html')

def gestionar_usuarios(request):
    return render(request, 'gestionar_usuarios.html')
def gestionar_peliculas(request):
    return render(request, 'gestionar_peliculas.html')

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
        lista_circular_doble.agregar_categoria(nombre)

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
            lista_circular_doble.agregar_pelicula(nombre, titulo,director,anio,fecha,hora,imagen,precio)
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
        categorias2 = lista_circular_doble.obtener_categorias()
        peliculas2 = lista_circular_doble.obtener_peliculas(categorias2)
        
                
        
        
        return render(request, 'mostrar_peliculas.html', {'categorias': categorias, 'peliculas_por_categoria': peliculas})

def agregar_categoria(request):
    if request.method == "POST":
        categorian = request.POST.get('categorian')
        
        # Cargar el archivo XML
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        # Verificar si la categoría ya existe
        categorias_existentes = [categoria.find('nombre').text for categoria in root.findall('categoria')]
        if categorian in categorias_existentes:
            mensaje = "La categoría ya existe."
        else:
            # Crear el elemento de categoría y agregarlo al árbol XML
            nueva_categoria = ET.Element('categoria')
            nombre = ET.SubElement(nueva_categoria, 'nombre')
            nombre.text = categorian
            peliculas = ET.SubElement(nueva_categoria,'peliculas')
            root.append(nueva_categoria)
            lista_circular_doble.agregar_categoria(nueva_categoria)

            # Guardar los cambios en el archivo XML
            tree.write('peliculas.xml')

            categoriasn = lista_circular_doble.obtener_categorias()

        return render(request, 'gestionar_peliculas.html')
    else:
        return render(request, 'gestionar_peliculas.html')

def agregar_pelicula(request):
    if request.method == "POST":
        peliculan = request.POST.get('peliculan')
        director = request.POST.get('director')
        anio = request.POST.get('anio')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        imagen = request.POST.get('imagen')
        precio = request.POST.get('precio')
        categoria_elegida = request.POST.get('categoria')

        # Cargar el archivo XML
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        # Buscar la categoría seleccionada
        categoria = root.find(".//categoria[nombre='" + categoria_elegida + "']")
        if categoria is not None:
            # Crear el elemento de película y agregarlo a la categoría
            nueva_pelicula = ET.Element('pelicula')
            titulo_element = ET.SubElement(nueva_pelicula, 'titulo')
            titulo_element.text = peliculan
            director_element = ET.SubElement(nueva_pelicula, 'director')
            director_element.text = director
            anio_element = ET.SubElement(nueva_pelicula, 'anio')
            anio_element.text = anio
            fecha_element = ET.SubElement(nueva_pelicula, 'fecha')
            fecha_element.text = fecha
            hora_element = ET.SubElement(nueva_pelicula, 'hora')
            hora_element.text = hora
            imagen_element = ET.SubElement(nueva_pelicula, 'imagen')
            imagen_element.text = imagen
            precio_element = ET.SubElement(nueva_pelicula, 'precio')
            precio_element.text = precio

            peliculas = categoria.find('peliculas')
            peliculas.append(nueva_pelicula)
            asd = lista_circular_doble.obtener_categorias()
            # Guardar los cambios en el archivo XML
            tree.write('peliculas.xml')

            print("Película agregada correctamente.")
            print(asd)
        else:
            print("La categoría seleccionada no existe.")

        return render(request, 'gestionar_peliculas.html')

def modificar_categoria(request):
    if request.method == "POST":
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        categoria_anterior = request.POST.get('cateam')
        categoria = root.find(".//categoria[nombre='" + categoria_anterior + "']")

        if categoria is not None:
            categoria_nueva = request.POST.get('catem')
            categoria.find('nombre').text = categoria_nueva

            # Guardar los cambios en el archivo XML
            tree.write('peliculas.xml')

            print("Categoria cambiada correctamente")
        else:
            print("La categoría especificada no existe")

        return render(request, 'gestionar_peliculas.html')

def modificar_peliculas(request):
    if request.method == "POST":
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()
        
        categoria_pelicula = request.POST.get('categoria')
        pelicula_anterior = request.POST.get('pelicula')
        
        categoria = root.find(".//categoria[nombre='" + categoria_pelicula + "']")
        
        if categoria is None:
            print("La categoría no existe")
            return
        
        pelicula = categoria.find(".//pelicula[titulo='" + pelicula_anterior + "']")
        
        if pelicula is None:
            print("La película no existe")
            return

        nuevo_titulo = request.POST.get('titulo')
        nuevo_director = request.POST.get('director')
        nuevo_anio = request.POST.get('anio')
        nueva_fecha = request.POST.get('fecha')
        nueva_hora = request.POST.get('hora')
        nueva_imagen = request.POST.get('imagen')
        nuevo_precio = request.POST.get('precio')
        
        pelicula.find('titulo').text = nuevo_titulo
        pelicula.find('director').text = nuevo_director
        pelicula.find('anio').text = nuevo_anio
        pelicula.find('fecha').text = nueva_fecha
        pelicula.find('hora').text = nueva_hora
        pelicula.find('imagen').text = nueva_imagen
        pelicula.find('precio').text = nuevo_precio

        # Guardar los cambios en el archivo XML
        tree.write('peliculas.xml')

        print("Película modificada correctamente")
        
        return render(request,'gestionar_peliculas.html')

def eliminar_categoria(request):
    if request.method == "POST":
        nombre_categoria = request.POST.get("categoriae")

        # Cargar el archivo XML
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        # Buscar la categoría en el XML
        categoria = root.find(".//categoria[nombre='" + nombre_categoria + "']")

        if categoria is not None:
            # Eliminar la categoría y todas sus películas
            root.remove(categoria)

            # Guardar los cambios en el archivo XML
            tree.write('peliculas.xml')

            mensaje = 'Categoría eliminada correctamente.'
            print(mensaje)
        else:
            mensaje = 'La categoría no existe.'
            print(mensaje)

        return render(request, 'gestionar_peliculas.html')

    return render(request, 'gestionar_peliculas.html')

def eliminar_pelicula(request):
    if request.method == "POST":
        categoria_buscar = request.POST.get('categoria')
        pelicula_eliminar = request.POST.get('peliculae')

        # Cargar el archivo XML
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        # Buscar la categoría en el XML
        categoria = root.find(".//categoria[nombre='" + categoria_buscar + "']")

        if categoria is not None:
            # Buscar la película en la categoría
            pelicula = categoria.find(".//pelicula[titulo='" + pelicula_eliminar + "']")

            if pelicula is not None:
                # Eliminar la película de la categoría
                categoria.find('peliculas').remove(pelicula)

                # Guardar los cambios en el archivo XML
                tree.write('peliculas.xml')

                mensaje = 'Película eliminada correctamente.'
                print(mensaje)
            else:
                mensaje = 'La película no existe en la categoría.'
                print(mensaje)
        else:
            mensaje = 'La categoría no existe.'

        return render(request, 'gestionar_peliculas.html')

    return render(request, 'gestionar_peliculas.html')      

def vista_peliculas(request):
    
    lista = construir_lista_doble_enlazada()
    titulos = obtener_titulos_lista(lista)
    imagenes = obtener_imagenes_lista(lista)

    peliculas = list(zip(titulos, imagenes))

    return render(request, 'login.html', {'peliculas': peliculas})
