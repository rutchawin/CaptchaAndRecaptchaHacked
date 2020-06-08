# custom-recaptcha-federal-sn-api

API customizada para acesso com quebra de reCaptcha ao serviço Federal do Simples Nacional

## .env
Segue a descrição e exemplos das variáveis do .env

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| PORT     | Número da Porta do Serviço | 5000 |
| LOG_LEVEL | Nível do Logger da API | DEBUG / INFO / ERROR |
| CHROME_DRIVER_PATH= | Caminho para o executável do Chrome Driver | /home/meta/Downloads/chromedriver |
| SN_FEDERAL_CONTEXTO | Contexto da Rota do SN da API | /api/v1/federal/sn |
| SN_FEDERAL_BACKEND_URL | URL do Backend Interno Referente ao Simples Nacional | https://consopt.www8.receita.fazenda.gov.br/consultaoptantes |

---
## Administração da API

### Instalar packages
Instala apenas os packages de produção.

```
pipenv install

```

### Instalar dev-packages
Instala apenas os packages que são usados em ambiente de desenvolvimento.

```
pipenv install --dev

```
**NÃO UTILIZA O AZcaptcha, possui solução própria através de uma vulnerabilidade encontrada na fonte**

## REQUESTs CNPJ

**OBS.:** não é preciso enviar todos os campus preenchidos, é necessário apenas o número, tipo de documento e o serviço. Os outros campus podem ser enviados em branco.
          ***Utilizar a letra J***  no "tipoDocumento" para consultar por CNPJ.

```
{
    "url":"http://....",
    "servico":"FederalSN",
    "documento":"{
        "tipoDocumento":"X",
        "numeroDocumento":"0000",
        "nome": "Irineu",
        "dataNascimento":"yyyymmdd",
        "nis":"0000",
        "tipoInstalacao": "xxxxx"
    }
}
```

# Response CNPJ


``` 
[{
    "numeroDocumento": "Número do CNPJ",
    "tipoDocumento: "CNPJ"
    "documentoB64: "HTML_B64"
}]
```

### ERROS

#### ERRO - Nome do Serviço Inválido

```json
{
    "codigo": 400,
    "mensagem": "Nome do Serviço inválido"
}
```
**HTTP STATUS:** 400


#### ERRO - Tipo de Documento Inválido

```json
{
    "codigo": 400,
    "mensagem": "Tipo de documento inválido"
}
```
**HTTP STATUS:** 400

#### ERRO - Número do Documento Inválido

```json
{
    "codigo": 400,
    "mensagem": "Número do documento inválido"
}
```
**HTTP STATUS:** 400

#### ERRO - Parâmetros inválidos

```json
{
    "codigo": 400,
    "mensagem": "Parâmetros inválidos"
}
```
#### ERRO - Bad request

```json
{
    "codigo": 400,
    "mensagem": "Bad request"
}
```
#### ERRO - Erro interno

```json
{
    "codigo": 503,
    "mensagem": "Erro inesperado na API"
}
```
