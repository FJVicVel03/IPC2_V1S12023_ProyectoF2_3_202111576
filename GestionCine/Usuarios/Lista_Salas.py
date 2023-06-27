import xml.etree.ElementTree as ET

class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.back = None
        
class Salas():
    def __init__(self, cine, n_sala, asiento):
        self.cine = cine
        self.n_sala = n_sala
        self.asiento = asiento

    def imprimir(self):
        print(f"Cine: {self.cine}, Sala: {self.n_sala}, Asiento: {self.asiento}")
        
class ListaDobleEnlazada:
    def __init__(self):
        self.cabeza = None
        self.charged = False

    def __iter__(self):
        return self.loop()

    def loop(self):
        actual = self.cabeza

        while actual:
            yield actual.data
            actual = actual.next

    def verificar_informacion(username, lista):
        nodo_actual = lista.cabeza

        while nodo_actual is not None:
            sala = nodo_actual.data.data  # Corrección aquí
            sala.imprimir()  # Imprimir la información de la sala o realizar la verificación que desees

            nodo_actual = nodo_actual.next

    def esta_vacia(self):
        return self.cabeza is None

    def add(self, data):
        nuevo_nodo = Nodo(data)

        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            nodo_actual = self.cabeza
            while nodo_actual.next is not None:
                nodo_actual = nodo_actual.next
            nodo_actual.next = nuevo_nodo
            nuevo_nodo.back = nodo_actual

    def mostrar(self):
        current = self.cabeza
        while current is not None:
            print(f"{current.data.cine}, Numero de sala: {current.data.num_sala}, Asiento: {current.data.asiento}")
            current = current.next

    def delete(self, data):
        if self.esta_vacia():
            return

        if self.cabeza.data == data:
            if self.cabeza.next is None:
                self.cabeza = None
            else:
                self.cabeza = self.cabeza.next
                self.cabeza.back = None
            return

        nodo_actual = self.cabeza
        while nodo_actual is not None:
            if nodo_actual.data == data:
                nodo_anterior = nodo_actual.back
                nodo_siguiente = nodo_actual.next
                nodo_anterior.next = nodo_siguiente
                if nodo_siguiente is not None:
                    nodo_siguiente.back = nodo_anterior
                return
            nodo_actual = nodo_actual.next

    def modify(self, data_vieja, data_nueva):
        if self.esta_vacia():
            return

        nodo_actual = self.cabeza
        while nodo_actual is not None:
            if nodo_actual.data.n_sala  == data_vieja: 
                nodo_actual.data.asiento = data_nueva
                return
            nodo_actual = nodo_actual.next

    def buscar(self, elemento):
        actual = self.cabeza

        while actual is not None:
            if actual.data == elemento:
                return True
            actual = actual.next

        return False

    def CargarXML_LED(self, operacion):
        if self.charged:
            return  # Si los datos ya han sido cargados, no se cargan de nuevo

        tree = ET.parse('salas.xml')
        root = tree.getroot()

        numeros_sala_cargados = ListaDobleEnlazada()  # Lista para almacenar los números de sala cargados

        for cine in root.findall('cine'):
            nombre_cine = cine.find('nombre').text
            salas_cine = cine.find('salas')

            for indice, sala in enumerate(salas_cine.findall('sala')):
                numero_sala = sala.find('numero').text
                asientos_sala = sala.find('asientos').text

                # Verificar si el número de sala ya ha sido cargado
                if numeros_sala_cargados.buscar(numero_sala):
                    continue  # Omitir la sala si ya ha sido cargada

                objeto = Salas(nombre_cine, numero_sala, asientos_sala)

                if operacion == 1:
                    self.add(objeto)
                elif operacion == 2:
                    self.modify(numero_sala, asientos_sala)
                elif operacion == 3:
                    self.delete(objeto)

                numeros_sala_cargados.add(numero_sala)  # Agregar el número de sala a la lista enlazada doble

        self.charged = True

    def agregarXML_LED(self, sal, Asientos):
        tree = ET.parse('salas.xml')
        root = tree.getroot()

        nuevo_sala = ET.Element("sala")

        elemento_titulo = ET.SubElement(nuevo_sala, 'numero')
        elemento_titulo.text = sal

        asientos = ET.SubElement(nuevo_sala, 'asientos')
        asientos.text = str(Asientos)

        objeto = Salas('Cine ABC', sal, asientos.text)
        self.add(objeto)

        cine = root.find('cine')
        salas = cine.find('salas')
        salas.append(nuevo_sala)

        tree.write('salas.xml')

        self.CargarXML_LED(1)

    def editarXML_LED(self, numero_sala, nuevos_asientos, nuevo_numero_sala):
        tree = ET.parse('salas.xml')
        root = tree.getroot()

        for cine in root.findall('cine'):
            salas_cine = cine.find('salas')

            for sala in salas_cine.findall('sala'):
                numero_sala_element = sala.find('numero')
                asientos_sala_element = sala.find('asientos')

                if numero_sala_element is not None and numero_sala_element.text == numero_sala:
                    if asientos_sala_element is not None:
                        asientos_sala_element.text = str(nuevos_asientos)
                        numero_sala_element.text = str(nuevo_numero_sala)
                        # Modificar el número de sala en la lista doblemente enlazada
                        nodo_actual = self.cabeza
                        while nodo_actual is not None:
                            if nodo_actual.data.n_sala == numero_sala:
                                nodo_actual.data.n_sala = nuevo_numero_sala
                            nodo_actual = nodo_actual.next
                    break

        tree.write('salas.xml')

        self.CargarXML_LED(2)

    def eliminar_LED(self, titulo):
        tree = ET.parse('salas.xml')
        root = tree.getroot()

        for cine in root.findall('cine'):
            for sala in cine.findall('salas/sala'):
                if sala.find('numero').text == titulo:
                    cine.find('salas').remove(sala)
                    self.delete(Salas(cine.find('nombre').text, titulo, sala.find('asientos').text))
                    break

        tree.write('salas.xml')

        self.CargarXML_LED(3)        