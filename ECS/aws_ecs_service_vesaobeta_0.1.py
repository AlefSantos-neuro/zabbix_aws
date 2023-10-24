#!/usr/bin/env python3
import datetime
from optparse import OptionParser
import boto3
import json

end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

### Arguments
parser = OptionParser()
parser.add_option("-c", "--cluster-name", dest="cluster_name", help="ECS cluster name")
parser.add_option("-a", "--access-key", dest="access_key", default="", help="AWS Access Key")
parser.add_option("-k", "--secret-key", dest="secret_key", default="", help="AWS Secret Access Key")
parser.add_option("-r", "--region", dest="region", default="us-east-1", help="ECS region")

(options, args) = parser.parse_args()

if (options.cluster_name is None):
    parser.error("-c ECS cluster name is required")
if (options.region is None):
    parser.error("-r Region is required")
if (options.access_key is None) or (options.secret_key is None):
    parser.error("-a | -k Access and Secret key is required")

# Ajuste do ambiente com mesmo nome devido ao Zabbix não aceitar hosts com o mesmo nome
if options.cluster_name[-3:] == "-sa" or options.cluster_name[-3:] == "-us":
    options.cluster_name = options.cluster_name[:-3]  # Remove a identificação do ambiente do nome do cluster

# Inicialize cluster_metrics fora do bloco try
cluster_metrics = None

# Metricas do Cluster
try:
    ecs_client = boto3.client('ecs', aws_access_key_id=options.access_key, aws_secret_access_key=options.secret_key, region_name=options.region)

    cluster_metrics = ecs_client.describe_clusters(clusters=[options.cluster_name])
    
    if 'clusters' in cluster_metrics and cluster_metrics['clusters']:
        cluster_status = cluster_metrics['clusters'][0]['status']
        running_tasks = str(cluster_metrics['clusters'][0]['runningTasksCount'])
        pending_tasks = str(cluster_metrics['clusters'][0]['pendingTasksCount'])
        services_qtd = str(cluster_metrics['clusters'][0]['activeServicesCount'])

        # Obtendo informações sobre tarefas no cluster
        tasks = ecs_client.list_tasks(cluster=options.cluster_name)
        task_descriptions = ecs_client.describe_tasks(cluster=options.cluster_name, tasks=tasks['taskArns'])

        task_info = []

        for task in task_descriptions['tasks']:
            task_arn = task['taskArn']
            task_definition = task['taskDefinitionArn']

            # Obtenha informações de uso de CPU e memória diretamente da tarefa
            stats = ecs_client.describe_task_definition(taskDefinition=task_definition)
            container_definitions = stats['taskDefinition']['containerDefinitions']

            # Suponha que a tarefa tenha apenas um contêiner (você pode iterar se houver vários)
            container = container_definitions[0]
            cpu = container.get('cpu', 'N/A')
            memory = container.get('memory', 'N/A')

            task_info.append({
                'TaskArn': task_arn,
                'TaskDefinition': task_definition,
                'CPU': cpu,
                'Memory': memory,
                'Status': task['lastStatus'],
            })

        response = {
            'cluster_status': 1 if cluster_status == 'ACTIVE' else 0,
            'running_tasks': running_tasks,
            'pending_tasks': pending_tasks,
            'services_qtd': services_qtd,
            'task_info': task_info
        }

        print(json.dumps(response))
    else:
        print("Cluster não encontrado.")
except Exception as e:
    print("Error describing cluster:" + str(e))
