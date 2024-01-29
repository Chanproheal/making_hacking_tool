1. Execute requirements before running the program
Before you can use a program, it must be installed by default.

sudo git https://https://github.com/Chanproheal/making_hacking_tool/dns_spoofing
sudo chmod +x requirement.txt
./requirement.txt

If you don't have MITM installed, the program will have a much lower chance of success,
so make sure you have MITM installed.


2.If you have completed the basic setup through step 1, next, run DNS spoofing.
cd ~/dns_spoofing
python3 dns_spoof -t <Target url> -r <Replacement URL(IP)>

