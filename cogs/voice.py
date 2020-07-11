import discord
import os
import time
import playsound
import shutil
import asyncio
import random
from gtts import gTTS
from discord.ext import commands
from discord.utils import get
from bot_preferences import spam_channels
from bot_preferences import bot_ID


thoughts = {}
channels = {}
on_cooldown = {}
accessing_thoughts = {}
bot_language = {}
avail_languages = {
        'zh-cn': 'Chinese (Mandarin/China)',
        'zh-tw': 'Chinese (Mandarin/Taiwan)',
        'en-GB': 'English (UK)',
        'en-AU': 'English (Australia)',
        'en-US': 'English (US)',
        'en-nz': 'English (New Zealand)',
        'en-ng': 'English (Nigeria)',
        'en-ph': 'English (Philippines)',
        'es-es': 'Spanish (spain)',
        'es-us': 'Spanish (US)',
        'pt-BR': 'Portuguese (Brasil)',
        'pt': 'Portuguese (Portugal)',
        'ar': 'Arabic',
        'bn': 'Bengali',
        'cs': 'Czech',
        'da': 'Danish',
        'nl': 'Dutch',
        'fi': 'Finnish',
        'fr': 'French',
        'de': 'German',
        'el': 'Greek',
        'hu': 'Hungarian',
        'id': 'indonesian',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'no': 'Norwegian',
        'ru': 'Russian',
        'sk': 'Slovak',
        'sv': 'Swedish',
        'th': 'Thai',
        'tr': 'Turkey',
        'uk': 'Ukraine',
        'vi': 'Vietnamese',
    }



#Function to enter the appropriate voice channel and play a text-to-speech message.
async def queue_voice(self, server, channel, message):
    global voice
    voice = get(self.client.voice_clients, guild=server)
    while server.id in accessing_thoughts.keys():
        await asyncio.sleep(0.2)
    if server.id in thoughts:
        accessing_thoughts[server.id] = True
        thoughts[server.id].append([message])
        channels[server.id].append([channel])
        del accessing_thoughts[server.id]
        return
    else:
        accessing_thoughts[server.id] = True
        thoughts[server.id] = [message]
        channels[server.id] = [channel]
        del accessing_thoughts[server.id]
    while server.id in thoughts.keys():
        while server.id in accessing_thoughts.keys():
            await asyncio.sleep(0.2)
        j = 0
        accessing_thoughts[server.id] = True
        for k in thoughts[server.id]:
            j += 1
        if j == 1:
            loop_message = thoughts[server.id][0]
            new_channel = channels[server.id][0]
            del thoughts[server.id]
            del channels[server.id]
        else:
            loop_message = thoughts[server.id].pop(0)
            new_channel = channels[server.id].pop(0)
        del accessing_thoughts[server.id]
        if server.id in bot_language.keys():
            lang_t_play = str(bot_language[server.id])
        else:
            lang_t_play = "en-GB"
        tts = gTTS(text=loop_message, lang=lang_t_play)
        filename = f'text_to_speech\{time.monotonic_ns()}.mp3'
        await asyncio.sleep(0.2)
        tts.save(filename)
        if voice and voice.is_connected():
            await voice.move_to(new_channel)
        else:
            try:
                voice = await new_channel.connect()
            except discord.errors.ClientException:
                print("error")
        if len(voice.channel.members) > 1:
            voice.play(discord.FFmpegPCMAudio(filename), after=None)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.5
        while voice.is_playing():
            await asyncio.sleep(0.5)
        if len(voice.channel.members) == 1:
            await voice.disconnect()



#Function to thank our servicemen.
async def thank_for_service(self, member, server, channel):
    chance_thank = random.randint(0,1)
    if chance_thank >= 1:
        with open('./assets/thank_for_service.txt', "r") as f:
            num_lines = 0
            for line in f:
                num_lines += 1
            line_choice = random.randint(0,(num_lines-1))
            f.seek(0)
            num_lines = 0
            for line in f:
                if num_lines == line_choice:
                    message = f.readline()
                num_lines += 1
    else:
        message = f'{member.name} joined.'
    await queue_voice(self, server, channel, message)


