import boto3
from datetime import datetime

# Configurações iniciais
region_name = 'sa-east-1'  # Região de São Paulo
aws_access_key_id = 'SEU_ACCESS_KEY_ID'
aws_secret_access_key = 'SEU_SECRET_ACCESS_KEY'

# Inicializando o cliente do boto3 para RDS
client = boto3.client('rds', 
                      region_name=region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

# Obtendo informações sobre o banco de dados RDS
db_instance_identifier = 'IDENTIFICADOR_DO_SEU_DB_INSTANCE'

# Consulta para obter informações do último backup
response = client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)

# Extraindo informações sobre o último backup
if 'DBInstances' in response and len(response['DBInstances']) > 0:
    db_instance = response['DBInstances'][0]
    if 'LatestRestorableTime' in db_instance:
        last_backup_time = db_instance['LatestRestorableTime']
        last_backup_time = datetime.strptime(last_backup_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        print(f'Último backup realizado em: {last_backup_time}')

# Consulta para obter o histórico de backups
response = client.describe_db_instance_automated_backups(DBInstanceIdentifier=db_instance_identifier)

# Extraindo informações do histórico de backups
if 'DBInstanceAutomatedBackups' in response and len(response['DBInstanceAutomatedBackups']) > 0:
    print('Histórico de backups:')
    for backup in response['DBInstanceAutomatedBackups']:
        backup_time = backup['InstanceCreateTime']
        backup_time = datetime.strptime(backup_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        print(f' - Backup realizado em: {backup_time}')

