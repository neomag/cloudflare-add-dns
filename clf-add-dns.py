import requests
import json
import os.path
from dotenv import load_dotenv
import getdkim
import mailcowadd_domain
import mailcowadd_mailbox


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


URLzones = os.getenv('URLzones')
TOKEN = os.getenv('TOKEN')

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+TOKEN
}

#раскоментировать это чтобы брать не из файла а из api !
#Get domains and IDs via CF API
response = requests.get(URLzones, headers=headers)
if response.status_code == 200:
    pass
else:
    print('CloudFlare api вернул ошибку!: {response.text} ')
    exit()

#сохраняем чтобы не дергать api при отладке
with open("data.json", "w") as json_file:
    json.dump(response.json(), json_file, indent=4)


#читам из файла дамп запроса к api чтобы не дергать api
with open('data.json') as file:
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
for d, ip in zip(domains_from_file, ips_from_file):
    for item in parsed_json["result"]:
        if item["name"] == d:
           print('в API Cloudflare найден домен: {d}')
           domains[d] = { 'domain_id': item["id"], 'domain_ip': ip }
           domaincount+=1
if domaincount == 0:
    print('в API Cloudflare  НЕ найден НИ один домен из domains.txt!  проверьте NS...')   
           
def add_record(content:str, name:str, type:str, id:str, domain:str,):
    ADDRECORD_URL = f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records'
    data = {}
    if type == 'A':
       data = {'content': content, 'name': name, 'proxied': False, 'type': type, 'id': id}

    if type == 'MX':
       data = {'content': content, 'name': name, 'proxied': False, 'type': type, 'id': id, 'priority': 10}

    if type == 'SRV':
      data = {'content': content, 'name': name, 'proxied': False, 'type': type, 'id': id, 'data': {'weight': 5, 'priority': 5, 'port': 443, 'target': content}}

    if type == 'CNAME':
       data = {'content': content, 'name': name, 'proxied': False, 'type': type, 'id': id}

    if type == 'TXT':
       data = {'content': content, 'name': name, 'proxied': False, 'type': type, 'id': id}

    response = requests.post(ADDRECORD_URL, headers = headers, json = data)
    print(f'ответ CloudFlare API: {response.text}')

#print(json.dumps(domains, indent=4))

#dirty
del domains['test.com']

#указывает на домен 3 уровня, где находится непосредственно smtp сервер
mailhost = 'mail'

# добавляем записи DNS в CloudFlare
for x in domains:
   # A-record  
   add_record(domains[x]['domain_ip'] , mailhost, 'A', domains[x]['domain_id'] , x)
      
   # MX-record
   add_record(f'{mailhost}.{x}', '@', 'MX', domains[x]['domain_id'], x)


   # CNAME autodiscover
   add_record(f'{mailhost}.{x}', 'autodiscover', 'CNAME', domains[x]['domain_id'], x)

   # SRV record  _autodiscover._tcp
   add_record( f'{mailhost}.{x}', '_autodiscover._tcp', 'SRV', domains[x]['domain_id'], x)

   # CNAME autoconfig
   add_record(f'{mailhost}.{x}', 'autoconfig', 'CNAME', domains[x]['domain_id'], x)

   # SPF
   add_record('v=spf1 mx a -all', '@', 'TXT', domains[x]['domain_id'], x)

   # DMARC  _dmarc
   add_record(f'v=DMARC1; p=reject; rua=mailto:test@{x}', '_dmarc', 'TXT', domains[x]['domain_id'], x)

   # DKIM  
   add_record(f'v=DKIM1;k=rsa;t=s;s=email;p={getdkim.getdkim(x)}', 'dkim._domainkey', 'TXT', domains[x]['domain_id'], x)

   # Разобраться с TLSA, хз - в API нет метода


#добавляем домен и почтовые ящики в mailcow
for x in domains:
   mailcowadd_domain.add(x)
   mailcowadd_mailbox.add(x)



