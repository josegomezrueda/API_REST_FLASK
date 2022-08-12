

from datetime import datetime
from lib2to3.pgen2 import token
from flask import Flask, jsonify, request
from db import Session, engine, connection_db
import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime


app=Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'

#DB
app.config['SQLALCHEMY_DATABASE_URI'] = connection_db
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db=SQLAlchemy(app)
session = Session()
from models import *

@app.route('/hola', methods=['GET'])
def hola():
    return jsonify({"mensaje":"Endpoint desde hola"})


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': ''})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'No has enviado el token'})
        return f(data['public_id'],*args, **kwargs)
   return decorator


@app.route('/login', methods=['GET'])
def login_user():

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"respuesta":"Could not verify"})
    with engine.connect() as con:
        user = con.execute(f"select * from usuario where username = '{auth.username}' ").one()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id':user[1], 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})
    else:
        return jsonify({"respuesta":"Contraseña incorrecta"})
    return jsonify({"respuesta":"Login requerido"})


@app.route('/create_user', methods=['POST'])
@token_required
def create_user(current_user):
    if current_user == "administrador":
        data=json.loads(request.data)
        
        if 'username' not in data:
            return jsonify({"respuesta":"No estás enviando el username"})
        if 'password' not in data:
            return jsonify({"respuesta":"No estás enviando el password"})

        if len(data['username']) == 0:
            return jsonify({"respuesta":"Username no puede estar vacío"})
        if len(data['password']) == 0:
            return jsonify({"respuesta":"password no puede estar vacío"})

        with engine.connect() as con:
            hash_password=generate_password_hash(data['password'], method="sha256")
            nuevo_usuario = Usuario(username=data['username'], password=hash_password)
            session.add(nuevo_usuario)
            try:
                session.commit()
            except:
                return jsonify({"respuesta":"Usuario ya creado en la base de datos"})
        return jsonify({"respuesta":"Usuario creado correctamente"})
    else:
        return jsonify({"respuesta":"Usuario no tiene permitido crear más usuarios"})

@app.route('/obtener_venta', methods=['GET'])
@token_required
def obtener_venta(current_user):
    data=json.loads(request.data)
    if 'username' not in data:
        return jsonify({"respuesta": "Username no enviado, validar datos!"})
    
    with engine.connect() as con:
        obtener_usuario = f"select * from usuario where username = '{data['username']}'"
        respuesta = con.execute(obtener_usuario).one()
        obtener_venta=f"select venta from ventas where username_id = '{respuesta[0]}'"
        respuestas_ventas = con.execute(obtener_venta)
        respuestas_ventas=[i[0]for i in respuestas_ventas]
        return jsonify({"ventas_usuario":{"usuario":data['username'], "ventas":respuestas_ventas}})

if __name__=="__main__":
    app.run(debug=True)