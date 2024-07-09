import requests
import os.path
#from dotenv import load_dotenv

def delete(d:str,  MAILCOWAPITOKEN:str, MAILCOWAPIURL:str, MAILCOWMBOXDEFAULTPASS:str, MAILCOWMBOXDEFAULTNAME:str, mailboxes:list ):
    #настраиваемся на каталог запуска, на случай вызова из непредвиденного места
    current_file = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file)
    os.chdir(current_directory)

    MAILCOWAPITOKEN = MAILCOWAPITOKEN
    MAILCOWAPIURL = MAILCOWAPIURL
    MAILCOWMBOXDEFAULTPASS = MAILCOWMBOXDEFAULTPASS
    MAILCOWMBOXDEFAULTNAME = MAILCOWMBOXDEFAULTNAME
    print(MAILCOWAPITOKEN, MAILCOWAPIURL, MAILCOWMBOXDEFAULTPASS, MAILCOWMBOXDEFAULTNAME, mailboxes)
    
    headers = {
        'accept': 'application/json',
        'X-API-Key': MAILCOWAPITOKEN
    }

    for mbox in mailboxes:
        data =  f"{mbox}@{d}"
        
        response = requests.post(f'{MAILCOWAPIURL}/api/v1/delete/mailbox', headers=headers, json=data)
        if response.status_code == 200:
            pass
        else:
            print('MailCow api вернул ошибку!: {response.text} ')
            exit()
        
        print(response.text)
    