import base64
from app import app
from flask import render_template
import matplotlib.pyplot as mlt
import numpy as np
import skfuzzy as fuzz
from time import sleep
from skfuzzy import control as ctrl
import io

@app.route('/')
@app.route('/index')
def index():
    nome = "dissertação2"
    criterio = {"nome":"Preço", "nota":"Médio"}
    return render_template('index.html', nome=nome, criterio=criterio)
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
    return render_template('resultado.html', nome=nome, criterio=criterio, imagem = encodes_img_data.decode('utf-8'))

     