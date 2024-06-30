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
    MAILCOWMBOXDEFAULTPASS = os.getenv('MAILCOWMBOXDEFAULTPASS')

    
    with open('mailbox.txt') as file:
        mailboxes = file.read().splitlines()

    headers = {
        'accept': 'application/json',
        'X-API-Key': MAILCOWAPITOKEN
    }

    for mbox in mailboxes:
        data =  {
            "active": "1",
            "domain": d,
            "local_part": mbox,
            "name": "Jon Doe",
            "password": MAILCOWMBOXDEFAULTPASS,
            "password2": MAILCOWMBOXDEFAULTPASS,
            "quota": "3072",
            "force_pw_update": "0",
            "tls_enforce_in": "0",
            "tls_enforce_out": "0",
            "tags": [
                "tag1",
                "tag2"
            ]
            }
        
        response = requests.post(f'{MAILCOWAPIURL}/api/v1/add/mailbox', headers=headers, json=data)
        if response.status_code == 200:
            pass
        else:
            print('MailCow api вернул ошибку!: {response.text} ')
            exit()
        
        print(response.text)
    