import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected.')


@bot.command(name='roll', help='Rolls some dice', usage="\n\nUse format: 'd6+2d4+10'"
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
        cmd = dice.split('+')
        for die in cmd:
            if die.find('d') > 0:
                sub_result = list()
                for _ in range(int(die.split('d')[0])):
                    res = random.randint(1, int(die.split('d')[1]))
                    sum += res
                    if res == int(die.split('d')[1]):
                        sub_result.append(f"***{res}***")
                    elif res == 1:
                        sub_result.append(f"__{res}__")
                    else:
                        sub_result.append(str(res))
                result.append(f"({', '.join(sub_result)})")
            elif die.find('d') == 0:
                res = random.randint(1, int(die[1:]))
                sum += res
                result.append(f"({res})")
            else:
                result.append(f'+ ({die})')
                sum += int(die)
        result.append(f'Total: {sum}')
        await ctx.send(' | '.join(result))
    except ValueError:
        await ctx.send("Haha, no. Try again in a different format maybe? *or check `>help roll`*")
        raise


@bot.command(name='twss', help='That\'s what she said!')
async def twss(ctx):
    await ctx.send(file=discord.File(open('the-office-thats-what-she-said.gif', 'rb')))


bot.run(TOKEN)
