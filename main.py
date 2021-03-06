"""

Copyright 2021 Akins

Apache License 2.0

ChessBot v7.0

"""


import os

import discord
from discord.ext import commands

from discord_slash import SlashCommand

from replit import db

if "users" not in db:
  db["users"] = {}

if "guilds" not in db:
  db["guilds"] = {}

if "game_id" not in db:
  db["game_id"] = 1  
  
bot = commands.Bot(
  command_prefix="ch!",
#   self_bot=True, #silences all attempts at handling message commands
  help_command=None, #silences discord default help commands
  description="A Chess bot for discord that uses an elo rating system.",
)

slash = SlashCommand(bot, sync_commands=True)

def main():
  cogs = [
    'plugins.core.errors.on_command_error',
    'plugins.core.startup.on_ready',
    'plugins.chess.chess',
    'plugins.general.commands', # a general cog for commands to avoid overcategorization
    'plugins.core.help'
  ]
  for cog in cogs:
    bot.load_extension(cog)
    
  bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
  main()
