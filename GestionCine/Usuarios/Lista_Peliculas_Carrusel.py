import xml.etree.ElementTree as ET

# Clase para los nodos de la lista doblemente enlazada
class Node:
    def __init__(self, title, image_url):
        self.title = title
        self.image_url = image_url
        self.prev = None
        self.next = None

# Método para construir la lista doblemente enlazada a partir del XML
def construir_lista_doble_enlazada():
    # Cargar el archivo XML
    tree = ET.parse('peliculas.xml')
    root = tree.getroot()

    # Crear la lista doblemente enlazada
    head = None
    tail = None

    # Recorrer el XML y construir la lista
    for categoria in root.findall('categoria'):
        peliculas = categoria.find('peliculas')
        for pelicula in peliculas.findall('pelicula'):
            titulo = pelicula.find('titulo').text
            imagen = pelicula.find('imagen').text

            new_node = Node(titulo, imagen)

            if head is None:
                head = new_node
                tail = new_node
            else:
                tail.next = new_node
                new_node.prev = tail
                tail = new_node

    return head

# Método para obtener los títulos de las películas de la lista
def obtener_titulos_lista(head):
    titles = []
    current = head
    while current is not None:
        titles.append(current.title)
        current = current.next
    return titles

# Método para obtener las URL de las imágenes de la lista
def obtener_imagenes_lista(head):
    images = []
    current = head
    while current is not None:
        images.append(current.image_url)
        current = current.next
    return images
