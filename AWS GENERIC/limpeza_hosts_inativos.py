from ast import For
#from ctypes.wintypes import PWORD
from pyzabbix import ZabbixAPI
import requests
import json
import email.message
import smtplib
import time

# Função para fazer login:
URL = '*********************'
USER = '*********************'
PWORD = '*********************:SGq'

# Login
r = requests.post(URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.login",
                      "params": {
                          "user": USER,
                          "password": PWORD},
                      "id": 1
                  })
TOKEN = r.json()["result"]

# Enviar email
def enviar(html):
    print(html)
    emails = ['noc@neurotech.com.br']
    msg = email.message.Message()
    msg.set_payload(html)
    msg['Subject'] = '[THREAD] ASSUNTO'
    msg['From'] = "Alertas Zabbix <*********************>"
    msg['To'] = ", ".join(emails)
    msg.add_header('Content-Type', 'text/html')
    s = smtplib.SMTP('*********************', 587)
    s.ehlo()
    s.starttls()
    s.login('*********************', '*********************')
    s.sendmail(msg['From'], emails, msg.as_string())
    s.quit()

# Array de hosts
id_host=[]
name_host=[]
i = 1


def list():
    # Lista hosts desativados
    hosts = []

    hosts = requests.post(URL,
                        json={
                            "jsonrpc": "2.0",
                            "method": "host.get",
                            "params": {
                                "output": ['name'],
                                "filter": {
                                    "status": "1"
                                },
                                "limit": "20"
                            },
                            "id": 2,
                        "auth": TOKEN
                        }
                        )
    hosts = hosts.json()

    if hosts['result'] == []:
        html = "Prezados, <br>Nenhum host desativado para ser removido! <br> <br> Att."          
        enviar(html)        
        return 0
    else:
        return 1

# Deleta hosts desativados
def deletar_host():

    # Lista hosts desativados
    hosts = []

    hosts = requests.post(URL,
                        json={
                            "jsonrpc": "2.0",
                            "method": "host.get",
                            "params": {
                                "output": ['name'],
                                "filter": {
                                    "status": "1"
                                },
                                "limit": "20"
                            },
                            "id": 2,
                        "auth": TOKEN
                        }
                        )
    hosts = hosts.json()

    for h in hosts['result']:
        id_host.append(h['hostid'])
        name_host.append(h['name'])
    
    # remove hosts desativados
    r = requests.post(URL,
                        json={
                            "jsonrpc": "2.0",
                            "method": "host.delete",
                            "params": id_host,
                            "auth": TOKEN
                            })
    html = "Prezados, <br> <br>" + "Hosts removidos ids: <br>" + str(id_host) + "<br> <br>" + "Hosts removidos: <br>" + str(name_host) + "</strong>" + " <br> " + "Removidos com sucesso" + "<br> <br> Att."                
    # Função enviar email
    enviar(html)

    if (id_host == []):
        i = 0
        return i
    else:
        i = 1
        return i

while list() > 0:
    deletar_host()

    id_host.clear()
    name_host.clear()

    time.sleep(5)
