

from datetime import datetime
from lib2to3.pgen2 import token
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Blueprint,abort
from db import Session, engine, connection_db
import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt
import requests
import datetime
from flask_restplus import Api, Resource, fields
from api.functions import *

authorizations = {
    'apiKey': {
        'type':'apiKey',
        'in':'header',
        'name':'x-access-token'
    }
}

app=Flask(__name__)
app.config['SECRET_KEY']='Th1s1ss3cr3t'

#DB
app.config['SQLALCHEMY_DATABASE_URI'] = connection_db
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db=SQLAlchemy(app)
session_bd = Session()

from models import *
bp_api = Blueprint('Api',__name__,url_prefix="/Api")

api = Api(bp_api, version="1.0", title="Api",description="End Points", authorizations=authorizations)
app.register_blueprint(bp_api)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'})
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            abort(401, {'message' : 'Token is invalid!'})
        return f(data, *args, **kwargs)

    return decorated


ns_model = api.namespace('Methods', description='Metodos')
ns_model_venta = api.namespace('API_Ventas', description='Ventas')
ns_model_usuario = api.namespace('API_Usuario', description='Usuarios')

class VerificacionDatos():
    Login = api.model('login',{
        "username":fields.String(description=u"username", required=True),
        "password":fields.String(description=u"password", required=True)
    })
    Crear_Venta = api.model('venta',{
        "id_username": fields.Integer(description=u"id_username", required=True),
        "venta": fields.Integer(description=u"valor de la cuenta", required=True),
        "ventas_productos": fields.Integer(description=u"venta producto", required=True),
    })
    Cambiar_Venta = api.model('cambiar venta',{
        "id": fields.Integer(description=u"id venta", required=True),
        "venta": fields.Integer(description=u"valor de la cuenta", required=True)
    })
    Eliminar_Venta = api.model('eliminar venta',{
        "id": fields.Integer(description=u"id venta", required=True),
    })
    Validar_Usuario = api.model('validar usuario',{
        "username": fields.String(description=u"usuario", required=True),
    })
    
@ns_model.route('/Login/')
@api.doc(description="Correo y contraseña")
class Login(Resource):
    @ns_model.expect(VerificacionDatos.Login, Validate=True)
    def post(self):
        auth=request.json
        valida = valida_user(auth["username"],auth["password"])
        if 'token' in valida:
            return jsonify(valida)
        return abort(401,'Credenciales incorrectas!')

@ns_model_usuario.route('/CreateUser/')
class CrearUsuario(Resource):
    @api.doc(description="Correo y contraseña", security='apiKey')
    @ns_model_usuario.expect(VerificacionDatos.Login, Validate=True)
    @token_required
    def post(data, self):
        if data['rol']=='admin':
            usuario = request.json
            usuario_creado = crear_usuario(usuario['username'], usuario['password'])
            return jsonify (usuario_creado)
        else:
            return {"respuesta":"No tiene permisos"}

@ns_model_usuario.route('/ValidarUsuario/')
@api.doc(description="Usuario")
class ValidarUsuario(Resource):
    @ns_model_usuario.expect(VerificacionDatos.Validar_Usuario, Validate=True)
    def post(self):
        body = request.json
        user = usuario(body['username'])
        return jsonify (user)

@ns_model_venta.route('/Ventas/')
@api.doc(description="Obtiene todas las ventas")
class Venta(Resource):
    @token_required
    @api.doc(security='apiKey')
    def get(data,self):
        print(data)
        if data['rol']=='admin':
            venta = obtener_venta()
            return jsonify (venta)
        else:
            return {"respuesta":"No tiene permisos"}, 401
            
    @ns_model_venta.expect(VerificacionDatos.Crear_Venta, Validate=True)
    def post(self):
        datos = request.json
        venta = crear_venta(datos["id_username"],datos["venta"],datos["ventas_productos"])
        return jsonify (venta)
    @ns_model_venta.expect(VerificacionDatos.Cambiar_Venta, Validate=True)
    def put(self):
        datos = request.json
        venta = actualizar_venta(datos["id"],datos["venta"])
        return jsonify (venta)
    @ns_model_venta.expect(VerificacionDatos.Eliminar_Venta, Validate=True)
    def delete(self):
        dato = request.json
        venta = eliminar_venta(dato["id"])
        return jsonify (venta)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')