import json
import requests
from json import *
from urllib import response
from pyexpat import model
from flask import Blueprint
from flask import request, render_template, redirect, jsonify, make_response
from app import FuncoesBIM, database
from app import models as tabelas
from app import ObjetoDeTransferencia
from app import funcoes

import os
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
    database.db.session.execute("insert into PacotesDeEntrega (descricao, unidadeBasica) "+
                             "select distinct pedidoMaterial.descricao, pedidoMaterial.unid " +
                                " from pedidoMaterial " +
                                " where pedidoMaterial.descricao not in (select PacotesDeEntrega.descricao "+
                                                                        " from PacotesDeEntrega) " )
   
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
               "children":[],
               "data":data}
        criterios.append(item)
    
   
    
    criterio = json.dumps(criterios)
    
    res = make_response(criterio)

    return res


@bp_materialPedidos.route('/GetMaterialPedido', methods=['GET','POST'])
def getMaterialPedido():
    req = request.get_json()
    #print(req)
    #mp = database.db.session.query(tabelas.PedidoMaterial).filter(tabelas.PedidoMaterial.pedido==req['pedido'])
    
    mp = database.db.session.execute( "select pm.descricao, "
      " pde.pacote,  "
       " sum(iif(pde.descricao is not null, pm.qtde/pde.conversao, 0.0000)) QtdePacote,  "
       " pm.mes,  "
       " pm.pedido ,  "
       " group_concat(pm.idElement,',') ListaId,   "
       " group_concat(pm.urn ,',') ListaUrn "
        " from pedidoMaterial pm  "
        " left join PacotesDeEntrega pde on pm.descricao = pde.descricao  "
        " where pm.pedido = '"+req['pedido']+"'"+
       "  group by pm.descricao, pde.pacote, pm.mes, pm.pedido")
    criterio = []
    for p in mp:
        item = {'descricao':p.descricao,
                'pacote':p.pacote,
                'QtdePacote':p.QtdePacote,
                'mes':p.mes,
                'pedido':p.pedido,
                'ListaId':p.ListaId,
                'ListaUrn':p.ListaUrn,
                'pedidoId':0}
        criterio.append(item)
    
    #print(criterio)
    elementIds = json.dumps(criterio)
    res = make_response(elementIds)
    return res   

@bp_materialPedidos.route('/GetPacoteDeEntrega', methods=['GET','POST'])
def getPacoteDeEntrega():
    req = request.get_json()
    #print(req)
    mp = database.db.session.query(tabelas.PacotesDeEntrega)
    criterio = []
    for p in mp:
        item = {"descricao": p.descricao,
                "unidadeBasica":p.unidadeBasica,
                "pacote":p.pacote,
                "conversao":p.conversao,
                "base":p.base ,
                "largura":p.largura ,
                "altura":p.altura ,
                "formato":p.formato ,
                "empolamento":p.empolamento,
                "preco":p.preco, 
                "alturaMaxima":p.alturaMaxima, 
                "areaBaseMaxima":p.areaBaseMaxima}
        criterio.append(item)
    
    #print(criterio)
    elementIds = json.dumps(criterio)
    res = make_response(elementIds)
    return res   
    
