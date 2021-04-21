import requests
from requests.auth import HTTPDigestAuth
import json
import time
import telebot

last = 0

TOKEN = ""
CHAT_ID = "619904882" # khodam ID 619904882


bot = telebot.TeleBot(TOKEN, parse_mode='Html')


def send(messages):
    bot.send_message(CHAT_ID, f"<b>{messages}</b>")
    # bot.send_document(CHAT_ID, open(which_file, 'rb'))
    return


def job():
    global last
    first = True
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    try:
        with requests.Session()as c:
            res = c.get('http://192.168.8.120/cgi-bin/get_miner_status.cgi?',
                        headers=headers, auth=HTTPDigestAuth('root', 'root'))
            for i in json.loads(res.text)['devs']:
                if float(i['dev_temp']) > 63:
                    send(messages="miner120---{}----------{}".format(i['dev_temp'], json.loads(res.text)['summary']['ghsav']))

                if first:
                    first = False
                    nlast = float(i['dev_temp'])
                    print(i['dev_temp'], 'minus last:', nlast-last)
                    last = float(i['dev_temp'])
                else:
                    print(i['dev_temp'])
            print("-----120------%s" % json.loads(res.text)['summary']['ghsav'])

    except Exception as e:
        print(str(e))

    return True


while True:
    job()
    time.sleep(20)
