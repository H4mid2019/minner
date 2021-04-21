import requests
from requests.auth import HTTPDigestAuth
import json
import time
from playsound import playsound
import telegram_send

last = 0


def job():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    global last
    first = True
    try:
        with requests.Session()as c:
            res = c.get('http://192.168.8.122/cgi-bin/get_miner_status.cgi?',
                        headers=headers, auth=HTTPDigestAuth('root', 'root'))
            for i in json.loads(res.text)['devs']:
                if float(i['dev_temp']) > 65:
                    telegram_send.send(messages=['batch3---122', "{}".format(i['dev_temp'])])
                    for _ in range(10):
                        playsound('beep.mp3')
                        time.sleep(2)
                if first:
                    first = False
                    nlast = float(i['dev_temp'])
                    print(i['dev_temp'], 'minus last:', nlast-last)
                    last = float(i['dev_temp'])
                else:
                    print(i['dev_temp'])

            print(f"-----122------{json.loads(res.text)['summary']['ghsav']}")

    except Exception as e:
        print(str(e))

    return True


while True:
    job()
    time.sleep(20)
