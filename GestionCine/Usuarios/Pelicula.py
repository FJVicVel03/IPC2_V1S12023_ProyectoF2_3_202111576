class Pelicula:
    def __init__(self, titulo, director, anio, fecha, hora, imagen, precio):
        self.titulo = titulo
        self.director = director
        self.anio = anio
        self.fecha = fecha
        self.hora = hora
        self.imagen = imagen
        self.precio = precio
        self.siguiente = None
        self.anterior = None


class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.peliculas = None
        self.siguiente = None
        self.anterior = None


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


    def agregar_categoria(self, nombre):
        nueva_categoria = Categoria(nombre)
        if self.cabeza is None:
            self.cabeza = nueva_categoria
            nueva_categoria.siguiente = nueva_categoria
            nueva_categoria.anterior = nueva_categoria
        else:
            ultima_categoria = self.cabeza.anterior
            ultima_categoria.siguiente = nueva_categoria
            nueva_categoria.anterior = ultima_categoria
            nueva_categoria.siguiente = self.cabeza
            self.cabeza.anterior = nueva_categoria

    def agregar_pelicula(self, categoria, titulo, director, anio, fecha, hora, imagen, precio):
        nueva_pelicula = Pelicula(titulo, director, anio, fecha, hora, imagen, precio)

        categoria_actual = self.cabeza
        while categoria_actual.nombre != categoria:
            categoria_actual = categoria_actual.siguiente
            if categoria_actual == self.cabeza:
                print("La categoría especificada no existe.")
                return

        if categoria_actual.peliculas is None:
            categoria_actual.peliculas = nueva_pelicula
            nueva_pelicula.siguiente = nueva_pelicula
            nueva_pelicula.anterior = nueva_pelicula
        else:
            ultima_pelicula = categoria_actual.peliculas.anterior
            ultima_pelicula.siguiente = nueva_pelicula
            nueva_pelicula.anterior = ultima_pelicula
            nueva_pelicula.siguiente = categoria_actual.peliculas
            categoria_actual.peliculas.anterior = nueva_pelicula

    def obtener_categorias(self):
        categorias = []
        if self.cabeza is not None:
            categoria_actual = self.cabeza
            while True:
                categorias.append(categoria_actual.nombre)
                categoria_actual = categoria_actual.siguiente
                if categoria_actual == self.cabeza:
                    break
        return categorias

    def obtener_peliculas(self, categoria):
        peliculas = []
        categoria_actual = self.cabeza
        while categoria_actual.nombre != categoria:
            categoria_actual = categoria_actual.siguiente
            if categoria_actual == self.cabeza:
                print("La categoría especificada no existe.")
                return peliculas

        if categoria_actual.peliculas is not None:
            pelicula_actual = categoria_actual.peliculas
            while True:
                peliculas.append(pelicula_actual.titulo)
                pelicula_actual = pelicula_actual.siguiente
                if pelicula_actual == categoria_actual.peliculas:
                    break

        return peliculas

