from sqlalchemy import desc
from flask import Flask, request, jsonify, make_response
from models import db, Carpincho, Ayudante, Mostrador, Nivel
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

port = 5000
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://esobrad:esobrad@localhost:5432/cya'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

@app.route("/carpincho", methods=["GET"])
def carpincho():
    try:
        carpincho = Carpincho.query.get(1)
        carpincho_data = {
            'id': carpincho.id,
            'nombre': carpincho.nombre,
            'plata': carpincho.plata,
            'nivel': carpincho.nivel
        }
        return jsonify(carpincho_data)
    except:
        return jsonify({'mensaje': 'El carpincho no existe'}), 404

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
    
@app.route('/mostrador', methods=["GET"])
def obtener_mostrador():
    try:
        mostrador = Mostrador.query.order_by(Mostrador.id_asado).all()
        print(mostrador)
        ayudante = Ayudante.query.order_by(Ayudante.id_ayudante).all()
        print(ayudante)
        mostrador_data = []
        for asado in mostrador:
            imagen_url = ayudante[asado.id_ayudante - 1].imagen_url
            mostrador_data.append({
                'imagen_url': imagen_url,
                'platos': asado.platos
            })
        print(mostrador_data)
        return jsonify(mostrador_data)
    except Exception as e:
        return jsonify({'message': 'Error al obtener el mostrador', 'error': str(e)}), 404

@app.route('/mostrador', methods=["POST"])
def agregar_asado():
    try:
        id_ayudante = Ayudante.query.where(Ayudante.obtenido == True).order_by(desc(Ayudante.id_ayudante)).first().id_ayudante
        asado = Mostrador.query.get(id_ayudante)
        if asado is None:
            return jsonify({'message': 'error'})
        asado.platos += 1
        db.session.commit()
        return jsonify({'message': 'Asado actualizado', 'asado': {'id': asado.id_asado, 'platos': asado.platos}})
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el asado', 'error': str(e)}), 500
    
@app.route('/mostrador', methods=["DELETE"])
def eliminar_asado():
    try:
        asado = Mostrador.query.where(Mostrador.platos > 0).order_by(Mostrador.id_asado).first()
        valor_asado = Ayudante.query.get(asado.id_ayudante).bonificacion
        if asado is None:
            return jsonify({'message': 'error'})
        asado.platos -= 1
        db.session.commit()
        return jsonify({'message': 'Asado actualizado', 'asado': {'id': asado.id_asado, 'platos': asado.platos, 'valor_asado': valor_asado}})
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el asado', 'error': str(e)}), 500
    
@app.route('/imagen', methods=['GET'])
def get_images():
    try:
        id_ayudante = Ayudante.query.where(Ayudante.obtenido == True).order_by(desc(Ayudante.id_ayudante)).first().id_ayudante
        imagen = Ayudante.query.get(id_ayudante).imagen_url
        print(imagen)
        return jsonify(imagen)
    except Exception as e:
        return jsonify({'message': 'Error al obtener la imagen', 'error': str(e)}), 404

@app.route('/plata', methods=['GET'])
def get_plata():
    try:
        carpincho = Carpincho.query.get(1)
        plata = carpincho.plata
        return jsonify(plata)
    except Exception as e:
        return jsonify({'message': 'Error al obtener la plata', 'error': str(e)}), 404

@app.route('/niveles', methods=['GET'])
def get_niveles():
    try:
        niveles = Nivel.query.order_by(Nivel.id_nivel).all()
        niveles_data = []
        estado = 2
        for nivel in niveles:
            if (nivel.obtenido):
                print(niveles_data) 
                niveles_data.append({
                    'id_nivel': nivel.id_nivel,
                    'estado': 3,
                    'costo': nivel.costo,
                    'tiempo_de_coccion': nivel.tiempo_de_coccion
                })
            else:
                niveles_data.append({
                    'id_nivel': nivel.id_nivel,
                    'estado': estado,
                    'costo': nivel.costo,
                    'tiempo_de_coccion': nivel.tiempo_de_coccion
                })
                estado = 1
        return jsonify(niveles_data)
    except Exception as e:
        return jsonify({'message': 'Error al obtener los niveles', 'error': str(e)}), 404

