import discord, utils, os
from discord.ext import commands
from replit import db

if 'game_id' not in db:
  db['game_id'] = 1

if 'tokens' not in db:
  db['tokens'] = []

bot = commands.Bot(
  command_prefix = utils.get_prefix,
  case_insensitive=True,
  description="A Chess Bot for Discord that uses a custom Elo rating system.",
  owner_id=707643377621008447,
  help_command=None,
  strip_after_prefix=True
)

@bot.event
async def on_ready():
  print("BOT STATUS - ONLINE\nDEVELOPED BY AKINS (C) 2021\nChess Bot v6.2.3")

plugins = [
  'plugins.chess.elo', 
  'plugins.chess.chess',
  'plugins.core.setup',
  'plugins.core.help',
  'plugins.core.on_command_error'
]

if __name__ == '__main__':
  for cog in plugins:
    bot.load_extension(cog)

bot.run(os.getenv("TOKEN"))