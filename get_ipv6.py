import netifaces

# заглушка под следующую версию: получение ipv6 для AAAA/PTR

# Получаем адреса только для интерфейса eth0
addrs = netifaces.ifaddresses('eth0')

if netifaces.AF_INET6 in addrs:
    for addr_info in addrs[netifaces.AF_INET6]:
        if 'addr' in addr_info:
            ipv6_addr = addr_info['addr']
            print(f"IPv6 адрес интерфейса eth0: {ipv6_addr}")
