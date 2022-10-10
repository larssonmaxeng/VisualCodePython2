import json
import requests
from json import *
from urllib import response
from pyexpat import model
from flask import Blueprint
from flask import request, render_template, redirect, jsonify, make_response
from app import database
from app import models as tabelas
bp_materialPedidos = Blueprint("materiaisPedidos", __name__, template_folder="templates")

@bp_materialPedidos.route('/createMaterialPedido', methods=['GET','POST'])
def createMaterialPedido():
   
    req = request.get_json()
    pedido = ''
    for i in req:
        pedido = i["pedido"] 
    database.db.session.execute("delete from pedidoMaterial where pedido = '"+pedido+"'")
    database.db.session.commit()
    
    for song in req:
        pedido  = tabelas.PedidoMaterial(song['descricao'],
                      song['unid'],
                      song['qtde'],
                      song['mes'],
                      song['objectId'],
                      song['pedidoGuid'],
                      song['pedido'],
                      song['nivel01'],
                      song['nivel02'],
                      song['id'], 
                      1,
                      song['urn'])
        database.db.session.add(pedido)
        
      
    database.db.session.commit()
    criterios = []
    criterios.append({"Situação":"Comitado"})
    
    criterio = json.dumps(criterios)
    #print(criterio)
    
    res = make_response(criterio)
    #print(res)
    
    return res

@bp_materialPedidos.route('/GetTreviewPedidoMaterial', methods=['GET','POST'])
def GetTreviewPedidoMaterial():
    mp = database.db.session.execute("select distinct pedido, pedidoId, urn  from pedidoMaterial")

    criterios = []
   
    for p in mp:
        data = {"pedido":p.pedido,
                "pedidoId":p.pedidoId,
                "urn":p.urn}
        item ={"text":p.pedido,
               "state":"open",
               "data":data}
        criterios.append(item)
    
    criterio = json.dumps(criterios)
    
    res = make_response(criterio)
    print(res)
    return res


@bp_materialPedidos.route('/GetMaterialPedido', methods=['GET','POST'])
def getMaterialPedido():
    mp = database.db.session.query(tabelas.PedidoMaterial.Pedido)
    """for p in mp:
        #print(p)
        print(p.descricao)"""
    criterio = jsonify(mp) 
    
    print(criterio)
    
    res = make_response(criterio)
    #print(res)
    
    return res   
    
    return 'Teste'  