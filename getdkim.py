import requests
import json
import os.path
from dotenv import load_dotenv

def getdkim(d:str):
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

    response = requests.get(f'{MAILCOWAPIURL}/api/v1/get/dkim/{MAILCOWAMAINDOMAIN}', headers=headers)
    if response.status_code == 200:
        pass
    else:
        print('MailCow api вернул ошибку!: {response.text} ')
        exit()


    r = json.loads(response.text)
    return r['pubkey']


