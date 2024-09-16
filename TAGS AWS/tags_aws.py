import boto3

#chaves de acesso aws
aws_access_key_id = 'ACCESS_KEY'
aws_secret_access_key = 'SECRET_KEY'
region_name = 'us-east-1'  #regiao


s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

#listar buckets da regiao
buckets = s3.list_buckets()['Buckets']

# Tags que vão ser validadas e adicionadas
required_tags = {
    'Enviroment': 'PRD', #EXEMPLO
    'Aplicação': 'SLA', #EXEMPLO
    'Cliente': 'SLA VEY', #EXEMPLO
    'Nome': 'JA DISSE SLA', #EXEMPLO
    'Ambiente': 'SLA_TO_SO_DANDO_EXEMPLO' #EXEMPLO
}

#AQUI ONDE A MAGICA ACONTECE, É A FUNÇÃO QUE VAI VALIDAR E ATRIBUIR AS TAGS SE NECESSARIO
def check_and_add_tags(bucket_name):
    try:
        # pega as tags atuais do bucket
        tagging = s3.get_bucket_tagging(Bucket=bucket_name)
        current_tags = {tag['Key']: tag['Value'] for tag in tagging['TagSet']}
    except s3.exceptions.NoSuchTagSet:
        current_tags = {}

    # Verifica se alguma das tags necessárias está faltando
    missing_tags = {key: value for key, value in required_tags.items() if key not in current_tags}

    if missing_tags:
        # Combina as tags atuais com as novas tags necessárias
        updated_tags = {**current_tags, **missing_tags}
        tag_set = [{'Key': k, 'Value': v} for k, v in updated_tags.items()]

        # Aplica as tags atualizadas ao bucket
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': tag_set
            }
        )
        print(f"Tags adicionadas ao bucket {bucket_name}: {missing_tags}")
    else:
        print(f"O bucket {bucket_name} já possui todas as tags necessárias.")

# Itera sobre todos os buckets e verifica/adiciona tags
for bucket in buckets:
    bucket_name = bucket['Name']
    print(f"Verificando tags no bucket: {bucket_name}")
    check_and_add_tags(bucket_name)
