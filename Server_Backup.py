
import os
import discord
from discord.ext import commands
import time #<- manage the file dumps
import asyncio
from dep import strManip
from dep import csLogger
from dep import dapiWrapper
from core import dataHandler

global save_data
save_data = []













def save_all_data_to_file(data, message = None):
    def file_dump(contents_as_list, explicit_file_path):
        file = open(explicit_file_path, 'a+', encoding='utf8') # <-- not sure if w+ is elevated enough
            
        for mess in contents_as_list:
            file.write(str(mess) + '\n')#IMPORTANT<<< UTF-8 ERROR
        file.close()

    #save to C:\Users\Chase\source\repos\Server Backup\dumps \?
    import os
    # use server id's in place of server names in file system

    dirname = r'C:\Users\Chase\source\repos\Server Backup\dumps'
    files = os.listdir(dirname)
    #print(files)

    for server in data:
        server_name = server[0] # <-- encode here
        if server_name in files:
            print('directory found')
            #server already has a file directory
            for channel in server[3]:
                #bug in logging where only one channel is stored
                #print(channel[0])
                path2 = os.path.join(dirname, server_name)
                known_channels = os.listdir(path2) # <- outputs known channels
                #print(known_channels) #Remove
                if channel[0] in known_channels:
                    #channel already known
                    path3 = os.path.join(path2, channel[0])
                    #print(path3)
                    name = str(time.time())
                    path3 = path3 + "\\" + name + '.txt'
                    file_dump(channel[1], path3) # <-- i dont trust this with anything
                    print('file dumped')
                    #

                    pass
                else:
                    #create new channel folder
                    path3 = os.path.join(path2, channel[0])
                    os.mkdir(path3)

                    # use this block to dump into a file in folder path 3
                    #copy save_player_data from neeko bot so i can use readlines
                    #DO NOT encode when dumping to file, thats unneccessary complexity, use utf-8 encoding on both ends
                    #print(path3)
                    name = str(time.time())
                    path3 = path3 + "\\" + name + '.txt'
                    file_dump(channel[1], path3) # <-- i dont trust this with anything
                    #print('file dumped')
                    #
                    pass
                
                channel_name = channel[0]
                for message in channel[1]:
                    print(';', message)


            pass
        else:
            #server needs a file directory
            path = os.path.join(dirname, server_name) # <-- might have to add a backslash to the end of parent directory
            os.mkdir(path)
            print('new directory created')

            with open(os.path.join(path, 'metadata.txt'), 'w+') as file: #METADATA
                fileData = file.read()
                print(fileData, type(fileData), 'fileFormattingMetadata')

                file.write("METADATA:\n")
                file.write(server_name) #make token the server ID
                file.close()
                pass

            #copy code from other function
            for channel in server[3]:
                #bug in logging where only one channel is stored
                print(channel[0])
                path2 = os.path.join(dirname, server_name)
                known_channels = os.listdir(path2) # <- outputs known channels
                print(known_channels) #Remove
                if channel[0] in known_channels:
                    #channel already known
                    path3 = os.path.join(path2, channel[0])
                    print(path3)
                    name = str(time.time())
                    path3 = path3 + "\\" + name + '.txt'
                    file_dump(channel[1], path3) # <-- i dont trust this with anything
                    print('file dumped')
                    #

                    pass
                else:
                    #create new channel folder
                    path3 = os.path.join(path2, channel[0])
                    os.mkdir(path3)

                    # use this block to dump into a file in folder path 3
                    #copy save_player_data from neeko bot so i can use readlines
                    #DO NOT encode when dumping to file, thats unneccessary complexity, use utf-8 encoding on both ends
                    print(path3)
                    name = str(time.time())
                    path3 = path3 + "\\" + name + '.txt'
                    file_dump(channel[1], path3) # <-- i dont trust this with anything
                    #print('file dumped')
                    #
                    pass
                
                channel_name = channel[0]
                for message in channel[1]:
                    print(';', message)





            #dump data to file

            #for emoji channel names, just encode them so i dont have to worry about ids

            


            pass
        pass
    i = 0
    for server in data: # empties all channels
        data[i][3] = []
        i += 1
    return(data) # <-- empties all message buffers before return

def empty_memory_buffer(data):
    i = 0
    for server in data: # empties all channels
        data[i][3] = []
        i += 1
    return(data)



    




def process(client, message):
    #print(message.author.avatar_url)
    return()

global globalPath
globalPath = r'C:\Users\Chase\source\repos\Server Backup\dumps'

Intents=intents=discord.Intents.all()

