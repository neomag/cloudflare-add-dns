import json
with open('domains.txt') as file:
  domains_from_file = file.read().splitlines()
  
total_servers = 4
total_domains = len(domains_from_file) 

divpoint = total_domains//total_servers

checkpoints = []
for x in range(total_domains):
   if x % divpoint == 0 and x <= total_domains and x != 0:
      checkpoints.append(x-1)

print(f"доменов {total_domains}")
print(f"серверов {total_servers}")
print(f"на каждом сервере по {divpoint}")
print(f"чекпоинт каждые {checkpoints}")


result_list = []

for x in domains_from_file:
    result_list.append(x)
    if domains_from_file.index(x)  in checkpoints:
      print(json.dumps(result_list))
      result_list = []
    
print(json.dumps(result_list))
print("можете копировать/вставить эти строки в поля ADDITIONAL_DOMAINS в файле привязки доменов к серверам mailcows.json")      
