import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Carpincho(db.Model):
    __tablename__ = 'carpinchos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    tiempo_de_coccion = db.Column(db.Integer, nullable=False)

class Ayudante(db.Model):
    __tablename__ = 'ayudantes'
    id_ayudante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    bonificacion = db.Column(db.Integer, nullable=False)

class Asado(db.Model):
    __tablename__ = 'venta_de_asados'
    id_asado = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('carpinchos'))
    ganancia = db.Column(db.Integer, nullable=False)
    fecha_de_venta = db.Column(db.DateTime, default = datetime.datetime.now())

class Compra(db.Model):
    __tablename__ = 'compra_de_personajes'
    id_compra = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('carpinchos'))
    id_ayudante = db.Column(db.Integer, db.ForeignKey('ayudantes'))
    costo = db.Column(db.Integer, nullable=False)

class Nivel(db.Model):
    __tablename__ = 'nivel'
    id_nivel = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('carpinchos'))