import boto3

def consultar_eventos_loadbalancer():
    # Configurar as credenciais da AWS
    session = boto3.Session(
        aws_access_key_id='*********************',
        aws_secret_access_key='*********************+*********************/***************************************************************/*********************',
        region_name='us-east-1'
    )
    
    # Criar um cliente para o serviço do Elastic Load Balancer
    elb_client = session.client('cloudwatch')
    
    # Listar os eventos dos load balancers
    response = elb_client.describe_events('HTTP 5xx')
    
    # Processar a resposta
    eventos = response['Events']
    
    # Imprimir os eventos
    for evento in eventos:
        print('Load Balancer: ', evento['ResourceArn'])
        print('Data/Hora: ', evento['Timestamp'])
        print('Tipo: ', evento['EventType'])
        print('Descrição: ', evento['Description'])
        print('---')
        
# Chamada da função para consultar os eventos dos load balancers
consultar_eventos_loadbalancer()
