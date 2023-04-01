import discord,random,json
from discord.ext import commands
"""
General commands
"""

class General(commands.Cog):
    def __init__(self,client):
        self.client=client
     
    @commands.command(aliases=["Toss","t"],brief="To Toss a coin <prefix> toss")
    async def toss(self,ctx):#toss a coin
        toss_option=["Heads","Tails"]
        toss_result=random.choice(toss_option)
        await ctx.send(f"***{toss_result}*** *won the toss!*")



    @commands.command(brief="To give truth to someone")
    async def truth(self,ctx,member:discord.Member):
        with open("./Cogs/Json/truthanddare.json","r") as f:
           truth_dict=json.load(f)
        truth=list(truth_dict.values())
        truth_chosen=random.choice(truth[0])
        embed=discord.Embed(title=f"***{ctx.author.name}*** *given truth to* ***{member.name}***",description=f"*{truth_chosen}*",colour=0xff0000)
        await ctx.send(embed=embed)


    @commands.command(brief="To give dare to someone")
    async def dare(self,ctx,member:discord.Member):
        with open("./Cogs/Json/truthanddare.json","r") as f:
           dare_dict=json.load(f)
        dare=list(dare_dict.values())
        dare_chosen=random.choice(dare[1])
        embed=discord.Embed(title=f"***{ctx.author.name}*** *given dare to* ***{member.name}***",description=f"*{dare_chosen}*",colour=0xff0000)
        await ctx.send(embed=embed)

    @commands.command(brief="To roll a dice")
    async def dice(self,ctx):
        await ctx.send(f"***{random.randint(1,6)}*** *falls on dice*")

def setup(client):
    client.add_cog(General(client))