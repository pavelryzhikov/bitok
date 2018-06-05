# -*- coding: utf-8 -*-
from flask import Flask, request
import logging
import config
import requests
print(2)
app = Flask(__name__)
TOKEN = config.TOKEN
print(3)
logging.basicConfig(filename='log_'+__name__+'.log', filemode='w', level=logging.DEBUG)
#logging.warning('And this, too')

@app.route('/')
def hello_world():
    logging.info('hello_world')
    return 'Hello, World!'


@app.route('/'+TOKEN+'/token')
def token():
    logging.info('token')
    return 'token'

@app.route('/'+TOKEN+'/webhook/activate')
def WebhookActivate():
    r = requests.post(url='https://api.telegram.org/bot'+config.TOKEN+'/setWebhook',
            data ={ 'url': 'https://'+config.SERVER_URL+':'+config.SERVER_PORT+'/'+config.TOKEN+'/getupdates'
                ,'certificate':''
                #,'certificate': open('webhook_cert.pem', 'rb')
                })
    logging.info(r.text)
    print(r.text)
    return r.text

@app.route('/'+TOKEN+'/webhook/deactivate')
def WebhookDeactivate():
    r = requests.post(url='https://api.telegram.org/bot'+config.TOKEN+'/setWebhook')
    logging.info(r.text)
    print(r.text)
    return r.text

@app.route('/'+TOKEN+'/webhook/info')
def getWebhookInfo():
    r = requests.get(url='https://api.telegram.org/bot'+config.TOKEN+'/getWebhookInfo')
    logging.info(r.text)
    print(r.text)
    return r.text

@app.route('/'+TOKEN+'/getupdates', methods=['POST'])
def getUpdates():
    logging.info('CALL GETUPADTES')
    try:
        logging.info(request.data)
    except:
        logging.error(request.data)
        pass
    return 'OK', 200

if __name__ == '__main__':
#    app = Flask(__name__)
#    from my_app import app
    print(1)
    app.run(
            host=config.SERVER_URL
            ,port=config.SERVER_PORT
            #,ssl_context='adhoc'
            #,ssl_context=('webhook_cert.pem', 'webhook_pkey.pem')
            )

