#!/usr/bin/python3
import psutil
import time
import shutil
from threading import Thread
import os
from datetime import datetime
import telebot
from threading import Thread


print('started...')
print('logs directory', os.path.abspath('logs'))
TOKEN = ""
CHAT_ID = "619904882" # khodam ID 619904882


bot = telebot.TeleBot(TOKEN, parse_mode='Html')


def sender(which_file, msg):
    bot.send_message(CHAT_ID, f"<b>{msg}</b>===========================")
    bot.send_document(CHAT_ID, open(which_file, 'rb'))
    return


def copier():
    now = datetime.now()
    shutil.copy2('mem-p.txt', os.path.join(os.path.abspath('logs'), 'mem--' + now.strftime("%H:%M:%S") + '.txt'))
    shutil.copy2('cpu-p.txt', os.path.join(os.path.abspath('logs'), 'cpu--' + now.strftime("%H:%M:%S") + '.txt'))
    return


def cpu_checker():
    while True:
        cpu_percent = psutil.cpu_percent()
        if cpu_percent > 65:
            # Thread(target=copier).start()

            def send():
                try:
                    sender('cpu-p.txt', f'ALERT! CPU over 65% -- current : {cpu_percent}')
                except Exception as e:
                    sender('cpu-p.txt', f"CPU over 65% -- current : {cpu_percent} \n ERROR: {str(e)}")

            Thread(target=send).start()

        time.sleep(60)


def cleaner():
    os.popen("apt --purge autoremove && apt autoclean && rm -rf /var/cache/apt/* && rm -rf /var/log/* && rm -rf /var/tmp/* && cat /dev/null > ~/.bash_history && history -c && history -w && shred -u ~/.bash_history && touch ~/.bash_history")
    time.sleep(300)
    total, _, free = shutil.disk_usage("/")
    free_percent = (free // (2 ** 30)) / (total // (2 ** 30)) * 100
    Thread(target=bot.send_message, args=(CHAT_ID, f'I did my best, right now disk usage is : {free_percent}\n')).start()
    return


def disk_monitor():
    while True:
        total, _, free = shutil.disk_usage("/")
        free_percent = (free // (2 ** 30)) / (total // (2 ** 30)) * 100
        if free_percent > 70:
            Thread(target=bot.send_message, args=(CHAT_ID, f'OH BOY! disk free space over 70% -- current : {free_percent}\nI will start removing redundant files, lonely in the server darkness and coldness...')).start()
            Thread(target=cleaner).start()
        time.sleep(43200)


def ram_checker():
    while True:
        mem_percent = psutil.virtual_memory().percent
        if mem_percent > 65:
            # Thread(target=copier).start()

            def send():
                try:
                    sender('mem-p.txt', f'ALERT! MEMORY over 65% -- current: {mem_percent}')
                except Exception as e:
                    sender('mem-p.txt', f'ALERT! MEMORY over 65% -- current: {mem_percent}\n ERROR: {str(e)}')

            Thread(target=send).start()

        time.sleep(60)


if __name__ == '__main__':
    PROCESSES = [Thread(target=cpu_checker), Thread(target=ram_checker)]
    # PROCESSES = [Process(target=cpu_checker), Process(target=ram_checker), Process(target=disk_monitor)]

    for proc in PROCESSES:
        proc.start()
