import discord
from random import random
from discord.ext import commands
from gtw.controller import GuessAWordGame

word="discord"
userguess=list()
class Games(commands.Cog):
    hint=""
    round=7
    current_round=1
    join_allowance=True
    game_channel=discord.channel.TextChannel
    main_channel=discord.channel.TextChannel


    def __init__(self,client):
        self.client=client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Games payload is loaded ✅")

    @commands.group(brief="Guess the Word game")
    async def gtw(self,ctx):#guess the game group
        ctx.gaw_game=GuessAWordGame()

    @gtw.command(name="start")
    async def gtw_start(self,ctx):
        channel_name_0=f"Guessthegame-hosted-by-{ctx.author.name}"
        guild=ctx.guild
        author=ctx.author
        category_name=ctx.channel.category
        result=await ctx.gaw_game.start_game(guild,author,category_name)
        if result is None:
            await ctx.send("*A game is already Running!*")
        else:
            self.main_channel=ctx.channel
            game=ctx.gaw_game.fetch_game()
            self.hint=game.hint
            embed=discord.Embed(title=f"A new game is created by **{ctx.author.name}**",
            description="Type *[prefix] gtw join* to join the game",colour=0xff0000)
            await ctx.send(embed=embed)
            channel_list=ctx.gaw_game.fetch_channel()
            channel_0=channel_list[0]
            self.game_channel=channel_0
            embed=discord.Embed(title="**Guess the Game with following info**",
            description=f'The first round is in the category:***{game.category}*** with a word length of ***{len(game.word)}*** \n the word is ***{game.missing}***',
            colour=0xff0000)
            await channel_0.send(embed=embed)

    @gtw.command(name="join")
    async def gtw_join(self,ctx):
        if self.join_allowance==True:
            channel=ctx.gaw_game.fetch_channel()
            await ctx.gaw_game.set_player_permission(channel[0],ctx.author)
            await ctx.send(f"**{ctx.author.name}** just joined the server")
        else:
            await ctx.send("Sorry! You can't join the game now")
        
    @gtw.command(name="guess",aliases=["g"])
    async def gtw_guess(self,ctx,*,guess:str):
        if ctx.channel.id==self.game_channel.id:
            channel_id=ctx.channel.id
            result,hint=ctx.gaw_game.guess(channel_id,guess)
            if result is None:
                await ctx.send("You are not allowed to play in this channel!")
            elif result is True:
                await ctx.send(f"**{ctx.author.name}** *Guessed it! and won this round with +25 points*")
                self.join_allowance=False
                if self.current_round<=self.round:
                    ctx.gaw_game.win_reward(ctx.author)
                    ctx.gaw_game.new_round(ctx.channel)
                    newgame=ctx.gaw_game.fetch_game()
                    self.hint=newgame.hint
                    embed=discord.Embed(description='The next round is in the category:**%s** with a word length of %s \n the word is %s' % (newgame.category, len(newgame.word),newgame.missing),colour=0xff0000)
                    await ctx.channel.send(embed=embed)
                    self.current_round+=1
                else:
                    await ctx.channel.send("The rounds ended")
            elif result is False:
                await ctx.channel.send(f"{ctx.author.name} guess is wrong  and you *Lost one health* ")
                rslt=ctx.gaw_game.reduce_life(ctx.author)
                stat=ctx.gaw_game.player_status(ctx.author)
                if stat[0]==0:
                    await ctx.gaw_game.degrade_player_permission(ctx.author,ctx.channel)
                    await ctx.channel.send(f"{ctx.author.name} is eliminated")
                if rslt==True:
                    self.join_allowance=True
                    self.current_round=1
                    self.game_channel=discord.channel.TextChannel
                    self.hint=""
                    stat=ctx.gaw_game.leaderboard()
                    embed=discord.Embed(title="**Leaderboards**",
                    description=f"**Name : Points**\n\n*{stat}*\n",
                    colour=0xff0000)
                    await self.main_channel.send(embed=embed)
                    await ctx.gaw_game.destroy(ctx.guild,ctx.channel.id)


        else:
            await ctx.channel.send("*You can only use these commands in game channel*")
    
    @gtw.command(name="hint")
    async def gtw_hint(self,ctx):
        if ctx.channel.id==self.game_channel.id:
            stat=ctx.gaw_game.player_status(ctx.author)
            if stat[1]>=15:
                ctx.gaw_game.buy_hint(ctx.author)
                await ctx.author.send(f'The hint is "*{self.hint}*"')
                await ctx.channel.send(f"*The hint is dm'ed to you ,check that*")
            else:
                await ctx.channel.send("*You don't have enough coins to buy hint*")
        else:
            await ctx.channel.send("*You can only use these commands in game channel*")

    @gtw.command(name="status")
    async def gtw_status(self,ctx):
        if ctx.channel.id==self.game_channel.id:
            stat=ctx.gaw_game.player_status(ctx.author)
            lives="❤️"*stat[0]+"🖤"*(3-stat[0])
            embed=discord.Embed(title=f"{ctx.author.name}'s Status",
            description=f"Lives Lift:{lives} \n Points:{stat[1]}",colour=0xff0000)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("*You can only use these commands in game channel*")

    @gtw.command(name="buylife")
    async def gtw_buy(self,ctx):
        if ctx.channel.id==self.game_channel.id:
            stat=ctx.gaw_game.player_status(ctx.author)
            if stat[0]<=3 and stat[1]>30:
                stat=ctx.gaw_game.buy_life(ctx.author)
                lives="❤️"*stat[0]+"🖤"*(3-stat[0])
                embed=discord.Embed(title=f"{ctx.author.name}'s Status",
                description=f"Lives Lift:{lives} \n Points:{stat[1]}",colour=0xff0000)
                await ctx.channel.send(embed=embed)

            elif stat[1]<30:
                await ctx.channel.send("*You don't have enough points to buy life*")
            else:
                await ctx.channel.send("*You already have full life*")
        else:
            await ctx.channel.send("*You can only use these commands in game channel*")

    @gtw.command(name="end")
    async def gtw_end(self,ctx):
        if ctx.channel.id==self.game_channel.id:
            self.join_allowance=True
            self.current_round=1
            self.game_channel=discord.channel.TextChannel
            self.hint=""
            stat=ctx.gaw_game.leaderboard()
            embed=discord.Embed(title="**Leaderboards**",
            description=f"**Name : Points**\n\n*{stat}*\n",
            colour=0xff0000)
            await self.main_channel.send(embed=embed)
            await ctx.gaw_game.destroy(ctx.guild,ctx.channel.id)
        else:
            await ctx.channel.send("*You can only use these commands in game channel*")

    @gtw.command(name="rule")
    async def gtw_rule(self,ctx):
        desc=ctx.gaw_game.rule()
        embed=discord.Embed(title="**Guess the game Game Rules**",description=desc,colour=0xff0000)
        await ctx.channel.send(embed=embed)

    @gtw.command(name="leaderboard",aliases=["lb"])
    async def gtw_leaderboard(self,ctx):
        if ctx.channel.id==self.game_channel.id:
            stat=ctx.gaw_game.leaderboard()
            embed=discord.Embed(title="**Leaderboards**",
            description=f"**Name:Points**\n\n*{stat}*\n",
            colour=0xff0000)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("*You can only use these commands in game channel*")



def setup(client):
    client.add_cog(Games(client))