import xml.etree.ElementTree as ET


class Nodo:
    def __init__(self, data):
        self.data = data
        self.next = None

class ListaEnlazadaSimple:
    def __init__(self):
        self.cabeza = None

    def __iter__(self):
        return iter(self.loop())
    
    def loop(self):
        actual = self.cabeza
       
        while actual:
            yield actual.data
            actual = actual.next

    def existe_usuario_correo(self, correo):
        actual = self.cabeza
        while actual is not None:
            if actual.data.correo == correo:
                return True
            actual = actual.next
        return False

    def add(self, data):        
        nuevo = Nodo(data)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.next is not None:
                if actual.data == data:
                    return
                actual = actual.next
            actual.next = nuevo
            if actual.data == data:
                return
            actual.next = nuevo

    def modify(self, data_nuevo, index):
        actual = self.cabeza
        indice = 0

        while actual is not None:
            if indice == index:
                actual.data = data_nuevo
                return
            indice += 1
            actual = actual.next

    def delete(self, correo):
        # Check if list is empty
        if self.cabeza is None:
            return

        # If the node to delete is the head node
        if self.cabeza.data.correo == correo:
            self.cabeza = self.cabeza.next
            return

        # Find the node to delete
        actual = self.cabeza
        while actual.next is not None:
            if actual.next.data.correo == correo:
                actual.next = actual.next.next
                return
            actual = actual.next

    def Imprimir(self):
        actual = self.cabeza
        while actual is not None:
            actual.data.imprimir()  # Llamar al método 'imprimir' del objeto Usuario
            actual = actual.next

    def CargarXML(self, operacion):
        tree = ET.parse('usuarios.xml')
        root = tree.getroot()

        for indice, usuario in enumerate(root.findall('usuario')):
            rol = usuario.find('rol').text
            nombre = usuario.find('nombre').text
            apellido = usuario.find('apellido').text
            telefono = usuario.find('telefono').text
            correo = usuario.find('correo').text
            contrasena = usuario.find('contrasena').text

            objeto = Usuario(rol, nombre, apellido, telefono, correo, contrasena)

            if self.existe_usuario_correo(objeto):
               continue  # Saltar el usuario repetido

            if operacion == 1:
                if self.existe_usuario_correo(correo):
                    print("\tEl cliente ya existe en la lista.")
                    return False

                else:
                    self.add(objeto)
            elif operacion == 2:
                self.modify(objeto, indice)
            elif operacion == 3:
                self.delete(objeto)

    def agregarXML(self, Nombre, Apellido, Telefono, Email, Password):
        tree = ET.parse('usuarios.xml')
        root = tree.getroot()

        nuevo_cliente = ET.Element("usuario")

        rol = ET.SubElement(nuevo_cliente, 'rol')
        rol.text = 'cliente'

        nombre = ET.SubElement(nuevo_cliente, 'nombre')
        nombre.text = Nombre

        apellido = ET.SubElement(nuevo_cliente, 'apellido')
        apellido.text = Apellido

        telefono = ET.SubElement(nuevo_cliente, 'telefono')
        telefono.text = Telefono

        correo = ET.SubElement(nuevo_cliente, 'correo')
        correo.text = Email

        contraseña = ET.SubElement(nuevo_cliente, 'contrasena')
        contraseña.text = Password

        objeto = Usuario(rol.text, nombre.text, apellido.text, telefono.text, correo.text, contraseña.text)
        self.add(objeto)

        root.append(nuevo_cliente)

        tree.write('usuarios.xml')

    def editarXML(self, new_rol, new_nombre, new_apellido, new_telefono, tmp_correo, new_contrasena):
        tree = ET.parse('usuarios.xml')
        root = tree.getroot()

        for user in root.findall('usuario'):
            if user.find('correo').text == tmp_correo:
                rol = user.find('rol')
                rol.text = new_rol
                nombre = user.find('nombre')
                nombre.text = new_nombre
                apellido = user.find('apellido')
                apellido.text = new_apellido
                telefono = user.find('telefono')
                telefono.text = new_telefono
                correo = user.find('correo')
                correo.text = tmp_correo
                contrasena = user.find('contrasena')
                contrasena.text = new_contrasena
                break

        tree.write('usuarios.xml')

        self.CargarXML(2)

    def eliminarXML(self, tmp_correo):
        tree = ET.parse('usuarios.xml')
        root = tree.getroot()

        for user in root.findall('usuario'):
            if user.find('correo').text == tmp_correo:
                root.remove(user)
                break

        tree.write('usuarios.xml')
        
    def buscar(self, correo, contrasena):
        current = self.cabeza
        while current:
            if current.data.correo == correo and current.data.contrasena == contrasena:
                return current.data
            current = current.next
        return None
    

class Usuario:
    def __init__(self, rol, nombre, apellido, telefono, correo, contrasena):
        self.rol = rol
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena
