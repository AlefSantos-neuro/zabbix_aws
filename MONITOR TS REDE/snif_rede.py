
import subprocess
import time
from scapy.all import rdpcap

def capture_packets(ip, duration=60, output_file="capture.pcap"):
    # Comando tcpdump para capturar pacotes para o IP especificado
    tcpdump_command = [
        "sudo", "tcpdump", "-i", "any", f"host {ip}", "-w", output_file
    ]
    
    # Inicia a captura de pacotes
    process = subprocess.Popen(tcpdump_command)
    
    # Aguarda o tempo especificado
    time.sleep(duration)
    
    # Termina a captura de pacotes
    process.terminate()
    process.wait()
    
    print(f"Pacotes capturados foram salvos em {output_file}")

def analyze_packets(pcap_file):
    # Lê o arquivo pcap
    packets = rdpcap(pcap_file)
    
    print(f"Total de pacotes capturados: {len(packets)}")
    
    for packet in packets:
        print(packet.summary())
        if packet.haslayer("IP"):
            ip_layer = packet.getlayer("IP")
            print(f"IP Source: {ip_layer.src}")
            print(f"IP Destination: {ip_layer.dst}")
        
        if packet.haslayer("TCP"):
            tcp_layer = packet.getlayer("TCP")
            print(f"Source Port: {tcp_layer.sport}")
            print(f"Destination Port: {tcp_layer.dport}")
        
        if packet.haslayer("UDP"):
            udp_layer = packet.getlayer("UDP")
            print(f"Source Port: {udp_layer.sport}")
            print(f"Destination Port: {udp_layer.dport}")
        
        print("\n")

if __name__ == "__main__":
    target_ip = "IP DE DESTINO"  # Substitua pelo IP de destino
    capture_duration = 60  # Duração da captura em segundos
    output_pcap = "capture.pcap"
    
    # Captura os pacotes
    capture_packets(target_ip, capture_duration, output_pcap)
    
    # Analisa os pacotes capturados
    analyze_packets(output_pcap)
