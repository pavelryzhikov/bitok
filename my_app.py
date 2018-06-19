# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import logging, time, sys, json, re
import config
import requests
app = Flask(__name__)
TOKEN = config.TOKEN
logging.basicConfig(filename='logs/'+__name__+'.log', filemode='w', level=logging.DEBUG)

@app.route('/')
def hello_world():
    logging.info('hello_world')
    #return "<h1 style='color:blue'>Hello There Rpe!</h1>"
    return '404',404

@app.route('/time')
def hello_time():
    return "<h1 style='color:blue'>Hello There " + time.ctime() + "</h1>"



@app.route('/'+TOKEN+'/orders')
def orders():
    with open('logs/orders','r') as file_orders:
        content=file_orders.read()
    return render_template("orders.html", content=content)



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
#        s = json.dumps(data, indent=4, sort_keys=True)
#        bytes_data = request.data
        dict_data = json.loads((request.data).decode('utf-8'))
        #logging.info(json.dumps(str_data, indent=4, sort_keys=True))
        logging.info(dict_data)
        _text=dict_data["message"]["text"]
        logging.info(_text)
        processing_messages(_text)
    except:
        logging.error(sys.exc_info()[0])
        pass
    return 'OK', 200

@app.route('/'+TOKEN+'/getupdates1', methods=['GET'])
def getUpdates1():
    try:
        r = requests.post(url='https://api.telegram.org/bot'+config.TOKEN+'/getUpdates')
    except:
        pass
    return r.text, 200


def processing_messages(_text):
    """
    fn filter and log incoming messages
    0. t=full text
    1. m=re.search("#\w{3,4}",t) = #SYS
    2. m1=re.search(m[0][1:]+"/\w{3,4}",t) = SYS/BTC
    3. m2 =re.search("BINANCE"),t.upper()) = BINANCE
    4. m4_1=re.search("BUY\D+\d+.+",t)[0] = BUY Ares 234-234
       m4=re.findall("([\d\.]+)+",m4_1) = ['234','234']
    """
    
    try:
        try:
        # platform
            platform=re.search("BINANCE",_text.upper())[0]    
        except:
            logging.error("platform")
            platform='+++'
        
        try:
        # hashtag
            hashtag=re.search("#\w{3,5}",_text)[0]
        except:
            logging.error("hashtag")
            hashtag='+++'

        try:
        # currency
            currency=re.search(hashtag[1:]+"/\w{3,5}",_text)[0]
        except:
            logging.error("currency")
            currency='+++'

        try:
        # buy
            buy_str=re.search("BUY\D+\d+.+",_text)[0]
            buy_list=re.findall("([\d\.]+)+",buy_str)

            if len(buy_list)==1:
                buy='equal '+buy_list[0]
            elif len(buy_list)==2:
                buy='between '+buy_list[0]+ ' and '+ buy_list[1]
            else: 
                buy=buy_str 
        except:
            logging.error("buy")
            buy='+++'

    except:
        logging.error("cant parse text")
        logging.error(sys.exc_info()[0])
    
    with open('logs/orders','a') as file_orders:
        file_orders.write("platform: "+platform+"\thashtag: "+hashtag+"\tcurrency: "+currency +"\tbuy cost: "+buy+"\n")



if __name__ == '__main__':
    app.run(host='0.0.0.0')

