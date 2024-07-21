import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Carpincho(db.Model):
    __tablename__ = 'carpinchos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    plata = db.Column(db.Integer, nullable=False)

class Ayudante(db.Model):
    __tablename__ = 'ayudantes'
    id_ayudante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=False)
    bonificacion = db.Column(db.Integer, nullable=False)
    obtenido = db.Column(db.Boolean, nullable=False)

class Mostrador(db.Model):
    __tablename__ = 'mostrador'
    id_asado = db.Column(db.Integer, primary_key=True)
    id_ayudante = db.Column(db.Integer, db.ForeignKey('ayudantes'))
    platos = db.Column(db.Integer, nullable=False)

class Nivel(db.Model):
    __tablename__ = 'nivel'
    id_nivel = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('carpinchos'))
    obtenido = db.Column(db.Boolean, nullable=False)
    tiempo_de_coccion = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Integer, nullable=False)