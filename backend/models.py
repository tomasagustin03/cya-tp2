import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Carpincho(db.model):
    _tablename_ = 'carpinchos'
    nombre = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    plata = db.Column(db.Integer, nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    fecha_de_creacion = db.Column(db.datetime, default = datetime.datetime.now()) 

class Asado(db.model):
    _tablename_ = 'tipos_de_asados'
    id = db.Column(db.Integer, primary_key=True)
    tipo_de_asado = db.Column(db.String(255), nullable=False)
    tiempo_de_preparacion = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    fecha_de_creacion = db.Column(db.datetime, default = datetime.datetime.now())

class Id_carpincho(db.model):
    _tablename_ = 'acompañante'
    id = db.Column(db.Integer, primary_key=True)
    id_carpincho = db.Column(db.Integer, db.ForeignKey('id_carpincho'))
    id_tipo_acompañante = db.Column(db.Integer, db.ForeignKey('id_tipo_acompañante'))
    fecha_venta= db.Column(db.datetime, default = datetime.datetime.now())
    fecha_de_creacion = db.Column(db.datetime, default = datetime.datetime.now())

class Nivel(db.mo0del):
    _tablename_ = 'nivel'
    tiempo_de_preparacion = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Integer, nullable=False)