class Pelicula:
    def __init__(self, titulo, director, anio, fecha, hora, imagen, precio):
        self.titulo = titulo
        self.director = director
        self.anio = anio
        self.fecha = fecha
        self.hora = hora
        self.imagen = imagen
        self.precio = precio

class Nodo:
    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazadaCircular:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        

    def esta_vacia(self):
        return self.primero is None

    def agregar_pelicula(self, pelicula):
        nuevo_nodo = Nodo(pelicula)

        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            nuevo_nodo.anterior = self.ultimo
            self.primero.anterior = nuevo_nodo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo

    def obtener_categorias(self):
        categorias = []

        if not self.esta_vacia():
            nodo_actual = self.primero

            while True:
                categoria = nodo_actual.pelicula.categoria

                if categoria not in categorias:
                    categorias.append(categoria)

                nodo_actual = nodo_actual.siguiente

                if nodo_actual == self.primero:
                    break

        return categorias

    def obtener_peliculas_por_categoria(self, categoria):
        peliculas_por_categoria = []

        if not self.esta_vacia():
            nodo_actual = self.primero

            while True:
                if nodo_actual.pelicula.categoria == categoria:
                    peliculas_por_categoria.append(nodo_actual.pelicula)

                nodo_actual = nodo_actual.siguiente

                if nodo_actual == self.primero:
                    break

        return peliculas_por_categoria