import discord
import json
import aiohttp
import random
from bot_preferences import spam_channels
from discord.ext import commands

class Giphy(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def giphy(self, ctx, *, search):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.blue())
        session = aiohttp.ClientSession()

        if search == '':
            response = await session.get('https://giphy.com/v1/gifs/random?api_key="API_KEY_GOES_HERE"')
            data = json.loads(await response.text())
            embed.set_image(url=data['data']['images']['original']['url'])
        else:
            search.replace(' ', '+')
            response = await session.get('https://api.giphy.com/v1/gifs/search?q=' + search + '&api_key="API_KEY_GOES_HERE"&limit=10')
            data = json.loads(await response.text())
            gif_choice = random.randint(0,9)
            embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

        await session.close()


        await ctx.send(embed=embed)
        message = 'I found a gif for ' + str(ctx.message.author.name) + ' using ***' + str(search) + '*** as a search!'
        if ctx.guild.id in spam_channels.keys():
            channel = spam_channels[ctx.guild.id]
            await channel.send(message)



def setup(client):
    client.add_cog(Giphy(client))
