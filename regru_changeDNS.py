import requests
import json
import os.path
from dotenv import load_dotenv

def change():
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
    REGRU_ACCOUT = os.getenv('REGRU_ACCOUNT')
    REGRU_PASS = os.getenv('REGRU_PASS')
    REGRU_APIURL = os.getenv('REGRU_APIURL')


    # CFL_NS1 = os.getenv('CFL_NS1')
    # CFL_NS2 = os.getenv('CFL_NS2')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+CFL_API_TOKEN
    }

    # создаем domains.txt и regru_domains.txt из mailcows.json для обратной совместимости с предыдущей версией кода
    # to-do: refactor
    # читаем mailcows.json
    try:
        with open('mailcows.json') as file:
            file_contents = file.read()
            mailcows = json.loads(file_contents)
    except:
        print('что-то пошло не так, скорее всего неверный формат файла mailcows.json, проверьте валидатором https://codebeautify.org/json-fixer')
        exit()
    domains_from_file = []
    for x in mailcows.values():
        ADDITIONAL_DOMAINS = x['ADDITIONAL_DOMAINS']
        for doms in ADDITIONAL_DOMAINS:
            domains_from_file.append(doms)

    with open('domains.txt', 'w') as file:
        file.write('\n'.join(domains_from_file))
    with open('regru-domains.txt', 'w') as file:
        file.write('\n'.join(domains_from_file))

    with open('regru-domains.txt') as file:
        domains_regru= file.read().splitlines()

    print('читаем домены из CloudFlare')
    response = requests.get(CFL_API_URLzones+'/?&per_page=1000', headers=headers)
    if response.status_code == 200:
        pass
    else:
        print(f'CloudFlare api вернул ошибку!: {response.text} ')
        exit()

    #сохраняем чтобы не дергать api при отладке
    with open("clf-verify-retarget.json", "w") as json_file:
        json.dump(response.json(), json_file, indent=4)

    #читам из файла дамп запроса к api чтобы не дергать api
    with open('clf-verify-retarget.json') as file:
        file_contents = file.read()
    parsed_json = json.loads(file_contents)



    for d in domains_regru:
        print('начинаем обработку regru-domains.txt и перенацеливание NS на CloudFlare')
        print(f'обработка домена {d}')

        for item in parsed_json["result"]:
            if item["name"] == d:
                CFL_NS1, CFL_NS2 = item["name_servers"]
                

        input_json= { 
        "dname": f"{d}",
        "nss": {
            "ns0": f"{CFL_NS1}",
            "ns1": f"{CFL_NS2}"
            }
        }
        
        result_url = f'{REGRU_APIURL}/domain/update_nss?input_data={json.dumps(input_json)}&input_format=json&password={REGRU_PASS}&username={REGRU_ACCOUT}'
    
        response = requests.get(result_url)
        print(response.text)
        if response.status_code == 200:
            with open("regru_changeDNS.json", "a") as json_file:
                json.dump(response.json(), json_file, indent=4)
        else:
            print(f'REG.RU api вернул ошибку!: {response.text} ')
            exit()


   