client=commands.Bot(command_prefix='!',intents=intents)
#client = discord.AutoShardedClient(shard_count=10) if i ever need to load balance, use a socket to match important data every x seconds in on_ready
#only globals need to be matched to global matching in on_ready would solve many issues caused by sharding

@client.event
async def on_ready():

    print(f'{client.user.name} has connected to Discord!') #i hate Fstrings
    global save_data
    i = 0
    while True:
        try:
            ##
            #print('changing status')
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(str("reading"))))#?.listening
            #i dont know why status is unaffected, my best idea is that it might be an intents issue
            await asyncio.sleep(30) #keep status loop at 60 seconds
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(str("writing"))))#?.listening
            await asyncio.sleep(30)

        except Exception as error:
            await dapiWrapper.phone_home(client, error, "status script")

        if i >= 60:
            i = 0
            try:
                print("attemping autosave")

                save_data = save_all_data_to_file(save_data)
            
                save_data = empty_memory_buffer(save_data)

            except Exception as error:
                print(error)
                await dapiWrapper.phone_home(client, error, "autosave failed")
        #remaining storage check, phone home if low
        try:
            ##
            pass
        except Exception as error:
            print(error)
            await dapiWrapper.phone_home(client, error, "storage check")
        i += 1



@client.event
async def on_message(message): #rebuild client
    
    #Ignore IDS
    if str(message.author) == "Neeko Bot#8935":
        print("function exited due to bot detection")
        #return() does not return cause i dont expect collisions

    #

    process(client, message)

    if str(message.author) == "Save Slot#7493":
        return()

    global save_data
    if '!dump' in message.content.lower():
        if str(message.author) == "Fushi_#6228":
            save_data = save_all_data_to_file(save_data, message)

            #log_players(data) ## might have to generate data outside of function <<

            save_data = empty_memory_buffer(save_data)

            #METADATA << metadata save function call
            return()

    ##
    #Front end code
    if "!ver" in message.content.lower():
        await message.channel.send("***Save Slot BETA 0.2\n   -Fushi_#6228***")
        pass

    if '!save help' in message.content.lower():
        if 'privacy' in message.content.lower():
            await message.channel.send("Uhhhhhh, we wont spy on you (add proper response)")
        elif 'contact' in message.content.lower():
            await message.channel.send("***For more information please DM Fushi_#6228***")
        elif 'backup' in message.content.lower():
            await message.channel.send("yeah we do those")
        elif 'rebuild' in message.content.lower():
            await message.channel.send("those too")
        elif "credit" in message.content.lower():
            await message.channel.send("***pfp: unknown\ndev: Fushi_#6228***")
        elif "donate" in message.content.lower():
            await message.channel.send("why?")
        else:
            #else clause
            await message.channel.send("***For more information, type\n !Save slot help <topic>\n -Privacy policy\n -Contacts \n -Backups\n -Rebuilds\n -Credits\n -Donate***")

    ##--------------------##


    early_content = str(message.content)
    try:
       url = message.attachments[0].url
       if url[0:26] == 'https://cdn.discordapp.com':
           #await message.channel.send(url)
           #print(url)
           early_content = early_content + url
    except:
        pass #<- no attatchment


    print('logging client active')
    save_data, is_new_server, rebuild_token = dataHandler.client_sort(save_data, str(message.guild), str(message.channel), early_content, str(message.author), str(message.guild.id), str(message.author.avatar_url)) #<- message.guild should take ID
    try:
        size = 0
        for server in save_data:
            size += len(server[3])

        print("Messages Chached: " + str(size))
    except:
        print("error counting cached messages")

    if is_new_server:
        #check for known in line here
        knownServerIDS = os.listdir(r'C:\Users\Chase\source\repos\Server Backup\dumps')
        if str(message.guild.id) not in knownServerIDS:
            
            await message.channel.send('***Thank you for adding save slot to your server, hence forth all the messages in the server will be stored on our servers, if you ever need to rebuild your server, you can use the token following with the command !server rebuild <token> if you wish for your data to be deleted please kick the bot from your server and message Fushi_#6228***')
            await message.channel.send(rebuild_token)
        else:
            print('frontend intro exempted or new server')
    
   

    print('rebuild client active')
    if str(message.author) == 'Fushi_#6228':
        #print(message.channel.id)

        if '!create text channel' in message.content.lower():
            await message.guild.create_text_channel('Temporary channel name')
            await message.channel.send('created text channel')
            return()
        if '!create voice channel' in message.content.lower():
            await message.guild.create_voice_channel('Temporary channel name')
            await message.channel.send('created voice channel')
            return()

    if '!specific channel test' in message.content.lower():
        channelid = '917502376607363072' ## <-- 
        channel = discord.utils.get(message.guild.channels, name="temporary-channel-name")
        await channel.send("Awww fuck yajjjj")
    if '!rebuild channel' in message.content.lower():
        pass # <-- start with channel rebuilding and then for loop that mf to guilds

    if '!server rebuild' in message.content.lower():
        ##


        if "save slot" in str(message.author).lower():
            return()

        args = strManip.string_to_args(message.content) #args
        delay = 0.5
        if "-slowbuild" in args:
            delay = 2

        

        ##grab token from input
        ##loop through saved servers and check server puuid (file name)

        token = message.content.split()[2]

        print(token)
        await message.channel.send("***verifying token***") #handle for perm errors URGENT


        dirname = r'C:\Users\Chase\source\repos\Server Backup\dumps'
        files22 = os.listdir(dirname)

        searchDirectory = None

        for serverDir in files22:
            if serverDir == token:
                ##
                searchDirectory = os.path.join(r'C:\Users\Chase\source\repos\Server Backup\dumps', token)
                
                pass

        if not searchDirectory:
            await message.channel.send("***invalid token, contact Fushi_#6228 for more details***")
            return()

        await message.channel.send("***token verified\n Server Rebuild can take several hours\n If the rebuild stops while incomplete please make sure the bot has Administrator Privleges\n If you encounter persistant errors please message Fushi_#6228***")

        ##here is the accual rebuild code
        ##
        channels = os.listdir(searchDirectory)
        #for channel in dir
        for channelID in channels:
            if str(channelID) == "metadata.txt": #excludes metadata

                continue ##?

            channel = await message.guild.create_text_channel(str(channelID))
            await channel.send("***This Channel was rebuilt from a backup using save slot, contact Fushi_#6228 for more details\n-------------------------***")

            lastUser = None
            for logFile in os.listdir(os.path.join(searchDirectory, str(channelID))):
                ##
                rMessages = strManip.loadChannelAsArray(token, channelID, logFile) #
                for iMessage in rMessages:
                    iMessage2 = eval(iMessage)
                    if "-noprofanity" in args:
                        iMessage2[1] = strManip.removeArrayFromString(strManip.importJson("profanities.json"), iMessage2[1])
                    if "-compact" not in args:
                        await asyncio.sleep(delay)
                        if lastUser != iMessage2[2]: #or time dif > 1 hour
                            lastUser = iMessage2[2]
                            await channel.send(iMessage2[2])
                            await asyncio.sleep(delay)
                            await channel.send("***[" + iMessage2[0] + "]***_ Today at 12AM _")
                        try:
                            await channel.send(iMessage2[1])
                        except:
                            pass
                    else:
                        await asyncio.sleep(delay)
                        await channel.send("***[" + iMessage2[0] + "]:*** " + iMessage2[1])


            #create channel
            #loop through files
            #loop though messages

        pass



    ####im going to the bathroom

