from flask import Flask, request, jsonify
from models import db, Carpincho, Ayudante, Asado, Compra, Nivel

app = Flask(__name__)
port = 5000
app.config('SQLALCHEMY_DATABASE_URI') 
