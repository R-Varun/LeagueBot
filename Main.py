import discord
import asyncio

import json
import RiotRequests
import distance

from config import Constants

ID_LOOKUP_CACHE = {}

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    #censorship
    if censor(message.content):
        client.send_message(message.channel, "please restrain yourself using racial slurs/ curse words")

    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith('!lookup '):
        data = RiotRequests.find_summoner_id(message.content[8:])
        sumID = None
        summoner_name = None
        if data[0] != 200:
            await client.send_message(message.channel, "Trouble finding Summoner or rate limited!")
            return
        else:
            sumID = data[1]['id']
            summoner_name = data[1]['name']

        sumData = RiotRequests.lookup_summoner_id(sumID)
        tier = "Unknown"
        division = "?"
        if sumData[0] != 200:
            await client.send_message(message.channel, "Rate Limit was exceeded. Wait and try again")
        else:
            tier = sumData[1]['tier']
            division = str(sumData[1]['division'])
            win_loss = str(sumData[1]['wins']) + "/" + str(sumData[1]['losses'])


        messageStr = "**Summoner Name** *{}*\n**Queue** Ranked Solo/Duo\n**Tier** {} {}\n**W/L** {}"
        await client.send_message(message.channel, messageStr.format(summoner_name, tier, division, win_loss))
        await client.send_message(message.channel, json.dumps(sumData[2], indent=4))



@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to the server!'
    await client.send_message(server, fmt.format(member))

def format_sum_id(aString):
    retString = "";
    for char in aString:
        if char != " ":
            retString += char
    return retString.lower()


#returns an tuple of (status_code, data)


def censor(aString):
    for word in aString.split(" "):
        for bannedword in Constants.getBannedWords():
            if distance.jaccard(word, bannedword) < 0.1:
                return True

    return False

client.run('MjU5ODg2MDM0ODAyNzA0Mzg2.CzeaLQ.7Ud9L_Cd9fSmloJ8ugBPiAYx_ho')