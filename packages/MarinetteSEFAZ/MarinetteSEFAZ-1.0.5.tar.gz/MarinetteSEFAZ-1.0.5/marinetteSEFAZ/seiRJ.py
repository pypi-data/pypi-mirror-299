import time
from time import sleep
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
from openpyxl import load_workbook
from datetime import date
from glob import glob
from shutil import move
import tabula
from PyPDF2 import PdfReader

def loginSEI(navegador: webdriver.Firefox, login, senha,nomeCoordenacao):
    
    navegador.get("https://sei.rj.gov.br/sip/login.php?sigla_orgao_sistema=ERJ&sigla_sistema=SEI")
    
    usuario = navegador.find_element(By.XPATH, value='//*[@id="txtUsuario"]')
    usuario.send_keys(login)

    campoSenha = navegador.find_element(By.XPATH, value='//*[@id="pwdSenha"]')
    campoSenha.send_keys(senha)

    exercicio = Select(navegador.find_element(By.XPATH, value='//*[@id="selOrgao"]'))
    exercicio.select_by_visible_text('SEFAZ')

    btnLogin = navegador.find_element(By.XPATH, value='//*[@id="Acessar"]')
    btnLogin.click()

    navegador.maximize_window()
    
    WebDriverWait(navegador,5).until(EC.presence_of_element_located, ((By.XPATH, "//div[text() = 'Controle de Processos']")))
    
    navegador.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE) 
    
    trocarCoordenacao(navegador, nomeCoordenacao)
    
    
def trocarCoordenacao(navegador: webdriver.Firefox, nomeCoordenacao):
    coordenacao = navegador.find_elements(By.XPATH, "//a[@id = 'lnkInfraUnidade']")[1]
    print(coordenacao)
    if coordenacao.get_attribute("innerHTML") != nomeCoordenacao:
        print(coordenacao)
        coordenacao.click()
        WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Trocar Unidade')]")))
        navegador.find_element(By.XPATH, "//td[text() = '"+nomeCoordenacao+"' ]").click() 
        
def abrirPastas(navegador: webdriver.Firefox):
    navegador.switch_to.default_content()
    WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
    listaDocs = WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.ID, "divArvore")))
    pastas = listaDocs.find_elements(By.XPATH, '//a[contains(@id, "joinPASTA")]')
    
    for doc in pastas[:-1]:
        doc.click() 
        WebDriverWait(navegador,5).until(EC.presence_of_element_located((By.XPATH, "//*[text() = 'Aguarde...']")))
        WebDriverWait(navegador,5).until(EC.invisibility_of_element((By.XPATH, "//*[text() = 'Aguarde...']")))
    
    navegador.switch_to.default_content()
    
def pesquisarProcesso(navegador: webdriver.Firefox, processoSEI):

    barraPesquisa = navegador.find_element(By.ID, "txtPesquisaRapida")
    barraPesquisa.send_keys(processoSEI)
    barraPesquisa.send_keys(Keys.ENTER)
    
def buscarInformacoesEmArquivos(navegador: webdriver.Firefox, listaArquivos, funcao= lambda x: None):
    listaArquivos = transformarElementoEmLista(listaArquivos)

    
    navegador.switch_to.default_content()
    WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
    docs = navegador.find_elements(By.XPATH, "//div[@id = 'divArvore']//div//a[@class = 'infraArvoreNo']")
    quantDocs = len(docs)
    for doc in (range(quantDocs)):
        docTexto = docs[doc].text
        if any(arquivo.upper() in docTexto.upper() for arquivo in listaArquivos):   
            docs[doc].click()
            navegador.switch_to.default_content()            
            WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrVisualizacao")))
            WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvoreHtml")))
            time.sleep(2)
            resultado = funcao()
    
            if resultado != None:
                return resultado

            else:
                navegador.switch_to.default_content()
                WebDriverWait(navegador,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifrArvore")))
                docs = navegador.find_elements(By.XPATH, "//div[@id = 'divArvore']//div//a[@class = 'infraArvoreNo']")         
            
    
def procurarEBaixarArquivos(navegador: webdriver.Firefox,listaArquivos, funcao= lambda x: None):
    
    listaArquivos = transformarElementoEmLista(listaArquivos)

    navegador.switch_to.default_content()
    arvore = WebDriverWait(navegador,10).until(EC.presence_of_element_located((By.ID, "ifrArvore")))    
    navegador.switch_to.frame(arvore)

    listaDocs =  WebDriverWait(navegador,10).until(EC.presence_of_element_located((By.ID, "divArvore")))  
    docs = listaDocs.find_elements(By.TAG_NAME, "a")

    for doc in docs:
        if any(arquivo.upper() in doc.text.upper() for arquivo in listaArquivos):
            doc.click()
            

def transformarElementoEmLista(listaArquivos):
    if listaArquivos == str:
        arquivo = listaArquivos
        listaArquivos = []
        listaArquivos.append(arquivo)
        return listaArquivos
    if listaArquivos == list:
        return listaArquivos