import discord
import json
import os
from api import GetValorantStats, UpdateAgentData

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
    #mbdhelp.add_field(name = "Informations About Agents :)", value = "Get any information / description / abilities, etc about an agent. Usage : `<Prefix> Agent <Agent Name>`")
    #mbdhelp.add_field(name = "Informations About Maps :)", value = "Get infos about any map. Usage : `<Prefix> Graph / Persp <Map>`")
    mbdhelp.add_field(name = "Help :)", value = "Get this page. Usage `<Prefix> Help`")
    mbdhelp.add_field(name = "Valorant Stats", value = "Get your ranked stats. Usage `<Prefix>val-stats <yourfullname>`")
    return mbdhelp

def GetMap(map):
#    desc, img, graph=GetMapData(map)
#    mbd=discord.Embed(title=map)
#    mbd.add_field(name="Description", value=desc)
#    mbd.set_thumbnail(url=img)
#    mbd.set_image(url=graph)
    return

def GetAgent(agent):
    UpdateAgentData()
    with open("data/agents.json", "r") as d:
        data=json.load(d)
        for info in data['data']:
            if info['displayName'] == agent:
                return info['description'], info['displayIcon'], info['fullPortraitV2']
    return

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
        data1, data2=GetValorantStats(username=args[1])
        mbd = discord.Embed(title=args[1])
        details=data1["data"]
        level=details["account_level"]
        region=details["region"]
        cards=details["card"]
        wide=cards["wide"]
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
        return

    if args[0]=="map":
        mbd=GetMap(args[1])
        await message.channel.send(embed=mbd)

    if args[0]=="agent":
        desc, icon, port =GetAgent(args[1])
        print(desc)
        mbd=discord.Embed(title=args[1])
        mbd.add_field(name="Description", value=desc)
        mbd.set_image(url=port)
        mbd.set_thumbnail(url=icon)
        await message.channel.send(embed=mbd)
    
client.run(TOKEN)