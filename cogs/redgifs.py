import discord
import json
import aiohttp
import random
import requests
from bot_preferences import spam_channels
from discord.ext import commands

class Redgifs(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Redgifs command required a more complicated structure than giphy because the site would return invalid URLs and cannot do a random search
    @commands.command()
    async def rg(self, ctx, *, search):
        await ctx.message.delete()
        if ctx.channel.is_nsfw():
            session = aiohttp.ClientSession()
            if search == '':
                return
            else:
                search.replace(' ', '+')
                response = await session.get(f'https://napi.redgifs.com/v1/gfycats/search?search_text={search}&count=25')
                data = json.loads(await response.text())
                grabbing_gif = True
                attempt_num = 0
                while grabbing_gif == True:
                    if attempt_num >= 10:
                        await session.close()
                        if ctx.guild.id in spam_channels.keys():
                            channel = spam_channels[ctx.guild.id]
                            await channel.send("Sorry, I couldn't find a gif.")
                        return
                    gif_choice = random.randint(0,20)
                    try:
                        link = (data['gfycats'][gif_choice]['mobileUrl'])
                        request = requests.get(link)
                        if request.status_code == 200:
                            grabbing_gif = False
                        else:
                            print(f"link doesn't work. Status code: {request.status_code}.")
                    except IndexError as e:
                        attempt_num += 1
                    except Exception as e:
                        print(e)
                        await session.close()
                        if ctx.guild.id in spam_channels.keys():
                            channel = spam_channels[ctx.guild.id]
                            await channel.send(f"Sorry, redgifs.com was unresponsive, please try again.")
                        return
                await session.close()
                await ctx.send(link)
                message = 'I found a redgif for ' + str(ctx.message.author.name) + ' using ***' + str(search) + '*** as a search!'
        else:
            message = "You must submit redgif request in a NSFW channel."
        if ctx.guild.id in spam_channels.keys():
            channel = spam_channels[ctx.guild.id]
            await channel.send(message)


def setup(client):
    client.add_cog(Redgifs(client))
