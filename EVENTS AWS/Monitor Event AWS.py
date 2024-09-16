from datetime import datetime
import boto3
import json
from datetime import date

dia = date.today().day
mes = date.today().month
ano = date.today().year

client = boto3.client('elasticbeanstalk', aws_access_key_id='*********************', 
                        aws_secret_access_key='*********************',
                        region_name='us-east-1')

# response = client.describe_events(
#     ApplicationName='AUTOWEB-GMAC-HML-JAVA8-2',
#     #TemplateName='string',
#     Severity='WARN',
#     StartTime= datetime(ano, mes, dia),
#     #EndTime=datetime(2023, 6, 13),
#     MaxRecords=1,
#     # PaginationConfig={
#     #     'MaxItems': 1 
#     # }
# )

response = client.describe_events(
    EnvironmentName='NOME DO BEANSTALK',
)

response_inst = client.describe_instances_health(
    EnvironmentName='NOME DO LB',
    AttributeNames=[
        'All',
    ],
)

mensagem_inst = []
for j in response_inst['InstanceHealthList']:
    mensagem_inst.append(j['Causes'])
for k in mensagem_inst:
    for l in k:
        print(l)
        if "memory" in l or "CPU" in l or "No data" in l:
            print('ok')

# mensagem = []
# for i in response['Events']:
#     mensagem.append(i['Message'])
#     if '5xx' in i['Message']:
#         status = {
#             "status": 1
#     }
# else:
#     status = {
#         "status": 0
#     }
