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


@bot.command(name='abilityroll', help='Rolls ability rolls for you', usage='Rolls 4d6 and keeps highest 3'
                                                                           'for each ability')
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
        detail_prompt += f"({', '.join(details)})"

    response = [str(i) for i in sorted(response, reverse=True)]
    await ctx.send(f"{detail_prompt}\n\nResults: {', '.join(response)}")


@bot.command(name='twss', help='That\'s what she said!')
async def twss(ctx):
    await ctx.send(file=discord.File(open(f"images/twss/{random.choice(os.listdir('images/twss/'))}", 'rb')))


bot.run(TOKEN)
