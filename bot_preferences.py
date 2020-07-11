import discord
import os

spam_channels = {}

bot_token = os.environ.get("BOT_TOKEN")
bot_ID = int(os.environ.get("BOT_ID"))
giphy_api_key = os.environ.get("GIPHY_API_KEY")


async def upd_console(ctx, message):
    if ctx.guild.id in spam_channels.keys():
        channel = spam_channels[ctx.guild.id]
        await channel.send(message)
    else:
        await ctx.send(str(message))
