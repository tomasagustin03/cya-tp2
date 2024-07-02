from flask import Flask, request, jsonify
from models import db, Carpincho, Ayudante, Asado, Compra, Nivel

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://esobrad:esobrad@localhost:5432/cya'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/')
def hello_world():
    return 'esta es mi pagina'

if __name__ == '__main__':
    print('starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print('started...')
    app.run(host='0.0.0.0', debug=True, port=port)