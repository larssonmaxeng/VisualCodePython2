from app import database 
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
class Pedido(database.db.Model):
  __tablename__="pedido"
  id = database.db.Column(database.db.Integer, primary_key=True)
  pedido = database.db.Column(database.db.String(100))
  def __init__(self, pedido):
    self.pedido = pedido

class PacotesDeEntrega(database.db.Model):
  __tablename__="PacotesDeEntrega"
  id=database.db.Column(database.db.Integer, primary_key=True)
  descricao=database.db.Column(database.db.String(500), unique=True)
  unidadeBasica = database.db.Column(database.db.String(10))
  pacote = database.db.Column(database.db.String(50))
  conversao= database.db.Column(database.db.Float)
  volume=database.db.Column(database.db.Float)
  base=database.db.Column(database.db.Float)
  largura=database.db.Column(database.db.Float)
  altura=database.db.Column(database.db.Float)
  formato=database.db.Column(database.db.String(50))
  empolamento=database.db.Column(database.db.Float)
  preco = database.db.Column(database.db.Float)
  alturaMaxima = database.db.Column(database.db.Float)
  areaBaseMaxima = database.db.Column(database.db.Float)  
  def __init__ (self,descricao,unidadeBasica,pacote,conversao, base, largura, 
                altura, formato, empolamento, preco, alturaMaxima, areaBaseMaxima):
      self.descricao = descricao
      self.unidadeBasica=unidadeBasica
      self.pacote=pacote
      self.conversao=conversao
      self.base=base 
      self.largura=largura 
      self.altura=altura 
      self.formato=formato 
      self.empolamento=empolamento
      self.preco=preco
      self.alturaMaxima=alturaMaxima
      self.areaBaseMaxima=areaBaseMaxima
  
class PedidoMaterial(database.db.Model):
  __tablename__="pedidoMaterial"
  id = database.db.Column(database.db.Integer, primary_key=True)
  descricao=database.db.Column(database.db.String(500))
  unid=database.db.Column(database.db.String(100))
  qtde=database.db.Column(database.db.Float)
  mes=database.db.Column(database.db.String(100))
  objectId=database.db.Column(database.db.String(100))
  pedidoGuid=database.db.Column(database.db.String(100))
  pedido=database.db.Column(database.db.String(100))
  nivel00=database.db.Column(database.db.String(100))
  nivel01=database.db.Column(database.db.String(100))
  nivel02=database.db.Column(database.db.String(100))
  idElement=database.db.Column(database.db.Integer)
  urn=database.db.Column(database.db.String(250))
  pedidoId = database.db.Column(database.db.Integer, ForeignKey("pedido.id", name="fk_material_pedido_01"))
  def __init__ (self, descricao,     unid,     qtde,     mes,     objectId,     pedidoGuid,   
    pedido,     nivel01,     nivel02,     idElement, pedidoId, urn, nivel00):
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
    self.nivel00 = nivel00

  def __repr__ (self):
    return self.id