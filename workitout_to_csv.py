#!/usr/bin/env python3

import requests
import csv
import json
from datetime import datetime

with open('mycreds.json') as credsfile:
    creds = json.load(credsfile)

cookies = {
    'PHPSESSID': creds["cookie"],
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    'DNT': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': creds["referer"],
    'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
}

response = requests.get(creds["url"], headers=headers, cookies=cookies)


to_keys = {
    "StammNr": "StammNr",
    "PreName": "FirstName",
    "Name": "LastName",
    "Zimmernummer": "RoomNr",
    "BlockedTill": "BlockedTill"
        }
d = list(response.json())
d = [{v: e[k] for k, v in to_keys.items()} for e in d]

for e in d:
    e["BlockedTill"], _ = e["BlockedTill"].split()
    if e["BlockedTill"] == "0000-00-00":
        e["BlockedTill"] = ""
    else:
        e["BlockedTill"] = datetime.strptime(e["BlockedTill"], "%Y-%m-%d").strftime("%d.%m.%Y")

with open("workitout_list.csv", "w") as outfile:
    dict_writer = csv.DictWriter(outfile, to_keys.values())
    dict_writer.writeheader()
    dict_writer.writerows(d)
