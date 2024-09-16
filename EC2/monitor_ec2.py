#!/usr/bin/env python3
import boto3
import psutil
import json
import paramiko

aws_region = 'us-east-1'
aws_access_key_id = '*********************'
aws_secret_access_key = '*********************'

def get_instance_metrics(instance_id):
    # Inicializa o cliente EC2
    ec2_client = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # Obtém informações sobre a instância
    response = ec2_client.describe_instances(InstanceIds=[instance_id])

    # Extrai o endereço IP público da instância
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

    # Inicializa o cliente SSH para se conectar à instância
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Conecta à instância usando a chave privada
    ssh_key = paramiko.RSAKey.from_private_key_file('/home/user/chave_de-acesso')
    ssh_client.connect(hostname=public_ip, username='USER DA MAQUINA', pkey=ssh_key)


    # Coleta métricas de sistema usando psutil
    #cpu_percent = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().used
    #disk_usage = psutil.disk_usage('/').used

    # Fecha a conexão SSH
    ssh_client.close()

    # Retorna as métricas coletadas em um dicionário
    ssh_client.close()

    # Retorna as métricas coletadas em um dicionário
    return {
        #'instance_id': instance_id,
        #'cpu_percent': cpu_percent,
        'memory_usage': memory_usage,
        #'disk_usage': disk_usage,
        #'current_cpu_usage': psutil.cpu_percent(),
        'current_memory_usage': psutil.virtual_memory().percent,
        #'current_disk_usage': psutil.disk_usage('/').percent
    }

def main():
    # ID da instância AWS
    instance_id = 'ID DA INSTANCIA'

    # Obtém métricas da instância
    instance_metrics = get_instance_metrics(instance_id)

    # Imprime as métricas coletadas em formato JSON
    print(json.dumps(instance_metrics, indent=4))

if __name__ == "__main__":
    main()
