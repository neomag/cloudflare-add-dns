#!/bin/bash
# openssl s_client -connect $1:465 -showcerts < /dev/null | openssl x509 -outform DER > server_cert.der
# openssl x509 -in server_cert.der -inform DER -outform PEM | openssl x509 -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256

# ./get-TLSA.sh abc.ru 2>/dev/null | awk -F'=' '{print($2)}' | sed 's/\s//'