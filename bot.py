import discord
import os
from bot_preferences import spam_channels
from bot_preferences import bot_token
from discord.ext import commands, tasks


client = commands.Bot(command_prefix = '!')


#HELP MENU CODE
client.remove_command('help')
@client.command(pass_context = True)
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name='HELP')
    embed.add_field(name='TEXT COMMANDS', value= '----------', inline=False)
    embed.add_field(name='!help', value= 'EX: "!help" returns this menu.', inline=False)
    embed.add_field(name='!set_console', value= 'EX: "!set_console channelname" set an existing channel for bot dumps.', inline=False)
    embed.add_field(name='!del_console', value= 'EX: "!del_console" remove the console.', inline=False)
    embed.add_field(name='!ping', value= 'EX: "!ping" returns the bot latency.', inline=False)
    embed.add_field(name='!game', value= 'EX: "!game text" sets game for Miss Jenny.', inline=False)
    embed.add_field(name='!say', value= 'EX: "!say text" sends message as Miss Jenny.', inline=False)
    embed.add_field(name='!react', value= 'EX: "!react x :emoji:" Miss Jenny will react to the x (integer) above message with your given emoji (includes animated emoji).', inline=False)
    embed.add_field(name='!clear', value= 'EX: "!clear x" clear the last x messages in your channel.', inline=False)
    embed.add_field(name='!define', value= 'EX: "!define text" returns urban dictionary definition.', inline=False)
    embed.add_field(name='!giphy', value= 'EX: "!giphy text" returns random giphy gif.', inline=False)
    embed.add_field(name='!rg', value= 'EX: "!rg text" returns a random redgif search result for given text.', inline=False)
    embed.add_field(name='VOICE COMMANDS', value= '----------', inline=False)
    embed.add_field(name='!tts', value= 'EX: "!tts text" Miss Jenny will join your voice channel and read your text message.', inline=False)
    embed.add_field(name='!lang', value= 'EX: "!lang it" Miss Jenny will set her TTS language on your server to the specified code (type "!lang help" for list).', inline=False)
    embed.add_field(name='!stop', value= 'EX: "!stop" Miss Jenny will be silenced and leave the voice channel.', inline=False)
    embed.add_field(name='!demons', value= 'EX: "!demons" Miss Jenny will play you the song of your people.', inline=False)
    await ctx.send(embed=embed)


#LOAD COMMAND
@client.command()
async def load(ctx, extension):
    await ctx.message.delete()
    client.load_extension(f'cogs.{extension}')
    print(f'cogs.{extension} Loaded.')
    message = f'I have loaded the {extension} cog.'
    if ctx.guild.id in spam_channels.keys():
        channel = spam_channels[ctx.guild.id]
        await channel.send(message)
    else:
        await ctx.send(str(message))


#UNLOAD COMMAND
@client.command()
async def unload(ctx, extension):
    await ctx.message.delete()
    client.unload_extension(f'cogs.{extension}')
    print(f'cogs.{extension} Unloaded.')
    message = f'I have unloaded the {extension} cog.'
    if ctx.guild.id in spam_channels.keys():
        channel = spam_channels[ctx.guild.id]
        await channel.send(message)
    else:
        await ctx.send(str(message))


#COGS LOAD ON STARTUP
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename} Loaded.')





#SET CONSOLE COMMAND
@client.command()
async def set_console(ctx, spam_channel):
    is_suc = "False"
    await ctx.message.delete()
    for channel in ctx.guild.channels:
        if channel.name == spam_channel:
            is_suc = "True"
            spam_channels.update({ctx.guild.id : channel})
            await channel.send("Successfully set up #" + str(channel.name) + " as my console.")
            with open("preferences.txt", 'w') as f:
                for server in spam_channels:
                    f.write(f'{server}:{channel.id}')
                    f.write("\n")
    if is_suc == "False":
        await ctx.send("I could not find the specified channel.")


#DELETE CONSOLE COMMAND
@client.command()
async def del_console(ctx):
    await ctx.message.delete()
    if ctx.guild.id in spam_channels.keys():
        element = spam_channels.pop(ctx.guild.id)
        with open("preferences.txt", "r+") as f:
            d = f.readlines()
            f.seak(0)
            for i in d:
                if int(i.split(':')[0]) != ctx.guild.id:
                    f.write(i)
            f.truncate()
        await ctx.send("Successfully removed #" + str(element) + " as my console.")
    else:
        await ctx.send("I could not find a console.")


#STARTUP EVENTS
@client.event
async def on_ready():
    #PREFERENCES LOAD ON STARTUP
    with open("preferences.txt", "r") as f:
        for line in f:
            server_get = line.split(':')
            channel = server_get[1].split('\n')
            channel_act = client.get_channel(int(channel[0]))
            spam_channels.update({int(server_get[0]):channel_act})
    print('Preferences.txt Loaded.')
    #SPLASH MESSAGE
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Global Thermonuclear War'))
    print("""
::::    :::: :::::::::::::::::::  ::::::::   :::::::::::::::::::::::::    :::::::    ::::::   :::
+:+:+: :+:+:+    :+:   :+:    :+::+:    :+:      :+:    :+:       :+:+:   :+::+:+:   :+::+:   :+:
+:+ +:+:+ +:+    +:+   +:+       +:+             +:+    +:+       :+:+:+  +:+:+:+:+  +:+ +:+ +:+
+#+  +:+  +#+    +#+   +#++:++#+++#++:++#++      +#+    +#++:++#  +#+ +:+ +#++#+ +:+ +#+  +#++:
+#+       +#+    +#+          +#+       +#+      +#+    +#+       +#+  +#+#+#+#+  +#+#+#   +#+
#+#       #+#    #+#   #+#    #+##+#    #+#  #+# #+#    #+#       #+#   #+#+##+#   #+#+#   #+#
###       ######################  ########    #####     #############    #######    ####   ###
version 0.73 updated 6/28/2020""")




client.run(bot_token)
