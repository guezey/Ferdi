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


@bot.command(name='roll', help='- Rolls some dice use format: \'1d6\'')
async def roll_dice(ctx, dice: str):
    try:
        command = (dice.split('d')[0], dice.split('d')[1])
        results = list()
        sum = 0
        for _ in range(int(command[0])):
            results.append(str(random.randint(1, int(command[1]))))
            sum += int(results[-1])
        results.append(f'Total: {sum}')
        await ctx.send(', '.join(results))
    except:
        await ctx.send("Haha, no. Try again in a different format maybe?")


@bot.command(name='twss', help='- That\'s what she said!')
async def twss(ctx):
    await ctx.send(file=discord.File(open('the-office-thats-what-she-said.gif', 'rb')))


bot.run(TOKEN)
