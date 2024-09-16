import boto3

# Substitua com suas chaves de acesso e a região desejada
aws_access_key_id = 'ACCESS_KEY'
aws_secret_access_key = 'SECRET_KEY'
region_name = 'us-east-1'  # Por exemplo, substitua pela sua região

# Inicializa a sessão do boto3
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Nome do bucket que você quer testar
bucket_name = 'meu-bucket-de-teste'  # Substitua pelo nome do seu bucket

# Tags que queremos verificar/adicionar
required_tags = {
    'Enviroment': 'Development',
    'Aplicação': 'DefaultApp',
    'Cliente': 'DefaultClient',
    'Nome': 'DefaultName',
    'Ambiente': 'DefaultEnv'
}

# Função para verificar e adicionar tags
def check_and_add_tags(bucket_name):
    try:
        # Obtém as tags atuais do bucket
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

# Verifica/adiciona tags no bucket especificado
print(f"Verificando tags no bucket: {bucket_name}")
check_and_add_tags(bucket_name)