class Voice(commands.Cog):

    def __init__(self, client):
        self.client = client


    #Event Listener to announce when a user's voice status changes.
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #Check to see if the user is the bot or not. Can also be implemented to check
        #for a bot role (no permissions) if multiple bots are run on the server.
        if member.id != bot_ID:
            server = member.guild
            channel = after.channel
            #User has changed voice channels.
            if before.channel != after.channel:
                #User has joined a voice channel.
                if after.channel:
                    #User has moved from another voice channel.
                    if before.channel:
                        #User has moved from an active voice channel and was not AFK.
                        if not before.afk:
                            channel = before.channel
                            message = f"{member.name} left."
                            await queue_voice(self, server, channel, message)
                    #User has moved to the AFK voice channel
                    if after.afk:
                        return
                    else:
                        #User has joined a voice channel from nowhere.
                        if not before.channel:
                            #Check to see if the user is a Veteran.
                            for roles in member.roles:
                                if roles.name == "VETERAN":
                                    channel = after.channel
                                    await thank_for_service(self, member, server, channel)
                                    return
                        channel = after.channel
                        message = f"{member.name} joined."
                if not after.channel:
                    channel = before.channel
                    message = f"{member.name} left."
                await queue_voice(self, server, channel, message)
            #User has been muted or deafened.
            if before.channel == after.channel:
                channel = after.channel
                if before.self_stream == False and after.self_stream == True:
                    message = f"{member.name} has begun streaming."
                if before.self_stream == True and after.self_stream == False:
                    message = f"{member.name} has stopped streaming."
                if member.id in on_cooldown.keys():
                    if on_cooldown[member.id] == 2:
                        return
                #Message order is important here because deafening a user also mutes them.
                if (before.mute == False and after.mute == True) or (before.self_mute == False and after.self_mute == True):
                    message = f"{member.name} has been muted."
                if (before.mute == True and after.mute == False) or (before.self_mute == True and after.self_mute == False):
                    message = f"{member.name} has been unmuted."
                if (before.deaf == False and after.deaf == True) or (before.self_deaf == False and after.self_deaf == True):
                    message = f"{member.name} has been deafened."
                if (before.deaf == True and after.deaf == False) or (before.self_deaf == True and after.self_deaf == False):
                    message = f"{member.name} has been undeafened."
                #Set a cooldown to prevent rapid mute/unmute abuse.
                if member.id in on_cooldown.keys():
                    on_cooldown[member.id] = 2
                    await asyncio.sleep(4)
                    await queue_voice(self, server, channel, message)
                if member.id not in on_cooldown.keys():
                    on_cooldown[member.id] = 1
                    await queue_voice(self, server, channel, message)
                    await asyncio.sleep(10)
                    del on_cooldown[member.id]




    #Command to set bot text-to-speech language.
    @commands.command()
    async def lang(self, ctx, new_language):
        is_suc = False
        await ctx.message.delete()
        for lang in avail_languages.keys():
            if new_language == lang:
                is_suc = True
                bot_language[ctx.guild.id] = new_language
        if is_suc == False:
            message = "Please use one of the following codes:\n```"
            for item, amount in avail_languages.items():
                message += item + ", " + amount + "\n"
            message += "```"
            await ctx.send(message)



    #Command to send text-to-speech to an active voice channel.
    @commands.command()
    async def tts(self, ctx, *, tex_input):
        await ctx.message.delete()
        server = ctx.guild
        channel = ctx.message.author.voice.channel
        message = f'{ctx.message.author.name} says: {tex_input}'
        await queue_voice(self, server, channel, message)


    #Command to play a custom, random .mp3 file.
    @commands.command()
    async def demons(self, ctx):
        server = ctx.guild
        channel = ctx.message.author.voice.channel
        await ctx.message.delete()
        voice = get(self.client.voice_clients, guild=server)
        if voice and voice.is_connected():
            if voice.channel != channel:
                await voice.move_to(channel)
        else:
            voice = await channel.connect()
        while voice.is_playing():
            await asyncio.sleep(0.5)
        if voice.is_playing() == False:
            co_unt = 0
            for filename in os.listdir('./assets/demons'):
                if filename.endswith('.mp3'):
                    co_unt += 1
            chance_2 = random.randint(1,co_unt)
            co_unt = 0
            for filename in os.listdir('./assets/demons'):
                if filename.endswith('.mp3'):
                    co_unt += 1
                if co_unt == chance_2:
                    fil_name = f"./assets/demons/{filename}"
            voice.play(discord.FFmpegPCMAudio(fil_name), after=None)
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.02


    #Command to stop the bot from playing audio and eject it from the voice channel.
    @commands.command()
    async def stop(self, ctx):
        await ctx.message.delete()
        global voice
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            if ctx.guild.id in spam_channels.keys():
                channel = spam_channels[ctx.guild.id]
                await channel.send(f'{ctx.message.author.name} silenced me!')
        if voice.is_connected():
            await voice.disconnect()




def setup(client):
    client.add_cog(Voice(client))
