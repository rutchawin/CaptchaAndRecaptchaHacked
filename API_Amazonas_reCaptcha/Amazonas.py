from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import requests
import flask
import json
import os

app = flask.Flask(__name__)
@app.route('/', methods = ['GET'])
def home():
    return "<h1><center>THIS IS THE HOME PAGE</center></H1>"

@app.route('/cnpj/<string:numberCnpj>', methods = ['GET'])
def getCnpj(numberCnpj):
    with requests.Session() as r:
        urlBase = 'https://online.sefaz.am.gov.br/sintegra/'
        loadImages = '<base href="http://online.sefaz.am.gov.br/sintegra/"><meta charset="utf-8">'
        url = 'https://online.sefaz.am.gov.br/sintegra/sintegra_cnpj.asp'
        html = urlopen('https://online.sefaz.am.gov.br/sintegra/sintegra_cnpj.asp')
        res = BeautifulSoup(html.read(),features="lxml")
        site_key = str(res.find("div", {"class": "g-recaptcha"})['data-sitekey'])
        HEADERS = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en,pt-BR;q=0.9,pt;q=0.8,en-US;q=0.7',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'491',
            'Content-Type':'application/x-www-form-urlencoded',
            'Origin':'https://online.sefaz.am.gov.br',
            'Referer':'https://online.sefaz.am.gov.br/sintegra/index.asp?nErr=5',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        login_data = {
            'cgc':numberCnpj,
            'g-recaptcha-response':site_key,
            'B3':'Consultar'
        }
        page = r.get(url, data=login_data,headers=HEADERS)
        soup = BeautifulSoup(page.content)
        documents = []
        count = 2
        length = len(soup.find_all('a'))
        for link in soup.find_all('a'):
            x = loadImages+r.get(urlBase+link.get('href')).text
            documents.append(x)
            count += 1
            if count == length: 
                length = length -2
                break
    if length == 1:
        return documents[0]
    elif length == 2:
        return documents[0]+documents[1]
    elif length == 3:
        return documents[0]+documents[1]+documents[2]
    elif length == 3:
        return documents[0]+documents[1]+documents[2]+documents[3]
    elif length == 3:
        return documents[0]+documents[1]+documents[2]+documents[3]+documents[4]
    elif length == 3:
        return documents[0]+documents[1]+documents[2]+documents[3]+documents[4]+documents[5]
    elif length == 3:
        return documents[0]+documents[1]+documents[2]+documents[3]+documents[4]+documents[5]+documents[6]
def main():
    port = int(os.environ.get("PORT", 5005))
    app.run(host="192.168.1.59",port=port, threaded = True, debug=True)
if __name__ == "__main__":
    main()
