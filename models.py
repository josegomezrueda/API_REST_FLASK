from sqlalchemy import Column, String, Integer
from db import Base, engine
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Usuario(db.Model):
    __tablename__='usuario'
    id = db.Column(Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(70), unique=False)
    password = db.Column(db.String(200))
    ventas = relationship('Ventas', backref="usuario", cascade="delete, merge")
class Ventas(db.Model):
    __tablename__='ventas'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username_id=db.Column(db.Integer, ForeignKey("usuario.id", ondelete="CASCADE"))
    venta=db.Column(db.Integer)
    ventas_productos = db.Column(db.Integer)
# Base.metadata.create_all(engine)