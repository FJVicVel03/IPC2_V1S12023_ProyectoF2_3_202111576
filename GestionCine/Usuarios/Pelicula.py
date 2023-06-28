import xml.etree.cElementTree as ET
from xml.dom import minidom

class Nodo:
    def __init__(self, data):
        self.data = data
        self.siguiente = None
        self.anterior = None

class Pelicula:
    def __init__(self, titulo, director, anio, fecha, hora, imagen, precio):
        self.titulo = titulo
        self.director = director
        self.anio = anio
        self.fecha = fecha
        self.hora = hora
        self.imagen = imagen
        self.precio = precio

class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.peliculas = ListaCircularDoblementeEnlazada()

    def agregar_pelicula(self, pelicula):
        self.peliculas.agregar(pelicula)

    def obtener_peliculas(self):
        return self.peliculas.obtener_elementos()


class ListaCircularDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        
    def __iter__(self):
        return self.loop()

    def loop(self):
        if self.cabeza is not None:
            actual = self.cabeza
            while True:
                yield actual.data
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

    def agregar(self, data):
        nuevo_nodo = Nodo(data)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
        else:
            ultimo_nodo = self.cabeza.anterior
            ultimo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = ultimo_nodo
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo

    def obtener_elementos(self):
        elementos = []
        if self.cabeza is not None:
            actual = self.cabeza
            while True:
                elementos.append(actual.data)
                actual = actual.siguiente
                if actual == self.cabeza:
                    break
        return elementos
    
    def cargar_peliculas_xml(self):
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        for categoria in root.findall('categoria'):
            nombre_categoria = categoria.find('nombre').text

            nueva_categoria = Categoria(nombre_categoria)

            for indice, pelicula in enumerate(categoria.findall('peliculas/pelicula')):
                titulo = pelicula.find('titulo').text
                director = pelicula.find('director').text
                anio = pelicula.find('anio').text
                fecha = pelicula.find('fecha').text
                hora = pelicula.find('hora').text
                imagen = pelicula.find('imagen').text
                precio = pelicula.find('precio').text

                nueva_pelicula = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)
                
                nueva_categoria.agregar_pelicula(nueva_pelicula)
                self.agregar(nueva_categoria)
                    
    def obtener_peliculas_xml(self):
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        peliculas = []

        for categoria in root.findall('categoria'):
            for pelicula in categoria.findall('peliculas/pelicula'):
                titulo = pelicula.find('titulo').text
                director = pelicula.find('director').text
                anio = pelicula.find('anio').text
                fecha = pelicula.find('fecha').text
                hora = pelicula.find('hora').text
                imagen = pelicula.find('imagen').text
                precio = pelicula.find('precio').text

                nueva_pelicula = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)
                peliculas.append(nueva_pelicula)

        return peliculas

    def agregar_pelicula_xml(self, categoria, pelicula):
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        categoria_existente = None
        for categoria_element in root.findall('categoria'):
            nombre_categoria = categoria_element.find('nombre').text
            if nombre_categoria == categoria:
                categoria_existente = categoria_element
                break

        if categoria_existente is None:
            categoria_element = ET.Element('categoria')
            nombre_element = ET.SubElement(categoria_element, 'nombre')
            nombre_element.text = categoria
            peliculas_element = ET.SubElement(categoria_element, 'peliculas')
            root.append(categoria_element)
        else:
            peliculas_element = categoria_existente.find('peliculas')

        pelicula_element = ET.SubElement(peliculas_element, 'pelicula')
        titulo_element = ET.SubElement(pelicula_element, 'titulo')
        titulo_element.text = pelicula.titulo
        director_element = ET.SubElement(pelicula_element, 'director')
        director_element.text = pelicula.director
        anio_element = ET.SubElement(pelicula_element, 'anio')
        anio_element.text = pelicula.anio
        fecha_element = ET.SubElement(pelicula_element, 'fecha')
        fecha_element.text = pelicula.fecha
        hora_element = ET.SubElement(pelicula_element, 'hora')
        hora_element.text = pelicula.hora
        imagen_element = ET.SubElement(pelicula_element, 'imagen')
        imagen_element.text = pelicula.imagen
        precio_element = ET.SubElement(pelicula_element, 'precio')
        precio_element.text = pelicula.precio

        tree.write('peliculas.xml')
        
    def modificar_nombre_categoria(self, nombre_anterior, nombre_nuevo):
        if self.cabeza is not None:
            actual = self.cabeza
            while True:
                if actual.data.nombre == nombre_anterior:
                    actual.data.nombre = nombre_nuevo
                    self.actualizar_xml(nombre_anterior, nombre_nuevo)
                    break
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

    def actualizar_xml(self, nombre_anterior, nombre_nuevo):
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        for categoria_element in root.findall('categoria'):
            nombre_categoria = categoria_element.find('nombre').text
            if nombre_categoria == nombre_anterior:
                categoria_element.find('nombre').text = nombre_nuevo

        tree.write('peliculas.xml')
        
        
    def eliminar_categoria(self, nombre_categoria):
        if self.cabeza is not None:
            actual = self.cabeza
            while True:
                if actual.data.nombre == nombre_categoria:
                    self.eliminar_xml(nombre_categoria)
                    self.eliminar_nodo(actual)
                    return
                actual = actual.siguiente
                if actual == self.cabeza:
                    break

    def eliminar_nodo(self, nodo):
        if self.cabeza == nodo:
            if self.cabeza.siguiente == self.cabeza:
                self.cabeza = None
            else:
                ultimo_nodo = self.cabeza.anterior
                self.cabeza = self.cabeza.siguiente
                ultimo_nodo.siguiente = self.cabeza
                self.cabeza.anterior = ultimo_nodo
        else:
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior

    def eliminar_categoria_xml(self, nombre_categoria):
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        for categoria_element in root.findall('categoria'):
            nombre_element = categoria_element.find('nombre')
            if nombre_element.text == nombre_categoria:
                root.remove(categoria_element)
                break

        tree.write('peliculas.xml')

    def eliminar_pelicula_xml(self, titulo_pelicula):
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()

        for categoria_element in root.findall('categoria'):
            peliculas_element = categoria_element.find('peliculas')
            for pelicula_element in peliculas_element.findall('pelicula'):
                titulo_element = pelicula_element.find('titulo')
                if titulo_element.text == titulo_pelicula:
                    peliculas_element.remove(pelicula_element)
                    break

        tree.write('peliculas.xml')

    def eliminar_pelicula(self, titulo_pelicula):
        if self.cabeza is not None:
            actual = self.cabeza
            while True:
                peliculas = actual.data.obtener_peliculas()
                for pelicula in peliculas:
                    if pelicula.titulo == titulo_pelicula:
                        actual.data.peliculas.eliminar_nodo(pelicula)
                        self.eliminar_pelicula_xml(titulo_pelicula)
                        return
                actual = actual.siguiente
                if actual == self.cabeza:
                    break
                
                
    def modificar_pelicula_xml(self,titulo_actual, titulo_nuevo, director, anio, fecha, hora, imagen, precio):
        tree = ET.parse('peliculas.xml')
        root = tree.getroot()
        
        for categoria in root.findall('categoria'):
            peliculas = categoria.find('peliculas')
            
            for pelicula in peliculas.findall('pelicula'):
                if pelicula.find('titulo').text == titulo_actual:
                    pelicula.find('titulo').text = titulo_nuevo
                    pelicula.find('director').text = director
                    pelicula.find('anio').text = anio
                    pelicula.find('fecha').text = fecha
                    pelicula.find('hora').text = hora
                    pelicula.find('imagen').text = imagen
                    pelicula.find('precio').text = precio

        tree.write('peliculas.xml')





           
    



