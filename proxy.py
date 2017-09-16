import shutil
import requests
from io import BytesIO
from flask import Flask, send_file, Response, make_response, request


URL_BASE = 'https://200.123.180.122:5743'
ID = '3382953'
SALDO = '/rest/getSaldoCaptcha/'
app = Flask(__name__)


def get():
    res = requests.get(URL_BASE + '/captcha.png', stream=True, verify=False)
    if res.status_code == 200:
        with open('captcha.png', 'wb') as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)

    res = requests.get(URL_BASE + '/captcha.png', verify=False)
    cookie = res.headers['Set-Cookie']
    print(res.headers)
    body = BytesIO(res.content)
    return body, cookie


@app.route("/captcha.png")
def hello():
    body, cookie = get()
    response = make_response(body.read())
    response.headers['Content-Type'] = 'image/png'
    response.set_cookie('Set-Cookie', cookie)
    return response
    # return send_file('captcha.png')


@app.route("/saldo/<captcha>")
def saldo(captcha):
    # print(request.cookies['Set'])
    url = URL_BASE + SALDO + ID + '/' + captcha
    res = requests.get(url, verify=False)
    print(res.content)
    return res.content
