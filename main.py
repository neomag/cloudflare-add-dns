import requests
import json
import os.path
from dotenv import load_dotenv
import mailcowadd_domain
import mailcowadd_mailbox
import clf_add_dns_v2
import regru_changeDNS
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--skipregru", help="пропускает шаг перенацеливания DNS REG.RU на CloudFlare",default = True, nargs='?')
args = parser.parse_args()


#настраиваемся на каталог запуска, на случай вызова из непредвиденного места
current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file)
os.chdir(current_directory)


# читаем mailcows.json
try:
    with open('mailcows.json') as file:
        file_contents = file.read()
        mailcows = json.loads(file_contents)
except:
    print('что-то пошло не так, скорее всего неверный формат файла mailcows.json, проверьте валидатором https://codebeautify.org/json-fixer')
    exit()

# создаем domains.txt и regru_domains.txt из mailcows.json для обратной совместимости с предыдущей версией кода
# to-do: refactor
domains_from_file = []
for x in mailcows.values():
    ADDITIONAL_DOMAINS = x['ADDITIONAL_DOMAINS']
    for doms in ADDITIONAL_DOMAINS:
        domains_from_file.append(doms)

with open('domains.txt', 'w') as file:
    file.write('\n'.join(domains_from_file))
with open('regru-domains.txt', 'w') as file:
    file.write('\n'.join(domains_from_file))


for x in mailcows.values():
    SMTP_ORIGIN = x['name']
    MAILCOWAPITOKEN = x['MAILCOWAPITOKEN']
    MAILCOWAPIURL = x['MAILCOWAPIURL']
    ADDITIONAL_DOMAINS = x['ADDITIONAL_DOMAINS']
    MAILCOWMBOXDEFAULTPASS = x['MAILCOWMBOXDEFAULTPASS']
    MAILCOWMBOXDEFAULTNAME = x['MAILCOWMBOXDEFAULTNAME']
    mailboxes = x['mailboxes']
    
    for doms in ADDITIONAL_DOMAINS:
        # debug, впишите сюда имя домена на котором остановиться
        #if doms == 'xxx.online':
        #    print('___STOP! by debug line')
        #    exit()
        mailcowadd_domain.add(doms, MAILCOWAPITOKEN, MAILCOWAPIURL )
        mailcowadd_mailbox.add(doms, MAILCOWAPITOKEN, MAILCOWAPIURL, MAILCOWMBOXDEFAULTPASS, MAILCOWMBOXDEFAULTNAME, mailboxes )
        #regru_changeDNS.change()
        clf_add_dns_v2.add_records_v2(doms, SMTP_ORIGIN, MAILCOWAPITOKEN, MAILCOWAPIURL )
        print('все скрипты завершили работу')
         


    

   
