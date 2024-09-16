import paramiko
from pysnmp.hlapi import *

def snmp_get(ip, oid, community='public', port=161):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((ip, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if error_indication:
        print(f"SNMP Get Error: {error_indication}")
        return None
    elif error_status:
        print(f"SNMP Get Error: {error_status}")
        return None
    else:
        return var_binds[0][1].prettyPrint()

def ssh_execute_command(ip, username, key_filename, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, key_filename=key_filename)

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        client.close()
        return output
    except paramiko.AuthenticationException as e:
        print("Authentication failed:", e)
    except paramiko.SSHException as e:
        print("SSH error:", e)
    except Exception as e:
        print("Error:", e)
    return None

def main():
    target_ip = 'IP DA MAQUIONA'  #  IP da Vyatta na AWS
    #vpn_oid = '1.3.6.1.2.1.16.9.1.3.1'  # OID da VPN específica
    remote_id = 'ID DA MAQUINA'
    # credenciais de acesso à Vyatta na AWS
    username = 'NOME DE USUARIO'
    key_filename = '/CAMINHO/PARA/O/DIRETORIO/CHAVE.ALGUMACOISA'

    #command = f'snmpget -v 2c -c public {target_ip} {vpn_oid}'
    command = f'snmpget -v 2c -c public {target_ip} {remote_id}'
    output = ssh_execute_command(target_ip, username, key_filename, command)

    if output is not None:
        vpn_status = output.split(':')[-1].strip()

        if vpn_status == '1':
            print("Status da VPN: UP")
            return 1
        elif vpn_status == '0':
            print("Status da VPN: DOWN")
            return 0
        else:
            print("Status da VPN: Desconhecido")
            return -1
    else:
        print("Falha ao executar o comando SSH.")
        return -1

if __name__ == "__main__":
    status = main()
