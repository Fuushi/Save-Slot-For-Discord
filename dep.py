class dapiWrapper(object):
    #dapiWrapper.phone_home
    async def phone_home(client, errorMessage, locationTag): #
        user = client.get_user(355951979429625862)
        await user.send("--\nPhone home\n" + str(locationTag) + "\nAn error has occured with status:\n" + str(errorMessage))
    

class strManip(object):

    def importJson(name): #name includes file type
        #profanities.json
        import json
        ##
        #open file
        file = open(name) ##utf-8 if it causes problems
        rList = []
        for item in file:
            item2 = item[3:]
            item2 = item2[:(len(item2) - 3)]
            print(item2, type(item2), len(item2))
            rList.append(item2)
        print(len(rList))
        return(rList)

    

    def removeArrayFromString(array, string):
        def aster(num):
            string = ''
            for i in range(num):
                string += '*'
            return(string)
        ##
        #
        for item in array:
            if item in string:
                print('profanity found')
                print(item)
                string = string.replace(item, aster(len(item)))

        return(string)

    def loadChannelAsArray(guildID, channelID, logID):
        path = os.path.join(os.path.join(os.path.join(r'C:\Users\Chase\source\repos\Server Backup\dumps', guildID), channelID), logID)

        f = open(path, "r", encoding='utf8') #might have to add .txt manually
        readlines = f.readlines() #<- carefull that this isnt just a memory address to an object
        f.close() #

        return(readlines) #FUCKS
    
    def string_to_args(string):
        ##
        args = string.split()

        return(args)



class csLogger(object):

    def userLog():
        ##
        #

        return()

    def serverLog():
        ##
        #

        return()

class template(object):
    pass