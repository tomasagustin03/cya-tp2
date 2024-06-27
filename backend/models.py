import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Carpincho(db.model):
    _tablename_ = 'carpinchos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    tiempo_de_coccion = db.Column(db.Integer, nullable=False)

class Ayudante(db.model):
    _tablename_ = 'tipos_de_ayudantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    bonificacion = db.Column(db.Integer, nullable=False)

class Asado(db.model):
    _tablename_ = 'venta_de_asados'
    id = db.Column(db.Integer, primary_key=True)
    id_carpincho = db.Column(db.Integer, db.ForeignKey('carpinchos'))
    ganancia = db.Column(db.Integer, nullable=False)
    fecha_de_venta = db.Column(db.datetime, default = datetime.datetime.now())

class Compra(db.model):
    _tablename_ = 'compra_de_personajes'
    id = db.Column(db.Integer, primary_key=True)
    id_carpincho = db.Column(db.Integer, db.ForeignKey('carpinchos'))
    id_ayudante = db.Column(db.Integer, db.ForeignKey('ayudantes'))
    costo = db.Column(db.Integer, nullable=False)

class Nivel(db.mo0del):
    id = db.Column(db.Integer, primary_key=True)
    id_carpincho = db.Column(db.Integer, db.ForeignKey('carpinchos'))