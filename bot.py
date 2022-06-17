import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

help_command = commands.DefaultHelpCommand(no_category='General commands')
bot = commands.Bot(command_prefix='>', help_command=help_command)


class Rolls(commands.Cog):
    @commands.command(name='roll', help='Rolls some dice', usage="\n\nUse format: 'd6+2d4+10'"
                                                                 "\nYou can use negative modifiers as: 'd20+-12'"
                                                                 "\nPut that damn plus between everything. Please."
                                                                 "\nNo parentheses. Why would you use them anyway?"
                                                                 "\n\nDo *NOT* put spaces in your expression."
                                                                 "\nEverything *MUST* be next to each other."
                                                                 "\nOtherwise rolls only the first one")
    async def roll_dice(self, ctx, dice: str):
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

    @commands.command(name='rollability', help='Rolls ability rolls for new D&D characters',
                      usage='\n\nRolls 6 sets of 4d6 and keeps highest 3 for each set', alias='ra')
    async def roll_ability(self, ctx):
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

    @commands.command(name='rollfate', help='Rolls Fate RPG dice',
                      usage="\n\nJust specify the modifier, like '>fateroll 2', "
                            "or ignore it if there is no modifier, "
                            "we'll make sure the rest is working ;)", alias='rf')
    async def roll_fate(self, ctx, mod: int = 0):
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


@bot.event
async def on_ready():
    print(f'{bot.user} has connected.')


@bot.command(name='twss', help='That\'s what she said!')
async def twss(ctx):
    await ctx.send(file=discord.File(open(f"images/twss/{random.choice(os.listdir('images/twss/'))}", 'rb')))


bot.add_cog(Rolls())
bot.run(TOKEN)
