from flask import Flask, request, render_template, jsonify
from models import db, Carpincho, Ayudante, Mostrador, Nivel

app = Flask(__name__, template_folder='../frontend')
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://esobrad:esobrad@localhost:5432/cya'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
ayudante =Ayudante(id_ayudante=1, nombre='Peron', costo=1000, bonificacion=50, obtenido=False)


@app.route('/', methods=["GET"])
def hello_world():
    return 'index.html'

@app.route('/carpincho', methods=["GET"])
def edicion_carpincho():
    return 'esta es mi pagina'

@app.route('/carpincho', methods=["POST"])
def nuevo_carpincho():
    #data = request.get_json()
    #nombre = data.get('nombre')
    nombre = request.json.get("nombre")
    print(nombre)
    return 'esta es mi pagina'


if __name__ == '__main__':
    print('starting server...')
    db.init_app(app)
    with app.app_context():
        #db.drop_all()
        db.create_all()
    print('started...')
    app.run(host='0.0.0.0', debug=True, port=port)