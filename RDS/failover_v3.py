import boto3
import requests
import json

# Configurações da AWS
aws_access_key = '*********************'
aws_secret_key = '*********************'
region_name = 'us-east-1'  # Região da Virgínia

# Nome do RDS
rds_instance_name = 'DNS DO RDS'

# URL do Webhook do Hangouts
hangouts_webhook_url = 'HANGOUTS URL API'

def send_hangouts_message(message):
    payload = {'text': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(hangouts_webhook_url, data=json.dumps(payload), headers=headers)
    return response

def check_rds_events():
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    
    rds_client = session.client('rds')
    
    try:
        response = rds_client.describe_events(SourceType='db-instance', SourceIdentifier=rds_instance_name)
        events = response.get('Events', [])
        
        for event in events:
            event_category = event['EventCategories'][0]
            if event_category in ['failover', 'notification', 'stop', 'start']:
                send_hangouts_message(f"ALERTA: Evento identificado - Categoria: {event_category}")
                return 1
        
        return 0
    except Exception as e:
        send_hangouts_message(f"ERRO: Ocorreu um problema - {str(e)}")
        return -1

if __name__ == '__main__':
    result = check_rds_events()
    if result == 0:
        print(result)
    elif result == 1:
        print(result)
    else:
        print(result)
