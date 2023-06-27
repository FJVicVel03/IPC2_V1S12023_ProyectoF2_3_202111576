from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route('/getUsuarios', methods=['GET'])
def getUsuario():
    try:
        if request.method == 'GET':
            retorno = [
                {
            "rol": "administrador",
            "nombre": "Paco",
            "apellido": "Argos",
            "telefono": "123456789",
            "correo": "paco@example.com",
            "contrasena": "159"
        },
        {
            "rol": "cliente",
            "nombre": "Fernando",
            "apellido": "Vicente",
            "telefono": "987654321",
            "correo": "fer@example.com",
            "contrasena": "123"
        },
        # Agrega aquí el tercer usuario
        {
            "rol": "cliente",
            "nombre": "Alice",
            "apellido": "Johnson",
            "telefono": "555555555",
            "correo": "alice.johnson@example.com",
            "contrasena": "alice123"
        }
                
            ]
        else:
            retorno = {"mensaje": "Error de la petición, método incorrecto"}
        return jsonify(retorno)
    except:
        return {'mensaje': 'Error interno del servidor', "status": 500}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)