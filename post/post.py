#!/usr/bin/env python

import requests

target_url = "http://192.168.111.154/dvwa/login.php"
data_dict = {"uesrname":"blabalab","password":"1234","Login":"submit"}
response = requests.post(target_url,data=data_dict)
print(response.content)


