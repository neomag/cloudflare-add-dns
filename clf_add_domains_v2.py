import requests
import json
import os.path
from dotenv import load_dotenv

def add_domains():
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


    CFL_API_URLzones = os.getenv('CFL_API_URLzones')
    CFL_API_TOKEN  = os.getenv('CFL_API_TOKEN')
    CFL_ACCOUNT_ID = os.getenv('CFL_ACCOUNT_ID')
    CFL_X_AUTH_KEY = os.getenv('CFL_X-Auth-Key')
    CFL_X_AUTH_EMAIL = os.getenv('CFL_X_AUTH_EMAIL')


    headers = {
        'Content-Type':  'application/json',
        'Authorization': 'Bearer '+CFL_API_TOKEN,
        'X-Auth-Email': CFL_X_AUTH_EMAIL, 
        'X-Auth-Key': CFL_X_AUTH_KEY
    }


    with open('regru-domains.txt') as file:
        domains_regru = file.read().splitlines()

    print('создаем домены на Cloudflare')

    data = {}

    # читаем из API,  закоментировать при чтении из файла
    for d in domains_regru:
        data = {
            "account": {
                "id": CFL_ACCOUNT_ID 
            },
            "name": d,
            "type": "full"
            }
        print(f'обработка домена {d}')
        
        response = requests.post(CFL_API_URLzones, headers=headers, json = data)
        if response.status_code == 200:
            # сохраняем чтобы не дергать api при отладке
            with open("clf-add-domains.json", "a") as json_file:
                json.dump(response.json(), json_file, indent=4)
        else:
            print(f'CloudFlare api вернул ошибку!: {response.text} ')





