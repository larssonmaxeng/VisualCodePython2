from math import ceil
from sklearn.datasets import load_iris
import base64
from email.encoders import encode_base64
import json
from json import *
from urllib import response
from app import app
from flask import render_template, redirect, jsonify, make_response, send_file
import matplotlib.pyplot as mlt
import numpy as np
import skfuzzy as fuzz
from time import sleep
from skfuzzy import control as ctrl
from flask import request
from app import funcoes
import requests
import pandas as pd
import string
from app import database 
from flask_migrate import Migrate
from app import materiaisPedidos, FuncoesBIM, ObjetoDeTransferencia
import os
import ifcopenshell
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.file
from enum import Enum
import uuid
import time
import tempfile

import io

from app import googleSheet
from app import bancoDeDados
O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.
@app.route('/')
@app.route('/index')
def index():
    nome = "dissertação2"
    criterio = {"nome":"Preço", "nota":"Médio"}
    print(app.config['UPLOAD_FOLDER'])
    medio = 'médio'
    muitoAlto = 'muito alto'
    alto = 'alto'
    baixo = 'baixo'
    muitoBaixo ='muito baixo'
    vePreco = 'Preço'
    vePagamento='Pagamento'
    veReajuste = 'Reajuste'
    vsCusto = 'Custo'
    
    # Cria as variáveis do problema
    preco = ctrl.Antecedent(np.arange(0, 11, 0.5), vePreco)
    pagamento = ctrl.Antecedent(np.arange(0, 11, .5), vePagamento)
    reajuste = ctrl.Antecedent(np.arange(0, 11, 0.5), veReajuste)
    custo = ctrl.Consequent(np.arange(0, 11, 0.1), vsCusto)
   
    namesPreco = [muitoAlto, alto, medio, baixo, muitoBaixo]
    preco.automf(5, names =  namesPreco)
    pagamento.automf(5, names =  namesPreco)
    reajuste.automf(5, names =  namesPreco)
    custo.automf(5, names =  namesPreco)
   
    r1 = ctrl.Rule((preco[muitoAlto] | preco[alto]) & 
                   (pagamento[muitoAlto] | 
                    pagamento[alto] |
                    pagamento[baixo] |
                    pagamento[medio] |
                    pagamento[muitoBaixo] )
                   & ( reajuste[muitoAlto] | 
                    reajuste[alto] |
                    reajuste[baixo] |
                    reajuste[medio] |
                    reajuste[muitoBaixo]
                       ),custo[muitoAlto])
    r2 = ctrl.Rule(preco[medio] ,custo[medio])
    r3 = ctrl.Rule(preco[baixo] ,custo[baixo])
    r4 = ctrl.Rule(preco[muitoBaixo] ,custo[muitoBaixo])
         
    custo_ctrl = ctrl.ControlSystem([r1, r2, r3, r4])
    #print('leu regras')
    custo_simulador = ctrl.ControlSystemSimulation(custo_ctrl)
    #print('simulou')
    custo_simulador.input[vePreco] =8# notasCusto[nota]
    custo_simulador.input[vePagamento] = 2;#notasCusto[nota]
    custo_simulador.input[veReajuste] = 2;#notasCusto[nota]
            
    

    custo_simulador.compute()

    v = fuzz.control.visualization.FuzzyVariableVisualizer(custo)
    imagem, b = v.view()
    data = io.BytesIO()
    imagem.savefig(data, format="PNG")
    encodes_img_data = base64.b64encode(data.getbuffer()).decode('ascii')
    figura = []
    figura.append(encodes_img_data)
    #print(nome)
    return render_template('index.html', nome=nome, criterio=criterio, fig = figura )

def create_ifcaxis2placement(ifcfile, point=O, dir1=Z, dir2=X):
        point = ifcfile.createIfcCartesianPoint(point)
        dir1 = ifcfile.createIfcDirection(dir1)
        dir2 = ifcfile.createIfcDirection(dir2)
        axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
        return axis2placement

# Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
def create_ifclocalplacement( ifcfile, point=O, dir1=Z, dir2=X, relative_to=None):
    axis2placement = create_ifcaxis2placement(ifcfile,point,dir1,dir2)
    ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
    return ifclocalplacement2

# Creates an IfcPolyLine from a list of points, specified as Python tuples
def create_ifcpolyline( ifcfile, point_list):
    ifcpts = []
    for point in point_list:
        point = ifcfile.createIfcCartesianPoint(point)
        ifcpts.append(point)
    polyline = ifcfile.createIfcPolyLine(ifcpts)
    return polyline

# Creates an IfcExtrudedAreaSolid from a list of points, specified as Python tuples
def create_ifcextrudedareasolid( ifcfile, point_list, ifcaxis2placement, extrude_dir, extrusion):
    polyline = create_ifcpolyline(ifcfile, point_list)
    ifcclosedprofile = ifcfile.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    ifcdir = ifcfile.createIfcDirection(extrude_dir)
    ifcextrudedareasolid = ifcfile.createIfcExtrudedAreaSolid(ifcclosedprofile, ifcaxis2placement, ifcdir, extrusion)
    return ifcextrudedareasolid

def create_guid():
    return  uuid.uuid4().hex # ifcopenshell.guid.compress(uuid.uuid1().hex)   

def CriarVolumeRetangular(ifcfile, dados):
       
        context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]
        
        material = ifcfile.by_type("IfcMaterial")[0]
        building_storey =   ifcfile.by_type("IfcBuildingStorey")[0]
        owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
        dado = ObjetoDeTransferencia.DadosCanteiro(dados.pedido, dados.material, dados.area, dados.volume, 
                                                   dados.base, dados.largura, dados.alturaMaxima, dados.raio, 
                                                   dados.mesesAplicacao, dados.formato, dados.ponto,
                                                   dados.unidade, dados.qtde)
        #142= IFCAXIS2PLACEMENT3D(#140,#20,#12);
        Variavel142 = create_ifcaxis2placement(ifcfile=ifcfile, point=dado.ponto)
        #143= IFCCIRCLE(#142,IFCPOSITIVELENGTHMEASURE(100));
        #143= IFCRECTANGLEPROFILEDEF(.AREA.,'Modelos gen\X2\00E9\X0\ricos 1',#142,1992.38939618349,4200.);
        
        point = ifcfile.createIfcCartesianPoint((0.,0.))
        dir1 = ifcfile.createIfcDirection((1.,0.))
        axis2placement = ifcfile.createIfcAxis2Placement2D(point, dir1)
        
        IfcRectangleProfileDef143 =ifcfile.createIfcRectangleProfileDef('AREA',None, axis2placement, dado.base, dado.largura)
        
               
        pontoInsercao170 =ifcfile.createIfcCartesianPoint(dado.ponto)
        
        #172= IFCAXIS2PLACEMENT3D(#170,$,$);
        ifcAxisPlacement172 = ifcfile.createIfcAxis2Placement3D(pontoInsercao170, None, None)
        #20
        ifcdir20 =  ifcfile.createIfcDirection((0.0, 0.0, 1.0))
        
        #173= IFCEXTRUDEDAREASOLID(#167,#172,#20,300.);
        ifcextrudedareasolid173 =ifcfile.createIfcExtrudedAreaSolid(IfcRectangleProfileDef143, ifcAxisPlacement172, ifcdir20, dado.alturaMaxima)
        #174= IFCSHAPEREPRESENTATION(#105,'Body','SweptSolid',(#173));
        
        body_representation = ifcfile.createIfcShapeRepresentation(context, "Body", "SweptSolid", [ifcextrudedareasolid173])
        

        product_shape = ifcfile.createIfcProductDefinitionShape(None, None, [body_representation])
        
       
        data = {"GlobalId": ifcopenshell.guid.new(),#	IfcGloballyUniqueId (STRING)	IfcRoot
                "OwnerHistory": owner_history,#	IfcOwnerHistory (ENTITY)	IfcRoot
                "Name": dado.material,#	IfcLabel (STRING)	IfcRoot
                "Description": dado.pedido,#	IfcText (STRING)	IfcRoot
                "ObjectType": 'Volume 1',#	IfcLabel (STRING)	IfcObject
                "ObjectPlacement": Variavel142,#	IfcObjectPlacement (ENTITY)	IfcProduct
                "Representation": product_shape ,#	IfcProductRepresentation (ENTITY)	IfcProduct
                #"TAG": 'xxxx',#	IfcIdentifier (STRING)	IfcElement
                "PredefinedType": None#	IfcBuildingElementProxyTypeEnum (ENUM)"""
            
        }       
        elementProxy = ifcfile.create_entity('IfcBuildingElementProxy', **data)
       
        #elementProxy = self.ifcfile.createIfcWallStandardCase(self.create_guid(), , "Wall", "An awesome wall", None, wall_placement, product_shape, None)                                    
         
        
        property_values = [
            ifcfile.createIfcPropertySingleValue("Pacote", "Pacote",ifcfile.create_entity("IfcText", dado.unidade), None),
             ifcfile.createIfcPropertySingleValue("Quantidade", "Quantidade",ifcfile.create_entity("IfcInteger", int(dado.qtde)), None),
            #self.ifcfile.createIfcPropertySingleValue("Tipo de instalações", "Qual material", self.ifcfile.create_entity("IfcText", "Hidrossanitário"), None),
            ifcfile.createIfcPropertySingleValue("Entregue", "Entregue", ifcfile.create_entity("IfcBoolean", False), None),
            
            #self.ifcfile.createIfcPropertySingleValue("IsExternal", "IsExternal", self.ifcfile.create_entity("IfcBoolean", True), None),
            #self.ifcfile.createIfcPropertySingleValue("ThermalTransmittance", "ThermalTransmittance", self.ifcfile.create_entity("IfcLengthMeasure", 2.569), None),
            ifcfile.createIfcPropertySingleValue("Base", "Base", ifcfile.create_entity("IfcLengthMeasure", dado.base), None),
            ifcfile.createIfcPropertySingleValue("Largura", "Largura", ifcfile.create_entity("IfcLengthMeasure", dado.largura), None),
            ifcfile.createIfcPropertySingleValue("Altura", "Altura", ifcfile.create_entity("IfcLengthMeasure", dado.alturaMaxima), None),
            ifcfile.createIfcPropertySingleValue("Volume", "Volume",  ifcfile.create_entity("IfcVolumeMeasure", dado.volume), None)
        ]
        property_set =ifcfile.createIfcPropertySet(create_guid(), owner_history, "Pset_almoxarifado", None, property_values)
        ifcfile.createIfcRelDefinesByProperties(create_guid(),owner_history, None, None, [elementProxy], property_set)
                
        cor = ifcfile.createIfcColourRgb(None, 0,0,1)
        render = ifcfile.createIfcSurfaceStyleRendering(SurfaceColour = cor,
                                                    Transparency=0.,
                                                    SpecularColour = ifcfile.createIfcRatioMeasure( 0.5),
                                                    SpecularHighlight = ifcfile.createIfcSpecularExponent(64.0))
        ##152= IFCSURFACESTYLE('Telhado padr\X2\00E3\X0\o',.BOTH.,(#151));
        ifcSurfaceStyle = ifcfile.createIfcSurfaceStyle("Representação do canteiro", "BOTH", [render])
         #154= IFCPRESENTATIONSTYLEASSIGNMENT((#152));
        IFCPRESENTATIONSTYLEASSIGNMENT = ifcfile.createIfcPresentationStyleAssignment([ifcSurfaceStyle])
        
       
        #156= IFCSTYLEDITEM(#149,(#154),$);
        IFCSTYLEDITEM=ifcfile.createIfcStyledItem(ifcextrudedareasolid173,[IFCPRESENTATIONSTYLEASSIGNMENT], None) 
        #169= IFCREPRESENTATIONMAP(#168,#159);?
        #173= IFCBUILDINGELEMENTPROXYTYPE('2fHeoK0OX5zfefqRhXROdu',#42,'Modelos gen\X2\00E9\X0\ricos 1',$,$,$,(#169),'2634',$,.NOTDEFINED.);

        ifcfile.createIfcMaterialDefinitionRepresentation(None, None,[elementProxy], material )
        
        ifcfile.createIfcRelAssociatesMaterial(create_guid(), owner_history, None, None, [elementProxy], material )
         
        ifcfile.createIfcRelContainedInSpatialStructure(create_guid(), owner_history, 
                                                             "Building Storey Container", 
                                                             None, 
                                                             [elementProxy], 
                                                             building_storey)


