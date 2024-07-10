from flask import Flask, request, jsonify, make_response
from models import db, Carpincho, Ayudante, Mostrador, Nivel
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

port = 5000
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://esobrad:esobrad@localhost:5432/cya'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
ayudante =Ayudante(id_ayudante=1, nombre='Peron', costo=1000, bonificacion=50, obtenido=False)


@app.route('/', methods=["GET"])
def hello_world():
    return 'index.html'

@app.route("/carpincho", methods=["GET"])
def carpincho():
    try:
        carpincho = Carpincho.query.get(1)
        carpincho_data = {
            'id': carpincho.id,
            'nombre': carpincho.nombre,
            'plata': carpincho.plata,
            'tiempo_de_coccion': carpincho.tiempo_de_coccion,
            'nivel': carpincho.nivel
        }
        return jsonify(carpincho_data)
    except:
        return jsonify({'mensaje': 'El carpincho no existe'})

@app.route('/carpincho', methods=["POST"])
def nuevo_carpincho():
    try:
        data = request.json
        nombre = data.get('nombre')
        carpincho = Carpincho.query.get(1)
        if carpincho is None:
            return jsonify({'message': 'error'})
        carpincho.nombre = nombre
        db.session.commit()
        print(f"Nombre recibido: {nombre}")
        return jsonify({'message': 'Carpincho actualizado', 'carpincho': {'id': carpincho.id, 'nombre': carpincho.nombre}})
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el carpincho', 'error': str(e)}), 500
    
"""@app.route('/juego/<id>/nuevo_asado/<id_asado>', methods=["POST"])
def nuevo_asado(id_asado, id):
    try:
        tipo_asado = TipoAsado.query.get(id_asado)
        carpincho = Carpincho.query.get(id)
        fecha_cosecha = datetime.datetime.now() + datetime.timedelta(seconds = carpincho.tiempo_de_coccion)
        nuevo_asado = Asado(id = id, tipo_asado_id = id_asado, fecha_cosecha = fecha_cosecha)
        db.session.add(nuevo_asado)
        db.session.commit()
        print(f"Nombre recibido: {nombre}")
        return jsonify({'message': 'Carpincho actualizado', 'carpincho': {'id': carpincho.id, 'nombre': carpincho.nombre}})
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el carpincho', 'error': str(e)}), 500"""

@app.route('/carpincho/ayudante/<id_ayudante>', methods=["POST"])
def comprar_ayudante():

    try:
        data = request.json
        nombre = data.get('nombre')
        obtenido = data.get('obtenido')
        ayudante = Ayudante.query.get(id)
        if ayudante is None:
            return jsonify({'message': 'error: no existe ese ayudante'})
        ayudante.nombre = nombre
        ayudante.obtenido = obtenido
        db.session.commit()
        print(f"Nombre recibido: {nombre}")
        print(f"Obtenido: {obtenido}")
        return jsonify({'message': 'Ayudante comprado', 'ayudante': {'id': ayudante.id_ayudante, 'nombre': ayudante.nombre}})
    except Exception as e:
        return jsonify({'message': 'Error al comprar el ayudante', 'error': str(e)})
    
@app.route('/carpincho/nivel/<id_nivel>', methods=["POST"])
def comprar_nivel(id_nivel):

    try:
        nivel = Nivel.query.get(id_nivel)
        carpincho = Carpincho.query.get(nivel.id)
        if nivel is None:
            return jsonify({'message': 'error: no existe ese nivel'})
        nivel.obtenido = True 
        carpincho.nivel = nivel
        db.session.commit()
        print(f"Nivel comprado: {nivel}")
        return jsonify({'message': 'Nivel comprado', 'nivel': {'id': nivel.id_nivel, 'obtenido': nivel.obtenido}})
    except Exception as e:
        return jsonify({'message': 'Error al comprar el nivel', 'error': str(e)})

if __name__ == '__main__':
    print('starting server...')
    db.init_app(app)
    with app.app_context():
        #db.drop_all()
        db.create_all()
    print('started...')
    app.run(host='0.0.0.0', debug=True, port=port)
    