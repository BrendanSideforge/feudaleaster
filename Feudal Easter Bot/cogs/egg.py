import discord 
from discord.ext import commands 
import pymongo 
from pymongo import MongoClient as mcl
from collections import defaultdict
import random

class Egg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.client = mcl("mongodb://Brendan:BS103261@ds137102.mlab.com:37102/feudaleaster")
        self.db = self.client["feudaleaster"]
        self.col = self.db["users"]
        self.data = self.col.find_one()
        self.bot.messages = defaultdict(int)
        self.bot.codes = 0
        self.bot.egg = ""
        self.channels = [
            422566574541766656,
            426515636571734016
        ]

    async def leaderboardData(self, ctx):
        self.data = self.col.find_one()
        server_users = self.data
        top = list(enumerate(sorted([(server_users[user]["eggs"], user) for user in server_users if len(user) == 18], reverse=True), start=1))
   
        async def leader_embed(eggs):
            embed = discord.Embed(color=self.bot.embed_colour)
            embed.title = "Egg hunters"
            desc = ""
            for pos, score in eggs:
                    user = await self.bot.fetch_user(score[1])
                    desc += f'**{pos}**. {user} • **{score[0]} eggs**\n'
            embed.description = "Click the arrows to navigate through the leaderboard!\n\n" + desc
            return embed
           
        message = await ctx.send(embed=await leader_embed(top[:10]))
       
       
        if len(top) > 10:
              await message.add_reaction("◀")
              await message.add_reaction("❌")
              await message.add_reaction("▶")
 
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == message.id:
                    if reaction.emoji == "▶" or reaction.emoji == "❌" or reaction.emoji == "◀":
                        return True
        x = 0
        while True:
            reaction, user3 = await self.bot.wait_for("reaction_add", check=reactioncheck)
            if reaction.emoji == "◀":
                await message.remove_reaction("◀", user3)
                x -= 10
                if x < 0:
                    x = 0
            elif reaction.emoji == "❌":
                await message.delete()
            elif reaction.emoji == "▶":
                await message.remove_reaction("▶", user3)
                x += 10
                if x > len(top):
                    x = len(top) - 10
            embed = await leader_embed(top[x:x+10])
            await message.edit(embed=embed)


    @commands.command()
    async def catch(self, ctx, code: int = None):
        self.data = self.col.find_one()
        if code == None:
            return 
        if code == self.bot.codes:
            if not str(ctx.author.id) in self.data:
                document = {"$set": {str(ctx.author.id):{
                    "eggs": 1,
                    "currency": 0,
                    "items": []
                }}}
                await ctx.send(f"{self.bot.egg} **|** {ctx.author.mention} has caught the egg [**{self.bot.codes}**]! They now have 1 egg!")
                self.bot.codes = 0
                self.col.update_one({"auth": True}, document)
                return
            document2 = {"$set": {str(ctx.author.id):{
                "eggs": self.data[str(ctx.author.id)]["eggs"] + 1,
                "currency": 0,
                "items": []
            }}}
            self.col.update_one({"auth": True}, document2)
            await ctx.send(f"{self.bot.egg} **|** {ctx.author.mention} has caught the egg [**{self.bot.codes}**]! They now have {self.data[str(ctx.author.id)]['eggs'] + 1} eggs!")
            self.bot.codes = 0
            return
        else:
            return

    @commands.command(aliases=["lb", "leading"])
    async def leaderboard(self, ctx):
        if not ctx.channel.id in self.channels:
            return
        await self.leaderboardData(ctx)

    @commands.command()
    async def messages(self, ctx):
        if not ctx.author.id == 481270883701358602:
            return
        await ctx.send(f"There are **{self.bot.messages[ctx.channel]}** messages found.")
    
    @commands.command(aliases=["eggs"])
    async def count(self, ctx, user: discord.Member = None):
        if not ctx.channel.id in self.channels:
            return
        self.data = self.col.find_one()
        if not user:
            user = ctx.author 
        if not str(user.id) in self.data:
            return await ctx.send(f"The user doesn't have any eggs or currency.")
        await ctx.send(f"**{user.name}** has {self.data[str(user.id)]['eggs']} eggs.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 551422203183497241:
            return
        self.data = self.col.find_one()
        eggs = [
            self.bot.uncommon_egg,
            self.bot.common_egg,
            self.bot.mystical_egg
        ]
        code = random.randint(100, 1000)
        self.bot.messages[message.channel] += 1 #add .id if needed
        if self.bot.messages[message.channel] == 150:
            random_egg = random.choice(eggs)
            self.bot.codes = code
            self.bot.egg = random_egg
            await message.channel.send(f"{random_egg} **|** Dropped an egg! Use the command **$catch {code}** to get the dropped egg..")
            self.bot.messages[message.channel] = 0
            return

def setup(bot):
    bot.add_cog(Egg(bot))