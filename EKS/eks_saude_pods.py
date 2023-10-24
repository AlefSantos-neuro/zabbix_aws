import argparse
import subprocess
import boto3

def check_pod_health(access_key, secret_key, region, namespace, app_name):
    try:
        # credenciais da AWS
        boto3.setup_default_session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

        # Usa kubectl para obter o status dos PODs
        cmd = f'kubectl get pods -n {namespace} -l app={app_name} -o custom-columns=NAME:.metadata.name,STATUS:.status.phase'
        result = subprocess.check_output(cmd, shell=True, text=True)

        # Divide a saída em linhas
        lines = result.strip().split('\n')
        pod_status = {}

        # Analisa a saída e armazenar o status dos PODs
        for line in lines[1:]:
            pod_name, status = line.split()
            pod_status[pod_name] = status

        # Verifica a saúde dos PODs
        problems = []
        for pod_name, status in pod_status.items():
            if status != 'Running':
                problems.append(f'Pod {pod_name} is {status}')

        if problems:
            return problems
        else:
            return "Todos os PODs estão saudáveis."
    except Exception as e:
        return f"Erro ao verificar a saúde dos PODs: {str(e)}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Verificar a saúde dos PODs em um cluster EKS")
    parser.add_argument("--access-key", required=True, help="Chave de acesso da AWS")
    parser.add_argument("--secret-key", required=True, help="Chave secreta da AWS")
    parser.add_argument("--region", required=True, help="Região da AWS")
    parser.add_argument("--namespace", required=True, help="Namespace da API Gateway")
    parser.add_argument("--app-name", required=True, help="Rótulo do app associado à API Gateway")

    args = parser.parse_args()

    result = check_pod_health(args.access_key, args.secret_key, args.region, args.namespace, args.app_name)
    print(result)
