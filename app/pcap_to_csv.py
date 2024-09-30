import pandas as pd
import scapy.all as scapy

def convert_pcap_to_csv(pcap_file):
    packets = scapy.rdpcap(pcap_file)
    data = []
    
    for packet in packets:
        row = {
            'src_ip': packet[scapy.IP].src if packet.haslayer(scapy.IP) else None,
            'dst_ip': packet[scapy.IP].dst if packet.haslayer(scapy.IP) else None,
            'protocol': packet[scapy.IP].proto if packet.haslayer(scapy.IP) else None,
            'length': len(packet)
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    csv_file = pcap_file.replace('.pcap', '.csv')
    df.to_csv(csv_file, index=False)
    
    return csv_file
