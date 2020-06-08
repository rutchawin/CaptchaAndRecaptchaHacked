from selenium.webdriver.remote.webdriver import WebDriver
from flask import Flask,request, jsonify, Response
from dotenv import load_dotenv, find_dotenv
from bradocs4py import ValidadorCnpj
from selenium import webdriver
from bs4 import BeautifulSoup
from waitress import serve
import random
import warnings
import requests
import logging
import base64
import json
import time
import os
import re

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument('headless')

load_dotenv(find_dotenv())
port = os.getenv('PORT')
host = os.getenv('IP')
back_end_url = os.getenv('SN_FEDERAL_BACKEND_URL')
route = os.getenv('SN_FEDERAL_CONTEXTO')
path = os.getenv('CHROME_DRIVER_PATH')
LOG_LEVEL = os.environ.get('LOG_LEVEL')
logging.basicConfig(format='%(asctime)s %(message)s',level = LOG_LEVEL)

random_ip = []
random_port = []

def random_proxy():
    r = requests.get(url='https://www.sslproxies.org/')
    soup = BeautifulSoup(r.text, 'html.parser')

    for x in soup.findAll('td')[::8]:
        random_ip.append(x.get_text())

    for y in soup.findAll('td')[1::8]:
        random_port.append(y.get_text())

    z = list(zip(random_ip, random_port))

    number = random.randint(0, len(z)-50)
    ip_random = z[number]

    ip_random_string = "{}:{}".format(ip_random[0],ip_random[1])

    proxy = {'https':ip_random_string}

    return proxy

app = Flask(__name__)
@app.route(route, methods=['POST'])
def api():
    servico = 'SIMPLESNACIONAL'
    statusType = False
    statusNumber = False
    data = request.get_json(force=True)
    document_number = data['documento']['numeroDocumento']
    docType = data['documento']['tipoDocumento']
    serv = data['servico']
  
    if docType.upper() == 'J':
        statusNumber = ValidadorCnpj.validar(document_number)
        statusType  = True

    if serv.upper() != servico:
        logging.error('Serviço inválido!')
        return jsonify({"codigo": 400, 
                            "mensagem": "Nome do serviço inválido"})
    if len(document_number) == 0 or len(docType) == 0:
        logging.error('Parâmetros inválidos!')
        return jsonify({"codigo": 400, 
                            "mensagem": "Parâmetros inválidos"})
    if statusType != True:
        logging.error('Tipo de documento inválido!')
        return jsonify({"codigo": 400, 
                        "mensagem": "Tipo de documento inválido"})

    if statusNumber != True:
        logging.error('Número do documento inválido!')
        return jsonify({"codigo": 400, 
                        "mensagem": "Número do documento inválido"})

    else:
        if len(document_number) == 14:
            go = webdriver.Chrome(path,options=chrome_options)
            go.implicitly_wait(3)
            go.get(back_end_url)
            time.sleep(0.2)
            RequestVerificationToken = go.find_element_by_xpath('//*[@id="conteudoPage"]/div[2]/form/input[2]').get_attribute('value')
            time.sleep(0.3)
            TokenRecapcha = go.find_element_by_xpath('//*[@id="tokenRecapcha"]').get_attribute('value')
            form = {
                'Cnpj':document_number,
            'TokenRecapcha':TokenRecapcha,
            '__RequestVerificationToken': RequestVerificationToken
            }
            r = requests.post(url='https://consopt.www8.receita.fazenda.gov.br/consultaoptantes',data=form,verify=False)
            page = r.text
            go.quit()
            soup = BeautifulSoup(page, 'html.parser')
            x=str(soup.find('div',{'class':'validation-summary-errors'}))
            error = x[47:100]
            while(error == 'Impedido por proteção Captcha. Comportamento de Robô.'):
                go = webdriver.Chrome(path,options=chrome_options)
                try:
                    go.implicitly_wait(3)
                    go.get(back_end_url)
                    time.sleep(0.2)
                    RequestVerificationToken = go.find_element_by_xpath('//*[@id="conteudoPage"]/div[2]/form/input[2]').get_attribute('value')
                    time.sleep(0.3)
                    TokenRecapcha = go.find_element_by_xpath('//*[@id="tokenRecapcha"]').get_attribute('value')
                    form = {
                        'Cnpj':document_number,
                    'TokenRecapcha':TokenRecapcha,
                    '__RequestVerificationToken': RequestVerificationToken
                    }
                    r = requests.post(url='https://consopt.www8.receita.fazenda.gov.br/consultaoptantes',data=form,verify=False, proxies=random_proxy())
                    page = r.text
                    go.quit()
                    soup = BeautifulSoup(page, 'html.parser')
                    x=str(soup.find('div',{'class':'validation-summary-errors'}))
                    error = x[47:100]
                except:
                    encodedBytes = base64.b64encode(page.encode("utf-8"))
                    encodedhtml = str(encodedBytes, "utf-8")
                    return jsonify ([{
                                "numeroDocumento":document_number,
                                "tipoDocumento": docType,
                                "documentoB64": encodedhtml
                                }])
            encodedBytes = base64.b64encode(page.encode("utf-8"))
            encodedhtml = str(encodedBytes, "utf-8")
            return jsonify ([{
                        "numeroDocumento":document_number,
                        "tipoDocumento": docType,
                        "documentoB64": encodedhtml
                        }])
    
@app.route('/favicon.ico')
def favicon():
    return ''

@app.errorhandler(500)
def internal_error(error):
    logging.error('Erro interno!')
    res = json.dumps({
        "codigo": 503,
        "mensagem": "Erro inesperado na API.",
    })
    status_code = Response(res, status=200)
    return status_code

@app.errorhandler(400)
def empt_field(error):
    logging.error('Bad request')
    res = json.dumps({
        "codigo": 400,
        "mensagem": "Bad request!",
    })
    status_code = Response(res, status=200)
    return status_code

if __name__ == "__main__":
    serve(app, port=port, threads = 4)
