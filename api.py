import json
import requests 

with open ("config.json") as js:
    config=json.load(js)

val_api=config["VALORANT"]

def curl(mode, url, headers):
    # data = {username : highscore}
    try:
        if mode=='GET':
            response = requests.get(url, headers=headers)
            return response
        elif mode=="POST":
            response=requests.post(url)
            return response
    except requests.exceptions.RequestException as e:
        return 'server offline'

def GetValorantStats(username):
    forurl=str(username).replace('#', '/')
    response=curl("GET", "https://api.henrikdev.xyz/valorant/v1/account/"+ forurl, {"Authorization" : val_api})
    region=((response.json())["data"])["region"]
    response2=curl("GET", "https://api.henrikdev.xyz/valorant/v3/mmr/"+ region + "/pc/"+forurl,  {"Authorization" : val_api})
    return response.json(), response2.json()

