import subprocess
import time
import csv
from scapy.all import rdpcap, TCP, UDP, ICMP, ARP, Ether, Raw

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

def analyze_packets(pcap_file, output_csv):
    # Lê o arquivo pcap
    packets = rdpcap(pcap_file)
    
    # Abre o arquivo CSV para escrita
    with open(output_csv, mode='w', newline='') as csv_file:
        fieldnames = [
            'Packet Number', 'Timestamp', 'Ethernet Source', 'Ethernet Destination', 'Ethernet Type',
            'IP Source', 'IP Destination', 'IP Version', 'IP Header Length', 'IP TOS', 'IP Length',
            'IP ID', 'IP Flags', 'IP Fragment Offset', 'IP TTL', 'IP Protocol', 'IP Checksum',
            'TCP Source Port', 'TCP Destination Port', 'TCP Sequence Number', 'TCP Acknowledgment Number',
            'TCP Data Offset', 'TCP Reserved', 'TCP Flags', 'TCP Window', 'TCP Checksum', 'TCP Urgent Pointer',
            'UDP Source Port', 'UDP Destination Port', 'UDP Length', 'UDP Checksum',
            'ICMP Type', 'ICMP Code', 'ICMP Checksum', 'ICMP ID', 'ICMP Sequence',
            'ARP Hardware Type', 'ARP Protocol Type', 'ARP Hardware Size', 'ARP Protocol Size',
            'ARP Opcode', 'ARP Source MAC', 'ARP Source IP', 'ARP Destination MAC', 'ARP Destination IP',
            'Raw Payload'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for i, packet in enumerate(packets, start=1):
            packet_info = {'Packet Number': i, 'Timestamp': packet.time}
            
            if packet.haslayer(Ether):
                ether_layer = packet.getlayer(Ether)
                packet_info.update({
                    'Ethernet Source': ether_layer.src,
                    'Ethernet Destination': ether_layer.dst,
                    'Ethernet Type': ether_layer.type
                })
                
            if packet.haslayer("IP"):
                ip_layer = packet.getlayer("IP")
                packet_info.update({
                    'IP Source': ip_layer.src,
                    'IP Destination': ip_layer.dst,
                    'IP Version': ip_layer.version,
                    'IP Header Length': ip_layer.ihl,
                    'IP TOS': ip_layer.tos,
                    'IP Length': ip_layer.len,
                    'IP ID': ip_layer.id,
                    'IP Flags': ip_layer.flags,
                    'IP Fragment Offset': ip_layer.frag,
                    'IP TTL': ip_layer.ttl,
                    'IP Protocol': ip_layer.proto,
                    'IP Checksum': ip_layer.chksum
                })

            if packet.haslayer(TCP):
                tcp_layer = packet.getlayer(TCP)
                packet_info.update({
                    'TCP Source Port': tcp_layer.sport,
                    'TCP Destination Port': tcp_layer.dport,
                    'TCP Sequence Number': tcp_layer.seq,
                    'TCP Acknowledgment Number': tcp_layer.ack,
                    'TCP Data Offset': tcp_layer.dataofs,
                    'TCP Reserved': tcp_layer.reserved,
                    'TCP Flags': tcp_layer.flags,
                    'TCP Window': tcp_layer.window,
                    'TCP Checksum': tcp_layer.chksum,
                    'TCP Urgent Pointer': tcp_layer.urgptr
                })

            if packet.haslayer(UDP):
                udp_layer = packet.getlayer(UDP)
                packet_info.update({
                    'UDP Source Port': udp_layer.sport,
                    'UDP Destination Port': udp_layer.dport,
                    'UDP Length': udp_layer.len,
                    'UDP Checksum': udp_layer.chksum
                })

            if packet.haslayer(ICMP):
                icmp_layer = packet.getlayer(ICMP)
                packet_info.update({
                    'ICMP Type': icmp_layer.type,
                    'ICMP Code': icmp_layer.code,
                    'ICMP Checksum': icmp_layer.chksum,
                    'ICMP ID': icmp_layer.id,
                    'ICMP Sequence': icmp_layer.seq
                })

            if packet.haslayer(ARP):
                arp_layer = packet.getlayer(ARP)
                packet_info.update({
                    'ARP Hardware Type': arp_layer.hwtype,
                    'ARP Protocol Type': arp_layer.ptype,
                    'ARP Hardware Size': arp_layer.hwlen,
                    'ARP Protocol Size': arp_layer.plen,
                    'ARP Opcode': arp_layer.op,
                    'ARP Source MAC': arp_layer.hwsrc,
                    'ARP Source IP': arp_layer.psrc,
                    'ARP Destination MAC': arp_layer.hwdst,
                    'ARP Destination IP': arp_layer.pdst
                })

            if packet.haslayer(Raw):
                raw_layer = packet.getlayer(Raw)
                packet_info['Raw Payload'] = raw_layer.load

            writer.writerow(packet_info)
    
    print(f"Relatório dos pacotes foi salvo em {output_csv}")

if __name__ == "__main__":
    target_ip = "IP DE DESTINO"  # Substitua pelo IP de destino
    capture_duration = 60  # Duração da captura em segundos
    output_pcap = "capture.pcap"
    output_csv = "report.csv"
    
    # Captura os pacotes
    capture_packets(target_ip, capture_duration, output_pcap)
    
    # Analisa os pacotes capturados e salva em CSV
    analyze_packets(output_pcap, output_csv)

               
