#!/usr/bin/env python

import requests


def request(url) :
    try :
        return requests.get("http://"+url)
    except requests.exceptions.ConnectionError :
        pass

target_url = "google.com"
with open("/home/chan_kali/python_hacking_tool/crawler/subdomains.txt","r") as world_list :
    for line in world_list :
        word = line.strip()
        test_url = word +"."+ target_url
        response = request(test_url)
        if response :
            print("[+] Discovered subdomain ---> "+ test_url)




