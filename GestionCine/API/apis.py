from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route('/getPeliculas', methods=['GET'])
def getPelicula():
    try:
        if request.method == 'GET':
            retorno = [
                        {
                            "titulo": "Your Name",
                            "director": "Makoto Shinkai",
                            "anio": "2016",
                            "fecha": "2023-06-28",
                            "hora": "15:30",
                            "imagen": "https://m.media-amazon.com/images/M/MV5BNGYyNmI3M2YtNzYzZS00OTViLTkxYjAtZDIyZmE1Y2U1ZmQ2XkEyXkFqcGdeQXVyMTA4NjE0NjEy._V1_.jpg",
                            "precio": "55"
                        },
                        {
                            "titulo": "Demon Slayer: Mugen Train",
                            "director": "Haruo Sotozaki",
                            "anio": "2020",
                            "fecha": "2023-06-28",
                            "hora": "16:45",
                            "imagen": "https://m.media-amazon.com/images/M/MV5BODI2NjdlYWItMTE1ZC00YzI2LTlhZGQtNzE3NzA4MWM0ODYzXkEyXkFqcGdeQXVyNjU1OTg4OTM@._V1_FMjpg_UX1000_.jpg",
                            "precio": "40"
                        },
                        {
                            "titulo": "Attack on Titan: The Final Season",
                            "director": "Masashi Koizuka",
                            "anio": "2020",
                            "fecha": "2023-06-28",
                            "hora": "18:00",
                            "imagen": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/3542/35422068_so.jpg",
                            "precio": "60"
                        }
                    ]
        else:
            retorno = {'mensaje': 'Error en la petición, método incorrecto'}
        return jsonify(retorno)
    except:
        return {"mensaje": "Error interno en el servidor", "status": 500}
    
    
@app.route('/getSalas', methods=['GET'])
def getSala():
    try:
        if request.method == 'GET':
            retorno = [
                {
  "cines": {
    "cine": {
      "nombre": "Cine ABC",
      "salas": {
        "sala": [
          {
            "numero": "#USAC_IPC2_20211576_1",
            "asientos": "115"
          },
          {
            "numero": "#USACIPC2_202212333_2",
            "asientos": "80"
          },
          {
            "numero": "#USACIPC2_202212333_3",
            "asientos": "120"
          }
        ]
      }
    }
  }
}

            ]
        else:
            retorno = {"mensaje": "Error de la petición, método incorrecto"}
        return jsonify(retorno)
    except:
        return {'mensaje': 'Error interno del servidor', "status": 500}
    
@app.route('/getTarjetas', methods=['GET'])
def getTarjeta():
    try:
        if request.method == 'GET':
            retorno = [
 {
 "tipo": "Debito",
 "numero": "1234567890123456",
 "titular": "John Doe",
 "fecha_expiracion": "12/2024"
 },
 {
 "tipo": "Credito",
 "numero": "9876543210987654",
 "titular": "Jane Smith",
 "fecha_expiracion": "08/2023"
 }
 ]

        else:
            retorno = {"mensaje": "Error de la petición, método incorrecto"}
        return jsonify(retorno)
    except:
        return {'mensaje': 'Error interno del servidor', "status": 500}
    
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
    app.run(host='0.0.0.0', port=5010)
