import discord 
from discord.ext import commands
import pymongo
from pymongo import MongoClient as mcl 
import traceback
from collections import defaultdict

TOKEN = "NTY1NjU3Nzg0NTExODg5NDQ4.XK5n4Q.GO_xFmOLgZ5cMFovziuOHyH8JzQ"

cogs = [
    "cogs.egg",
    "cogs.shop"
]

class FeudalEaster(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("$"), case_insensitive=True)

        self.x_mark = "<:feudal_x:560243237672058887>"
        self.check_mark = "<:feudal_check:560243202586574858>"
        self.omg = "<:omg:565714172168634372>"
        self.mutliplier = "<:multiplier:566381680181510164>"

        self.client = mcl("mongodb://Brendan:BS103261@ds137102.mlab.com:37102/feudaleaster")
        self.db = self.client["feudaleaster"]
        self.col = self.db["users"]
        self.data = self.col.find_one()

        self.devs = [
            481270883701358602 #BrendanTheBigBoi
        ]

        self.embed_colour = 0x7289da

        # Eggs
        self.common_egg = "<:common:565706716843343913>"
        self.uncommon_egg = "<:uncommon:565706709880799247>"
        self.mystical_egg = "<:mystical:565706700825427978>"

        self.blacklisted = [
            280444560973234176
        ]

        self.messages = 0

    async def on_ready(self):
        print("Feudal Easter bot is now online!")
        for cog in cogs:
            try:
                await bot.load_extension(cog)
                print(f"Loaded {cog}")
            except Exception as er:
                exc = ''.join(traceback.format_exception(type(er), er, er.__traceback__, chain=False))
                print(f"Couldn't load {cog}")
                print(exc)


bot = FeudalEaster()

@bot.command()
async def reload(ctx, *, cog = None):
    # Add some decorators for the command, including to check if the author is a developer or not
    if not ctx.author.id in bot.devs:
        return 
    if not cog:
        return 
    list_cogs = ''
    # See if the cog parameter is "all" and if it is, we will reload all of the cogs/extensions 
    if cog.lower() == "all":
        # Loop through all of the cogs 
        for cog in cogs:
            # Try statement is for catching errors and problems within the code/file
            try:
                bot.reload_extension(cog)
                list_cogs += f"{cog}\n"
            except Exception as er:
                exc = ''.join(traceback.format_exception(type(er), er, er.__traceback__, chain=False))
                embed = discord.Embed(color=bot.embed_colour)
                embed.description = exc 
                return await ctx.send(f"{bot.x_mark} Looks like there was an error loading `{cog}`!", embed=embed)
        return await ctx.send(f"{bot.check_mark} Reloaded all of the cogs successfully!\nList of all of the reloaded cogs:\n{list_cogs}")


    # Try statement is for catching errors and problems within the code/file
    try:
        bot.reload_extension(cog)
        await ctx.send(f"{bot.check_mark} Reloaded `{cog}` successfully!")
    except Exception as er:
        exc = ''.join(traceback.format_exception(type(er), er, er.__traceback__, chain=False))
        embed = discord.Embed(color=bot.embed_colour)
        embed.description = exc 
        return await ctx.send(f"{bot.x_mark} Looks like there was an error loading `{cog}`!", embed=embed)


bot.run(TOKEN)
