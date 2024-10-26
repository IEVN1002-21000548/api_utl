from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

""" from flask_cors import CORS """

from config import config

app = Flask(__name__)

# Configuración de la conexión MySQL
con = MySQL(app)

@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql = 'SELECT * FROM alumnos'
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            }
            alumnos.append(alumno)  # Agregar cada alumno dentro del bucle
        
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos', 'exito': True})

    except Exception as ex:
        print("Error de conexión:", ex)  # Para depuración
        return jsonify({"message": f"Error al conectar la base de datos: {ex}", 'exito': False})

# Manejo de error 404
def pagina_no_encontrada(error):
    return "<h1> La página que estás buscando no existe</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='127.0.0.1', port=5000, debug=True)
