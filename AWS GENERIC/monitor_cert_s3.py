import boto3
import io
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Substitua estas variáveis pelos seus valores
AWS_ACCESS_KEY_ID = 'sua-access-key'
AWS_SECRET_ACCESS_KEY = 'sua-secret-key'
BUCKET_NAME = '*********************'
PREFIX = 'BUCKET NO S3 ONDE TA O CERTIFICADO'

# Inicialize o cliente S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Liste os objetos no bucket com o prefixo especificado
response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)

# Função para verificar validade do certificado
def check_cert_expiry(cert_data):
    cert = x509.load_pem_x509_certificate(cert_data, default_backend())
    return cert.not_valid_before, cert.not_valid_after

# Baixe e verifique cada certificado
for obj in response.get('Contents', []):
    file_key = obj['Key']
    print(f"Verificando {file_key}")

    # Baixe o arquivo do S3
    cert_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    cert_data = cert_obj['Body'].read()

    # Verifique a validade
    not_valid_before, not_valid_after = check_cert_expiry(cert_data)
    print(f"Certificado: {file_key}")
    print(f"Válido de: {not_valid_before}")
    print(f"Válido até: {not_valid_after}")
    print('---')

