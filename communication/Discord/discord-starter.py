#!/usr/bin/python
import requests
import re
import os
import json
import time
import shutil
import subprocess
from math import *
def _get_net_data():
    try:
        r = requests.head('https://discord.com/api/download?platform=linux&format=tar.gz')
        dl_url = r.headers['location']
        filename = dl_url.split('?')[0].split('/')[-1]
        version = re.search(r'(\d+\.\d+\.\d+)', filename).group(1)
        return {"filename": filename,"version":version,"url": dl_url}
    except Exception:
        return "Error: bad response..."
    

def _get_local_data():
    with open(os.path.expanduser("~/.local/share/Discord/resources/build_info.json"),"r") as dat:
        loc=json.load(dat)
    return loc

def update_local(local_data,net_data):
    version=net_data['version']
    local_data["version"] = version
    with open(os.path.expanduser("~/.local/share/Discord/resources/build_info.json"),"w") as dat:
        json.dump(local_data,dat)

if not os.path.exists(os.path.expanduser("~/.local/share/Discord/Discord")):
    discord_net_data = _get_net_data()
    secs=0
    while type(discord_net_data) == str:
        print("Internet Error,",str(secs)+"s,","trying again in 3 seconds")
        time.sleep(3)
        secs+=3
        discord_net_data = _get_net_data()
    tmppath = discord_net_data["filename"]+'.temp'
    print(f'downloading {discord_net_data["url"]}')
    with requests.get(discord_net_data["url"], stream=True) as r:
        total_length = int(r.headers.get('content-length'))
        downloaded=0
        with open(tmppath,'wb') as fp:
            for chunk in r.iter_content(chunk_size=65536):
                fp.write(chunk)
                downloaded+=65536
                print("\r",floor(downloaded/total_length*100),"% of",round(total_length/1000000,1),"Mo downloaded...",end="")
    print()
    shutil.move(tmppath,discord_net_data["filename"])
    if os.path.exists(os.path.expanduser("~/.local/share/Discord/")):
        shutil.move(os.path.expanduser("~/.local/share/Discord"),os.path.expanduser("~/.local/share/Discord.old"))
    print("Unzipping Discord... ")
    subprocess.run(['tar', 'zxvfC', discord_net_data["filename"], os.path.expanduser("~/.local/share/")], check=True)
    print("Done")
print("Discord local version: ",end="")
discord_local = _get_local_data()
print(discord_local["version"])
print("Getting latest version number from server... ",end="")
discord_net_data = _get_net_data()
secs=0
while type(discord_net_data) == str:
    print("Internet Error,",str(secs)+"s,","trying again in 3 seconds")
    time.sleep(3)
    secs+=3
    discord_net_data = _get_net_data()
print(discord_net_data['version'])
if discord_net_data["version"]>discord_local["version"]:
    update_local(discord_local,discord_net_data)
quit(os.system(os.path.expanduser("~/.local/share/Discord/Discord")+" >/tmp/discord.log"))