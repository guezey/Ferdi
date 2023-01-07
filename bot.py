import discord
import os
import random
import asyncio
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
intents = discord.Intents().default()
intents.message_content = True
bot = commands.Bot(
    intents=intents,
    command_prefix='>',
    help_command=commands.DefaultHelpCommand(no_category='\nOther')
)

yt_dl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

voice_clients = {}


@bot.command(name='play')
async def play_url(ctx, url: str):
    try:
        voice_client = await ctx.message.author.voice.channel.connect()
        voice_clients[ctx.guild.id] = voice_client
    except discord.ClientException:
        voice_client = voice_clients[ctx.guild.id]

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

    song = data['url']
    player = discord.FFmpegOpusAudio(song, **ffmpeg_options, executable="C:\\ffmpeg\\ffmpeg.exe")

    voice_client.play(player)


@bot.command(name='pause')
async def pause(ctx):
    voice_clients[ctx.guild.id].pause()


@bot.command(name='resume')
async def resume(ctx):
    voice_clients[ctx.guild.id].resume()


@bot.command(name='roll', help='Rolls some dice', description="\n\nUse format: 'd6+2d4+10'"
                                                              "\nYou can use negative modifiers as: 'd20+-12'"
                                                              "\nPut that damn plus between everything. Please."
                                                              "\nNo parentheses. Why would you use them anyway?"
                                                              "\n\nDo *NOT* put spaces in your expression."
                                                              "\nEverything *MUST* be next to each other."
                                                              "\nOtherwise rolls only the first one")
async def roll_dice(ctx, dice: str):
    try:
        result = list()
        sum = 0

        for set in dice.split('+'):  # for each die set
            if set.find('d') > 0:  # if set includes multiple dice
                sub_result = list()
                for _ in range(int(set.split('d')[0])):
                    res = random.randint(1, int(set.split('d')[1]))
                    sum += res
                    if res == int(set.split('d')[1]):
                        sub_result.append(f"***{res}***")
                    elif res == 1:
                        sub_result.append(f"__{res}__")
                    else:
                        sub_result.append(str(res))
                result.append(f"({', '.join(sub_result)})")

            elif set.find('d') == 0:  # if set is only one die
                res = random.randint(1, int(set[1:]))
                sum += res
                result.append(f"({res})")

            else:  # if set is a constant modifier
                result.append(f'+ ({set})')
                sum += int(set)

        result.append(f'Total: {sum}')
        await ctx.send(' | '.join(result))

    except ValueError:
        await ctx.send("Haha, no. Try again in a different format maybe? *or check `>help roll`*")


@bot.command(name='rollability', help='Rolls ability rolls for new D&D characters',
             description='\n\nRolls 6 sets of 4d6 and keeps highest 3 for each set')
async def roll_ability(ctx):
    detail_prompt = ''
    response = list()

    for _ in range(6):
        sum = 0
        results = list()
        temp = list()
        details = list()

        for _ in range(4):
            res = random.randint(1, 6)
            results.append(res)
            temp.append(str(res))
        results.sort()
        cnt = 0
        for s in temp:
            if int(s) == results[0] and not cnt:
                details.append(f'{s}')
                cnt += 1
            else:
                details.append(f'**{s}**')
        for i in results[1:]:
            sum += i
        response.append(sum)
        detail_prompt += f"({', '.join(details)})\n"

    response = [str(i) for i in sorted(response, reverse=True)]
    await ctx.send(f"{detail_prompt}\nResults: {', '.join(response)}")


@bot.command(name='rollfate', help='Rolls Fate RPG dice', description="\n\nJust specify the modifier, like "
                                                                      "'>fateroll 2', "
                                                                      "or ignore it if there is no modifier, "
                                                                      "we'll make sure the rest is working ;)")
async def roll_fate(ctx, mod: int = 0):
    dice = [random.randint(-1, 1) for _ in range(4)]
    response = list()

    sum = 0
    for die in dice:
        if die == 1:
            response.append('(+)')
        elif die == -1:
            response.append('(-)')
        else:
            response.append('(  )')
        sum += die

    sum += mod
    response.append(f'| Mod: {mod}')
    response.append(f'\nResult: {sum}')

    await ctx.send(' '.join(response))


@bot.command(name='twss', help='That\'s what she said!', hidden=True)
async def twss(ctx):
    """
        Sends a link to GIPHY.com to the chat. Discord automatically
        shows the GIF inside the link in the chat.

        It uses links to the GIFs instead of the actual .gif file
        to decrease response time (It did use the files for some time
        actually, and it was sooo slow. So let's use the links instead).
    """

    msg = list()
    with open('images/twss.txt', 'rt') as links:
        for line in links:
            msg.append(line)

    await ctx.send(random.choice(msg))


@bot.command(name='source', help='Me, basically.', hidden=True)
async def source(ctx):
    await ctx.send('https://github.com/guezey/Ferdi. You\'re welcome.')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected.')


bot.run(TOKEN)