@app.route('/GetCriaCanteiro', methods=['POST'])
def GetCriaCanteiro():
    req = request.get_json()
    #print(req)
    #mp = database.db.session.query(tabelas.PedidoMaterial).filter(tabelas.PedidoMaterial.pedido==req['pedido'])
    mp = database.db.session.execute( "select pm.descricao, "+
                                        "pde.pacote, "+
                                        "sum(iif(pde.descricao is not null, pm.qtde/pde.conversao, 0.0000)) QtdePacote, "+
                                        "group_concat(pm.mes) mes, "+
                                        'pm.pedido , '+
                                        "group_concat(pm.idElement,',') ListaId,  "+
                                        "group_concat(pm.urn ,',') ListaUrn,"+
                                        "pde.unidadeBasica	,"+
                                        "pde.pacote,"+
                                        "pde.conversao,	"+
                                        "sum(pm.qtde  *  pde.volume * pde.empolamento) volumeTotal,	"+
                                        "pde.base	,"+
                                        "pde.volume,"+
                                        "pde.largura	,"+
                                        "pde.altura	,"+
                                        "pde.formato,"	+
                                        "pde.empolamento,	"+
                                        "pde.preco,	"+
                                        "pde.alturaMaxima,	"+
                                        "pde.areaBaseMaxima,"+
                                        "case pde.formato "+
                                            "when 'Retangular' then pde.base * pde.largura  * pde.alturaMaxima "+
                                            "when 'Cilindrico' then 3.14 * pde.base * pde.base / 4 * pde.alturaMaxima "+
                                            "else null "+
                                            "end VolumeMaximo    "+
                                                "from pedidoMaterial pm "+
                                                "left join PacotesDeEntrega pde on pm.descricao = pde.descricao "+
                                                " where pm.pedido = '"+req['pedido']+"'" +
                                                " group by pm.descricao, pde.pacote,  pm.pedido")
        #" where pm.pedido = '"+req['pedido']+"'"+
      # "  group by pm.descricao, pde.pacote,  pm.pedido")
    try:
       #ifcfile =FuncoesBIM.ifcFuzzy(arquivoBase="")
       # BULK.set_bulk_Key(uniqueKey, ifc_file)
        #return {"key":"uniqueKey"}, 200
       
       
       ifc_file = ifcopenshell.open(r"C:\Users\Usuario\Desktop\VisualCodePython2\hello_wall.ifc")
       
       x=0.
       y=0.
       z=0.
       pontoDeOrigem =(x,y,z) 
       for p in mp:
        qtdeDePacotes = ceil(p.QtdePacote)#417
        qtdeDeInsumoNoVolumeMaximo = int(p.VolumeMaximo //(p.volume*p.empolamento))
        volumeReal = qtdeDeInsumoNoVolumeMaximo*p.volume*p.empolamento
        alturaReal = volumeReal/p.areaBaseMaxima   
        qtdePacotesParaInserir = ceil(p.QtdePacote)#41
        volumeMaximo = volumeReal
        volumeMaterial = qtdeDePacotes * (p.volume*p.empolamento)
        inteiro =int(volumeMaterial//volumeMaximo )
        parteFracionada= volumeMaterial/volumeMaximo-inteiro
        i = 0
        while i<inteiro:
            i=i+1
          
            dadosCanteiro = ObjetoDeTransferencia.DadosCanteiro(pedido=p.pedido, 
                                                                material=p.descricao,
                                                                area=0, 
                                                                volume=volumeMaximo, 
                                                                base=p.base, 
                                                                largura=p.largura, 
                                                                raio=p.base,
                                                                mesesAplicacao=p.mes, 
                                                                formato=p.formato, 
                                                                ponto=pontoDeOrigem,
                                                                altura= alturaReal,
                                                                unidade = p.pacote,
                                                                qtde = qtdeDeInsumoNoVolumeMaximo)       
            match p.formato:
                case 'Retangular':
                      CriarVolumeRetangular(ifcfile=ifc_file, dados= dadosCanteiro)

            pontoDeOrigem = funcoes.incrementarPontoDeOrigem(pontoDeOrigem, p.base) 
            qtdePacotesParaInserir = qtdePacotesParaInserir-qtdeDeInsumoNoVolumeMaximo         
        volumeParaInserir = qtdePacotesParaInserir*p.volume*p.empolamento
        pontoDeOrigem = funcoes.incrementarPontoDeOrigem(pontoDeOrigem, p.base)  
        if parteFracionada>0:
            dadosCanteiro = ObjetoDeTransferencia.DadosCanteiro(pedido=p.pedido, material=p.descricao, area=0, 
                                                                volume=parteFracionada,base=p.base, 
                                                                largura=p.largura, 
                                                                raio=p.base, 
                                                                mesesAplicacao=p.mes, 
                                                                formato=p.formato,
                                                                ponto=pontoDeOrigem, 
                                                                altura=volumeParaInserir/p.base/p.largura,
                                                                unidade = p.pacote,
                                                                qtde = qtdePacotesParaInserir)
            match p.formato:
                case 'Retangular':
                      CriarVolumeRetangular(ifcfile=ifc_file, dados= dadosCanteiro)        
           
       ifc_file.write(app.config['UPLOAD_FOLDER']+"\\hellow2.ifc") 
       criterios = []
       criterios.append({"teste":"teste"})
       criterio = json.dumps(criterios)  
       return send_file(app.config['UPLOAD_FOLDER']+"\\hellow2.ifc", as_attachment=True)

       #res = make_response(criterio)
       #return res
       
    except Exception as exc:
                            criterios = []
                            criterios.append({"teste":str(exc)})
                            criterio = json.dumps(criterios)  
                            res = make_response(criterio)
                            return res
   

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/forge')
def forge():
    return render_template('forge.html')
@app.route('/autenticar', methods=['GET'])
def autenticar():
    usuario = request.args.get('usuario')
    return "Usuario logado"    

@app.route('/resultado')
def resultado():
    medio = 'médio'
    muitoAlto = 'muito alto'
    alto = 'alto'
    baixo = 'baixo'
    muitoBaixo ='muito baixo'
    ruim = 'ruim'
    muitoRuim = 'muito ruim'
    aceitavel = 'aceitável'
    muitoBom = 'muito bom'
    excelente = 'excelente'
    vePreco = 'Preço'
    vequalidade='Qualidade'
    vemeioAmbiente = 'Meio Ambiente'
    veGeral = 'Geral'
    vePrazo = 'Prazo'
    veGestao = 'Gestao'
    vsFecharCompra = 'FecharCompra'
    tMeioAmbientePouquissimoCuidado = 'Pouquíssimo Cuidado'
    tMeioAmbientePoucoCuidado = 'PoucoCuidado'
    tMeioAmbienteCuidadoMediano = 'CuidadoMediano'
    tMeioAmbienteCuidadoAcimaDaMedia = 'CuidadoAcimaDaMedia'
    tMeioAmbienteCuidadoExcelente = 'CuidadoExcelente'
    muitoAlto2 = 'muitoAlto2'
    muitoAlto1 = 'muitoAlto1'



    # Cria as variáveis do problema
    preco = ctrl.Antecedent(np.arange(0, 11, 0.5), vePreco)
    qualidade = ctrl.Antecedent(np.arange(0, 11, .5), vequalidade)
    meioAmbiente = ctrl.Antecedent(np.arange(0, 11, 0.5), vemeioAmbiente)
    geral = ctrl.Antecedent(np.arange(0, 11, 0.5), veGeral)
    gestao = ctrl.Antecedent(np.arange(0, 11, 0.5), veGestao)
    prazo = ctrl.Antecedent(np.arange(0, 11, 0.5), vePrazo)


    fecharCompra = ctrl.Consequent(np.arange(0, 11, 0.1), vsFecharCompra)

    qualidade[muitoRuim] = fuzz.gaussmf(qualidade.universe,  0, .8 )
    qualidade[ruim] = fuzz.gaussmf(qualidade.universe,  2.5, .8 )
    qualidade[aceitavel] = fuzz.gaussmf(qualidade.universe,  5, .8)
    qualidade[muitoBom] = fuzz.gaussmf(qualidade.universe,7.5,.8)
    qualidade[excelente] = fuzz.gaussmf(qualidade.universe,10,.8)

    # Cria automaticamente o mapeamento entre valores nítidos e difusos
    # usando uma função de pertinência padrão (triângulo)
    #preco.automf(names=[alto, medio, baixo])

    preco[muitoAlto] = fuzz.gaussmf(preco.universe,  0, .8 )
    preco[alto] = fuzz.gaussmf(preco.universe,  2.5, .8 )
    preco[medio] = fuzz.gaussmf(preco.universe,  5, .8)
    preco[baixo] = fuzz.gaussmf(preco.universe,7.5,.8)
    preco[muitoBaixo] = fuzz.gaussmf(preco.universe,10,.8)

    #prazo
    prazo[muitoAlto] = fuzz.gaussmf(prazo.universe,  0, .8 )
    prazo[alto] = fuzz.gaussmf(prazo.universe,  2.5, .8 )
    prazo[medio] = fuzz.gaussmf(prazo.universe,  5, .8)
    prazo[baixo] = fuzz.gaussmf(prazo.universe,7.5,.8)
    prazo[muitoBaixo] = fuzz.gaussmf(prazo.universe,10,.8)
    # Cria as funções de pertinência usando tipos variados

    #Gestão
    gestao[muitoBaixo] = fuzz.trimf(gestao.universe,  [-1, 0, 1] )
    gestao[baixo] = fuzz.trimf(gestao.universe,  [0,1 ,2])
    gestao[medio] = fuzz.trimf(gestao.universe,  [1,2,3])
    gestao[alto] = fuzz.trapmf(gestao.universe, [2, 4, 5, 7])
    gestao[muitoAlto] = fuzz.trimf(gestao.universe,  [5, 10, 10] )

    #Geral
    geral[muitoBaixo] = fuzz.trimf(geral.universe,  [-1, 0, 1] )
    geral[baixo] = fuzz.trimf(geral.universe,  [0,1 ,2])
    geral[medio] = fuzz.trimf(geral.universe,  [1,2,3])
    geral[alto] = fuzz.trapmf(geral.universe, [2, 4, 5, 7])
    geral[muitoAlto] = fuzz.trimf(geral.universe,  [5, 10, 10] )

    #qualidade[excelente] = fuzz.gaussmf(qualidade.universe, 10,1)
    #qualidade[excelente] = fuzz.trapmf(qualidade.universe, [0, 8,10, 11])
    #meioAmbiente[tMeioAmbientePouquissimoCuidado] = fuzz.trimf(meioAmbiente.universe, [0, 0, 4])
    #meioAmbiente[tMeioAmbientePoucoCuidado] = fuzz.trimf(meioAmbiente.universe, [0, 0, 5])
    meioAmbiente[tMeioAmbientePouquissimoCuidado] = fuzz.trimf(meioAmbiente.universe,  [-1, 0, 1] )
    meioAmbiente[tMeioAmbientePoucoCuidado] = fuzz.trimf(meioAmbiente.universe,  [0,1 ,2])
    meioAmbiente[tMeioAmbienteCuidadoMediano] = fuzz.trimf(meioAmbiente.universe,  [1,2,3])
    meioAmbiente[tMeioAmbienteCuidadoAcimaDaMedia] = fuzz.trapmf(meioAmbiente.universe, [2, 4, 5, 7])#fuzz.trimf(meioAmbiente.universe,  [5, 6, 7] )
    meioAmbiente[tMeioAmbienteCuidadoExcelente] = fuzz.trimf(meioAmbiente.universe,  [5, 10, 10] )

    fecharCompra[muitoBaixo] = fuzz.gaussmf(fecharCompra.universe,  0, .8 )
    fecharCompra[baixo] = fuzz.gaussmf(fecharCompra.universe,  2.5, .8 )
    fecharCompra[medio] = fuzz.gaussmf(fecharCompra.universe,  5, .8)
    fecharCompra[alto] = fuzz.gaussmf(fecharCompra.universe,7.5,.8)
    fecharCompra[muitoAlto] = fuzz.gaussmf(fecharCompra.universe,8.5,.8)
    fecharCompra[muitoAlto1] = fuzz.gaussmf(fecharCompra.universe,9.5,.8)
    fecharCompra[muitoAlto2] = fuzz.gaussmf(fecharCompra.universe,10,.8)
   
    #    #print('começou')

    ##print('terminou')
    #fecharCompra_ctrl = ctrl.ControlSystem([r4, r41, r2, r3, r5, r1, r11 , r7])
    r1 = ctrl.Rule((preco[muitoAlto] & qualidade[muitoRuim] ) | (preco[alto] & qualidade[muitoRuim] & prazo[muitoAlto]) ,fecharCompra[alto]) 
    fecharCompra_ctrl = ctrl.ControlSystem([r1])
    #print('leu regras')
    fecharCompra_simulador = ctrl.ControlSystemSimulation(fecharCompra_ctrl)
    #print('simulou')

    fecharCompra_simulador.input[vequalidade] = 7
    fecharCompra_simulador.input[vePreco] = 9
    fecharCompra_simulador.input[vePrazo] = 5

    #fecharCompra_simulador.input[vemeioAmbiente] =7
    #fecharCompra_simulador.input[veGestao] = 8
    #fecharCompra_simulador.input[veGeral] = 8

    fecharCompra_simulador.compute()

    v = fuzz.control.visualization.FuzzyVariableVisualizer(preco)
    imagem, b = v.view()
    #preco.view(sim=fecharCompra_simulador)
    #qualidade.view(sim=fecharCompra_simulador)
    #prazo.view(sim=fecharCompra_simulador)
    #meioAmbiente.view(sim=fecharCompra_simulador)
    #gestao.view(sim=fecharCompra_simulador)
    #geral.view(sim=fecharCompra_simulador)
    data = io.BytesIO()
    imagem.savefig(data, format="PNG")
    encodes_img_data = base64.b64encode(data.getbuffer())

    """fecharCompra.view(sim=fecharCompra_simulador)
    #print(fecharCompra_simulador.output[vsFecharCompra])"""
    nome = "dissertação2"
    criterio = {"nome":"Preço", "nota":"Médio"}
    return render_template('resultado.html', modo="Limpeza", criterios = [], subcriterios = [], imagens=[])

@app.route('/limpar')
def limpar():
    #criterio = {"nome":"Preço", "nota":"Médio"}
    criterios = []
    criterios.append(['01- Custo', 'crisp', 'Custo'])
    criterios.append(['02- Qualidade','fuzzy', 'Qualidade'])
    criterios.append(['03- Prazo','fuzzy', 'Prazo' ])
    criterios.append(['04- Gestão', 'fuzzy', 'Gestao'])
    criterios.append(['05- Geral', 'fuzzy', 'Geral'])
    variavelLinguistica3Opcoes = ['Selecionar', 'Ruim', 'Medio', 'Bom']
    subcriterios = [] 
    subcriterios.append(['01- Custo', 'Preço', 'crisp', [], 'CustoPreco'])
    subcriterios.append(['01- Custo', 'Condições de pagamento', 'fuzzy', variavelLinguistica3Opcoes, 'CustoPgto'])
    subcriterios.append(['01- Custo', 'Modelo de reajuste','fuzzy', variavelLinguistica3Opcoes, 'CustoReajuste'])
    #sheet = googleSheet.GoogleSheet()
    ##print(sheet.GetParametros( SAMPLE_RANGE_NAME= 'DadosGerais!A2:A5', SAMPLE_SPREADSHEET_ID="1NLqJWL8LeRECbK04Bm41AYq0tu95VbYgsT6DTX6Sq1g"))
    subcriterios.append(['02- Qualidade', 'Baixas taxas de devolução', 'fuzzy', variavelLinguistica3Opcoes, 'QualiDevolucao'])
    subcriterios.append(['02- Qualidade', 'Precisão nas dimensões', 'fuzzy', variavelLinguistica3Opcoes, 'QualiDimensoes'])
    subcriterios.append(['02- Qualidade', 'Equipe técnica capacitada','fuzzy', variavelLinguistica3Opcoes, 'QualiEquipe'])

   
    
    subcriterios.append(['03- Prazo', 'Prazo atender a obra', 'fuzzy', variavelLinguistica3Opcoes, 'PrazoPrazo'])
    subcriterios.append(['03- Prazo', 'Capacidade de produção', 'fuzzy', variavelLinguistica3Opcoes, 'PrazoProducao'])
    subcriterios.append(['03- Prazo', 'Capacidade de resposta','fuzzy', variavelLinguistica3Opcoes, 'PrazoResposta'])
  
   
    
    subcriterios.append(['04- Gestão', 'Clareza nas informações da entrega do produto', 'fuzzy', variavelLinguistica3Opcoes, 'GestaoEntrega'])
    subcriterios.append(['04- Gestão', 'Cooperação em situações adversas', 'fuzzy', variavelLinguistica3Opcoes, 'GestaoCooperacao'])
    subcriterios.append(['04- Gestão', 'Mantêm parceria','fuzzy', variavelLinguistica3Opcoes, 'GestaoParceria'])
    subcriterios.append(['04- Gestão', 'Traz informações transparentes','fuzzy', variavelLinguistica3Opcoes, 'GestaoTransparência'])
    subcriterios.append(['04- Gestão', 'Ter boa comunicação','fuzzy', variavelLinguistica3Opcoes, 'GestaoComunicacao'])
    


    
    subcriterios.append(['05- Geral', 'Cumpre leis trabalhistas', 'fuzzy', variavelLinguistica3Opcoes, 'GeralLeis'])
    subcriterios.append(['05- Geral', 'Interesse em executar o serviço', 'fuzzy', variavelLinguistica3Opcoes, 'GeralInteresses'])
    subcriterios.append(['05- Geral', 'Não usa substâncias tóxica', 'fuzzy', variavelLinguistica3Opcoes, 'GeralToxico'])
    subcriterios.append(['05- Geral', 'Histórico de entregar no prazo', 'fuzzy', variavelLinguistica3Opcoes, 'GeralHistoricoPrazo'])
    subcriterios.append(['05- Geral', 'Parceira de longo prazo', 'fuzzy', variavelLinguistica3Opcoes, 'GeralParceria'])
    subcriterios.append(['05- Geral', 'Histórico de fornecimento', 'fuzzy', variavelLinguistica3Opcoes, 'GeralHistorico'])
    subcriterios.append(['05- Geral', 'Proporciona saúde e seg do trab', 'fuzzy', variavelLinguistica3Opcoes, 'GeralSaudeESeguranca'])                        
    
    return render_template('resultado.html', modo="Limpeza", criterios = criterios, subcriterios = subcriterios, imagens=[])

@app.route('/your_url', methods=["GET", "POST", "PUT"])
def your_url():
    #criterio = {"nome":"Preço", "nota":"Médio"}
    #req = request.div["div3"]
    #print(req.name)
    req = request.get_json()
    print(req)
    #for song in req:
    #    print(song, ":", req[song])
    """if request.method == "POST":
       print(request)
    print('foi ate aqui')
    print(request)
    #print(req)"""
    #print("passou")
    #criterios = []
    #criterios.append({"nome":"Preço", "nota":"Médio"})
    #criterios.append({"nome":"Preço1", "nota":"Médio1"})
    planilha= googleSheet.GoogleSheet()
    criteriosCusto = []
    criteriosCusto.append({"nomeDaVariavel":"Preço",
        "QtdeDeCasas":5,
        "Opções": ["muitoAlto", "alto", "medio", "baixo", "muitoBaixo"],
        "Criterio":"Custo",
        "NotaCrisp": str(req["CustoPreco"]),
        "NotaFuzzy":""})
    criteriosCusto.append({"nomeDaVariavel":"Pagamento",
        "QtdeDeCasas":3,
        "Opções": ["ruim", "medio", "bom"],
        "Criterio":"Custo",
        "NotaCrisp": "",
        "NotaFuzzy":str(req["CustoPgto"])})
    criteriosCusto.append({"nomeDaVariavel":"Reajuste",
        "QtdeDeCasas":3,
        "Opções": ["ruim", "medio", "bom"],
        "Criterio":"Custo",
        "NotaCrisp": "",
        "NotaFuzzy":str(req["CustoReajuste"])})
     
    variavelDeSaidaCusto = {"nomeDaVariavel":"Custo",
        "QtdeDeCasas":0,
        "Opções": ["muitoAlto", "alto", "medio", "baixo", "muitoBaixo"],
        "Criterio":"Custo",
        "NotaCrisp": "",
        "NotaFuzzy":""}
     
    custo, imagemCusto = ConstruirControladorFuzzy( 
                                                   inomeDasVariaveisDeEntrada=criteriosCusto, 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaCusto,
                                                   iRegra = "Custo",
                                                   idDaPlanilha="1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524", 
                                                   planilha=planilha, 
                                                   nomeDaAba="RegrasCriterioCusto"
                                                   )   
   
    variavelDeSaidaQualidade = GetVariavelDeSaida(nomeDaVariavel="Qualidade", opcoes=["muitoBaixo", "baixo", "medio", "alto", "muitoAlto"], criterio= "Qualidade")
    qualidade, imagemQualidade =ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosQualidade(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaQualidade,
                                                   iRegra = "Qualidade",
                                                   idDaPlanilha="1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524", 
                                                   planilha=planilha, 
                                                   nomeDaAba="RegrasCriterioQualidade")  
    
    variavelDeSaidaPrazo = GetVariavelDeSaida(nomeDaVariavel="PrazoSaida", opcoes= ["muitoBaixo", "baixo", "medio", "alto", "muitoAlto"],criterio= "Prazo")
    prazo, imagemPrazo = ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosPrazo(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaPrazo,
                                                   iRegra = "Prazo",
                                                   idDaPlanilha="1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524", 
                                                   planilha=planilha, 
                                                   nomeDaAba="regrasCriterioPrazo")  
    
    variavelDeSaidaGestao = GetVariavelDeSaida(nomeDaVariavel="Gestão", opcoes=["muitoBaixo", "baixo", "medio", "alto", "muitoAlto"],criterio= "Gestao")
    gestao, imagemGestao = ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosGestao(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaGestao,
                                                   iRegra = "Prazo",
                                                    idDaPlanilha="1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524", 
                                                   planilha=planilha, 
                                                   nomeDaAba="regrasCriterioGestao"
                                                   )  
    variavelDeSaidaGeral = GetVariavelDeSaida(nomeDaVariavel="Geral", opcoes=["muitoBaixo", "baixo", "medio", "alto", "muitoAlto"],criterio= "Geral")   
    geral, imagemGeral = ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosGeral(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaGeral,
                                                   iRegra = "Geral",
                                                   idDaPlanilha="1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524", 
                                                   planilha=planilha, 
                                                   nomeDaAba="regrasCriterioGeral"
                                                   )     
    
    df = bancoDeDados.GetCriterios(sheet=planilha, nomeDaAba="criterio")
    opcoes = []
    
    for k in str(df["variavelDeSaida"][0]).split(','):  
        opcoes.append(str(k))
    print(opcoes)    
    nomeDoCriterio = "Critério de seleção"    
    variavelDeSaidaCriterioSelecao = GetVariavelDeSaida(nomeDaVariavel=nomeDoCriterio, opcoes=opcoes,criterio= nomeDoCriterio)
    #***************Definição das notas**********************
    notas ={'01- Custo':custo,
            '02- Qualidade':qualidade,
            '03- Prazo':prazo,
            '04- Gestão':gestao,
            '05- Geral':geral}
    
    
    criterioDeSelecao, imagemCriterioDeSelecao = ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosGeralDoGoogleSheet(notas=notas,
                                                                                                             nomeDoCriterio=nomeDoCriterio,
                                                                                                             df=df), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaCriterioSelecao,
                                                   iRegra = nomeDoCriterio,
                                                   idDaPlanilha="1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524", 
                                                   planilha=planilha, 
                                                   nomeDaAba="RegrasCriteriosGerais"
                                                   )     
    criterios = []
    criterios.append({"idHtml":"imagemCusto", "valor":str(imagemCusto)})
    criterios.append({"idHtml":"crispCusto", "valor":str(round(custo*1, 2))})
    criterios.append({"idHtml":"imagemQualidade", "valor":str(imagemQualidade)})
    criterios.append({"idHtml":"crispQualidade", "valor":str(round(qualidade*1, 2))})
    
    criterios.append({"idHtml":"imagemPrazo", "valor":str(imagemPrazo)})
    criterios.append({"idHtml":"crispPrazo", "valor":str(round(prazo*1, 2))})
    
    criterios.append({"idHtml":"imagemGestao", "valor":str(imagemGestao)})
    criterios.append({"idHtml":"crispGestao", "valor":str(round(gestao*1, 2))})
    
    criterios.append({"idHtml":"imagemGeral", "valor":str(imagemGeral)})
    criterios.append({"idHtml":"crispGeral", "valor":str(round(geral*1, 2))})
    
    criterios.append({"idHtml":"imagemCriterioDeSelecao", "valor":str(imagemCriterioDeSelecao)})
    criterios.append({"idHtml":"crispCriterioDeSelecao", "valor":str(round(criterioDeSelecao*1, 2))})
    
    criterio = json.dumps(criterios)
    #print(criterio)
    
    res = make_response(criterio)
    #print(res)
    
    return res



@app.route('/SalvarPedido', methods=["GET", "POST", "PUT"])
def SalvarPedido():
    
    req = request.get_json()
    pedido = ''
    for i in req:
        pedido = i["pedido"]    
    print(pedido)
    listaParaLimpar = []
    j = 2;
    dados = []
    #notaPedidoForncedorId	pedidoId	fornecedorId	criterio	subcriterio	nota	htmlId	ativo
    for song in req:
        dados.append([
                      song['descricao'],
                      song['unid'],
                      song['qtde'],
                      song['mes'],
                      song['objectId'],
                      song['pedidoGuid'],
                      song['pedido'],
                      song['nivel01'],
                      song['nivel02'],
                      song['id'] ])
    dfPedido =  bancoDeDados.GetPedidoMaterial(sheet=googleSheet.GoogleSheet())    
    for i in dfPedido.index:
        if (dfPedido["pedido"][i]==pedido):
            listaParaLimpar.append(j)  
        j = j+1     
    print(listaParaLimpar)
    sheet = googleSheet.GoogleSheet().GetService()
    bancoDeDados.SetPedidoMaterial(sheet=sheet, valores=dados, listaParaLimpar=listaParaLimpar)
    #print(criterio)
    #bancoDeDados.SetSubCriterios(sheet=sheet,valores=dados)
    criterios = []
    criterios.append({"Resultado":"Foi"})
    criterio = json.dumps(criterios)
    res = make_response(criterio)
    #print(res)
    
    return res
   
        
    criterios = []
    
    criterios.append({"resultado":"foi"})
    
    criterio = json.dumps(criterios)
    
    res = make_response(criterio)
    
    return res


@app.route('/salvarDados', methods=["GET", "POST", "PUT"])
def salvarDados():
    
    req = request.get_json()
    print(req)
 
        
    dados = []
    #notaPedidoForncedorId	pedidoId	fornecedorId	criterio	subcriterio	nota	htmlId	ativo
    for song in req:
        dados.append([(req["dadosArvore"])["pedidoId"],
                      (req["dadosArvore"])["fornecedorId"],
                      "", 
                      "",
                      req[song],
                      song,
                      1])
    dados = dados[:-1]    
    print("**************************************")
    print(dados)
    dfnota =  bancoDeDados.GetNotaPedidoFornecedor(sheet=googleSheet.GoogleSheet())
    dfnotaPedido = dfnota.loc[dfnota["fornecedorId"]!=0]
    j = 3;
    listaParaLimpar = []
    for i in dfnotaPedido.index:
        if ((dfnotaPedido["pedidoId"][i]==(req["dadosArvore"])["pedidoId"])&
            (dfnotaPedido["fornecedorId"][i]==(req["dadosArvore"])["fornecedorId"])):
            listaParaLimpar.append(j)  
        j = j+1     
    print(listaParaLimpar)
    sheet = googleSheet.GoogleSheet().GetService()
    bancoDeDados.SetSubCriterios(sheet=sheet, valores=dados, listaParaLimpar=listaParaLimpar)
    #print(criterio)
    #bancoDeDados.SetSubCriterios(sheet=sheet,valores=dados)
    criterios = []
    criterios.append({"Resultado":"Foi"})
    criterio = json.dumps(criterios)
    res = make_response(criterio)
    #print(res)
    
    return res
    
   
def CalcularCriterioQualidade(notasCusto, ):    
    medio = 'médio'
    muitoAlto = 'muito alto'
    alto = 'alto'
    baixo = 'baixo'
    muitoBaixo ='muito baixo'
    vePreco = 'Preço'
    vePagamento='Pagamento'
    veReajuste = 'Reajuste'
    vsCusto = 'Custo'
    ruim = 'ruim'
    bom = 'bom'
    # Cria as variáveis do problema
    preco = ctrl.Antecedent(np.arange(0, 11, 0.5), vePreco)
    pagamento = ctrl.Antecedent(np.arange(0, 11, .5), vePagamento)
    reajuste = ctrl.Antecedent(np.arange(0, 11, 0.5), veReajuste)
    custo = ctrl.Consequent(np.arange(0, 11, 0.1), vsCusto)
   
    namesPreco = [muitoAlto, alto, medio, baixo, muitoBaixo]
    names = [ruim, bom, medio]
    preco.automf(5, names =  namesPreco)
    pagamento.automf(3, names =  names)
    reajuste.automf(3, names =  names)
    custo.automf(5, names =  namesPreco)
   
    r1 = ctrl.Rule((preco[muitoAlto] | preco[alto]) & 
                   (pagamento[ruim] | 
                    pagamento[bom] |
                    pagamento[medio] )
                   & ( reajuste[ruim] | 
                    reajuste[bom] |
                    reajuste[medio] 
                       ),custo[muitoAlto])
    r2 = ctrl.Rule(preco[medio] ,custo[medio])
    r3 = ctrl.Rule(preco[baixo] ,custo[baixo])
    r4 = ctrl.Rule(preco[muitoBaixo] ,custo[muitoBaixo])
    r5 = ctrl.Rule(preco[muitoAlto] ,custo[alto])
         
    custo_ctrl = ctrl.ControlSystem([r1, r2, r3, r4, r5])
    print('leu regras')
    custo_simulador = ctrl.ControlSystemSimulation(custo_ctrl)
    print('simulou')
    print(notasCusto) 
    for nota1 in notasCusto:


        match str(nota1):
            case "CustoPreco":
                print(str(notasCusto[nota1]))
                print(float(str(notasCusto[nota1])))
                custo_simulador.input[vePreco] = float(str(notasCusto[nota1]));
            case "CustoPgto":
                print(str(notasCusto[nota1]))
                custo_simulador.input[vePagamento] = funcoes.Desfuzzificar(nota=str(notasCusto[nota1]));
            case "CustoReajuste":
                print(str(notasCusto[nota1]))
                custo_simulador.input[veReajuste] =  funcoes.Desfuzzificar(nota=str(notasCusto[nota1]));
            
    

    custo_simulador.compute()

    v = fuzz.control.visualization.FuzzyVariableVisualizer(custo)
    imagem, b = v.view(sim=custo_simulador)
    data = io.BytesIO()
    imagem.savefig(data, format="PNG")
    encodes_img_data = base64.b64encode(data.getbuffer()).decode('ascii')
    #print(custo_simulador.output[vsCusto])
    #print(encodes_img_data)
    return custo_simulador.output[vsCusto] , encodes_img_data

        
def ConstruirControladorFuzzy(inomeDasVariaveisDeEntrada, inomeDaVariavelDeSaida, iRegra, idDaPlanilha, planilha, nomeDaAba):    
     
    variaveisFuzzy = []
    for nome in inomeDasVariaveisDeEntrada:
        variavelFuzzy = ctrl.Antecedent(np.arange(0, 11, 0.5), nome["nomeDaVariavel"])
        variavelFuzzy.automf(nome["QtdeDeCasas"], names = nome["Opções"])
        variaveisFuzzy.append(variavelFuzzy)
        #print(variavelFuzzy.label)
   
    variavelDeSaida = ctrl.Consequent(np.arange(0, 11, 0.1), inomeDaVariavelDeSaida["nomeDaVariavel"])
    variavelDeSaida.automf(inomeDaVariavelDeSaida["QtdeDeCasas"], names = inomeDaVariavelDeSaida["Opções"])
    print('Gerando regras para :'+iRegra) 
    custo_ctrl = ctrl.ControlSystem(GerarRegras(variaveisDeEntrada=variaveisFuzzy, variavelDeSaida=variavelDeSaida, nomeDaRegraDeCriterio = iRegra,
                                                idDaPlanilha=idDaPlanilha,planilha=planilha, nomeDaAba=nomeDaAba))
    print('leu regras:'+iRegra)
    custo_simulador = ctrl.ControlSystemSimulation(custo_ctrl)
    print('simulou:'+iRegra)
    print(inomeDasVariaveisDeEntrada)

    for nome in inomeDasVariaveisDeEntrada:
        print(nome["nomeDaVariavel"])
        print(nome["NotaCrisp"])
        print(nome["NotaFuzzy"])
        if (nome["nomeDaVariavel"] == "Preço") | (iRegra=="Critério de seleção"):
           custo_simulador.input[nome["nomeDaVariavel"]] = float(str(nome["NotaCrisp"]))
        else:
           custo_simulador.input[nome["nomeDaVariavel"]] = funcoes.Desfuzzificar(nota=str(nome["NotaFuzzy"]));           
    custo_simulador.compute()

    v = fuzz.control.visualization.FuzzyVariableVisualizer(variavelDeSaida)
    imagem, b = v.view(sim=custo_simulador)
    data = io.BytesIO()
    imagem.savefig(data, format="PNG")
    encodes_img_data = base64.b64encode(data.getbuffer()).decode('ascii')
    #print(custo_simulador.output[vsCusto])
    #print(encodes_img_data)
    return custo_simulador.output[inomeDaVariavelDeSaida["nomeDaVariavel"]] , encodes_img_data

def GerarRegras(variaveisDeEntrada, variavelDeSaida, nomeDaRegraDeCriterio, idDaPlanilha, planilha, nomeDaAba):
    colunas = []
    
    for i in variaveisDeEntrada:
        colunas.append(i.label)
        
    colunas.append('Resultado')
    colunas.append('FORMULA')	
    colunas.append('Regra')
  
    a = list(string.ascii_uppercase)
    colunaFim=a[len(colunas)]
  
    resultados = []
    
    dfRegrasBase = bancoDeDados.GetBaseRegras(sheet=planilha, sampleRange=nomeDaAba+"!B2:"+colunaFim+"15000", idDaPlanilha=idDaPlanilha, colunas=colunas )
    print(dfRegrasBase)
    for r in dfRegrasBase.index:
        
        entradas = dfRegrasBase["Regra"][r].split('|')[0]
        resultado = dfRegrasBase["Regra"][r].split('|')[1]    
        v = [entradas, resultados]
        resultados.append([str(dfRegrasBase["Regra"][r].split('|')[0]),  str(dfRegrasBase["Regra"][r].split('|')[1])])
       
    dfRegraSaida = pd.DataFrame(data=resultados, columns=['regra', 'saida'])
    
    dfSaidas = (dfRegraSaida["saida"]).drop_duplicates()
    
   # print(dfSaidas)
    dfRegra = dfRegraSaida.drop_duplicates()
   # print(dfRegra)
   # print('************************************************')
    regras = []   
    ldict = {}
    l = {'ctrl':ctrl,'variaveisDeEntrada':variaveisDeEntrada, 'variavelDeSaida':variavelDeSaida}
    """r = ctrl.Rule((variaveisDeEntrada[0]['muitoAlto'] & variaveisDeEntrada[1]['bom'] & variaveisDeEntrada[2]['medio'] ) |
                    (variaveisDeEntrada[0]['muitoAlto'] & variaveisDeEntrada[1]['bom'] & variaveisDeEntrada[2]['bom'] ) |
                    (variaveisDeEntrada[0]['alto'] & variaveisDeEntrada[1]['ruim'] & variaveisDeEntrada[2]['bom'] ) |
                    (variaveisDeEntrada[0]['alto'] & variaveisDeEntrada[1]['medio'] & variaveisDeEntrada[2]['bom'] ) |
                    (variaveisDeEntrada[0]['alto'] & variaveisDeEntrada[1]['bom'] & variaveisDeEntrada[2]['bom'] ) |
                    (variaveisDeEntrada[0]['medio'] & variaveisDeEntrada[1]['medio'] & variaveisDeEntrada[2]['bom'] ) |
                    (variaveisDeEntrada[0]['medio'] & variaveisDeEntrada[1]['bom'] & variaveisDeEntrada[2]['medio'] ) ,variavelDeSaida['alto'])"""
    for i in dfSaidas.index:
        comando = "r = ctrl.Rule("
        resultado = dfSaidas[i]
        dfRegrasAtuais = dfRegra.loc[dfRegra["saida"]==dfSaidas[i]]
        
        
        for k in dfRegrasAtuais.index:
            entradas = dfRegrasAtuais["regra"][k]           
            regrasAntecedentes = entradas.split(';')
            qtde = len(regrasAntecedentes)
            #print(qtde)
            w=0
            regraAdicional = "\n ("
            while w < qtde:
                
                regraAdicional = regraAdicional+"variaveisDeEntrada["+str(w)+"]['"+regrasAntecedentes[w]+"'] & "
                w = w+1
            regraAdicional = regraAdicional[:-2]+')'    
            
            comando = comando+regraAdicional+' | '
           
           
        comando = comando[:-2] +",variavelDeSaida['"+resultado+"'])" 
        exec(comando, l, ldict)
        regras.append(ldict['r'])
        #print(comando)
       #r = ctrl.Rule(((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) |((((variaveisDeEntrada[0][regrasAntecedentes[0]]) &variaveisDeEntrada[1][regrasAntecedentes[1]]) &variaveisDeEntrada[2][regrasAntecedentes[2]]) &) ,variavelDeSaida[medio])
    return regras
       
    
    #daqui para baixo deu certo
    dfRegrasBase = bancoDeDados.GetBaseRegras(sheet=planilha, sampleRange=nomeDaAba+"!B2:"+colunaFim+"15000", idDaPlanilha=idDaPlanilha, colunas=colunas )
    
    
    dfRegras = dfRegrasBase["Regra"]
    dfRegras = dfRegras.drop_duplicates()
    #print(dfRegras)
    regras = []

    for i in dfRegras.index:
        entradas = dfRegras[i].split('|')[0]
        resultado = dfRegras[i].split('|')[1]
        regrasAntecedentes = entradas.split(';')
        qtde = len(regrasAntecedentes)
        """print("Entradas:" + entradas)
        print("resultdos:" + resultado)
        print("regrasAntecedentes:")
        print(regrasAntecedentes)
        print("qtde:" + str(qtde))"""
        if(qtde==7): 
            r = ctrl.Rule(variaveisDeEntrada[0][regrasAntecedentes[0]]&
                          variaveisDeEntrada[1][regrasAntecedentes[1]]& 
                          variaveisDeEntrada[2][regrasAntecedentes[2]]&
                          variaveisDeEntrada[3][regrasAntecedentes[3]]&
                          variaveisDeEntrada[4][regrasAntecedentes[4]]&
                          variaveisDeEntrada[5][regrasAntecedentes[5]]&
                          variaveisDeEntrada[6][regrasAntecedentes[6]],
                          variavelDeSaida[resultado])
            regras.append(r)
        if(qtde==6): 
            r = ctrl.Rule(variaveisDeEntrada[0][regrasAntecedentes[0]]&
                          variaveisDeEntrada[1][regrasAntecedentes[1]]& 
                          variaveisDeEntrada[2][regrasAntecedentes[2]]&
                          variaveisDeEntrada[3][regrasAntecedentes[3]]&
                          variaveisDeEntrada[4][regrasAntecedentes[4]]&
                          variaveisDeEntrada[5][regrasAntecedentes[5]],
                          variavelDeSaida[resultado])
            regras.append(r)    
        if(qtde==5): 
            r = ctrl.Rule(variaveisDeEntrada[0][regrasAntecedentes[0]]&
                          variaveisDeEntrada[1][regrasAntecedentes[1]]& 
                          variaveisDeEntrada[2][regrasAntecedentes[2]]&
                          variaveisDeEntrada[3][regrasAntecedentes[3]]&
                          variaveisDeEntrada[4][regrasAntecedentes[4]],
                          variavelDeSaida[resultado])
            regras.append(r)    
        if(qtde==4): 
            r = ctrl.Rule(variaveisDeEntrada[0][regrasAntecedentes[0]]&
                          variaveisDeEntrada[1][regrasAntecedentes[1]]& 
                          variaveisDeEntrada[2][regrasAntecedentes[2]]&
                          variaveisDeEntrada[3][regrasAntecedentes[3]],
                          variavelDeSaida[resultado])
            regras.append(r)  
        if(qtde==3): 
            """print('*****************Vaqriavel de entrada****************')
            print(variaveisDeEntrada[0].label)
            print(variaveisDeEntrada[1].label)
            print(variaveisDeEntrada[2].label)
 
            print('*****************Varivel Linguistica****************')
            print(regrasAntecedentes[0])
            print(regrasAntecedentes[1])
            print(regrasAntecedentes[2])"""

            r = ctrl.Rule(variaveisDeEntrada[0][regrasAntecedentes[0]]&
                          variaveisDeEntrada[1][regrasAntecedentes[1]]& 
                          variaveisDeEntrada[2][regrasAntecedentes[2]],
                          variavelDeSaida[resultado])
            regras.append(r)   
        if(qtde==2): 
            """print('*****************Vaqriavel de entrada****************')
            print(variaveisDeEntrada[0].label)
            print(variaveisDeEntrada[1].label)
            print('*****************Varivel Linguistica****************')
            print(regrasAntecedentes[0])
            print(regrasAntecedentes[1])"""

            r = ctrl.Rule(variaveisDeEntrada[0][regrasAntecedentes[0]]&
                          variaveisDeEntrada[1][regrasAntecedentes[1]],
                          variavelDeSaida[resultado])
            regras.append(r) 
        if(qtde==1): 
            """print('*****************Vaqriavel de entrada****************')
            print(variaveisDeEntrada[0].label)
            print('*****************Varivel Linguistica****************')
            print(regrasAntecedentes[0])"""
            
            r = ctrl.Rule(variaveisDeEntrada[0][regrasAntecedentes[0]],
                          variavelDeSaida[resultado])
            regras.append(r)                                  
        #print('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/')
    return regras
    
    if nomeDaRegraDeCriterio=="Custo":
        preco = variaveisDeEntrada[0]
        pagamento = variaveisDeEntrada[1]
        reajuste = variaveisDeEntrada[2]
        custo = variavelDeSaida
        
        r1 = ctrl.Rule((preco["muitoAlto"] | preco["alto"]) & 
                   (pagamento["ruim"] | 
                    pagamento["bom"] |
                    pagamento["medio"] )
                   & ( reajuste["ruim"] | 
                    reajuste["bom"] |
                    reajuste["medio"] 
                        ),custo["muitoAlto"])
        r2 = ctrl.Rule(preco["medio"] ,custo["medio"])
        r3 = ctrl.Rule(preco["baixo"] ,custo["baixo"])
        r4 = ctrl.Rule(preco["muitoBaixo"] ,custo["muitoBaixo"])
        r5 = ctrl.Rule(preco["muitoAlto"] ,custo["alto"])
        regras.append(r1)
        regras.append(r2)
        regras.append(r3)
        regras.append(r4)
        regras.append(r5)
    if nomeDaRegraDeCriterio=="Qualidade":
        devolucao = variaveisDeEntrada[0]
        dimensoes = variaveisDeEntrada[1]
        equipe = variaveisDeEntrada[2]
        qualidade = variavelDeSaida
        
        r1 = ctrl.Rule( devolucao["bom"] & dimensoes["bom"] & equipe["bom"],qualidade["muitoAlto"])
        r2 = ctrl.Rule( devolucao["bom"] & ((dimensoes["bom"] | equipe["medio"]) |
                                           (dimensoes["medio"] | equipe["bom"])),qualidade["alto"])
        
        r3 = ctrl.Rule( (devolucao["bom"] | devolucao["medio"]) & dimensoes["medio"] & equipe["medio"],qualidade["medio"])
        r4 = ctrl.Rule( devolucao["bom"] & dimensoes["ruim"] & equipe["ruim"],qualidade["baixo"])
        r5 = ctrl.Rule( devolucao["ruim"] ,qualidade["muitoBaixo"])
    if nomeDaRegraDeCriterio=="Prazo":
        prazo = variaveisDeEntrada[0]
        producao = variaveisDeEntrada[1]
        resposta = variaveisDeEntrada[2]
        prazoGeral = variavelDeSaida
        
        r1 = ctrl.Rule( prazo["bom"] | producao["bom"] | resposta["bom"],prazoGeral["bom"])
        r2 = ctrl.Rule( prazo["medio"] | producao["medio"] | resposta["medio"],prazoGeral["medio"])
        r3 = ctrl.Rule( prazo["ruim"] | producao["ruim"] | resposta["ruim"],prazoGeral["ruim"])
        
       
        regras.append(r1)
        regras.append(r2)
        regras.append(r3)
    if nomeDaRegraDeCriterio=="Gestao":
        entrega = variaveisDeEntrada[0]
        cooperacao = variaveisDeEntrada[1]
        parceria = variaveisDeEntrada[2]
        transparencia = variaveisDeEntrada[3]
        comunicacao = variaveisDeEntrada[4]
        gestao = variavelDeSaida
        
        """r1 = ctrl.Rule( (entrega["bom"] | entrega[] ,gestao["bom"])
        r1 = ctrl.Rule( prazo["bom"] | producao["bom"] | resposta["bom"],prazoGeral["bom"])
        r1 = ctrl.Rule( prazo["bom"] | producao["bom"] | resposta["bom"],prazoGeral["bom"])
        r1 = ctrl.Rule( prazo["bom"] | producao["bom"] | resposta["bom"],prazoGeral["bom"])
        r1 = ctrl.Rule( prazo["bom"] | producao["bom"] | resposta["bom"],prazoGeral["bom"])
        """
       
        regras.append(r1)
        regras.append(r2)
        regras.append(r3)
              
    return regras

def GetCriteriosQualidade(req):
    criterios = []
    criterios.append({"nomeDaVariavel":"Devolução",
                      "NotaFuzzy":req["QualiDevolucao"]})
    criterios.append({"nomeDaVariavel":"Dimensões",
                      "NotaFuzzy":req["QualiDimensoes"]})
    criterios.append({"nomeDaVariavel":"Equipe",
                      "NotaFuzzy":req["QualiEquipe"]})
    
    return PreparaCriterios(listaDeCriterios=criterios, criterio="Qualidade")
    
def GetCriteriosPrazo(req):
    criterios = []
    criterios.append({"nomeDaVariavel":"Prazo",
                      "NotaFuzzy":req["PrazoPrazo"]})
    criterios.append({"nomeDaVariavel":"Produção",
                      "NotaFuzzy":req["PrazoProducao"]})
    criterios.append({"nomeDaVariavel":"Resposta",
                      "NotaFuzzy":req["PrazoResposta"]})
    
    return PreparaCriterios(listaDeCriterios=criterios, criterio="Prazo")

def GetCriteriosGestao(req):
    criterios = []
    criterios.append({"nomeDaVariavel":"Clareza",   "NotaFuzzy":req["GestaoEntrega"]})
    criterios.append({"nomeDaVariavel":"Cooperação",   "NotaFuzzy":req["GestaoCooperacao"]})
    criterios.append({"nomeDaVariavel":"Parceria",      "NotaFuzzy":req["GestaoParceria"]})
    criterios.append({"nomeDaVariavel":"Transparência",      "NotaFuzzy":req["GestaoTransparência"]})
    criterios.append({"nomeDaVariavel":"Boa comunicação",    "NotaFuzzy":req["GestaoComunicacao"]})
    return PreparaCriterios(listaDeCriterios=criterios, criterio="Gestao")

def GetCriteriosGeral(req):
    criterios = []
    criterios.append({"nomeDaVariavel":"Cumpre leis trabalhistas",     "NotaFuzzy":req["GeralLeis"]})
    criterios.append({"nomeDaVariavel":"Interesse",       "NotaFuzzy":req["GeralInteresses"]})
    criterios.append({"nomeDaVariavel":"Não usa substâncias tóxica",   "NotaFuzzy":req["GeralToxico"]})
    
    criterios.append({"nomeDaVariavel":"Histórico",     "NotaFuzzy":req["GeralHistoricoPrazo"]})
    criterios.append({"nomeDaVariavel":"Parceira",       "NotaFuzzy":req["GeralParceria"]})
    criterios.append({"nomeDaVariavel":"Histórico de fornecimento",   "NotaFuzzy":req["GeralHistorico"]})
    criterios.append({"nomeDaVariavel":"SSEGT",   "NotaFuzzy":req["GeralSaudeESeguranca"]})  
    
    
    return PreparaCriterios(listaDeCriterios=criterios, criterio="Geral")

def GetCriteriosGeralDoGoogleSheet(notas, df, nomeDoCriterio):
    
    
    criterios = []
    for registro in df.index:
        opcoes = []
        for k in str(df["variaveisDeEntrada"][registro]).split(','):
            opcoes.append(str(k))
        if(df["tipo"][registro]=="crisp"):
            crisp = notas[df["criterio"][registro]] 
            notaFuzzy = ""     
        criterios.append({"nomeDaVariavel":df["criterio"][registro],
                          "QtdeDeCasas":len(str(df["variaveisDeEntrada"][registro]).split(',')),
                          "Opções": opcoes,
                          "Criterio": nomeDoCriterio,
                          "NotaCrisp": crisp,
                          "NotaFuzzy": notaFuzzy})    
    return criterios

def PreparaCriterios( listaDeCriterios, criterio):
    criterios = []
    for item in listaDeCriterios:
        criterios.append({"nomeDaVariavel":item["nomeDaVariavel"],
            "QtdeDeCasas":3,
            "Opções": ["ruim", "medio", "bom"],
            "Criterio": criterio,
            "NotaCrisp": "",
            "NotaFuzzy": item["NotaFuzzy"]})
    return criterios    

def GetVariavelDeSaida(nomeDaVariavel, opcoes, criterio):
    return {"nomeDaVariavel":nomeDaVariavel,
        "QtdeDeCasas":0,
        "Opções": opcoes,
        "Criterio":criterio,
        "NotaCrisp": "",
        "NotaFuzzy":""}
    
#@app.route("/access_tokenTeste",  methods=["GET", "POST", "PUT"])
def access_tokenTeste():
   
    print("fsde")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = (
        f"client_id=puOWchQKGqbKGXsCmvJ38F8qRhEJlCln"
        f"&client_secret=o1IVbhcn3eVxfmg2"
        "&grant_type=client_credentials"
        "&scope=bucket:create bucket:read data:read bucket:update bucket:delete account:write user:write data:create data:write viewables:read"
    )
    #print(body)
    res =  requests.post("https://developer.api.autodesk.com/authentication/v1/authenticate", data=body, headers=headers)
    data = res.json()
    #print(data)
    
    #GetItens(data["access_token"])
   #j = GetBucketRota(token=data["access_token"])
   # print(j)
    
    """Esse funciona 
         res = make_response(data)
    """

    return data    
@app.route("/access_token",  methods=["GET", "POST", "PUT"])
def access_token():
    print("fsde")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = (
        f"client_id=puOWchQKGqbKGXsCmvJ38F8qRhEJlCln"
        f"&client_secret=o1IVbhcn3eVxfmg2"
        "&grant_type=client_credentials"
        "&scope=bucket:create bucket:read data:read bucket:update bucket:delete account:write user:write data:create data:write viewables:read"
    )
    #print(body)
    res =  requests.post("https://developer.api.autodesk.com/authentication/v1/authenticate", data=body, headers=headers)
    data = res.json()

    res = make_response(data)

    return res

#viewables:read data:read

def GetHubs(token):
    headers = {"Authorization": "Bearer "+token+"\""}#application/x-www-form-urlencoded"}
    
    res = requests.get("https://developer.api.autodesk.com/project/v1/hubs",  headers=headers)
    data = res.json()
    print(data)
    return data
@app.route("/CreateBucket/<nome>",  methods=["GET", "POST", "PUT"])
def CreateBucket(nome):

    token = access_tokenTeste()
    
    jtoken = token["access_token"]
    print("puowchhggffddaaaayyttrreehhhhggfgffn11111"+nome)
    header= { "Content-Type": "application/json", "Authorization": "Bearer "+jtoken   }   
    body = {
       "bucketKey":"puowchhggffddaaaayyttrreehhhhggfgffn11111"+nome,
       "policyKey":"persistent"}
    h = json.dumps(header, indent = 4) 
    b = json.dumps(body, indent = 4)
    res = requests.post("https://developer.api.autodesk.com/oss/v2/buckets", json= body  , headers=header)

    data = res.json()
    print(data)
    return data
@app.route("/DeleteBucket/<bucketKey>",  methods=["GET", "POST", "PUT","DELETE"])
def DeleteBucket(bucketKey):
    token = access_tokenTeste()   
    jtoken = token["access_token"]
    header= { "Authorization": "Bearer "+jtoken   }   
    """body = {     
       "bucketKey":"puowchhggffddaaaayyttrreehhhhggfgffn11111"+nome,
       "policyKey":"transient"}
    h = json.dumps(header, indent = 4) 
    b = json.dumps(body, indent = 4)"""
    res = requests.delete("https://developer.api.autodesk.com/oss/v2/buckets/"+bucketKey,  headers=header)
    return res.json()
@app.route("/GetBucketRot/<token>",  methods=["GET", "POST", "PUT"])
def GetBucketRota(token):
    header= {"Authorization": "Bearer "+token}     
    res = requests.get("https://developer.api.autodesk.com/oss/v2/buckets",  headers=header)
    buckets = res.json()
    
    return buckets
@app.route("/GetItensRota",  methods=["GET", "POST", "PUT"])
def GetItensRota():
    req = request.get_json()
    
    token = req["token_acess"]
    bucket = req["bucket"]    
    header= {"Authorization": "Bearer "+token}   
    res = requests.get("https://developer.api.autodesk.com/oss/v2/buckets/"+bucket+"/objects",  headers=header)
    itens = res.json()
   
    return itens
@app.route("/GetTreeViewModels",  methods=["GET", "POST", "PUT"])
def GetTreeViewModels():
    treeViewModels = []
    
    token = access_tokenTeste()
    
    jtoken = token["access_token"]
    ##print(jtoken["access_token"])

   
    buketsItem = GetBucket(jtoken)
    ##print(buketsItem["items"])
    #for buketItem in buketsItem:
    modelosBom = GetListBOM()
    #print(modelosBom)
    for bucket in buketsItem["items"]:
        
        ##print(bucket["bucketKey"])
        bucket = bucket["bucketKey"]   
        header= {"Authorization": "Bearer "+jtoken}   
        res = requests.get("https://developer.api.autodesk.com/oss/v2/buckets/"+bucket+"/objects",  headers=header)
        itens = res.json()
        ##print(itens)
        modelos = []
        i = 0
        for item in itens["items"]:
            listBom = []
            for itemBom in modelosBom:
                """#print(type(itemBom).__name__)
                #print(str(i)+'********************Item bOM*******************')
                #print(itemBom)
                #print(itemBom["MODELO"]) """
                i=i+1
                if(itemBom["MODELO"]==item["objectKey"]):
                    listBom.append({"bucketKey":bucket, "objectId":item["objectId"], "objectKey":item["objectKey"], "Nivel":2, "bom":itemBom})
            modelos.append({"bucketKey":bucket, "objectId":item["objectId"], "objectKey":item["objectKey"], "Nivel":1, "ListBom": listBom})           
        treeViewModels.append({"bucketKey":bucket, "Nivel":0, "objetos":modelos })    
    criterio = json.dumps(treeViewModels)
    res = make_response(criterio)
    ##print(criterio)
    
    return res
def GetBucket(token):
    header= {"Authorization": "Bearer "+token}     
    res = requests.get("https://developer.api.autodesk.com/oss/v2/buckets",  headers=header)
    buckets = res.json()
    return buckets
@app.route("/GetListBOM",  methods=["GET", "POST", "PUT"])
def GetListBOM():
    sheet = googleSheet.GoogleSheet()

    
    dataFrame = bancoDeDados.GetListBOM(nomeDaAba="EstruturaBOM",sheet=sheet)
    ##print(dataFrame)
   
    df = dataFrame.groupby(["MODELO", "NIVEL01"])
    ##print(df.first())
    Modelos = GetModelos(dataFrame=dataFrame)
    ##print(Modelos)

    vetorModelos = []
    vetorNiveis1 = []
    for modelo in Modelos.index:
        m = dataFrame.loc[dataFrame["MODELO"]==modelo]
        ##print('***************Modelo filtrado**************************')
       # #print(m)
        niveis1 = GetNivel01(dataFrame=m, modelo=modelo)
        
        for nivel1 in niveis1.index:
            ##print('***************Modelo filtrado nivel 1**************************')
            dfNivel1 = m.loc[m["NIVEL01"]==nivel1]
            ###print(dfNivel1)
            niveis2 = (dfNivel1.loc[dataFrame["NIVEL01"]==nivel1]).groupby("NIVEL02").first()
           # #print('***************Modelo filtrado nivel 2**************************')
            ##print(niveis2) 
            vetorNiveis2 = []
            for nivel2 in niveis2.index:
                vetorNiveis2.append({"MODELO":modelo, "NIVEL01":nivel1, "NIVEL02":nivel2, "Nivel":3})
            vetorNiveis1.append({"MODELO":modelo, "NIVEL01":nivel1, "NIVEL02":vetorNiveis2})
        vetorModelos.append({"MODELO":modelo, "NIVEL01":vetorNiveis1})
    #print(vetorNiveis1)        
    
    return vetorNiveis1
    
def GetModelos(dataFrame):
    df = (dataFrame.filter(items=["MODELO"])).groupby(["MODELO"]).first()
    return df
    
def GetNivel01(dataFrame, modelo):
    df = (dataFrame.loc[dataFrame["MODELO"]==modelo]).groupby("NIVEL01").first()
   # #print('******************GetMNivel01*********************')
    ##print(df)
    return df    
@app.route("/GetTreeViewPedidos",  methods=["GET", "POST", "PUT"])
def GetTreeViewPedidos():

   
    sheet = googleSheet.GoogleSheet()
    dfPedido = bancoDeDados.GetPedidos(sheet=sheet)
    #print("**********************************")
    #print(dfPedido)
    dfPedidoFornecedor = bancoDeDados.GetPedidoFornecedor(sheet=sheet)
    #print("**********************************")
    #print(dfPedidoFornecedor)
    
    #dfFornecedor = bancoDeDados.GetFornecedores(sheet=sheet)
    #print("**********************************")
    #print(dfFornecedor)
    treeViewPedidos=[]
    for i in dfPedido.index:
        dfFiltroFornecedor = dfPedidoFornecedor.loc[dfPedidoFornecedor["pedidoId"]==dfPedido["pedidoId"][i]]
        fornecedoresPedido = []
        for j in dfFiltroFornecedor.index:
            fornecedorPedido = {'text':dfFiltroFornecedor["fornecedorId"][j]+'-'+dfFiltroFornecedor["fornecedor"][j],
                                'data':{'fornecedorId':dfFiltroFornecedor["fornecedorId"][j], 'pedidoId':dfFiltroFornecedor["pedidoId"][j]}}
            fornecedoresPedido.append(fornecedorPedido)
        treeViewPedidos.append({'text':dfPedido["pedidoId"][i]+'-'+dfPedido["pedido"][i],
                       'children':fornecedoresPedido, 
                       'data':{'pedidoId':dfPedido["pedidoId"][i], 'pedido':dfPedido["pedido"][i]}})    
    criterio = json.dumps(treeViewPedidos)
    res = make_response(criterio)
    #print(criterio)
    
    return res
   
@app.route("/GetNotaPedidos",  methods=["GET", "POST", "PUT"])
def GetNotaPedidos():

    req = request.get_json()
    #print("**************************Req************")
    #print(req)
   
    sheet = googleSheet.GoogleSheet()
    dfnotaPedido = bancoDeDados.GetNotaPedidoFornecedor(sheet=sheet)
    dfFiltroNotaPedido = dfnotaPedido.loc[(dfnotaPedido["pedidoId"]==req["pedidoId"])&(dfnotaPedido["fornecedorId"]==req["fornecedorId"])]
    #print("**************FiltroNotaPedido****************")
    #print(dfFiltroNotaPedido)
    dfCriterios = bancoDeDados.GetCriterios(sheet=sheet, nomeDaAba='subcriterio')
    
    dfSubCriterios = bancoDeDados.GetSubCriterios(sheet=sheet)
    #print(dfSubCriterios)
    notas = []
    
    for i in dfSubCriterios.index:
        dfNotaSubCriterio = dfFiltroNotaPedido.loc[(dfFiltroNotaPedido["htmlId"]==dfSubCriterios["htmlId"][i])&
                                                   (dfFiltroNotaPedido["ativo"]=="1")]
        #print("**************NotaSubCriterio****************")
        #print(dfNotaSubCriterio )
        if(dfNotaSubCriterio.shape[0]>0):
            for j in dfNotaSubCriterio.index:
                nota={'htmlId':dfSubCriterios["htmlId"][i], 'nota':dfNotaSubCriterio["nota"][j]}
                notas.append(nota)
               
        else:
            if(dfSubCriterios["htmlId"][i]=='CustoPreco'):
                
                nota={'htmlId':dfSubCriterios["htmlId"][i], 'nota':0}    
                notas.append(nota)
            else:
                nota={'htmlId':dfSubCriterios["htmlId"][i], 'nota':'Selecionar'}    
                notas.append(nota)
         
    # print(notas)
    criterio = json.dumps(notas)
    res = make_response(criterio)
    #print(criterio)
    
    return res
    
    
@app.route("/GetSubCriterios",  methods=["GET", "POST", "PUT"])
def GetSubCriterios():

    #req = request.get_json()
    #print(req)  
    sheet = googleSheet.GoogleSheet()   
    dfSubCriterios = bancoDeDados.GetSubCriterios(sheet=sheet)
    #criterio = json.dumps(dfSubCriterios.to_json(orient="records"))
    criterio = dfSubCriterios.to_json(orient="records")
    res = make_response(criterio) 
    return res
@app.route("/GeraCombinacoes",  methods=["GET", "POST", "PUT"])
def GeraCombinacoes():

    #vetor = [["muitoAlto", "alto", "medio", "baixo", "muitoBaixo"],["ruim", "medio", "bom"], ["ruim", "medio", "bom"] ]
    
  

    
    
    #vetor = [["ruim", "medio", "bom"],["ruim", "medio", "bom"],["ruim", "medio", "bom"],["ruim", "medio", "bom"],["ruim", "medio", "bom"],["ruim", "medio", "bom"], ["ruim", "medio", "bom"] ]
    #colunas = ['Clareza','Cooperação','Parceria','Transparência','Boa comunicação']
    #colunas = ['Cumpre leis trabalhistas','Interesse','Não usa substâncias tóxica','Histórico','Parceira','Histórico de fornecimento','SSEGT']
    colunas = ['Preço',	'Pagamento',	'Reajuste']
    
    vetor = [["muitoAlto", "alto", "medio", "baixo", "muitoBaixo"], ["ruim", "medio", "bom"],["ruim", "medio", "bom"]]
    combinacoes=[]
    if(len(colunas)==3):
        for i in vetor[0]:
            for j in vetor[1]:
                for u in vetor[2]:                 
                     combinacoes.append([i, j, u])
    if(len(colunas)==7):
        for i in vetor[0]:
            for j in vetor[1]:
                for u in vetor[2]:
                    for z in vetor[3]:
                        for x in vetor[4]:
                            for p in vetor[5]:
                                for l in vetor[6]:
                                    combinacoes.append([i, j, u, z, x, p, l])
   
    if(len(colunas)==5):
        for i in vetor[0]:
            for j in vetor[1]:
                for u in vetor[2]:
                    for z in vetor[3]:
                        for x in vetor[4]:
                            combinacoes.append([i, j, u, z, x])
    

   
    df = pd.DataFrame(data=combinacoes, columns=colunas)
    
    #df = pd.DataFrame(data=combinacoes, columns=['Devolução', 'Dimensões','Equipe'])
    df.to_clipboard()
    criterio = df.to_json(orient="records")
    res = make_response(criterio) 
    return res
@app.route("/ConstruirRegrasRota/<colunas>/<opcoes>/<nomeDaPlanilha>",  methods=["GET", "POST", "PUT"])
def ConstruirRegrasRota(colunas, opcoes, nomeDaPlanilha):
    colunas1 =[]
    for i in colunas.split(','):
        colunas1.append(i)
    opcoesPorColuna1 = [] 
    for i in opcoes.split(','):
        opcoesPorColuna1.append(int(i))
       
    #print(opcoesPorColuna1)
    #print(colunas1)
    #colunas = ['Preco', 'Pagamento', 'Reajuste', 'Resultado', 'Formula', 'Regra']
    #opcoesPorColuna = [5,3,3]
    return ConstruirRegrasFuncao(colunas=colunas1, opcoesPorColuna=opcoesPorColuna1, nomeDaPlanilha=nomeDaPlanilha,idDaPlanilha= "1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524")
    

def ConstruirRegrasFuncao(colunas, opcoesPorColuna, nomeDaPlanilha,idDaPlanilha ):
    planilha = googleSheet.GoogleSheet()
    #colunas = ['Preco', 'Pagamento', 'Reajuste', 'Resultado', 'Formula', 'Regra']
    #opcoesPorColuna = [5,3,3]
    #print(colunas[0])

    a = list(string.ascii_uppercase)
    colunaFim=a[len(colunas)]#o primeiro  +1 é da formula e o segundo +1 é a Regra
    #print(a)
    #print("*******************COLUNA FIM******************")
    #print(colunaFim)
    #print(nomeDaPlanilha+"!B2:"+colunaFim+"15000")
   
     
    dfRegrasBase = bancoDeDados.GetBaseRegras(sheet=planilha, 
                                              sampleRange=nomeDaPlanilha+"!B2:"+colunaFim+"15000", 
                                              idDaPlanilha=idDaPlanilha,
                                              colunas=colunas)
    
    for i in dfRegrasBase.index:
        dfRegrasBase["Formula"][i]="Indefinido"
    #print(dfRegrasBase)
    qtdeDeCriterios = len(colunas)-3
    ff = 0
    if(qtdeDeCriterios>=7):
        for i in dfRegrasBase.index:
            dff = dfRegrasBase.loc[(dfRegrasBase[colunas[0]]==dfRegrasBase[colunas[0]][i])&
                                   (dfRegrasBase[colunas[1]]==dfRegrasBase[colunas[1]][i])&
                                   (dfRegrasBase[colunas[2]]==dfRegrasBase[colunas[2]][i])&
                                   (dfRegrasBase[colunas[3]]==dfRegrasBase[colunas[3]][i])&
                                   (dfRegrasBase[colunas[4]]==dfRegrasBase[colunas[4]][i])&
                                   (dfRegrasBase[colunas[5]]==dfRegrasBase[colunas[5]][i])&
                             
                                   (dfRegrasBase["Resultado"]==dfRegrasBase["Resultado"][i])&
                                   (dfRegrasBase["Formula"]=='Indefinido')
                                ]
            dff7Colunas = dff[[colunas[0], colunas[1],  colunas[2], colunas[3], colunas[4],colunas[5], 'Resultado', 'Formula']]
            ##print('******************************************')
            ##print(dff7Colunas)
            ##print(str(len(dff7Colunas.index)))
            ##print(str(opcoesPorColuna[6]))
            
            if(len(dff7Colunas.index)<opcoesPorColuna[6]):              
                for k in dff7Colunas.index:
                    #print("o "+str(k)+" foi definido como 7"+" Total index "+ str(len(dff7Colunas.index)))
                    dfRegrasBase["Formula"][k]=7
    #print("Passou o 7")    
   
    if(qtdeDeCriterios>=6):
        for i in dfRegrasBase.index:
            dff = dfRegrasBase.loc[(dfRegrasBase[colunas[0]]==dfRegrasBase[colunas[0]][i])&
                                (dfRegrasBase[colunas[1]]==dfRegrasBase[colunas[1]][i])&
                                (dfRegrasBase[colunas[2]]==dfRegrasBase[colunas[2]][i])&
                                (dfRegrasBase[colunas[3]]==dfRegrasBase[colunas[3]][i])&
                                (dfRegrasBase[colunas[4]]==dfRegrasBase[colunas[4]][i])&
                        
                                (dfRegrasBase["Resultado"]==dfRegrasBase["Resultado"][i])&
                                (dfRegrasBase["Formula"]=='Indefinido')
                                ]
            dff6Colunas = dff[[colunas[0], colunas[1],  colunas[2],colunas[3], colunas[4], 'Resultado', 'Formula']]
           # #print(dff6Colunas)
            if(len(dff6Colunas.index)<(opcoesPorColuna[5])):              
                for k in dff6Colunas.index:
                    #print("o "+str(k)+" foi definido como 6")
                    dfRegrasBase["Formula"][k]=6
    #print("Passou o 6")    
       
    if(qtdeDeCriterios>=5):
        for i in dfRegrasBase.index:
            dff = dfRegrasBase.loc[(dfRegrasBase[colunas[0]]==dfRegrasBase[colunas[0]][i])&
                                (dfRegrasBase[colunas[1]]==dfRegrasBase[colunas[1]][i])&
                                (dfRegrasBase[colunas[2]]==dfRegrasBase[colunas[2]][i])&
                                (dfRegrasBase[colunas[3]]==dfRegrasBase[colunas[3]][i])&
                               
                                (dfRegrasBase["Resultado"]==dfRegrasBase["Resultado"][i])&
                                (dfRegrasBase["Formula"]=='Indefinido')
                                ]
            dff5Colunas = dff[[colunas[0], colunas[1],  colunas[2],colunas[3],  'Resultado', 'Formula']]
            if(len(dff5Colunas.index)<(opcoesPorColuna[4])):              
                for k in dff5Colunas.index:
                    #print("o "+str(k)+" foi definido como 5")
                    dfRegrasBase["Formula"][k]=5        
    #print("Passou o 5")  
    if(qtdeDeCriterios>=4):
        for i in dfRegrasBase.index:
            dff = dfRegrasBase.loc[(dfRegrasBase[colunas[0]]==dfRegrasBase[colunas[0]][i])&
                            (dfRegrasBase[colunas[1]]==dfRegrasBase[colunas[1]][i])&
                            (dfRegrasBase[colunas[2]]==dfRegrasBase[colunas[2]][i])&                           
                            (dfRegrasBase["Resultado"]==dfRegrasBase["Resultado"][i])&
                            (dfRegrasBase["Formula"]=='Indefinido')
                            ]
            dff4Colunas = dff[[colunas[0], colunas[1],  colunas[2], 'Resultado', 'Formula']]
            if(len(dff4Colunas.index)<(opcoesPorColuna[3])):              
                for k in dff4Colunas.index:
                    #print("o "+str(k)+" foi definido como 5")
                    dfRegrasBase["Formula"][k]=4  
    for i in dfRegrasBase.index:
        dff = dfRegrasBase.loc[(dfRegrasBase[colunas[0]]==dfRegrasBase[colunas[0]][i])&
                               (dfRegrasBase[colunas[1]]==dfRegrasBase[colunas[1]][i])&
                               (dfRegrasBase["Resultado"]==dfRegrasBase["Resultado"][i])&
                               (dfRegrasBase["Formula"]=='Indefinido')
                               ]
        dff3Colunas = dff[[colunas[0], colunas[1],  'Resultado', 'Formula']]
        if(len(dff3Colunas.index)<(opcoesPorColuna[2])):              
                for k in dff3Colunas.index:
                    dfRegrasBase["Formula"][k]=3 
      
    for i in dfRegrasBase.index:
        dff = dfRegrasBase.loc[(dfRegrasBase[colunas[0]]==dfRegrasBase[colunas[0]][i])&
                               (dfRegrasBase["Resultado"]==dfRegrasBase["Resultado"][i])&
                               (dfRegrasBase["Formula"]=='Indefinido')
                               ]
        dff2Colunas = dff[[colunas[0],  'Resultado', 'Formula']]

        if(len(dff2Colunas.index)<opcoesPorColuna[1]):              
                for k in dff2Colunas.index:
                    dfRegrasBase["Formula"][k]=2 
    for i in (dfRegrasBase.loc[dfRegrasBase["Formula"]=="Indefinido"]).index:
        if(dfRegrasBase["Formula"][i]=='Indefinido'):        
           dfRegrasBase["Formula"][i]=1 

    for i in dfRegrasBase.index:
        regra = ""

        j = 0
        w = dfRegrasBase["Formula"][i]
        while  j < w:
            regra = regra+dfRegrasBase[colunas[j]][i]+";"
            j = j+1
        regra = regra[:-1] +'|'+dfRegrasBase["Resultado"][i]
        dfRegrasBase["Regra"][i] = regra
    v = dfRegrasBase.values.tolist()
    sheet = planilha.GetService()
    bancoDeDados.SetBaseRegras(sheet=sheet, valores=v, nomeDaPlanilha=nomeDaPlanilha, 
                               idDaPlanilha="1dBgZ4Zzl0B4esOjsSy5h0YeYD_XaqftJzqQPithL524", 
                               coluna= colunaFim)    
   
    return dfRegrasBase.to_json(orient='records')
   
   