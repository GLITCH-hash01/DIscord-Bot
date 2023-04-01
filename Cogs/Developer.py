import discord,json
from discord.ext import commands

class Developer(commands.Cog):
    def __init__(self,client):
        self.client=client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Developer Payload is loaded ✅")
        
    """
    Commands
    """
   
    @commands.command()
    @commands.is_owner()
    async def startconv(self,ctx):
        """
        Command to chat as the bot
        Only accessible to the owner 
        """
        if ctx.author.id=="owner id":

            await ctx.channel.purge(limit=1)
            while True:
                msg=input(">")
                if msg!="break":
                    await ctx.send(msg)
                else:
                    break
        else:
            await ctx.send("Sorry You Don't have persmission")
    
    @commands.command()
    @commands.is_owner()
    async def load(self,ctx,extension):
        """
        Loading Modules
        """
        commands.load_extension(f"Cogs.{extension}")

    @commands.command()
    @commands.is_owner()
    async def unload(self,ctx,extension):
        """
        Unloading Modules
        """
        commands.unload_extension(f"Cogs.{extension}")
    
def setup(client):
    client.add_cog(Developer(client))