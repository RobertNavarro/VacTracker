import discord
from discord.ext import commands
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("---disable-gpu")
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path='./chromeDriver/chromedriver.exe')
import os

client = commands.Bot(command_prefix = '!')
@client.event
async def on_ready():
    print('The bot is ready to be used.')

client.run('NjU3MzY0MTIwMzkxMTIyOTQ1.XfwIew.TalwSs3MIWWLhskzaRGZuwFEo5A')

def findProfile(profileUrl, textFile):
    isFound = False
    for line in textFile:
        if line.strip('\n ') == profileUrl: 
            isFound = True
            return isFound
    return isFound

def compareBanVal(profileUrl,profileDictionary):
    if profileDictionary.get(profileUrl) == getBanCount(profileUrl):
        #print("they match")
        return False
    return True

def addProfile(profileUrl, textFile):
    profileUrl+='\n'
    textFile.write(profileUrl)

def addNotBanned(profileUrl, textFile,  profileDictionary):
    banCount = getBanCount(profileUrl)
    profileDictionary[profileUrl] = banCount
    profileUrl = profileUrl + " " + banCount +'\n'
    textFile.write(profileUrl)

def getBanCount(profileUrl):
    driver.get(profileUrl)
    try:
        banCount = driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div[2]/div').text
        banCount = banCount[0]
    except NoSuchElementException as exception:
        banCount = "0"
        return banCount
    return banCount

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

def main():
    profileDictionary = {}
    #notBannedList = open("notBanned.txt","r")
    createDictionary(profileDictionary, "notBanned.txt")
    #print (profileDictionary)
    userOption = input("Hello, please choose an input:\na - add new user\ns - scan your tracked players\ne - exit program\n")
    while userOption is not "e":
        if userOption == "a":
            url = input("Please paste in a steam url to track a new user: ")
            #print(url)
            masterList = open("masterList.txt","r")
            containsMatch = findProfile(url, masterList)
            if containsMatch is not True:
               masterList = open("masterList.txt","a")
               notBannedList = open("notBanned.txt","a")
               addProfile(url, masterList)
               addNotBanned(url, notBannedList, profileDictionary)
               print("The player is now being tracked!")
               masterList.close()
               notBannedList.close()
            else:
                print("The player you tried to add is already being tracked.")
        if userOption == "s":
            updatedList = False
            notBannedListRead = open("notBanned.txt","r+")
            notBannedListWrite = open("notBannedTemp.txt","w+")
            bannedList = open("banned.txt","a")
            for line in notBannedListRead:
                tempKey = line.strip('\n ')
                #tempKey = tempKey[0:len(tempKey)-3]
                (key, val) = line.split()
                #print("it is comparing: " + key)
                if compareBanVal(key, profileDictionary) is True: #only true if the previous amount of bans doesnt match current
                    print("One or more of your tracked users has been banned. Please check your ban file")
                    addProfile(tempKey[0:len(tempKey)-2], bannedList)
                    del profileDictionary[tempKey[0:len(tempKey)-2]]
                    #print(profileDictionary)
                    updatedList = True
            rewriteNotBanned(profileDictionary,notBannedListWrite)
            if updatedList == False:
                print("Looks like nobody you are tracking has been banned.")
            bannedList.close()
            notBannedListRead.close()
            notBannedListWrite.close()
            os.replace("notBannedTemp.txt", "notBanned.txt")
        userOption = input("Hello, please choose an input:\na - add new user\ns - scan your tracked players\ne - exit program\n")
main()