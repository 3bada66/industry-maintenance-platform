# backend/services/pcap_parser.py

from multiprocessing import Process, Queue
from collections import defaultdict
import pyshark


def normalize_protocol(protocol_name):
    """
    Normalizza i nomi dei protocolli estratti dal PCAP per corrispondere
    alle opzioni standard del form di modifica asset.
    """
    if not protocol_name:
        return None
    
    protocol_name = protocol_name.upper().strip()
    
    # Mappa dei protocolli industriali comuni
    protocol_mapping = {
        # Protocolli Modbus
        'MODBUS': 'Modbus',
        'MODBUS-TCP': 'Modbus',
        'MODBUS-RTU': 'Modbus',
        'MODBUS-ASCII': 'Modbus',
        
        # Protocolli Profinet
        'PROFINET': 'Profinet',
        'PN': 'Profinet',
        'PROFINET-IO': 'Profinet',
        
        # Protocolli OPC
        'OPC-UA': 'OPC-UA',
        'OPCUA': 'OPC-UA',
        'OPC': 'OPC-UA',
        
        # Protocolli EtherNet/IP
        'ETHERNET/IP': 'EtherNet/IP',
        'ETHERNETIP': 'EtherNet/IP',
        'ENIP': 'EtherNet/IP',
        'CIP': 'EtherNet/IP',
        
        # Protocolli BACnet
        'BACNET': 'BACnet',
        'BACNET-IP': 'BACnet',
        'BACNET-MSTP': 'BACnet',
        
        # Protocolli DNP3
        'DNP3': 'DNP3',
        'DNP': 'DNP3',
        
        # Protocolli KNX
        'KNX': 'KNX',
        'KNXNET': 'KNX',
        
        # Protocolli M-Bus
        'M-BUS': 'M-Bus',
        'MBUS': 'M-Bus',
        
        # Protocolli IEC 61850
        'IEC61850': 'IEC 61850',
        'IEC-61850': 'IEC 61850',
        'MMS': 'IEC 61850',  # Manufacturing Message Specification
        
        # Protocolli S7
        'S7': 'S7',
        'S7COMM': 'S7',
        'S7-PROTOCOL': 'S7',
        
        # Protocolli MQTT
        'MQTT': 'MQTT',
        'MQTT-SN': 'MQTT',
        
        # Protocolli HTTP/HTTPS (per sistemi SCADA web)
        'HTTP': 'Other',
        'HTTPS': 'Other',
        
        # Protocolli FTP
        'FTP': 'Other',
        'FTPS': 'Other',
        'SFTP': 'Other',
        
        # Protocolli SSH/Telnet
        'SSH': 'Other',
        'TELNET': 'Other',
        
        # Protocolli SNMP
        'SNMP': 'Other',
        'SNMPV1': 'Other',
        'SNMPV2': 'Other',
        'SNMPV3': 'Other',
        
        # Protocolli DNS/DHCP
        'DNS': 'Other',
        'DHCP': 'Other',
        
        # Protocolli di base (non industriali)
        'TCP': None,
        'UDP': None,
        'IP': None,
        'ARP': None,
        'ICMP': None,
        'ICMPV6': None,
        'IPV6': None,
    }
    
    # Controlla prima la mappa esatta
    if protocol_name in protocol_mapping:
        return protocol_mapping[protocol_name]
    
    # Controlla se contiene uno dei protocolli industriali come substring
    for key, value in protocol_mapping.items():
        if key in protocol_name and value:
            return value
    
    # Se non trova corrispondenze, restituisce il nome originale
                    # but only if it's not a base protocol (TCP, UDP, etc.)
    if protocol_name not in ['TCP', 'UDP', 'IP', 'ARP', 'ICMP', 'ICMPV6', 'IPV6']:
        return protocol_name
    
    return None


def _parse_pcap_worker(pcap_path, queue):
    cap = pyshark.FileCapture(pcap_path, keep_packets=False)
    cap.load_packets()

    devices = defaultdict(lambda: {"ips": set(), "protocols": set()})
    communications = defaultdict(
        lambda: defaultdict(int)
    )  # src_mac -> dst_mac -> count

    for pkt in cap:
        try:
            eth = pkt.eth
            src_mac = eth.src.upper()
            dst_mac = eth.dst.upper()
            ip = None
            if hasattr(pkt, "ip"):
                ip = pkt.ip.src

            # aggiorna devices
            if ip:
                devices[src_mac]["ips"].add(ip)
            
            # Normalizza il protocollo prima di aggiungerlo
            proto = pkt.highest_layer
            normalized_proto = normalize_protocol(proto)
            if normalized_proto:
                devices[src_mac]["protocols"].add(normalized_proto)

            # traccia comunicazione tra src e dst MAC
            communications[src_mac][dst_mac] += 1
        except AttributeError:
            continue

    cap.close()

    # Converti set in lista prima di restituire
    for mac in devices:
        devices[mac]["ips"] = list(devices[mac]["ips"])
        devices[mac]["protocols"] = list(devices[mac]["protocols"])

    queue.put((dict(devices), dict(communications)))


def extract_assets_and_communications_from_pcap(pcap_path):
    """
    Estrae da un file pcap la lista di dispositivi rilevati.
    Restituisce un dizionario con MAC address come chiavi.
    """
    queue = Queue()
    proc = Process(target=_parse_pcap_worker, args=(pcap_path, queue))
    proc.start()
    proc.join()

    if not queue.empty():
        devices, communications = queue.get()
        return devices, communications
    else:
        return {}, {}
