import requests
import json
import os.path
import mailcowdelete_mailbox


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


domains_from_file = []
# получаем список доменов на уделение
for x in mailcows.values():
    ADDITIONAL_DOMAINS = x['ADDITIONAL_DOMAINS']
    for doms in ADDITIONAL_DOMAINS:
        domains_from_file.append(doms)

def confirm():
    print('***  ВНИМАНИЕ ! **** вы хотите удалить все домены в на всех серверах?:')
    print(domains_from_file)
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("ваш выбор [Y/N]? ").lower()
    return answer == "y"    

# запрашиваем подтверждение перед опасной операцией
confirm()

# possible error:   searching inside all domains all boxes
for x in mailcows.values():
    MAILCOWAPITOKEN = x['MAILCOWAPITOKEN']
    MAILCOWAPIURL = x['MAILCOWAPIURL']
    ADDITIONAL_DOMAINS = x['ADDITIONAL_DOMAINS']
    MAILCOWMBOXDEFAULTPASS = x['MAILCOWMBOXDEFAULTPASS']
    MAILCOWMBOXDEFAULTNAME = x['MAILCOWMBOXDEFAULTNAME']
    mailboxes = x['mailboxes']


    print('начинаю удаление почтовых ящиков на mailcow серверах...')
    if len(ADDITIONAL_DOMAINS) == 0:
        print('дополнительных доменов нет. skip')
    else:
        for doms in ADDITIONAL_DOMAINS:         
            mailcowdelete_mailbox.delete(doms, MAILCOWAPITOKEN, MAILCOWAPIURL, MAILCOWMBOXDEFAULTPASS, MAILCOWMBOXDEFAULTNAME, mailboxes )

    
    headers = {
    'accept': 'application/json',
    'X-API-Key': MAILCOWAPITOKEN
    }

    print('начинаю удаление доменов на mailcow серверах...')
    if len(ADDITIONAL_DOMAINS) == 0:
        print('дополнительных доменов нет. skip')
    else:
        for doms in ADDITIONAL_DOMAINS:       
            data = doms
            response = requests.post(f'{MAILCOWAPIURL}/api/v1/delete/domain', headers=headers, json=data)
            if response.status_code == 200:
                print(response.text)
            else:
                print(f'MailCow api вернул ошибку!: {response.text} ')
                exit()
            print(response.text)
            
    

   
