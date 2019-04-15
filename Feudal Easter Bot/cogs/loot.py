import discord 
from discord.ext import commands 
import pymongo 
from pymongo import MongoClient as mcl
from collections import defaultdict
import random

class Lootdrops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = mcl("mongodb://Brendan:BS103261@ds137102.mlab.com:37102/feudaleaster")
        self.db = self.client["feudaleaster"]
        self.col = self.db["users"]
        self.data = self.col.find_one()
        self.bot.messages1 = defaultdict(int)
        self.bot.codes = 0
        self.bot.egg = ""
        self.channels = [
            422566574541766656,
            426515636571734016
        ]

    @commands.command()
    async def catchloot(self, ctx, code: int = None):
        self.data = self.col.find_one()
        if ctx.author.id in self.bot.blacklisted:
            return await ctx.author.send(f"Nope, you're not gonna use any commands.")
        if code == None:
            return 
        if code == self.bot.codes1:
            if not str(ctx.author.id) in self.data:
                print("OK User not registered.")
                document1 = {"$set": {str(ctx.author.id):{
                        "eggs": 5,
                        "currency": 0,
                        "items": self.data[str(ctx.author.id)]["items"],
                        "egg-streak": self.data[str(ctx.author.id)]["egg-streak"],
                        "loot-streak": self.data[str(ctx.author.id)]["loot-streak"] + 1,
                        "animals": self.data[str(ctx.author.id)]["animals"],
                        "team": self.data[str(ctx.author.id)]["team"]
                    }}}
                await ctx.send(f"{self.bot.lootbox} **|** {ctx.author.mention} has caught the drop [**{self.bot.codes1}**]! They now have 5 eggs!")
                self.bot.codes1 = 0
                self.col.update_one({"auth": True}, document1)
                return
            else:
                print("Ok")
                document2 = {"$set": {str(ctx.author.id):{
                        "eggs": self.data[str(ctx.author.id)]["eggs"] + 5,
                        "currency": 0,
                        "items": self.data[str(ctx.author.id)]["items"],
                        "egg-streak": self.data[str(ctx.author.id)]["egg-streak"],
                        "loot-streak": self.data[str(ctx.author.id)]["loot-streak"] + 1,
                        "animals": self.data[str(ctx.author.id)]["animals"],
                        "team": self.data[str(ctx.author.id)]["team"]
                }}}
                self.col.update_one({"auth": True}, document2)
                await ctx.send(f"{self.bot.lootbox} **|** {ctx.author.mention} has caught the drop [**{self.bot.codes1}**]! They now have {self.data[str(ctx.author.id)]['eggs'] + 5} eggs!")
                self.bot.codes1 = 0
                count = True
                return
        else:
            return
            

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 551422203183497241:
            return
        self.data = self.col.find_one()
        code = random.randint(100000, 1000000)
        self.bot.messages1[message.channel] += 1 #add .id if needed
        if self.bot.messages1[message.channel] == 600:
            self.bot.codes1 = code
            await message.channel.send(f"{self.bot.lootbox} **|** Loot has dropped! Use **$catchloot {code}** to get 5 eggs!")
            self.bot.messages1[message.channel] = 0
            return
        

def setup(bot):
    bot.add_cog(Lootdrops(bot))
