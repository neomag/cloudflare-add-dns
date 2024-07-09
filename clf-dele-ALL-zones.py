import requests
import json
import os.path
from dotenv import load_dotenv

# читаем mailcows.json
try:
    with open('mailcows.json') as file:
        file_contents = file.read()
        mailcows = json.loads(file_contents)
except:
    print('что-то пошло не так, скорее всего неверный формат файла mailcows.json, проверьте валидатором https://codebeautify.org/json-fixer')
    exit()

domains_from_file = []
# получаем список доменов на уделение зон
print('внимание! что скрипт удаляет содержимое зон доменов, но не сами домены')
for x in mailcows.values():
    ADDITIONAL_DOMAINS = x['ADDITIONAL_DOMAINS']
    for doms in ADDITIONAL_DOMAINS:
        domains_from_file.append(doms)

def confirm():
    print('***  ВНИМАНИЕ ! **** вы хотите удалить все настройки DNS в Clouflare в зонах:')
    print(domains_from_file)
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("ваш выбор [Y/N]? ").lower()
    return answer == "y"


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
CFL_API_TOKEN = os.getenv('CFL_API_TOKEN')
CFL_X_AUTH_KEY = os.getenv('CFL_X-Auth-Key')
CFL_X_AUTH_EMAIL = os.getenv('CFL_X_AUTH_EMAIL')

headers = {
    'Content-Type':  'application/json',
    'Authorization': 'Bearer '+CFL_API_TOKEN,
    'X-Auth-Email': CFL_X_AUTH_EMAIL,
    'X-Auth-Key': CFL_X_AUTH_KEY
}


# подтвержждение перед опасной операцией
if confirm():
    pass
else:
    exit()

print('запрашиваю список доменов с ClouFlare')
response = requests.get(CFL_API_URLzones+'/?&per_page=1000', headers=headers)
if response.status_code == 200:
    pass
else:
    print(f'CloudFlare api вернул ошибку!: {response.text} ')
    exit()

#сохраняем чтобы не дергать api при отладке
with open("clf-delete-ALL-zones.json", "w") as json_file:
    json.dump(response.json(), json_file, indent=4)


#читам из файла дамп запроса к api чтобы не дергать api
with open('clf-delete-ALL-zones.json') as file:
  file_contents = file.read()
parsed_json = json.loads(file_contents)

for d in domains_from_file:
   for item in parsed_json["result"]:
      if item["name"] == d:
           zoneid = item["id"]
           response = requests.get(f'{CFL_API_URLzones}/{zoneid}/dns_records?&per_page=1000', headers=headers)
           if response.status_code == 200:
                for record in response.json()['result']:
                    record_id = record['id']
                    print(f'{CFL_API_URLzones}/{zoneid}/dns_records/{record_id}')
                    r = requests.delete(f'{CFL_API_URLzones}/{zoneid}/dns_records/{record_id}', headers=headers)
                    print(r.text)
                    if r.status_code == 200:
                        print('запись удалена')

           else:
                print(f'CloudFlare api вернул ошибку!: {response.text} ')
                exit()


