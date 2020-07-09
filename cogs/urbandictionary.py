import discord
import urbandictionary as ud
import json
from urbandictionary import define
from bot_preferences import spam_channels
from discord.ext import commands


class urbandictionary(commands.Cog):

    def __init__(self, client):
        self.client = client

    #The define command uses the Urban Dictionary python library to return a definition and example for a search.
    @commands.command()
    async def define(self, ctx, *search):
        await ctx.message.delete()
        wurd = ' '.join(search)
        wurd.replace(',','')
        #If no word is given, it will return a random search.
        if wurd == '':
            rand = ud.random()
            w_definition = f"""\n>>> **{rand[0].word}**\n\nDefinition:\n```{rand[0].definition}``` \nExample:\n```{rand[0].example}```\n⬆️ {rand[0].upvotes}     ⬇️ {rand[0].downvotes}\n"""
            await ctx.send(w_definition)
        #If there is something to search for it will try to find it
        else:
            rand = ud.define(str(wurd))
            if not rand:
                print("list is empty")
            w_definition = f"""\n>>> **{rand[0].word}**\n\nDefinition:\n```{rand[0].definition}``` \nExample:\n```{rand[0].example}```\n⬆️ {rand[0].upvotes}     ⬇️ {rand[0].downvotes}\n"""
            await ctx.send(w_definition)
        message = message = 'I found an urban definition for ' + str(ctx.message.author.name) + ' using ***' + str(wurd) + '*** as a search!'
        if ctx.guild.id in spam_channels.keys():
            channel = spam_channels[ctx.guild.id]
            await channel.send(message)



def setup(client):
    client.add_cog(urbandictionary(client))
