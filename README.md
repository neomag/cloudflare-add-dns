## Автоматизация для настройки связки CloudFlare + MailCow  
Автоматически создает указанные в .env:  
домены, указанные в domains.txt  
почтовые ящики, указанные в mailbox.txt  
все необходимые DNS записи для функционирования почты  DKIM/DMARC/SPF/TXT/CNAME/SRV  

запуск:   
1. выполнить базовую установку, описанную в INSTALL  
2. получить CloudFlare API KEY  
3. получить MailCow API KEY  
4. заполнить .env  
5. запустить python3 ./ clf-add-dns.py    


