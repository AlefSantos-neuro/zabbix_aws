from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_vcenter_connection(host, user, password):
    # Ignorar a verificação de certificado SSL (somente pra teste) (CONFIA!!! XD)
    context = ssl._create_unverified_context()
    
    #fecha a conexão com o vcenter
    service_instance = SmartConnect(
        host=host,
        user=user,
        pwd=password,
        sslContext=context
    )
    
    return service_instance

def get_datastores_info(service_instance):
    #pega o conteúdo do inventário do vCenter
    content = service_instance.RetrieveContent()

    #pega os datastores disponíveis
    datastores = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True).view

    datastore_info = []

    for datastore in datastores:
        name = datastore.name
        capacity = datastore.summary.capacity / (1024 ** 3)  # Converter para GB
        free_space = datastore.summary.freeSpace / (1024 ** 3)  # Converter para GB
        used_space = capacity - free_space

        datastore_info.append({
            'name': name,
            'capacity_gb': capacity,
            'free_space_gb': free_space,
            'used_space_gb': used_space
        })

    return datastore_info

def main():
    # Defina a URL e credenciais do seu vCenter
    vcenter_host = 'https://VCENTER_NEWSUPRI'
    vcenter_user = 'USER'
    vcenter_password = 'SENHA'

    #Conectar no vCenter
    service_instance = get_vcenter_connection(vcenter_host, vcenter_user, vcenter_password)

    #pega informações dos datastores
    datastores_info = get_datastores_info(service_instance)

    #cospe as informações dos datastores
    for datastore in datastores_info:
        print(f"Datastore: {datastore['name']}")
        print(f"Capacidade (GB): {datastore['capacity_gb']:.2f}")
        print(f"Espaço Livre (GB): {datastore['free_space_gb']:.2f}")
        print(f"Espaço Utilizado (GB): {datastore['used_space_gb']:.2f}")
        print('-' * 50)

    #desconecta do vCenter (SEMPRE BOM NEEEEEE!!!)
    Disconnect(service_instance)

if __name__ == "__main__":
    main()
