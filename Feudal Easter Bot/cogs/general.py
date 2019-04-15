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
        users_count = 0
        server_users = self.data 
        users = [x for x in server_users if len(x) == 18]
        for user in users:
            print(user)
            users_count += 1
            document = {"$set":{str(user):{
                "eggs": self.data[str(user)]["eggs"],
                "currency": self.data[str(user)]["currency"],
                "items": self.data[str(user)]["items"],
                "egg-streak": self.data[str(user)]["egg-streak"],
                "loo-streak": self.data[str(user)]["loot-streak"],
                "animals": []
            }}}
            self.col.update_one({"auth": True}, document)
        await ctx.send(f"{self.bot.check_mark} I have changed all of the users in the database. I changed **{users_count}** users successfully.")

def setup(bot):
    bot.add_cog(General(bot))
