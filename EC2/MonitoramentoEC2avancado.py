import argparse
import boto3
import psutil
import time
import json

def get_ec2_instance_metrics(instance_id, region):
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances(InstanceIds=[instance_id])

    if not response['Reservations']:
        return None

    instance = response['Reservations'][0]['Instances'][0]

    # Coleta métricas da instância
    cpu_utilization = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_utilization = memory_info.percent
    disk_usage = psutil.disk_usage('/')
    disk_utilization = disk_usage.percent

    # Coleta latência (ping) para o IP público da instância
    public_ip = instance['PublicIpAddress']
    ping_latency = ping(public_ip)

    # Coleta tráfego de rede da instância
    network_info = psutil.net_io_counters(pernic=False)
    network_bytes_sent = network_info.bytes_sent
    network_bytes_received = network_info.bytes_recv

    # Coleta status da instância
    instance_status = instance['State']['Name']

    return {
        'CPU_Utilization': cpu_utilization,
        'Memory_Utilization': memory_utilization,
        'Disk_Utilization': disk_utilization,
        'Ping_Latency': ping_latency,
        'Network_Bytes_Sent': network_bytes_sent,
        'Network_Bytes_Received': network_bytes_received,
        'Instance_Status': instance_status
    }

def ping(host):
    import subprocess
    try:
        result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        latency = float(output.split('\n')[1].split('=')[3].split(' ')[0])
        return latency
    except Exception as e:
        print(f"Erro ao executar ping: {str(e)}")
        return None

def main(instance_id, region, access_key, secret_key):
    # Configura as credenciais do Zabbix
    boto3.setup_default_session(region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    
    metrics = get_ec2_instance_metrics(instance_id, region)
    
    if metrics:
        print(json.dumps(metrics, indent=4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coleta métricas de uma instância EC2 da AWS e retorna em formato JSON")
    parser.add_argument("instance_id", type=str, help="ID da instância EC2 a ser consultada")
    parser.add_argument("region", type=str, help="Região da AWS onde a instância está localizada")
    parser.add_argument("access_key", type=str, help="Chave de acesso da AWS")
    parser.add_argument("secret_key", type=str, help="Chave secreta da AWS")
    args = parser.parse_args()
    main(args.instance_id, args.region, args.access_key, args.secret_key)
