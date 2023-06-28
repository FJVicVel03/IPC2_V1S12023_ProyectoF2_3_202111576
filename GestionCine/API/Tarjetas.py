from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

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
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
