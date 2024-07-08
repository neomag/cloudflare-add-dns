import requests
import json
import os.path
from dotenv import load_dotenv

def get(d:str, MAILCOWAPITOKEN:str, MAILCOWAPIURL:str ):
    print(f'd={d} MAILCOWAPITOKEN = {MAILCOWAPITOKEN}  MAILCOWAPIURL = {MAILCOWAPIURL}')

    MAILCOWAPIURL      = MAILCOWAPIURL
    MAILCOWAPITOKEN    = MAILCOWAPITOKEN
    

    headers = {
        'accept': 'application/json',
        'X-API-Key': MAILCOWAPITOKEN
    }

    response = requests.get(f'{MAILCOWAPIURL}/api/v1/get/dkim/{d}', headers=headers)
    print(f'{MAILCOWAPIURL}/api/v1/get/dkim/{d}')
    if response.status_code == 200:
        pass
    else:
        print(f'MailCow api вернул ошибку!: {response.text} ')
        exit()

    r = json.loads(response.text)
    return r['pubkey']


