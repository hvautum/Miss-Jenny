# Miss Jenny
*Assistant to the regional manager.*

Miss Jenny is a discord bot created in python using discord.py to improve the quality of life of managing a discord server. The bot can use a variety of functions, each requiring installation of their own dependencies, should they be included in the cogs folder.

## Installation
This bot was developed in a PowerShell on a Windows 10 (64 bit) machine. Examples of installation for other operating systems can be found in the provided documentation links.

### Chocolatey
Chocolatey was used to install some of the cog dependencies from github as their pip libraries were out of date. It may also be used to get python. https://chocolatey.org/

### Python 3.8+
Miss Jenny requires python 3.8 or higher. https://www.python.org/downloads/

You may download and manually install the folder, however this may require you to perform extra work in setting up paths for using pip to install python libraries.
It may be easier to search for the latest version of python on the Windows Store and install it there. Remember to verify the publisher and version.

### Discord.py
Miss Jenny runs using discord.py 1.40a+. https://github.com/Rapptz/discord.py
> python -3 -m pip install -U discord.py

or for voice support:
> python -3 -m pip install -U discord.py[voice]


### Urbandictionary.py
The UrbanDictionary function requires installation of the urbandictionary.py library.
The pypy library for urbandictionary is out of date and not functional, so it must be pulled from github. https://github.com/bocong/urbandictionary-py

If you are using chocolaty you may want to install git from an PowerShell with administrative privileges:
>choco install git

>pip install git+https://github.com/bocong/urbandictionary-py.git


### Voice.py
Voice functionality uses gTTS and FFMPEG to convert text to speech and subsequently play it.
for gTTS https://pypi.org/project/gTTS/
>pip install gTTS

for FFmpeg https://ffmpeg.org/
>pip install ffmpeg


### Notes
1. The giphy cog will require you to input your own api key for their website into the giphy.py file.

2. You will have to generate your own bot Token for discord. https://discordpy.readthedocs.io/en/latest/discord.html

3. You may have to grab the bot ID from discord (in developer mode) https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-

4. You may wish to set the relevant enviornment variables in your OS to hide the bot token, bot ID, and api keys in bot_preferences.py. Alternatively, you can just declare them in the file to get the bot working with minimal effort.



## Usage


### Passive Features
The bot will join a voice channel and announce when users join or leave in their respective channels. The bot will also disconnect if there is no one in a voice channel.

The bot will load preferences for what channel is designated in via the !set_console command on startup. The preferences can be cleared by using the !del_console command in discord or deleting relevant server in the preferences.txt file.


### Commands
*Commands may be altered frequently throughout development and as such, this section may be out of date*
Commands are entered in a discord server the bot is active in. Note that it may be useful to use the !set_console command to dump relevant administrative information into such as who called certain commands or what arguments were used to search for something.

Core Commands
>!help

Returns a formatted help menu listing the current commands and usage examples.

>!set_console Channel_Name

Takes an existing channel name on that server as an argument to set as a console for the bot to post useful console type messages.

>!del_console

Removes any existing channel set as a console from memory and server preferences.txt

Administrative Commands

>!ping

Returns the bot latency in ms.

>!game Hello Kitty Island Adventure

Takes a string as an argument to set the bot status to "Playing: string"

>!say I am a good bot.

Takes a string as an argument to then repeat as the bot in the channel called.

>!react :smile:

Takes an integer and a unicode or custom emoji formatted as :emoji: as arguments. The integer refers to how many messages above the command message for the bot to grab and react to with the given emoji.

>!clear 10

Takes an integer as an argument to clear that many messages in the called channel, sorted by most recent first.

UrbanDictionary Commands

>!define Cher

Takes a string as an argument to search for an urban dictionary reference to deliver to the called channel.

Giphy Commands

>!giphy Dancing Dogs

Takes a string as an argument to search for a giphy .gif and embed a random result in the called channel.

RedGifs Commands

>!rg NSFW

Takes a string as an argument to search for a redgifs .mp4 link to post in the called channel if it is designated for NSFW content in discord.

Voice Commands

>!tts I am a bot.

Takes a string as an argument to convert to a text to speech .mp3 and play in the user's voice channel.

>!stop

Silences the bot and ejects it from any voice channel.

>!demons

Plays a custom .mp3 for you in your voice channel.
