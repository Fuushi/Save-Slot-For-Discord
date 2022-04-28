class dataHandler(object):

    def client_sort(data, Mguild, Mchannel, Mcontent, Mauthor, MguildID, attatchment_id = None):
        attatchment_id = attatchment_id.replace("size=1024", "size=32")
        #print(data, Mguild, Mchannel, Mcontent, MguildID)
        print('-_-_-')
        #data data and adds to the array
        #[guilds]
        #[guild_id, guild_name, guild_token, [chanels]]
        #[channel_name, messages] # <- when message list goes over ~1000 items it archives it to save on recourses
        #[authors_name, message, attatchment_id]
        #attachment_id = first ~20 charachters of the hash
        #format _> [[guild_id, guild_name, channels->[channel_name, message->[]]], [guild2]]

        #maybe run a computer vision algorithm on attatchments to reject anything sus
            #instantly reject anything with a sus filename, notify user with a self deleting message gey
    

        #first im going to want to check if the server is in the data list, if not notify users that future messages will be logged
        #unless opted out, do not log first message
        found = False
        rebuild_token = None
        guild_index = 0
        i = 0
        for server in data:
            if server[0] == MguildID:
                server_data = server
                found = True
                guild_index = i
            i += 1

        if not found:
            print('it wasnt found')
            #add server to list
            rebuild_token = 'arbitrary stuff' # <- make this random
        
            data.append([MguildID, Mguild, rebuild_token, [[Mchannel, [[Mauthor, Mcontent, attatchment_id]]]]])  #<- does log first comment
        ### if this runs it found server
        else:
            found_channel = False
            channel_index = 0
            i = 0
            for channel in server[3]:
                #print(channel, server[3], '---------------------------')
                #print(Mchannel, channel[0], '[][]][][][][][]][][[][][]][')
                if Mchannel == channel[0]:
                    found_channel = True
                    print('channel aleady exists') #< this always returns true for some reason
                    channel_index = i 
                i += 1
            if found_channel:
                #print(data[guild_index][3])
                data[guild_index][3][channel_index][1].append([Mauthor, Mcontent, attatchment_id])
                #add message to channel
                pass
            else:
                #add channel to list
                data[guild_index][3].append([Mchannel, [[Mauthor, Mcontent, attatchment_id]]]) #might need to adjust []
                pass
        is_new_server = not found
        return(data, is_new_server, rebuild_token)




