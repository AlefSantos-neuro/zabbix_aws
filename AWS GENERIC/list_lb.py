import boto3
import json

def listar_beanstalks_lld(aws_region, aws_access_key_id, aws_secret_access_key):
    client = boto3.client('elasticbeanstalk', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    
    response = client.describe_applications()

    beanstalks = []

    if 'Applications' in response:
        for app in response['Applications']:
            beanstalks.append({
                '{#APPNAME}': app['ApplicationName'],
                '{#APPDESC}': app.get('Description', 'Sem descrição'),
                '{#APPARN}': app.get['ApplicationArn']
    else:
        print("Nenhuma aplicação Elastic Beanstalk encontrada na região.")

    lld_data = {
        "data": beanstalks
    }

    # Retorna o JSON para o Zabbix
    return json.dumps(lld_data)

if __name__ == "__main__":
    # Especifique a região da AWS (exemplo: us-east-1)
    #regiao = 'us-east-1'
    aws_access_key_id = '*********************'
    aws_secret_access_key = '*********************'
    aws_region = 'sa-east-1'
    print(listar_beanstalks_lld(aws_region, aws_access_key_id, aws_secret_access_key))
