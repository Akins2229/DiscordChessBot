"""

Copyright 2021 Akins

Apache License 2.0

ChessBot v7.0

"""

import discord
from discord.ext import commands

class OnReady(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_ready(self) -> None:
    return print(
      "BOT STATUS - ONLINE\nDEVELOPED BY AKINS (C) 2021\nChess Bot v7.0"
    )

def setup(bot: commands.Bot):
  bot.add_cog(OnReady(bot))
