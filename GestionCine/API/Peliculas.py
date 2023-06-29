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
                            "imagen": "https://example.com/your_name.png",
                            "precio": "55"
                        },
                        {
                            "titulo": "Demon Slayer: Mugen Train",
                            "director": "Haruo Sotozaki",
                            "anio": "2020",
                            "fecha": "2023-06-28",
                            "hora": "16:45",
                            "imagen": "https://example.com/demon_slayer.png",
                            "precio": "40"
                        },
                        {
                            "titulo": "Attack on Titan: The Final Season",
                            "director": "Masashi Koizuka",
                            "anio": "2020",
                            "fecha": "2023-06-28",
                            "hora": "18:00",
                            "imagen": "https://example.com/attack_on_titan.png",
                            "precio": "60"
                        }
                    ]
        else:
            retorno = {'mensaje': 'Error en la petición, método incorrecto'}
        return jsonify(retorno)
    except:
        return {"mensaje": "Error interno en el servidor", "status": 500}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
