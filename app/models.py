from app import database 
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
class Pedido(database.db.Model):
  __tablename__="pedido"
  id = database.db.Column(database.db.Integer, primary_key=True)
  pedido = database.db.Column(database.db.String(100))
  def __init__(self, pedido):
    self.pedido = pedido

class PedidoMaterial(database.db.Model):
  __tablename__="pedidoMaterial"
  id = database.db.Column(database.db.Integer, primary_key=True)
  descricao=database.db.Column(database.db.String(100))
  unid=database.db.Column(database.db.String(100))
  qtde=database.db.Column(database.db.Float)
  mes=database.db.Column(database.db.String(100))
  objectId=database.db.Column(database.db.String(100))
  pedidoGuid=database.db.Column(database.db.String(100))
  pedido=database.db.Column(database.db.String(100))
  nivel01=database.db.Column(database.db.String(100))
  nivel02=database.db.Column(database.db.String(100))
  idElement=database.db.Column(database.db.Integer)
  urn=database.db.Column(database.db.String(250))
  pedidoId = database.db.Column(database.db.Integer, ForeignKey("pedido.id", name="fk_material_pedido_01"))
  def __init__ (self, descricao,     unid,     qtde,     mes,     objectId,     pedidoGuid,   
    pedido,     nivel01,     nivel02,     idElement, pedidoId, urn):
    self.descricao = descricao
    self.unid=unid
    self.qtde=qtde
    self.mes=mes
    self.objectId=objectId
    self.pedidoGuid=pedidoGuid
    self.pedido=pedido
    self.nivel01=nivel01
    self.nivel02=nivel02
    self.idElement=idElement
    self.urn=urn
    self.pedidoId = pedidoId

  def __repr__ (self):
    return self.id