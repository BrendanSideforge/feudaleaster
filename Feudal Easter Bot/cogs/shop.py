import discord 
from discord.ext import commands 
import pymongo 
from pymongo import MongoClient as mcl
from collections import defaultdict
import random

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = mcl("mongodb://Brendan:BS103261@ds137102.mlab.com:37102/feudaleaster")
        self.db = self.client["feudaleaster"]
        self.col = self.db["users"]
        self.data = self.col.find_one()
        self.channels = [
            422566574541766656,
            426515636571734016
        ]

    @commands.command()
    async def shop(self, ctx):
        if not ctx.channel.id in self.channels:
            return
        embed = discord.Embed(color=self.bot.embed_colour)
        embed.title = "Egg Shop"
        embed.add_field(name=f"{self.bot.mutliplier} Egg Multiplier", value=f"""
        **Item ID:** 4320
        **Cost:** 5 eggs
        **Description:** Everytime you catch an egg you get 2x the amount of eggs.
        """)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Shop(bot))
