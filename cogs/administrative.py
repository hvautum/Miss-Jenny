import discord
from bot_preferences import spam_channels
from discord.ext import commands

class Administrative(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def ping(self, ctx):
        await ctx.message.delete()
        message = f'Pong! {round(self.client.latency * 1000)}ms'
        if ctx.guild.id in spam_channels.keys():
            channel = spam_channels[ctx.guild.id]
            await channel.send(message)
        else:
            await ctx.send(str(message))

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def game(self, ctx, *, message):
        await ctx.message.delete()
        await self.client.change_presence(status=None, activity=discord.Game(message))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.message.delete()
        if amount > 20:
            amount = 20
        try:
            await ctx.channel.purge(limit=amount)
            if amount==1:
                message = f'{amount} message cleared in {ctx.channel.name}.'
            else:
                message = f'{amount} messages cleared in {ctx.channel.name}.'
            if ctx.guild.id in spam_channels.keys():
                channel = spam_channels[ctx.guild.id]
                await channel.send(message)
        except Exception as e:
            print(str(e))


    @commands.command()
    async def react(self, ctx, num_above, emoji_in):
        await ctx.message.delete()
        if not num_above:
            num = 1
        if int(num_above) > 49:
            num = 1
        else:
            num = int(num_above)
        j = 0
        async for message in ctx.channel.history(limit =50):
            j +=1
            if j == num:
                mess = message
                break
        try:
            name = emoji_in.split(':')
            emoji = discord.utils.get(ctx.guild.emojis, name=name[1])
        except:
            emoji = emoji_in
        if emoji:
            try:
                await mess.add_reaction(emoji)
            except Exception as e:
                print(str(e))



def setup(client):
    client.add_cog(Administrative(client))
