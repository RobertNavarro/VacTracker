from steamCommands import *
import discord
from discord.ext import commands
import os


def getDiscordKey():
     keyFile = open("keys.gitignore","r")
     lines = keyFile.readlines()
     discordKey = lines[0].strip('\n')
     keyFile.close()
     return discordKey
def getsteamAPIKey():
     keyFile = open("keys.gitignore","r")
     lines = keyFile.readlines()
     steamAPIKey = lines[1].strip('\n')
     keyFile.close()
     return steamAPIKey
discordKey = getDiscordKey()
steamAPIKey = getsteamAPIKey()

client = commands.Bot(command_prefix = '!')
@client.event
async def on_ready():
    print('The bot is ready to be used.')
    getSteamID('https://steamcommunity.com/id/unboundchaos/')


def findProfile(profileID, textFile):
    isFound = False
    for line in textFile:
        if line.strip('\n ') == profileID: 
            isFound = True
            return isFound
    return isFound

def compareBanVal(profileID,profileDictionary):
    jsonURL = 'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=8FFF2A64C0C2BFADC1E45F3C4F92805E&steamids=' + profileID
    banCount = str(getBanCount(jsonURL))
    if str(profileDictionary.get(profileID)) == banCount:
        print("banCount: " + banCount + " matches the dictionary val: " + profileDictionary.get(profileID))
        return False
    print("banCount: " + banCount + " DOES NOT MATCH the dictionary val: " + profileDictionary.get(profileID))
    return True

def addProfile(profileUrl, textFile):
    steamUserID = str(getSteamID(profileUrl))
    steamUserID+='\n'
    textFile.write(steamUserID)

def addBannedProfile(profileID, textFile):
    steamProfile = str('http://steamcommunity.com/profiles/'+profileID+'\n')
    textFile.write(steamProfile)

def addNotBanned(profileID, textFile,  profileDictionary):
    jsonURL = 'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key='+steamAPIKey+'&steamids='
    jsonURL += profileID
    banCount = str(getBanCount(jsonURL))
    profileDictionary[profileID] = banCount
    profileID = profileID + " " + banCount +'\n'
    textFile.write(profileID)


def createDictionary(dict, textFile):
    with open(textFile) as f:
        for line in f:
            (key, val) = line.split()
            dict[key] = val

def rewriteNotBanned(dict, textFile):
    textFile.truncate(0)
    for key,val in dict.items():
        #print("the key is:" + key)
        textFile.write(key + " " + val + '\n')

profileDictionary = {}
createDictionary(profileDictionary, "notBanned.txt")

@client.command()
async def add(ctx, url):
    masterList = open("masterList.txt","r")
    containsMatch = findProfile(getSteamID(url), masterList)
    if containsMatch is not True:
        masterList = open("masterList.txt","a")
        notBannedList = open("notBanned.txt","a")
        addProfile(url, masterList)
        addNotBanned(getSteamID(url), notBannedList, profileDictionary)
        masterList.close()
        notBannedList.close()
        await ctx.send('Added a new player to the tracking list!')
    else:
          await ctx.send('The player you tried to add is already being tracked.')

@client.command()
async def scan(ctx):
    updatedList = False
    notBannedListRead = open("notBanned.txt","r+")
    notBannedListWrite = open("notBannedTemp.txt","w+")
    bannedList = open("banned.txt","a")
    for line in notBannedListRead:
        tempKey = line.strip('\n ')
        (key, val) = line.split()
        #print("the val is " + val)
        #print("the dict value is " + profileDictionary.get(key))
        if compareBanVal(key, profileDictionary) is True: #only true if the previous amount of bans doesnt match current
            await ctx.send("It looks like a there has been a ban! Do !r to request the ban file.")
            #print(tempKey[0:len(tempKey)-2])
            addBannedProfile(tempKey[0:len(tempKey)-2], bannedList)
            del profileDictionary[tempKey[0:len(tempKey)-2]]
            updatedList = True
    rewriteNotBanned(profileDictionary,notBannedListWrite)
    if updatedList == False:
        await ctx.send("Looks like nobody has been banned.")
    bannedList.close()
    notBannedListRead.close()
    notBannedListWrite.close()
    os.replace("notBannedTemp.txt", "notBanned.txt")

@client.command()
async def r(ctx):
    await ctx.send("Here is the text file containing all banned players:")
    await ctx.send(file=discord.File('banned.txt'))

   

#steamCommands.main()
client.run(discordKey)