@app.route('/ultimonivel', methods=['GET'])
def ultimo_nivel():
    try:
        ultimo_nivel = Nivel.query.where(Nivel.obtenido == True).order_by(desc(Nivel.id_nivel)).first()
        if ultimo_nivel:
            return jsonify({'mensaje': 'Exito', 'id_ultimo_nivel': ultimo_nivel.id_nivel, 'costo': ultimo_nivel.costo, 'tiempo_de_coccion': ultimo_nivel.tiempo_de_coccion})
        else:
            return jsonify({'mensaje': 'Exito', 'id_ultimo_nivel': ultimo_nivel.id_nivel, 'costo': ultimo_nivel.costo, 'tiempo_de_coccion': ultimo_nivel.tiempo_de_coccion})
    except Exception as e:
        return jsonify({'message': 'Error al obtener el ultimo nivel', 'error': str(e)}), 404

@app.route('/reiniciar', methods=['PUT'])
def reiniciarprogreso():
    try:
        carpincho = Carpincho.query.get(1)
        print(carpincho)
        carpincho.plata = 0
        carpincho.nombre = 'Asador'

        ayudantes = Ayudante.query.where(Ayudante.id_ayudante > 1)
        for ayudante in ayudantes:
            ayudante.obtenido = False

        mostrador = Mostrador.query.all()
        for plato in mostrador:
            plato.platos = 0

        niveles = Nivel.query.where(Nivel.id_nivel > 1)
        for nivel in niveles:
            nivel.obtenido = False

        db.session.commit()
        return jsonify({'message' : 'Progreso reiniciado'})
    except Exception as e:
        return jsonify({'message': 'Error al reiniciar el progreso', 'error': str(e)}), 500
 
@app.route('/plata', methods=['PUT'])
def put_plata():
    try:
        data = request.json
        print(data)
        plata = data.get('valor')
        carpincho = Carpincho.query.get(1)
        if carpincho is None:
            return jsonify({'message': 'error'})
        carpincho.plata += plata
        db.session.commit()
        return jsonify({'message': 'Plata actualizada', 'carpincho': {'id': carpincho.id, 'plata': carpincho.plata}})
    except Exception as e:
        return jsonify({'message': 'Error al actualizar la plata', 'error': str(e)}), 500
    
@app.route('/islas', methods=['GET'])
def get_islas():
    try:
        ayudantes = Ayudante.query.order_by(Ayudante.id_ayudante).all()
        islas_data = []
        estado = 2
        for ayudante in ayudantes:
            if (ayudante.obtenido):
                islas_data.append({
                    'id_ayudante': ayudante.id_ayudante,
                    'estado': 3,
                    'costo': ayudante.costo
                })
            else:
                islas_data.append({
                    'id_ayudante': ayudante.id_ayudante,
                    'estado': estado,
                    'costo': ayudante.costo
                })
                estado = 1
        return jsonify(islas_data)
    except Exception as e:
        return jsonify({'message': 'Error al obtener las islas', 'error': str(e)}), 404

@app.route('/comprarayudante', methods=["POST"])
def comprar_ayudante():
    try:
        data = request.json
        id = data.get('id')
        ayudante = Ayudante.query.get(id)
        if ayudante is None:
            return jsonify({'message': 'error: no existe ese ayudante', 'exitoso': 'false'})
        ayudante.obtenido = True
        db.session.commit()
        return jsonify({'message': 'Ayudante comprado', 'ayudante': {'id': ayudante.id_ayudante, 'nombre': ayudante.nombre}, 'exitoso': 'true'})
    except Exception as e:
        return jsonify({'message': 'Error al comprar el ayudante', 'error': str(e), 'exitoso': 'false'}), 500
    
@app.route('/carpincho/nivel/<id_nivel>', methods=["POST"])
def comprar_nivel(id_nivel):

    try:
        nivel = Nivel.query.get(id_nivel)
        carpincho = Carpincho.query.get(nivel.id)
        if nivel is None:
            return jsonify({'message': 'error: no existe ese nivel', 'exito': False})
        nivel.obtenido = True 
        carpincho.nivel = nivel.id_nivel
        db.session.commit()
        print(f"Nivel comprado: {nivel}")
        return jsonify({'exito': True, 'nivel': {'id': nivel.id_nivel, 'obtenido': nivel.obtenido}})
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print('starting server...')
    db.init_app(app)
    with app.app_context():
        ##db.drop_all()
        db.create_all()
    print('started...')
    app.run(host='0.0.0.0', debug=True, port=port)
    