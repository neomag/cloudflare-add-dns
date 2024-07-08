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


CFL_API_URLzones = os.getenv('CFL_API_URLzones')
CFL_API_TOKEN = os.getenv('CFL_API_TOKEN')

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+CFL_API_TOKEN
}

#раскоментировать это чтобы брать не из файла а из api !
#Get domains and IDs via CF API
response = requests.get(CFL_API_URLzones+'/?&per_page=1000', headers=headers)
if response.status_code == 200:
    pass
else:
    print(f'CloudFlare api вернул ошибку!: {response.text} ')
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
if len(domains_from_file) != len(ips_from_file):
   print('количество строк в domains.txt и ips.txt не совпадает...')
for d, ip in zip(domains_from_file, ips_from_file):
    for item in parsed_json["result"]:
        if item["name"] == d:
           domains[d] = { 'domain_id': item["id"], 'domain_ip': ip }
           domaincount+=1
if domaincount == 0:
    print('в API Cloudflare  НЕ найден НИ один домен из domains.txt!  проверьте NS, pfgecnbnt clf-verify-retarget-ns.pys')   
           
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

#dirty
del domains['test.com']
print(json.dumps(domains, indent =4))

#указывает на домен 3 уровня, где находится непосредственно smtp сервер
mailhost = 'smtp'

# добавляем записи DNS в CloudFlare
for x in domains:
   #debug 
   break

   print(f'добавляем записи DNS для домена {x} ')
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
   # add_record(f'v=DKIM1;k=rsa;t=s;s=email;p={getdkim.getdkim(x)}', 'dkim._domainkey', 'TXT', domains[x]['domain_id'], x)

   # Разобраться с TLSA, хз - в API нет метода, возможно в БД лежит
   # с mailcow community:
   # openssl s_client -connect [YOUR-SERVER]:465 -showcerts < /dev/null | openssl x509 -outform DER > server_cert.der
   # openssl x509 -in server_cert.der -inform DER -outform PEM | openssl x509 -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256


# добавляем домен и почтовые ящики в mailcow. Если нужно первичное засеивание доменов то в domains(т.к. проверяет их наличие в cloudflare) 
# и ips нужно указывать соответствующие адреса
# и использовать domains.
# для добавления доменов к уже настроенному per host почтовику нужно использовать domains(а не domains_from_file) и для каждого почтовика 
# скопировав каталог использовать разные MAILCOWAPITOKEN MAILCOWAPIURL MAILCOWAMAINDOMAIN
# если несколько доменов ведут на один и тот же ip то просто повторяем его по количеству доменов

# for x in domains_from_file:
#    mailcowadd_domain.add(x)
#    mailcowadd_mailbox.add(x)

for x in domains_from_file[0:1]:
   mailcowadd_domain.add(x)
