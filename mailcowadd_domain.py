import requests
import json
import os.path
from dotenv import load_dotenv

def add(d:str):
    #настраиваемся на каталог запуска, на случай вызова из непредвиденного места
    current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file)
    os.chdir(current_directory)

    #читаем .env
    if os.path.isfile('.env'):
        load_dotenv()
    else:
        print("ERROR! .env file NOT found, exit")
        exit()

    MAILCOWAPITOKEN    = os.getenv('MAILCOWAPITOKEN')
    MAILCOWAPIURL      = os.getenv('MAILCOWAPIURL')
    MAILCOWAMAINDOMAIN = os.getenv('MAILCOWAMAINDOMAIN')


    headers = {
        'accept': 'application/json',
        'X-API-Key': MAILCOWAPITOKEN
    }

    data =  {
        "active": "1",
        "aliases": "400",
        "backupmx": "0",
        "defquota": "3072",
        "description": "",
        "domain": d,
        "mailboxes": "10",
        "maxquota": "10240",
        "quota": "10240",
        "relay_all_recipients": "0",
        "rl_frame": "s",
        "rl_value": "0",
        "restart_sogo": "10",
        "tags": [
            "tag1",
            "tag2"
        ]
        }
    

    response = requests.post(f'{MAILCOWAPIURL}/api/v1/add/domain', headers=headers, json=data)
    if response.status_code == 200:
        pass
    else:
        print('MailCow api вернул ошибку!: {response.text} ')
        exit()
    print(response.text)
    

