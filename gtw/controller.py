import random
from .model import GuessAWord

games={

}
player_dict={

}
guessed_words=[

]
chnl=[]

class GuessAWordGame:

    current_game=None

    def rule(self):
        description='''In 'Guess the game' Game, Each player has 3 hearts and 50 points in start.
        The game has total of 7 rounds,In each round player has to guess the game by given hints\n
        **The correct guess will award +25 points**\n 
        **The wrong guess will deduct a life **\n
        **A hint costs 15 points **\n
        **A life costs 30 oints**\n
        **NOTE**:You need min 1 life to survive
        The person who has most points after 7 rounds will win\n
        To know about the commands type <prefix>help gtw.
        '''
        return description

    def leaderboard(self):
        leaderboards=""
        v=player_dict.values()
        temp=[]
        for x in v:
            temp.append(x[1])
        temp.sort(reverse=True)
        k=player_dict.keys()
        for x in temp:
            for y in v:
                if x==y[1]:
                    str_0=str(y[3])+":"+str(x)
                    leaderboards+=str_0
        return leaderboards

    def fetch_channel(self):
        return chnl

    def fetch_game(self):
        return self.current_game

    def fetch_player_status(self,player):
        return player_dict[player.id]

    def reduce_life(self,player):
        player_dict[player.id][0]-=1
        if player_dict[player.id][0]==0:
            player_dict[player.id][2]=False
        k=player_dict.keys()
        for x in k:
            if player_dict[x][2]==True:
                return False
            else:
                return True

    def player_status(self,player):
        return player_dict[player.id]
    
    def buy_life(self,player):
        player_dict[player.id][0]+=1
        player_dict[player.id][1]-=30
        return player_dict[player.id]
    
    def buy_hint(self,player):
        player_dict[player.id][1]-=15
        return player_dict[player.id]

    def win_reward(self,player):
        player_dict[player.id][1]+=25
    
    async def degrade_player_permission(self,player,channel):
        await channel.set_permissions(player,view_channel=True,send_messages=False)

    def get_game(self,channel_id):
        self.current_game=None
        for g in games.keys():
            if channel_id==g:
                self.current_game=games[g]
            
    def new_round(self,channel):
        self.current_game=None
        newgame=self.create_game_instane(channel.id,channel.name)
        self.save(newgame)
        self.get_game(channel.id)

    def guess(self,channel_id,guess):
        self.get_game(channel_id)
        if self.current_game is None:
            return None
        return self.current_game.guess(guess)

    def create_game_instane(self,channel_id,channel_name):
            while True:
                random_instance=self.get_random_word()
                if random_instance["word"] in guessed_words:
                    continue
                else:
                    guessed_words.append(random_instance["word"])
                    newgame=GuessAWord(random_instance["word"],random_instance["category"],random_instance["missing"],random_instance["hint"])
                    newgame.channel_id=channel_id
                    newgame.channel_name=channel_name
                    return newgame

    async def start_game(self,guild,author,category_name):
        channel_name=f"Guessthegame-hosted-by-{author.name}"
        existing_channel=self.get_channel_by_name(guild,channel_name)
        if existing_channel is None:
            await self.create_channel(guild,channel_name,category_name)
            channel=self.get_channel_by_name(guild,channel_name)
            await self.set_permissions(guild,channel)
            await self.set_player_permission(channel,author)
            
            self.channel_save(channel)

            newgame=self.create_game_instane(channel.id,channel.name)

            self.save(newgame)
            self.channel_save(channel)
            self.get_game(channel.id)

            return True
        return None

    def channel_save(self,chn):       
        chnl.append(chn)
        
    def save(self,game):
        games[game.channel_id]=game

    async def destroy(self,guild,channel_id):
        chnl.clear()
        guessed_words.clear()
        player_dict.clear()
        games.pop(channel_id)
        await self.delete_channel(guild, channel_id)

    async def delete_channel(self, guild, channel_id):
        """
        Deletes a text channel by its id
        """
        channel = guild.get_channel(channel_id)
        await channel.delete()

    async def set_permissions(self,guild,channel):

        await channel.set_permissions(guild.default_role,view_channel=False,send_messages=False)

        #Get channel object by channel……name
        
    async def set_player_permission(self,channel,player):
        await channel.set_permissions(player,view_channel=True,send_messages=True)
        player_dict[player.id]=[3,50,True,player.name]

    def get_channel_by_name(self, guild, channel_name):
        channel=None
        for c in guild.channels:
            
            if c.name == channel_name.lower():
                channel = c
                break
        return channel

    async def create_channel(self,guild,channel_name,category_name):
        await guild.create_text_channel(channel_name,category=category_name)

    def get_random_word(self):
        return random.choice([
            {
                "word":"PES",
                "category":"Sports",
                "missing":"………S",
                "hint":"Ball"
            },
            {
                "word":"PlayerUnknown's Battlegrounds",
                "category":"Battle Royale",
                "missing":"P…………U…………'s B…………………………s",
                "hint":"PUB"
            },
            {
                "word":"Resident evil",
                "category":"Story mode",
                "missing":"……e……si……e…… E……",
                "hint":"Also have movie and anime ig"
            },
            {
                "word":"Minecraft",
                "category":"Survival",
                "missing":"………………c…………t",
                "hint":"blocks"
            },
            {
                "word":"Pacman",
                "category":"classic",
                "missing":"P……………n",
                "hint":"maze with yellow ghosts but you have to eat"
            },
            {
                "word":"Among us",
                "category":"Classic",
                "missing":"…m……… ……",
                "hint":"red su....."
            },
            {
                "word":"Fortnite",
                "category":"Battle Royale",
                "missing":"………t……te",
                "hint":"You have to build"
            },
            {
                "word":"Apex Legends",
                "category":"Battle Royale",
                "missing":"…p…… …e………d…",
                "hint":"Pick your legend.."
            },
            {
                "word":"Grand Theft Auto",
                "category":"Open world",
                "missing":"G………… …h……… A………",
                "hint":"When is its 6th version releasing"
            },
            {
                "word":"Assassin's Creed",
                "category":"Open World",
                "missing":"………a……i…'… …r……d",
                "hint":"knife coming out of hand"
            },
            {
                "word":"Far Cry",
                "category":"Open World",
                "missing":"……e……si……e…… E……",
                "hint":"……… 😭"
            },
            {
                "word":"Ludo",
                "category":"Board games",
                "missing":"………o",
                "hint":"Four house on Four corner"
            },
            {
                "word":"snake and ladder",
                "category":"Board games",
                "missing":"s………… …n… …a……e…",
                "hint":"you climb up high but get eaten when 1 step left"
            },
            {
                "word":"Monopoly",
                "category":"Board games",
                "missing":"…o……p………",
                "hint":"Business"
            },
            {
                "word":"Hearthstone",
                "category":"Card game",
                "missing":"H………t…s………e",
                "hint":"Disguised Toast"
            },
            {
                "word":"League of legends",
                "category":"Moba",
                "missing":"L…………… o… …e………d…",
                "hint":"Worlds"
            },
            {
                "word":"Valorant",
                "category":"Fps",
                "missing":"……l……a……",
                "hint":"VCT"
            },
            {
                "word":"Chess",
                "category":"Board games",
                "missing":"…h………",
                "hint":"Black and white tiles"
            },
            {
                "word":"Clash of Clan",
                "category":"strategy",
                "missing":"……a…… o… …l……",
                "hint":"I am having 2 builder"
            },
            {
                "word":"Forza Horizon",
                "category":"Racing game",
                "missing":"F………… H…r………",
                "hint":"Published by Xbox Game studio"
            },
            {
                "word":"Counter Strike",
                "category":"FPS",
                "missing":"C……………… S……………e",
                "hint":"Plant on A"
            },
            {
                "word":"Trackmania",
                "category":"Racing Game",
                "missing":"…r………m………",
                "hint":"Ubisoft game"
            },
            {
                "word":"UNO",
                "category":"Board game",
                "missing":"…N…",
                "hint":"Reverse"
            },
            {
                "word":"Vice city",
                "category":"open World",
                "missing":"V……… C………",
                "hint":"COMEFLYWITHME,PANZER"
            },
            {
                "word":"Detroit",
                "category":"Open World",
                "missing":"D……r………",
                "hint":"Human and Robots"
            },
            {
                "word":"Candy Crush",
                "category":"Match 3",
                "missing":"…a……… C…………",
                "hint":"🍫"
            },
            {
                "word":"Bejeweled",
                "category":"Match 3",
                "missing":"B………w……e…",
                "hint":"💎"
            },
            {
                "word":"Rocket League",
                "category":"Car game",
                "missing":"R………e… …e…………",
                "hint":"⚽🚗"
            },
            {
                "word":"Mario",
                "category":"Platform",
                "missing":"…a………",
                "hint":"Legenderay games back in days"
            },
            {
                "word":"Roblox",
                "category":"RP game",
                "missing":"R………o…",
                "hint":"NO REALSTIC GRAPHICS,KIDS CAN PLAY(MOSTLY THEY LOVE),RP,FPS"
            }
          

            
        ])
