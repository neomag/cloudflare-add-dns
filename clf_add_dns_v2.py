import requests
import json
import os.path
from dotenv import load_dotenv
import getdkim

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

# получаем domain_id по имени через Cloudflare API
def get_domain_id(d:str):
   params = {"name": d}
   response = requests.get(CFL_API_URLzones+'/?&per_page=1000', headers=headers, params = params)
   if response.status_code == 200:
      id = response.json()["result"][0]["id"]
      return id
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
      exit()


def add_records_v2(domain:str, SMTP_ORIGIN:str, MAILCOWAPIURL:str, MAILCOWAPITOKEN:str):   
   data = {}
   MAILCOWAPIURL = MAILCOWAPIURL
   MAILCOWAPITOKEN = MAILCOWAPITOKEN
   id = get_domain_id(domain)

   # MX
   print('создается MX запись')
   data = {'content': SMTP_ORIGIN, 'name': '@', 'proxied': False, 'type': 'MX', 'id': id, 'priority': 10, 'ttl': 300}
   response = requests.post( f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records', headers = headers, json = data)
   if response.status_code == 200:
      pass
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
   print(f'ответ CloudFlare API: {response.text}')


   # CNAME autodiscover
   print('создается CNAME autodiscover запись')
   data = {'content': SMTP_ORIGIN, 'name': 'autodiscover', 'proxied': False, 'type': 'CNAME', 'id': id, 'ttl': 300}
   response = requests.post( f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records', headers = headers, json = data)
   if response.status_code == 200:
      pass
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
   print(f'ответ CloudFlare API: {response.text}')


   # SRV
   print('создается SRV запись')
   data = {'data': {'weight': 5, 'priority': 5, 'port': 443, 'target': SMTP_ORIGIN}, 'name': '_autodiscover._tcp', 'proxied': False, 'type': 'SRV', 'id': id, 'ttl': 300}
   response = requests.post( f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records', headers = headers, json = data)
   if response.status_code == 200:
      pass
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
   print(f'ответ CloudFlare API: {response.text}')

   # autoconfig CNAME
   print('создается CNAME autodiscover запись')
   data = {'content': SMTP_ORIGIN, 'name': 'autoconfig', 'proxied': False, 'type': 'CNAME', 'id': id, 'ttl': 300}
   response = requests.post( f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records', headers = headers, json = data)
   if response.status_code == 200:
      pass
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
   print(f'ответ CloudFlare API: {response.text}')


   # SPF
   print('создается SPF запись')
   data = {'content': 'v=spf1 mx a -all', 'name': '@', 'proxied': False, 'type': 'TXT', 'id': id, 'ttl': 300}
   response = requests.post( f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records', headers = headers, json = data)
   if response.status_code == 200:
      pass
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
   print(f'ответ CloudFlare API: {response.text}')


   # DMARC
   # add_record(f'v=DMARC1; p=reject; rua=mailto:test@{x}', '_dmarc', 'TXT', domains[x]['domain_id'], x)
   print('создается DMARC запись')
   data = {'content': f'v=DMARC1; p=reject; rua=mailto:test@{domain}', 'name': '_dmarc', 'proxied': False, 'type': 'TXT', 'id': id, 'ttl': 300}
   response = requests.post( f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records', headers = headers, json = data)
   if response.status_code == 200:
      pass
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
   print(f'ответ CloudFlare API: {response.text}')


   # получаем DKIM для домена
   try:
      dkim = getdkim.get(domain, MAILCOWAPIURL, MAILCOWAPITOKEN)
      print(f'dkim = {dkim}')
   except:
      print("ERROR! получение DKIM записи завершилось ошибкой, возможно такого домена не существует еще на mailcow сервере! Проверьте mailcows.json и что в админке почтовика")
      exit()
   # DKIM
   print('создается DKIM запись')
   data = {'content': f'v=DKIM1;k=rsa;t=s;s=email;p={dkim}', 'name': 'dkim._domainkey', 'proxied': False, 'type': 'TXT', 'id': id, 'ttl': 300}
   response = requests.post( f'https://api.cloudflare.com/client/v4/zones/{id}/dns_records', headers = headers, json = data)
   if response.status_code == 200:
      pass
   else:
      print(f'CloudFlare api вернул ошибку!: {response.text} ')
   print(f'ответ CloudFlare API: {response.text}')