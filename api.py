import json
import requests 

with open ("config.json") as js:
    config=json.load(js)

val_api=config["VALORANT"]

def curl(mode, url, headers):
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
    with open('test.json', 'w') as f:
        json.dump(response.json(), f, indent=2)
    region=((response.json())["data"])["region"]
    response2=curl("GET", "https://api.henrikdev.xyz/valorant/v3/mmr/"+ region + "/pc/"+forurl,  {"Authorization" : val_api})
    with open('test2.json', 'w') as f2:
        json.dump(response2.json(), f2, indent=2)
    print(response2.json)
    return response.json(), response2.json()

def UpdateAgentData():
    response=curl("GET", "https://valorant-api.com/v1/agents", None)
    with open('data/agents.json', 'w') as f:
        #print(response.json())
        json.dump(response.json(), f, indent=2)
        return

def UpdateMapsData():
    response=curl("GET", "https://valorant-api.com/v1/maps", None)
    with open('data/maps.json', 'w') as f:
        #print(response.json())
        json.dump(response.json(), f, indent=2)
        return