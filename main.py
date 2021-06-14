import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

token = "YOUR TOKEN"

bot = commands.Bot(command_prefix="-", intents=intents)

extensions = ['cogs.chatmoderator']

bot.load_extension(extensions[0])

bot.run(token)
