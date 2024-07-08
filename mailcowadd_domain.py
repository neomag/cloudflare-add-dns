import requests
# import os.path
# from dotenv import load_dotenv

def add(d:str, MAILCOWAPITOKEN:str, MAILCOWAPIURL:str):
    print(d, MAILCOWAPITOKEN, MAILCOWAPIURL)
    #exit()
    
    # #настраиваемся на каталог запуска, на случай вызова из непредвиденного места
    # current_file = os.path.realpath(__file__)
    # current_directory = os.path.dirname(current_file)
    # os.chdir(current_directory)

    # #читаем .env
    # if os.path.isfile('.env'):
    #     load_dotenv()
    # else:
    #     print("ERROR! .env file NOT found, exit")
    #     exit()

    # MAILCOWAPITOKEN    = os.getenv('MAILCOWAPITOKEN')
    # MAILCOWAPIURL      = os.getenv('MAILCOWAPIURL')
  

    headers = {
        'accept': 'application/json',
        'X-API-Key': MAILCOWAPITOKEN
    }

    data =  {
        "active": "1",
        "aliases": "400",
        "backupmx": "0",
        "defquota": "3072",
        "description": "",
        "domain": d,
        "mailboxes": "300",
        "maxquota": "1024000", #10240
        "quota": "1024000",
        "relay_all_recipients": "0",
        "rl_frame": "s",
        "rl_value": "0",
        "restart_sogo": "10",
        "tags": [
            "tag1",
            "tag2"
        ]
        }
    

    response = requests.post(f'{MAILCOWAPIURL}/api/v1/add/domain', headers=headers, json=data)
    if response.status_code == 200:
        pass
    else:
        print(f'MailCow api вернул ошибку!: {response.text} ')
        exit()
    print(response.text)




    