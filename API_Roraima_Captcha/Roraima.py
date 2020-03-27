from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from flask import Flask, escape, request, jsonify
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from flask_cors import CORS
import urllib.request
import requests
import urllib
import time
import os

os.environ["LANG"] = "en_US.UTF-8"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
loadImages = '<base href="https://portalapp.sefaz.rr.gov.br/siate/servlet/">'
siteLink = 'https://portalapp.sefaz.rr.gov.br/siate/servlet/wp_siate_consultasintegra'
captchaWord = ['0',
    'polish', 'soap', 'wood', 'great', 'school', 'sudden',
    'wind', 'step', 'credit','pain', 'design','front',
    'profit', 'push', 'seem', 'cord','sound','scale',
    'with', 'wind', 'cloth', 'screw','garden','bent',
    'west','judge','goat', 'animal', 'warm','join',
    'turn', 'school', 'white','keep','collar','basin',
    'tooth', 'face', 'range', 'tight', 'nail', 'seem',
    'female', 'public','potato','where','idea','snake',
    'flowe', 'narrow', 'still', 'hope','glass', 'lock',
    'hand', 'face', 'weight', 'fear', 'copper', 'debt',
    'shoe', 'paint', 'butter', 'roll', 'blood','story',
    'doubt', 'again', 'meat', 'offer','clean','memory',
    'like', 'wrong', 'jump', 'amount','regret', 'free',
    'weight', 'crush', 'pull', 'dress', 'door', 'male',
    'black', 'please', 'flag', 'fact',   'nose', 'boat',
    'taste', 'snake', 'cold', 'attack','crush','canvas',
    'shame', 'book', 'wound', 'nation','small','fire',
    'good', 'past', 'profit','sound','chin','flag',
    'body', 'salt', 'birth','crime','false','sleep',
    'part', 'square', 'canvas','mine','safe','mark',
    'degree', 'bell', 'color','expert','rule','when',
    'parcel', 'degree','waste','after','army','moon',
    'brain', 'news', 'silver','rain', 'much', 'stiff',
    'horse', 'smile', 'shirt','this', 'grip', 'sharp',
    'knot', 'neck', 'woman', 'seed', 'smell', 'nound',
    'linen', 'same','right', 'adjust', 'jewel','bell',
    'pocket', 'green', 'soap', 'mother', 'mine','rice',
    'loss', 'tail', 'foot', 'porter','spring','desire',
    'screw', 'glove', 'spade', 'bent','letter','glass',
    'sugar', 'fear','every', 'muscle', 'right', 'rate',
    'sticky', 'butter','sail','summer','snake','wheel',
    'sheep', 'glove', 'poison', 'tooth', 'bucket',
]

def removeDot(numberWithDot):
    numberWithoutDot = ''
    for eachCharacter in numberWithDot:
        if eachCharacter == '.':
            break
        else:
            numberWithoutDot += eachCharacter
    numberWithoutDot = int(numberWithoutDot)
    return captchaWord[numberWithoutDot]

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you sent': some_json}), 201
    else:
        return '''<p><h1 align = "center">WELCOME TO THIS PAGE!</h1></p>'''

@app.route('/ie/<string:numberIe>', methods=['GET'])
def getIe(numberIe):
    go = webdriver.Chrome(chrome_options=chrome_options)
    go.get(siteLink)
    time.sleep(0.5)
    go.find_element_by_xpath('//*[@id="vDOCUMENTO"]').send_keys(numberIe)
    imgUrl = go.find_element_by_xpath('//*[@id="captchaImage"]/img').get_attribute("src")
    numberWithDot = imgUrl[62:]
    go.find_element_by_xpath('//*[@id="_cfield"]').send_keys(removeDot(numberWithDot))
    go.find_element_by_name('BTNCONSULTAR').click()
    time.sleep(0.7)    
    return loadImages + go.page_source

@app.route('/cnpj/<string:numberCnpj>', methods=['GET'])
def getCnpj(numberCnpj):
    go = webdriver.Chrome(chrome_options=chrome_options)
    go.get(siteLink)
    time.sleep(0.5)
    go.find_element_by_xpath('//*[@id="TBLFILTRO"]/tbody/tr[1]/td[2]/span/input[2]').click()
    go.find_element_by_xpath('//*[@id="vDOCUMENTO"]').send_keys(numberCnpj)
    imgUrl = go.find_element_by_xpath('//*[@id="captchaImage"]/img').get_attribute("src")
    numberWithDot = imgUrl[62:]
    go.find_element_by_xpath('//*[@id="_cfield"]').send_keys(removeDot(numberWithDot))
    go.find_element_by_name('BTNCONSULTAR').click()
    time.sleep(0.7)
    return loadImages + go.page_source

def main():
    port = int(os.environ.get("PORT", 5001))
    app.run(host="10.20.20.127", port=port)
    
if __name__ == '__main__':
    main()
