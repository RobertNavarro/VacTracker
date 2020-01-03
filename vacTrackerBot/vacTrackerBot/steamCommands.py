#import discord
import json
import requests
import steam
#from discord.ext import commands
from steam import SteamID
from steam import WebAPI
from steam.enums.emsg import EMsg



def getBanCount(url):
    response = requests.get(url=url, params=None)
    #json_data = json.loads(response.text)
    banCount = json.loads(response.text)['players'][0]['NumberOfVACBans']#requests returns a really                                                                               
    #print(banCount)                                                      #nasty dictionary of lists of dictionaries
    return banCount
   

def getSteamID(url):
    id = str(steam.steamid.steam64_from_url(url))
    return id