import requests
import json
import os.path
from dotenv import load_dotenv

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

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+CFL_API_TOKEN
}

with open('regru-domains.txt') as file:
  domains_regru= file.read().splitlines()

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


#создаем словарь с id zone CloudFlare и IP из ips.txt
domains = {
    "test.com": {
        "domain_id": -1,
        "domain_ip": "127.0.0.3"
    }
}

with open('domains.txt') as file:
  domains_from_file = file.read().splitlines()

ips_from_file = []
with open('ips.txt') as file:
  ips_from_file = file.read().splitlines()

domaincount = 0
activecount = 0
if len(domains_from_file) != len(ips_from_file):
   print('количество строк в domains.txt и ips.txt не совпадает...')


for d in  domains_from_file:
   for item in parsed_json["result"]:
       if item["name"] == d:
          print(f'в API Cloudflare найден домен: {d}')
          print(f'nameserver: {item["name_servers"]}')
          if item["status"] == "pending":
             print(f"pending")
          if item["status"] == "active":   
              print(f"active")
              activecount += 1
          domaincount+=1


if domaincount == 0:
    print('в API Cloudflare  НЕ найден НИ один домен из domains.txt!  проверьте NS, запустите еще раз regru_changeDNS.py и дождитесь применения настроек 30 мин')
    exit()

if domaincount == len(domains_from_file)  and domaincount == activecount:
    print(f'всего найдено {domaincount} из {len(domains_from_file)}')   
    print(f'из них активно {activecount}')
    print('все хорошо, можно переходить к следующему шагу')
else:
    print(f'всего найдено {domaincount} из {len(domains_from_file)}')  
    print(f'из них активно {activecount}')

