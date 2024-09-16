import boto3
from datetime import datetime, timedelta

#S3_CLIENT
s3 = boto3.client('s3',
    aws_access_key_id='*********************',
    aws_secret_access_key='*********************',
    region_name='sa-east-1'
)

#NOME DO BUCKET
bucket_name = '*********************'
#PATH
folder_path = '*********************'

#Função para verificar alterações
def verifica_alteracoes():
    try:
        #olha os ultimos 30 minutos
        trinta_minutos_atras = datetime.now() - timedelta(minutes=30)

        #lista todas as versõe
        versions = s3.list_object_versions(Bucket=bucket_name, Prefix=folder_path)

        # Verifica se há alguma versão mais recente do que a versão atual nos últimos 30 minutos
        if versions.get('Versions'):
            print("1")  # Houve alteração
            for version in versions['Versions']:
                if version['IsLatest'] and version['LastModified'] > trinta_minutos_atras:
                    print(f"Nome do arquivo alterado: {version['Key']}")
        else:
            print("0")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    verifica_alteracoes()
