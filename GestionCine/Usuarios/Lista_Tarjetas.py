import xml.etree.cElementTree as ET

class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.back = None

class Tarjetas:
    def __init__(self, tipo, numero, titular, fecha_exp):
        self.tipo = tipo
        self.numero = numero
        self.titular = titular
        self.fecha_exp = fecha_exp

    def imprimir(self):
        print(f"Tipo: {self.tipo}, Numero: {self.numero}, Titular: {self.titular}, Expira en: {self.fecha_exp}")

class ListaTarjetasEnlazada:
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
    
    def existe_numero_tarjeta(self, numero):
        actual = self.cabeza
        while actual is not None:
            if actual.data.numero == numero:
                return True
            actual = actual.next
        return False
            
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
            print(f"{current.data.tipo}, Numero: {current.data.numero}, Titular: {current.data.titular}, Expira en: {current.data.fecha_exp}")
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
            if nodo_actual.data.numero  == data_vieja:
                nodo_actual.data = data_nueva
                return
            nodo_actual = nodo_actual.next

    def buscar(self, elemento):
        actual = self.cabeza

        while actual is not None:
            if actual.data == elemento:
                return True
            actual = actual.next
        
        return False
    
    def CargarXML_TAR(self, operacion):
        if self.charged:
            return
        
        tree = ET.parse('tarjetas.xml')
        root = tree.getroot()

        for indice, tarjeta in enumerate(root.findall('tarjeta')):
            tipo = tarjeta.find('tipo').text
            numero = tarjeta.find('numero').text
            titular = tarjeta.find('titular').text
            fecha_expiracion = tarjeta.find('fecha_expiracion').text

            objeto = Tarjetas(tipo, numero, titular, fecha_expiracion)

            if self.existe_numero_tarjeta(objeto):
                continue  # Omitir la sala si ya ha sido cargada

            if operacion == 1:
                self.add(objeto)
            elif operacion == 2:
                self.modify(objeto, indice)
            elif operacion == 3:
                self.delete(objeto)

        self.charged = True

    def agregarXML_TAR(self, typetar, number, person, datex):
        tree = ET.parse('tarjetas.xml')
        root = tree.getroot()

        nueva_tarjeta = ET.Element('tarjeta')

        tipo_tarjeta = ET.SubElement(nueva_tarjeta, 'tipo')
        tipo_tarjeta.text = typetar

        numero_tarjeta = ET.SubElement(nueva_tarjeta, 'numero')
        numero_tarjeta.text = number

        titular_tarjeta = ET.SubElement(nueva_tarjeta, 'titular')
        titular_tarjeta.text = person

        fechaex_tarjeta = ET.SubElement(nueva_tarjeta, 'fecha_expiracion')
        fechaex_tarjeta.text = datex

        objeto = Tarjetas(tipo_tarjeta.text, numero_tarjeta.text, titular_tarjeta.text, fechaex_tarjeta.text)
        self.add(objeto)

        root.append(nueva_tarjeta)

        tree.write('tarjetas.xml')
        self.CargarXML_TAR(1)

    def editarXML_TAR(self, tmp_type, tmp_number, tmp_person, tmp_date):
        tree = ET.parse('tarjetas.xml')
        root = tree.getroot()

        for tarjeta in root.findall('tarjeta'):
            if tarjeta.find('numero').text == tmp_number:
                tipo = tarjeta.find('tipo')
                tipo.text = tmp_type
                numero = tarjeta.find('numero')
                numero.text = tmp_number
                titular = tarjeta.find('titular')
                titular.text = tmp_person
                fecha_expiracion = tarjeta.find('fecha_expiracion')
                fecha_expiracion.text = tmp_date
                break

        tree.write('tarjetas.xml')

        self.CargarXML_TAR(2)

    def eliminar_TAR(self, number):
        tree = ET.parse('tarjetas.xml')
        root = tree.getroot()

        for tarjeta in root.findall('tarjeta'):
            if tarjeta.find('numero').text == number:
                root.remove(tarjeta)
                break

        tree.write('tarjetas.xml')
        
        self.CargarXML_TAR(3)