#main channel id is 407994638692253698
#new channel id is 917502376607363072 <----

client.run(open('key.txt', 'r+').readlines()[0])


#get bitsize of cache, if greater than x, dump
    #run check on each message
#encrypt attatchments with key and save them in an attatchments file, name each file with the random ID
    #random ID is stored in message instead of adding attatchments to the end of the message like i do now

#so i need
    #function to download file
        #download_file(id, attatchment_link, attatchment_file_path):
            
            #i want this to return file in memory

            #return(file, success, error_code = None)
        
        #encrypt_file(file, key): <<< probly integrate into download file but allow calling anywhere in the program
            #return(encrypted_file)

        #save_file(file, id):
            #return(success, error_code = None)


    #re_invite_past_users
        #log_players(guild_id, puuid):
            #return(success, error_code = None)

        #find_logged_puuids(guild_id):
            #return(users)

        #find_logged_puuids_from_key(key):
            #return(users)

        #invite(users, new_guild_id):
            #return(success, error_code = None)
            


#--

#use the log of users to re-invite all players who were in the original server, use not just my own logs
#but also a get_users function preiodically to update user base

#add a function that allows users to remove their data on request, this is where a user ID would be userful
#so that your data cannot be deleted on your bahalf by another user, 

#for segmentation store messages in files by day, dumping data to a text file at midnight, the file heirarchy would
#be something like the following, while attatchments are sorted by month and labeled with time.time
#
#Guild
#!-->channel
#!  !-->march 1st
#!  !-->march 2nd
#!-->channel2
#!  !-->june 12th
#!-->attatchments
#!  !-->June
#Guild2
#
##--

#only date messages down to month and year
#i will worry about message dating later



#https://discord.com/oauth2/authorize?client_id=917552319770550332&scope=bot