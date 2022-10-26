from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import jwt 
from db import engine
from querys import *

llave='Th1s1ss3cr3t'

def valida_user(username, password):
    with engine.connect() as con:
        try:
            user = con.execute(f"select * from usuario where username = '{username}' ").one()
        except:
            user = None
    if user:
        if check_password_hash(user[2], password):
            token = jwt.encode({'public_id':user[1], 'rol': user[3],'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, llave)
            return {'token':token.decode('UTF-8')}
            
    return {"respuesta":"Contraseña incorrecta"}

def crear_usuario(username, password):
    hash_password=generate_password_hash(password, method='sha256')
    with engine.connect() as con:
        try:
            engine.execute(insertar_usuario(username, hash_password))
        except:
            return {"respuesta":"Usuario ya creado en la base de datos"}
        return {"respuesta":"Usuario creado correctamente"}

def obtener_venta():
    respuesta_ventas=engine.execute(obtener_ventas())
    lista = list()
    for i in respuesta_ventas:
        lista.append({"ID_VENTA":i[0], "valor_venta":i[2]})
    return {"Ventas":lista}

def crear_venta(username_id, venta, ventaprod):
    try:
        venta=engine.execute(create_venta(username_id, venta, ventaprod))
    except:
        return {"Respuesta":"Fallo"}
    return {"Respuesta":"Venta creada"}

def actualizar_venta(id, venta):
    try:
        venta_act=engine.execute(update_venta(id, venta))
    except:
        return {"Respuesta":"Fallo actualización"}
    return {"Respuesta":"Venta actualizada"}

def eliminar_venta(id):
    try:
        venta_act=engine.execute(delete_venta(id))
    except:
        return {"Respuesta":"Venta no eliminada"}
    return {"Respuesta":"Venta eliminada"}

def usuario(username):
    print(username)
    try:
        usuario = engine.execute(user_valida(username)).one()
    except:
        return {"Respuesta":"No eliminada"}
    return {"rol":usuario[3]}
