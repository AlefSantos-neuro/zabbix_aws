#!/usr/bin/env python3
import boto3
from datetime import datetime, timedelta

# Configurações
aws_access_key_id = '*********************'
aws_secret_access_key = '*********************'
aws_region = 'us-east-1'  # Exemplo: 'us-east-1'
tags_a_verificar = ['Platform', 'Component', 'Client', 'Environment']
tempo_de_inicio = datetime.now() - timedelta(minutes=10)

# Inicialização do cliente da AWS
session = boto3.Session(region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Lista de serviços da AWS para os quais queremos procurar recursos
servicos_aws = ['ec2', 'lambda', 'rds', 'apigateway']  # Adicione outros serviços conforme necessário

# Verifica recursos em cada serviço da AWS
for servico in servicos_aws:
    client = session.client(servico)
    if servico == 'ec2':
        # Listar instâncias e VPCs
        instances = client.describe_instances()['Reservations']
        vpcs = client.describe_vpcs()['Vpcs']
        resources = instances + vpcs
        for resource in resources:
            if 'InstanceId' in resource:
                resource_id = resource['InstanceId']
                instance_ip = resource.get('PublicIpAddress', 'N/A')
                user = resource.get('KeyName', 'N/A')
                print(f"ID do Recurso: {resource_id}")
                print(f"IP do Recurso: {instance_ip}")
                print(f"Usuário que iniciou o recurso: {user}")
                print()

    elif servico == 'lambda':
        # Listar funções lambda
        functions = client.list_functions()['Functions']
        for function in functions:
            function_name = function['FunctionName']
            print(f"Nome da Função Lambda: {function_name}")
            print()

    elif servico == 'rds':
        # Listar instâncias de RDS
        resources = client.describe_db_instances()['DBInstances']
        for resource in resources:
            resource_id = resource['DBInstanceIdentifier']
            instance_ip = resource.get('Endpoint', {}).get('Address', 'N/A')
            user = 'N/A'
            print(f"ID do Recurso RDS: {resource_id}")
            print(f"IP do Recurso RDS: {instance_ip}")
            print()

    elif servico == 'apigateway':
        # Listar chaves de API no API Gateway
        apis = client.get_api_keys()['items']
        for api in apis:
            api_key_id = api['id']
            api_name = api['name']
            api_description = api.get('description', 'N/A')  # Obtém a descrição ou 'N/A' se não existir
            print(f"ID da Chave de API: {api_key_id}")
            print(f"Nome da Chave de API: {api_name}")
            print(f"Descrição da Chave de API: {api_description}")

            # Obter tags da chave de API
            resource_arn = f"arn:aws:apigateway:{aws_region}::/apikeys/{api_key_id}"
            tags = client.get_tags(resourceArn=resource_arn)['tags']
            print("Tags da Chave de API:")
            for key, value in tags.items():
                print(f"{key}: {value}")
            print()