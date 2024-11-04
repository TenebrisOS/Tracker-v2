import discord
import json
import os
from api import GetValorantStats, UpdateAgentData, UpdateMapsData
import ast

with open ("config.json") as js:
    config=json.load(js)

#region Var
TOKEN=config["TOKEN"]
intents=discord.Intents.all()
intents.message_content=True
client=discord.Client(intents=intents)
PREFIX="'"
#endregion

def ReadValorantJson(data):
    details=data["data"]
    level=details["account_level"]
    region=details["region"]
    cards=details["card"]
    img=cards["small"]
    print(level, region, img)
    return level, region, img

def GetHelp():
    mbdhelp = discord.Embed(title="Help")
    mbdhelp.add_field(name = "Prefix", value = "` ' `")
    mbdhelp.add_field(name = "Agents", value = "Description / abilities, etc about an agent. Usage : `<Prefix>Agent <agentname>`")
    mbdhelp.add_field(name = "Maps", value = "Basic infos about any map. Usage : `<prefix>map <mapname>`")
    mbdhelp.add_field(name = "Help ", value = "Get this page. Usage `<prefix>Help`")
    mbdhelp.add_field(name = "Valorant Stats", value = "Get your ranked stats. Usage `<prefix>val-stats <username>`")
    return mbdhelp

def GetMap(map):
    UpdateMapsData()
    try: 
        with open("data/maps.json", "r") as d:
            data=json.load(d)
            for info in data['data']:
                if info['displayName'] == map:
                    return info['displayIcon'], info['splash'], info['tacticalDescription']
    except:
        return 0

def GetAgent(agent):
    UpdateAgentData()
    try: 
        with open("data/agents.json", "r") as d:
            data=json.load(d)
            for info in data['data']:
                if info['displayName'] == agent:
                    return info['description'], info['displayIcon'], info['fullPortraitV2'], info['role']['displayName'], info['role']['displayIcon'], info['role']['description'], info['abilities']
                    
    except:
        return 0

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="your mom"))

@client.event
async def on_message(message:discord.Message):
    if message.author.bot or not(str(message.content).startswith(PREFIX)):
        return
    args = message.content.split(" ")
    args[0] = args[0][1::]
    print(args)
    if args[0] == "val-stats" :
        if len(args)==2:
            username=args[1]
        else:
            username=""
            for part in args[1::]:
                username+=part+" "

        print(username)

        data1, data2=GetValorantStats(username=username)
        mbd = discord.Embed(title=username)
        details=data1["data"]
        level=details["account_level"]
        region=details["region"]
        cards=details["card"]
        wide=cards["wide"]
        try:
            current_rank=(((data2["data"])["current"])["tier"])["name"]
            peak_rank=(((data2["data"])["peak"])["tier"])["name"]
            rankurl=(str(current_rank).replace(" ", "_")) + "_Rank.png"
            mbd.add_field(name = "Level", value = level)
            file = discord.File("rank_png/"+rankurl, filename="output.png")
            mbd.set_thumbnail(url="attachment://output.png")
            mbd.set_image(url=wide)
            mbd.add_field(name = "Region", value = region)
            mbd.add_field(name = "Current Rank", value = current_rank)
            mbd.add_field(name = "Peak Rank", value = peak_rank)
            await message.channel.send(embed=mbd, file=file)
        except:
            await message.channel.send("**"+username+"**"+" has not played any ranked match")
        return

    if args[0]=="map":
        try:
            icon, image, tact = GetMap(args[1])
            mbd=discord.Embed(title=args[1])
            mbd.add_field(name="Tactical Description", value=tact)
            mbd.set_image(url=image)
            mbd.set_thumbnail(url=icon)
            await message.channel.send(embed=mbd)
        except:
            await message.channel.send("**"+args[1]+"** is not a valorant map.")

    if args[0]=="agent":
        try:
            desc, icon, port, role, roleicon, roledesc, abilities = GetAgent(args[1])
            print(desc)
            mbd=discord.Embed(title=args[1])
            mbd.add_field(name="Description", value=desc)
            mbd.add_field(name=role, value=roledesc)
            mbd.set_image(url=port)
            for i in abilities:
                mbd.add_field(name=i['slot']+" "+i['displayName'], value=i['description'])
            mbd.set_thumbnail(url=roleicon)
            await message.channel.send(embed=mbd)
        except:
            await message.channel.send("**"+args[1]+"** is not a valorant agent.")
client.run(TOKEN)