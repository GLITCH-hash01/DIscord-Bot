from datetime import datetime
import discord, os, json, random
from discord.ext import commands, tasks
from discord.ui import Button, button, View
from discord.interactions import Interaction
from discord.ext.commands.errors import CommandNotFound, MissingPermissions, MissingRequiredArgument
"""
Functions
"""


def get_prefix(client, message):
    with open("./Cogs/Json/prefixes.json", "r") as f:
        prefixes = json.load(f)
        pre = prefixes[str(message.guild.id)]
        prefixlist = [pre]
    return prefixlist


def when_mentioned_or_function(func):
    def inner(client, message):
        r = func(client, message)
        r = commands.when_mentioned(client, message) + r
        return r

    return inner


"""
Client intializing
"""
client = commands.Bot(
    command_prefix=when_mentioned_or_function(get_prefix),
    help_command=commands.help.MinimalHelpCommand(no_category="Others"))
"""
Events
"""


@client.event
async def on_ready():
    logs.start()
    print("Bot is online")
    await client.change_presence(activity=discord.Game("p1help"))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.channel.send(
            random.choice([
                "*Sorry,I don't know any command like that*",
                "**404 no such command**",
                "*Oops!Don't know about that command*"
            ]))
    elif isinstance(error, MissingPermissions):
        await ctx.send(
            "*Sorry,You Don't have enough permissions to use this command,Ask the admin for perms before using next time*"
        )
    elif isinstance(error, MissingRequiredArgument):
        await ctx.channel.send("*Missing Arguments*")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.channel.send("Pls try again after a min")
    else:
        print(error)


@client.event
async def on_guild_join(guild):
    with open("./Cogs/Json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "p1"

    with open("./Cogs/Json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=5)


@client.event
async def on_guild_remove(guild):
    with open("./Cogs/Json/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open("./Cogs/Json/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=5)


class view_0(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="0", custom_id="counter_button")
    async def creator(self, button: Button, interaction: Interaction):
        label = int(button.label)
        label += 1
        button.label = str(label)
        await interaction.response.edit_message(view=self)

    @button(label="1", custom_id="counter_button_0", style=4)
    async def creator_0(self, button: Button, interaction: Interaction):
        label = int(button.label)
        label += 1
        button.label = str(label)
        await interaction.response.send_message("Text",
                                                ephemeral=True,
                                                view=view_0())


"""
Commmands
"""


@client.command()
async def test(ctx):
    await ctx.send("Button", view=view_0())


for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")
    else:
        pass


@tasks.loop(minutes=15)
async def logs():
    time_now = datetime.now().strftime('%Y:%m:%d %H:%M:%S %Z %z')
    with open("logs.txt", "a") as f:
        f.write(f"[{time_now}] The server is alive!\n")
    print(f"[{time_now}] The server is alive!")


Token = "TOKEN"
keep_alive()client.run(Token)
