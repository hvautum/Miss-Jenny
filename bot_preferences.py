import discord

spam_channels = {}
bot_token = 'TOKEN GOES HERE'
bot_ID = BOT ID GOES HERE


async def upd_console(ctx, message):
    if ctx.guild.id in spam_channels.keys():
        channel = spam_channels[ctx.guild.id]
        await channel.send(message)
    else:
        await ctx.send(str(message))
