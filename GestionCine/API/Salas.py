from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

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
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)
