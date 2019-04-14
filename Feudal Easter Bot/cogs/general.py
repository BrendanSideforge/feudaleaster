import discord 
from discord.ext import commands 
import pymongo 
from pymongo import MongoClient as mcl
from collections import defaultdict
import random 

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = mcl("mongodb://Brendan:BS103261@ds137102.mlab.com:37102/feudaleaster")
        self.db = self.client["feudaleaster"]
        self.col = self.db["users"]
        self.data = self.col.find_one()

    @commands.command()
    async def changeall(self, ctx):
        self.data = self.col.find_one()
        if not ctx.author.id in self.bot.devs:
            return 
        users = 0
        print(self.data)
        for user in self.data:
            users += 1
            document = {"$set":{str(user):{
                "eggs": self.data[user]["eggs"],
                "currency": self.data[user]["currency"],
                "items": self.data[user]["items"],
                "egg-streak": 0,
                "loo-streak": 0
            }}}
            self.col.update_one({"auth": True}, document)
        await ctx.send(f"{self.bot.check_mark} I have changed all of the users in the database. I changed **{users}** users successfully.")

def setup(bot):
    bot.add_cog(General(bot))