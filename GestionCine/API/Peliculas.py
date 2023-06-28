from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route('/getPeliculas', methods=['GET'])
def getPelicula():
    try:
        if request.method == 'GET':
            retorno = {
                "categoria": [
                    {
                        "nombre": "Aventura",
                        "peliculas": {
                            "pelicula": [
                                {
                                    "titulo": "Las momias del faraon",
                                    "director": "Luc Besson",
                                    "anio": "2010",
                                    "fecha": "2023-02-05",
                                    "hora": "19:30",
                                    "imagen": "https://es.web.img2.acsta.net/medias/nmedia/18/78/77/56/19477844.jpg",
                                    "precio": "52"
                                },
                                {
                                    "titulo": "Aladdin",
                                    "director": "Chad Stahelski",
                                    "anio": "2019",
                                    "fecha": "2023-06-06",
                                    "hora": "20:00",
                                    "imagen": "https://m.media-amazon.com/images/M/MV5BMjQ2ODIyMjY4MF5BMl5BanBnXkFtZTgwNzY4ODI2NzM@._V1_FMjpg_UX1000_.jpg",
                                    "precio": "55"
                                }
                            ]
                        }
                    },
                    {
                        "nombre": "Infantil",
                        "peliculas": {
                            "pelicula": [
                                {
                                    "titulo": "Sing 2",
                                    "director": "Garth Jenningsr",
                                    "anio": "2021",
                                    "fecha": "2023-04-05",
                                    "hora": "14:30",
                                    "imagen": "https://www.universalpictures.com.ar/tl_files/content/movies/sing2/posters/01.jpg",
                                    "precio": "75"
                                },
                                {
                                    "titulo": "spirited away",
                                    "director": "Hayao Miyazaki",
                                    "anio": "2001",
                                    "fecha": "2023-07-07",
                                    "hora": "21:15",
                                    "imagen": "https://cinematecadebogota.gov.co/sites/default/files/styles/318_x_460/public/afiches/screen_shot_2021-07-30_at_4.18.59_pm.png?itok=9pijB2o2",
                                    "precio": "82"
                                }
                            ]
                        }
                    }
                ]
            }
        else:
            retorno = {"mensaje": "Error de la petición, método incorrecto"}
        return jsonify(retorno)
    except:
        return {'mensaje': 'Error interno del servidor', "status": 500}
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
