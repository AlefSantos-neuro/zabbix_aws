import boto3
from botocore.exceptions import NoCredentialsError
import smtplib
import email.message

aws_access_key_id = '*********************'
aws_secret_access_key = '*********************'
aws_region = 'sa-east-1'

def get_elb_policy(load_balancer_name):
    elbv2 = boto3.client('elbv2')

    response = elbv2.describe_load_balancers(Names=[load_balancer_name])

    if 'LoadBalancers' in response and len(response['LoadBalancers']) > 0:
        load_balancer = response['LoadBalancers'][0]
        listeners = load_balancer.get('Listeners', [])

        for listener in listeners:
            if 'DefaultActions' in listener and len(listener['DefaultActions']) > 0:
                default_action = listener['DefaultActions'][0]
                if 'Type' in default_action and default_action['Type'] == 'fixed-response':
                    return default_action.get('FixedResponseConfig', {}).get('ContentType', '')

    return None

def main():
    hosted_zone_name = 'dominio.com.br'
    elb_security_policy = 'ELBSecurityPolicy-TLS-1-2-Ext-2018-06'

    aws_access_key_id = '*********************'
    aws_secret_access_key = '*********************'
    aws_region = 'sa-east-1'

    route53 = boto3.client('route53', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

    response = None

    try:
        response = route53.list_hosted_zones_by_name(DNSName=hosted_zone_name)
    except Exception as e:
        print(f"Erro ao obter zonas hospedadas: {e}")

    if response and 'HostedZones' in response and len(response['HostedZones']) > 0:
        hosted_zone_id = response['HostedZones'][0]['Id']
        print(f'Hosted Zone ID: {hosted_zone_id}')
    
    if 'HostedZones' in response and len(response['HostedZones']) > 0:
        hosted_zone_id = response['HostedZones'][0]['Id']

        elbs = boto3.client('elbv2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
        response = elbs.describe_load_balancers()

        for elb in response['LoadBalancers']:
            elb_name = elb['LoadBalancerName']
            dns_name = elb['DNSName']

            if dns_name.endswith(hosted_zone_name):
                policy = get_elb_policy(elb_name)

                if policy == elb_security_policy:
                    print(f'The Load Balancer {elb_name} in DNS {dns_name} has the correct security policy.')
                else:
                    print(f'The Load Balancer {elb_name} in DNS {dns_name} does not have the correct security policy.')

if __name__ == "__main__":
    main()


def envia_email(url, ambiente, tls_version):
    corpo_email = (
        f"<p>Prezados,</p>"
        f"<p>Identificamos casos de versão inconsistente na política de segurança do TLS para a URL: {url}.</p>"
        f"<p>Detalhes:</p>"
        "<table border='1'>"
        "<tr><th>URL</th><th>Ambiente</th><th>Versão do TLS</th></tr>"
        f"<tr><td>{url}</td><td>{ambiente}</td><td>{tls_version}</td></tr>"
        "</table>"
    )

    emails = ['noc@neurotech.com.br']

    msg = email.message.Message()
    msg.set_payload(corpo_email)
    msg['Subject'] = 'Alerta: Versão Inconsistente do TLS'
    msg['From'] = 'remetente visivel'
    msg['To'] = ", ".join(emails)
    msg.add_header('Content-Type', 'text/html')

    try:
        s = smtplib.SMTP('*********************', 587)
        s.ehlo()
        s.starttls()
        s.login('*********************', '*********************')
        s.sendmail(msg['From'], emails, msg.as_string().encode('utf-8'))
        s.quit()

        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
