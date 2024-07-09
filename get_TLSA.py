import ssl
import hashlib

# заглушка для следующей версии: получение TLSA сертификата для базового домена mailcow

def get(d:str):
    pass
    # url = d
    # cert = ssl.get_server_certificate((url, 443))
    # sha256_hash = hashlib.sha256(cert.encode()).hexdigest()
    # print(f'SHA-256 хэш сертификата для {d}: {sha256_hash}')


get('smtp.abc.com')

