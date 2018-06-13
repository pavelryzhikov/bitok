# -*- coding: utf-8 -*-
from flask import Flask, request
import logging, time
import config
import requests
app = Flask(__name__)
TOKEN = config.TOKEN
logging.basicConfig(filename='log_'+__name__+'.log', filemode='w', level=logging.DEBUG)

@app.route('/')
def hello_world():
    logging.info('hello_world')
    return "<h1 style='color:blue'>Hello There Rpe!</h1>"

@app.route('/time')
def hello_time():
    return "<h1 style='color:blue'>Hello There " + time.ctime() + "</h1>"



@app.route('/'+TOKEN+'/token')
def token():
    return 'token'



@app.route('/'+TOKEN+'/webhook/activate')
def WebhookActivate():
    """
it does not works for own servers
only for pythonanywhere

use curl from 
https://stackoverflow.com/questions/33256898/telegram-bot-on-openssl/33260827#33260827
    """
    r = requests.post(url='https://api.telegram.org/bot'+config.TOKEN+'/setWebhook',
            data ={ 'url': 'https://'+config.SERVER_URL+'/'+config.TOKEN
                ,'certificate': open('/etc/nginx/ssl/YOURPUBLIC.pem', 'rb')
                })
    logging.info(r.text)
    return r.text

@app.route('/'+TOKEN+'/webhook/deactivate')
def WebhookDeactivate():
    r = requests.post(url='https://api.telegram.org/bot'+config.TOKEN+'/setWebhook')
    return r.text

@app.route('/'+TOKEN+'/webhook/info')
def getWebhookInfo():
    r = requests.get(url='https://api.telegram.org/bot'+config.TOKEN+'/getWebhookInfo')
    return r.text

@app.route('/'+TOKEN, methods=['POST'])
def getUpdates():
    try:
        logging.info(request.data)
    except:
        logging.error('ERROR!!!')
        pass
    return 'OK', 200

@app.route('/'+TOKEN+'/getupdates1', methods=['GET'])
def getUpdates1():
    try:
        r = requests.post(url='https://api.telegram.org/bot'+config.TOKEN+'/getUpdates')
    except:
        pass
    return r.text, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')

