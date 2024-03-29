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
        if ctx.author.id in self.bot.blacklisted:
            return await ctx.author.send(f"Nope, you're not gonna use any commands.")
        embed = discord.Embed(color=self.bot.embed_colour)
        embed.title = "Egg Shop"
        embed.add_field(name=f"{self.bot.mutliplier} Egg Multiplier", value=f"""
        **Item ID:** 4320
        **Cost:** 5 eggs
        **Description:** Everytime you catch an egg you get 2x the amount of eggs.
        """)
        embed.set_footer(text="Use the command - $buy <item_id> - to buy a item!")
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, item: int = None):
        if not ctx.channel.id in self.channels:
            return
        self.data = self.col.find_one()
        if not item:
            return await ctx.send(f"{self.bot.x_mark} Please use the command **$shop** to see all of the items.")
        if not str(ctx.author.id) in self.data:
            document = {"$set": {str(ctx.author.id):{
                "eggs": 0,
                "currency": 0,
                "items": [],
                "egg-streak": 0,
                "loot-streak": 0,
                "animals": []
            }}}
            self.col.update_one({"auth": True}, document)
            return await ctx.send(f"{self.bot.x_mark} You do not have enough eggs to buy any item.")
        if item == 4320:
            eggs = self.data[str(ctx.author.id)]["eggs"]
            if eggs < 5:
                return await ctx.send(f"{self.bot.x_mark} Very sorry **{ctx.author.name}**! You do not have enough eggs to buy the **Egg Multiplier**! Your current eggs are **{eggs}/5**.")
            else:
                items = self.data[str(ctx.author.id)]['items']
                if "Egg Multiplier" in items:
                    return await ctx.send(f"Very sorry **{ctx.author.name}**! You already have this item!")
                document = {"$set": {str(ctx.author.id):{
                    "eggs": eggs - 5,
                    "currency": self.data[str(ctx.author.id)]["currency"],
                    "items": [*items, 'Egg Multiplier'],
                    "egg-streak": self.data[str(ctx.author.id)]["egg-streak"],
                    "loot-streak": self.data[str(ctx.author.id)]["loot-streak"],
                    "animals": self.data[str(ctx.author.id)]["animals"]
                }}}
                self.col.update_one({"auth": True}, document)
                await ctx.send(f"{self.bot.check_mark} Yay! You have bought the {self.bot.mutliplier} **Egg Multiplier**! You will now get 2x the amount of eggs!")
        else:
            print("wtf")
                
def setup(bot):
    bot.add_cog(Shop(bot))
