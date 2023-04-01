import discord,json
from discord.ext import commands
"""
Moderation Commands
"""
class Moderation(commands.Cog):
    def __init__(self,commands):
        self.commands=commands
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation payload is loaded ✅")
    
    """
    Commands
    """
    @commands.command(brief="To clear messages",description=" <prefix>clear <no of messages> \n by default 1 message is cleared without no of messages mentioned")
    @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amount=2):#clear command
        await ctx.channel.purge(limit=amount)
        await ctx.send("*Messages has been cleared!*")
        await ctx.channel.purge(limit=2)


    @commands.command(brief="To kick members",description="<prefix> kick <member>")
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def kick(self,ctx,*,member:discord.Member):#kick command
        await member.kick()
        await ctx.channel.send(f"***{member.name}*** *has been kicked by {ctx.author.name}*")


    @commands.command(brief="To ban members",description="<prefix> ban <member>")
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def ban(self,ctx,*,member:discord.Member,):#ban command
        await member.ban()
        await ctx.channel.send(f"***{member.name}*** *has been banned by {ctx.author.name}*")


    @commands.command(brief="To unban members",description="<prefix>unban <member>")
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def unban(self,ctx,*,member):#unban command
        banned_users=await ctx.guild.bans()
        member_name,member_tag=member.split("#")
        for ban_entry in banned_users:
            user=ban_entry.user
            if (user.name,user.discriminator)==(member_name,member_tag):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"***{user.name}*** *has been unbanned by {ctx.author.name}*")
                return


    @commands.command(aliases=["cf"],brief="To change the prefix of the server",description="<current prefix> changeprefix <new prefix> Note:Can use cf instead of changeprefix")
    @commands.has_permissions(manage_guild=True)
    async def changeprefix(self,ctx,prefix):#changeprefix command
        with open("./Cogs/Json/prefixes.json","r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)]=prefix

        with open("./Cogs/Json/prefixes.json","w") as f:
            json.dump(prefixes,f,indent=5)
        await ctx.send(f"*prefix changed to {prefix}*")


    @commands.command(brief="To view current prefix",description="<Mention> prefix")
    async def prefix(self,ctx):#To view Current prefix
      with open("./Cogs/Json/prefixes.json","r") as f:
        prefixes = json.load(f)
      pre=prefixes[str(ctx.guild.id)]
      await ctx.send(f"***The prefix is {pre}***")

    @commands.command()
    async def poll(self,ctx,*,args):
        await ctx.channel.purge(limit=1)
        emoji_0="👍"
        emoji_1="👎"
        embed=discord.Embed(title=f"Poll by {ctx.author.name}",
        description=f"*{args}*",colour=0xff0000)
        msg=await ctx.send(embed=embed)
        await msg.add_reaction(emoji_0)
        await msg.add_reaction(emoji_1)

def setup(client):
    client.add_cog(Moderation(client))    
