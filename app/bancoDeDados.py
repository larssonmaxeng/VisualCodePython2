import pandas as pd
from app import googleSheet
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
def GetFornecedores(sheet):
    linha = GetLinhaMaxima(nome="fornecedor", sheet=sheet)+1
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='fornecedor!A3:B'+str(linha), SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    df = pd.DataFrame(planilha, columns=['fornecedorId','fornecedor'])
    return df
def GetFornecedore(nome, sheet):
    df = GetFornecedores(sheet)
    dfFiltro = df.loc[df["fornecedor"]==nome]
    for f in dfFiltro.index:
        print(f)
        return f
    return []
def GetPedidos(sheet):
    linha = GetLinhaMaxima(nome="pedido", sheet=sheet)+1
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='pedido!A3:B'+str(linha), SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    df = pd.DataFrame(planilha, columns=['pedidoId','pedido'])
    return df
def GetNotaPedidoFornecedor(sheet):
    linha = GetLinhaMaxima(nome="notaPedidoFornecedor", sheet=sheet)+1
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='notaPedidoFornecedor!A3:H'+str(linha), SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    df = pd.DataFrame(planilha, columns=['notaPedidoForncedorId', 'pedidoId',	'fornecedorId'	,'criterio',	'subcriterio',	'nota', 'htmlId', 'ativo'])   
    #print(df)
    return df
    dfFiltropedido = df.loc[df["pedidoId"]==pedidoId]
    dfFiltroFornecedor = dfFiltropedido.loc[dfFiltropedido["pedidoId"]==fornecedorId]
    return dfFiltroFornecedor
def GetPedidoFornecedor(sheet):
    linha = GetLinhaMaxima(nome="pedidoFornecedor", sheet=sheet)+1
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='pedidoFornecedor!A3:E'+str(linha), SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    df = pd.DataFrame(planilha, columns=['pedidoFornecedorId',	'fornecedorId',	'pedidoId','fornecedor','pedido' ])   
    return df
    """dfFiltropedido = df.loc[df["pedidoId"]==pedidoId]
    dfFiltroFornecedor = dfFiltropedido.loc[dfFiltropedido["pedidoId"]==fornecedorId]
    return dfFiltroFornecedor"""
def GetLinhaMaxima(nome, sheet):
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='NumeroRegistros!A2:B10', SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    df = pd.DataFrame(planilha, columns=['tabela','numeroRegistro'])
    dfFiltro = df.loc[df['tabela']==nome]
    #print(dfFiltro)
    for f in dfFiltro.index:
        #print(dfFiltro["numeroRegistro"][f])
        return int(dfFiltro["numeroRegistro"][f])
    return []

def GetCriterios(sheet):
    linha = 7#GetLinhaMaxima(nome="pedido", sheet=sheet)+1
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='criterio!A3:D'+str(linha), SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    df = pd.DataFrame(planilha, columns=['criterioId','criterio','tipo','htmlId'])
    return df
def GetSubCriterios(sheet):
    linha = 23#GetLinhaMaxima(nome="pedido", sheet=sheet)+1
    planilha = sheet.GetDados(SAMPLE_RANGE_NAME='subcriterio!A3:G'+str(linha), SAMPLE_SPREADSHEET_ID='13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig')
    df = pd.DataFrame(planilha, columns=['subcriterioId',	'criterioId',	'subcriterio',	'tipo',	'variavelLinguistica',	'htmlId',	'criterio'])
    return df
def SetSubCriterios(sheet, valores, listaParaLimpar):
    linha =GetLinhaMaxima(nome="notaPedidoFornecedor", sheet=googleSheet.GoogleSheet())+1+1
    zerar = []
    zerar.append([0])
    for l in listaParaLimpar:
        sheet.values().update(spreadsheetId= "13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig", 
                              range="notaPedidoFornecedor!C"+str(l)+":C"+str(l) , 
                              valueInputOption="RAW",
                              body={"values":zerar}).execute()
        print("Excluído:"+str(l))
        
    print(linha)
    print(str(linha + len(valores)))
    
    response = sheet.values().update(spreadsheetId= "13uGK7sZM0z2YOkJPiLJ_Tby0dwsooCaIIOg__FTdFig", 
                          range="notaPedidoFornecedor!B"+str(linha)+":H"+str(linha + len(valores)) , 
                          valueInputOption="RAW",
                          body={"values":valores}).execute()
    print(response)
    
def GetBaseRegras(sheet, sampleRange, idDaPlanilha, colunas ):

    planilha = sheet.GetDados(SAMPLE_RANGE_NAME=sampleRange, SAMPLE_SPREADSHEET_ID=idDaPlanilha)
    df = pd.DataFrame(planilha, columns=colunas)
    return df    
def SetBaseRegras(sheet, valores, nomeDaPlanilha, idDaPlanilha, coluna ):
    linha =len(valores)+1
    
    response = sheet.values().update(spreadsheetId= idDaPlanilha, 
                          range=nomeDaPlanilha+"!B2:"+coluna+str(linha) , 
                          valueInputOption="RAW",
                          body={"values":valores}).execute()
    print(response)
    