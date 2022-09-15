from sklearn.datasets import load_iris
import base64
from email.encoders import encode_base64
import json
from json import *
from urllib import response
from app import app
from flask import render_template, redirect, jsonify, make_response
import matplotlib.pyplot as mlt
import numpy as np
import skfuzzy as fuzz
from time import sleep
from skfuzzy import control as ctrl
from flask import request
from app import funcoes
import requests
import pandas as pd


import io

from app import googleSheet
from app import bancoDeDados

@app.route('/')
@app.route('/index')
def index():
    nome = "dissertação2"
    criterio = {"nome":"Preço", "nota":"Médio"}
    
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
    print('leu regras')
    custo_simulador = ctrl.ControlSystemSimulation(custo_ctrl)
    print('simulou')
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
    print(nome)
    return render_template('index.html', nome=nome, criterio=criterio, fig = figura )

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
   
    #    print('começou')

    #print('terminou')
    #fecharCompra_ctrl = ctrl.ControlSystem([r4, r41, r2, r3, r5, r1, r11 , r7])
    r1 = ctrl.Rule((preco[muitoAlto] & qualidade[muitoRuim] ) | (preco[alto] & qualidade[muitoRuim] & prazo[muitoAlto]) ,fecharCompra[alto]) 
    fecharCompra_ctrl = ctrl.ControlSystem([r1])
    print('leu regras')
    fecharCompra_simulador = ctrl.ControlSystemSimulation(fecharCompra_ctrl)
    print('simulou')

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
    print(fecharCompra_simulador.output[vsFecharCompra])"""
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
    #print(sheet.GetParametros( SAMPLE_RANGE_NAME= 'DadosGerais!A2:A5', SAMPLE_SPREADSHEET_ID="1NLqJWL8LeRECbK04Bm41AYq0tu95VbYgsT6DTX6Sq1g"))
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
    print(criteriosCusto)   
    custo, imagemCusto = ConstruirControladorFuzzy( 
                                                   inomeDasVariaveisDeEntrada=criteriosCusto, 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaCusto,
                                                   iRegra = "Custo")   
   
    
    variavelDeSaidaQualidade = GetVariavelDeSaida(nomeDaVariavel="Qualidade", opoces =["muitoBaixo", "baixo", "medio", "alto", "muitoAlto"],criterio= "Qualidade")
    qualidade, imagemQualidade =ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosQualidade(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaQualidade,
                                                   iRegra = "Qualidade")  
    
    variavelDeSaidaPrazo = GetVariavelDeSaida(nomeDaVariavel="PrazoSaida", opoces = ["ruim", "medio", "bom"],criterio= "Prazo")
    prazo, imagemPrazo = ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosPrazo(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaPrazo,
                                                   iRegra = "Prazo")  
    
    variavelDeSaidaGestao = GetVariavelDeSaida(nomeDaVariavel="Gestão", opoces = ["ruim", "medio", "bom"],criterio= "Gestao")
    gestao, imagemGestao = ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosGestao(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaGestao,
                                                   iRegra = "Prazo")  
    variavelDeSaidaGeral = GetVariavelDeSaida(nomeDaVariavel="Geral", opoces = ["ruim", "medio", "bom"],criterio= "Geral")   
    geral, imagemGeral = ConstruirControladorFuzzy(
                                                   inomeDasVariaveisDeEntrada=GetCriteriosGeral(req=req), 
                                                   inomeDaVariavelDeSaida=variavelDeSaidaGeral,
                                                   iRegra = "Geral")     
    
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
    
    criterio = json.dumps(criterios)
    #print(criterio)
    
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

        
def ConstruirControladorFuzzy(inomeDasVariaveisDeEntrada, inomeDaVariavelDeSaida, iRegra):    
     
    variaveisFuzzy = []
    for nome in inomeDasVariaveisDeEntrada:
        variavelFuzzy = ctrl.Antecedent(np.arange(0, 11, 0.5), nome["nomeDaVariavel"])
        variavelFuzzy.automf(nome["QtdeDeCasas"], names = nome["Opções"])
        variaveisFuzzy.append(variavelFuzzy)
   
    variavelDeSaida = ctrl.Consequent(np.arange(0, 11, 0.1), inomeDaVariavelDeSaida["nomeDaVariavel"])
    variavelDeSaida.automf(inomeDaVariavelDeSaida["QtdeDeCasas"], names = inomeDaVariavelDeSaida["Opções"])
      
    custo_ctrl = ctrl.ControlSystem(GerarRegras(variaveisDeEntrada=variaveisFuzzy, variavelDeSaida=variavelDeSaida, nomeDaRegraDeCriterio = iRegra))
    print('leu regras')
    custo_simulador = ctrl.ControlSystemSimulation(custo_ctrl)
    print('simulou')
    #print(inotasCusto) 
    print(inomeDasVariaveisDeEntrada)

    for nome in inomeDasVariaveisDeEntrada:
        print(nome["nomeDaVariavel"])
        print(nome["NotaCrisp"])
        print(nome["NotaFuzzy"])
        if nome["nomeDaVariavel"] == "Preço":
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

def GerarRegras(variaveisDeEntrada, variavelDeSaida, nomeDaRegraDeCriterio):
    regras = []
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
    print(buckets)
    return buckets
@app.route("/GetItensRota",  methods=["GET", "POST", "PUT"])
def GetItensRota():
    req = request.get_json()
    print(req)
    token = req["token_acess"]
    bucket = req["bucket"]    
    header= {"Authorization": "Bearer "+token}   
    res = requests.get("https://developer.api.autodesk.com/oss/v2/buckets/"+bucket+"/objects",  headers=header)
    itens = res.json()
    print(itens)
    return itens
@app.route("/GetTreeViewModels",  methods=["GET", "POST", "PUT"])
def GetTreeViewModels():
    treeViewModels = []
    
    token = access_tokenTeste()
    
    jtoken = token["access_token"]
    #print(jtoken["access_token"])

   
    buketsItem = GetBucket(jtoken)
    #print(buketsItem["items"])
    #for buketItem in buketsItem:
    modelosBom = GetListBOM()
    for bucket in buketsItem["items"]:
        
        #print(bucket["bucketKey"])
        bucket = bucket["bucketKey"]   
        header= {"Authorization": "Bearer "+jtoken}   
        res = requests.get("https://developer.api.autodesk.com/oss/v2/buckets/"+bucket+"/objects",  headers=header)
        itens = res.json()
        #print(itens)
        modelos = []
        i = 0
        for item in itens["items"]:
            listBom = []
            for itemBom in modelosBom:
                print(type(itemBom).__name__)
                print(str(i)+'********************Item bOM*******************')
                print(itemBom)
                print(itemBom["MODELO"]) 
                i=i+1
                if(itemBom["MODELO"]==item["objectKey"]):
                    listBom.append({"bucketKey":bucket, "objectId":item["objectId"], "objectKey":item["objectKey"], "Nivel":2, "bom":itemBom})
            modelos.append({"bucketKey":bucket, "objectId":item["objectId"], "objectKey":item["objectKey"], "Nivel":1, "ListBom": listBom})           
        treeViewModels.append({"bucketKey":bucket, "Nivel":0, "objetos":modelos })    
    criterio = json.dumps(treeViewModels)
    res = make_response(criterio)
    #print(criterio)
    
    return res
def GetBucket(token):
    header= {"Authorization": "Bearer "+token}     
    res = requests.get("https://developer.api.autodesk.com/oss/v2/buckets",  headers=header)
    buckets = res.json()
    return buckets
@app.route("/GetListBOM",  methods=["GET", "POST", "PUT"])
def GetListBOM():
    sheet = googleSheet.GoogleSheet()
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='Nivel2!b2:d10', SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    index = sheet.GetDados(SAMPLE_RANGE_NAME='Nivel2!A2:a10', SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    colunas = sheet.GetDados(SAMPLE_RANGE_NAME='Nivel2!b1:d1', SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    #print(index)
    
    dataFrame = pd.DataFrame(planilha, columns=colunas[0])
    #print(dataFrame)
   
    df = dataFrame.groupby(["MODELO", "NIVEL01"])
    #print(df.first())
    Modelos = GetModelos(dataFrame=dataFrame)
    #print(Modelos)

    vetorModelos = []
    vetorNiveis1 = []
    for modelo in Modelos.index:
        m = dataFrame.loc[dataFrame["MODELO"]==modelo]
        #print('***************Modelo filtrado**************************')
       # print(m)
        niveis1 = GetNivel01(dataFrame=m, modelo=modelo)
        
        for nivel1 in niveis1.index:
            #print('***************Modelo filtrado nivel 1**************************')
            dfNivel1 = m.loc[m["NIVEL01"]==nivel1]
            ##print(dfNivel1)
            niveis2 = (dfNivel1.loc[dataFrame["NIVEL01"]==nivel1]).groupby("NIVEL02").first()
           # print('***************Modelo filtrado nivel 2**************************')
            #print(niveis2) 
            vetorNiveis2 = []
            for nivel2 in niveis2.index:
                vetorNiveis2.append({"MODELO":modelo, "NIVEL01":nivel1, "NIVEL02":nivel2})
            vetorNiveis1.append({"MODELO":modelo, "NIVEL01":nivel1, "NIVEL02":vetorNiveis2})
        vetorModelos.append({"MODELO":modelo, "NIVEL01":vetorNiveis1})
    print(vetorNiveis1)        
    
    return vetorNiveis1
    
def GetModelos(dataFrame):
    df = (dataFrame.filter(items=["MODELO"])).groupby(["MODELO"]).first()
    return df
    
def GetNivel01(dataFrame, modelo):
    df = (dataFrame.loc[dataFrame["MODELO"]==modelo]).groupby("NIVEL01").first()
   # print('******************GetMNivel01*********************')
    #print(df)
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
    print(req)
   
    sheet = googleSheet.GoogleSheet()
    dfnotaPedido = bancoDeDados.GetNotaPedidoFornecedor(sheet=sheet)
    dfFiltroNotaPedido = dfnotaPedido.loc[(dfnotaPedido["pedidoId"]==req["pedidoId"])&(dfnotaPedido["fornecedorId"]==req["fornecedorId"])]
    return dfFiltroNotaPedido.to_json(orient="records")
    
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