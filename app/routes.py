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
import io

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
    
    
    
    return render_template('resultado.html', modo="Limpeza", criterios = criterios, subcriterios = subcriterios, imagens=[])

@app.route('/your_url', methods=["GET", "POST", "PUT"])
def your_url():
    #criterio = {"nome":"Preço", "nota":"Médio"}
    #req = request.div["div3"]
    #print(req.name)
    req = request.get_json()
    print(req)
    for song in req:
        print(song, ":", req[song])
    """if request.method == "POST":
       print(request)
    print('foi ate aqui')
    print(request)
    #print(req)"""
    print("passou")
    #criterios = []
    #criterios.append({"nome":"Preço", "nota":"Médio"})
    #criterios.append({"nome":"Preço1", "nota":"Médio1"})
    custo, imagemCusto = CalcularCriterioPreco(notasCusto = req)   
    criterios = []
    criterios.append({"idHtml":"imagemCusto", "valor":str(imagemCusto)})
    criterios.append({"idHtml":"crispCusto", "valor":str(round(custo*1, 2))})
    criterio = json.dumps(criterios)
    #print(criterio)
    
    res = make_response(criterio)
    #print(res)
    
    return res
  
def CalcularCriterioPreco(notasCusto):
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

    for nota in notasCusto:
        match nota:
            case "CustoPreco":
                custo_simulador.input[vePreco] =8# notasCusto[nota]
            case "CustoPgto":
                custo_simulador.input[vePagamento] = 2;#notasCusto[nota]
            case "CustoReajuste":
                custo_simulador.input[veReajuste] = 2;#notasCusto[nota]
            
    

    custo_simulador.compute()

    v = fuzz.control.visualization.FuzzyVariableVisualizer(custo)
    imagem, b = v.view(sim=custo_simulador)
    data = io.BytesIO()
    imagem.savefig(data, format="PNG")
    encodes_img_data = base64.b64encode(data.getbuffer()).decode('ascii')
    #print(custo_simulador.output[vsCusto])
    #print(encodes_img_data)
    return custo_simulador.output[vsCusto] , encodes_img_data

     