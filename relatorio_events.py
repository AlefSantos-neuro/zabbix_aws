# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI
import csv
from datetime import datetime, timedelta
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def enviar_email_csv(destinatario, assunto, corpo, arquivo_csv):
    remetente = "seu_email@dominio.com"
    senha = "sua_senha"

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    mensagem.attach(MIMEText(corpo, 'plain'))

    with open(arquivo_csv, "rb") as arquivo:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(arquivo.read())
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', f'attachment; filename={arquivo_csv}')
        mensagem.attach(parte)

    with smtplib.SMTP('smtp.dominio.com', 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)

URL = "sua_url_api"
TOKEN = "seu_token"

resposta = requests.post(URL,
                         json={
                             "jsonrpc": "2.0",
                             "method": "event.get",
                             "params": {
                                 "output": "extend",
                                 "hostids": ID_HOST,
                                 "time_from": int(datetime(2024, 7, 1).timestamp()),
                                 "time_till": int(datetime(2024, 7, 31, 23, 59, 59).timestamp()),
                                 "select_acknowledges": "extend"
                             },
                             "auth": TOKEN,
                             "id": 1
                         })

informacoes_host = resposta.json()['result']

dados_csv = [["ID", "Descrição", "Início", "Fim", "Comentários"]]

for evento in informacoes_host:
    id_evento = evento['eventid']
    descricao = evento['name']
    inicio_timestamp = int(evento['clock'])
    duracao_minutos = int(evento['value'])
    fim_timestamp = inicio_timestamp + (duracao_minutos * 60)
    inicio_data_hora = datetime.fromtimestamp(inicio_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    fim_data_hora = datetime.fromtimestamp(fim_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    comentarios = ""
    if 'acknowledges' in evento and evento['acknowledges']:
        comentarios = "; ".join([ack['message'] for ack in evento['acknowledges']])

    dados_csv.append([id_evento, descricao, inicio_data_hora, fim_data_hora, comentarios])

arquivo_csv = "relatorio_eventos.csv"
with open(arquivo_csv, "w", newline="") as arquivo:
    escritor_csv = csv.writer(arquivo)
    escritor_csv.writerows(dados_csv)

enviar_email_csv("teste@dominio.com", 
                 "Relatório de Eventos com Comentários", 
                 "Segue em anexo o relatório de eventos com comentários incluídos.", 
                 arquivo_csv)