"""

Copyright 2021 Akins

Apache License 2.0

ChessBot v7.0

"""

import typing

import discord
from discord.ext import commands

class OnCommandError(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot=bot
    
  @commands.Cog.listener()
  async def on_command_error(
    self,
    ctx: commands.Context,
    exception: typing.Any
  ) -> discord.Message:
    return await ctx.send(
      embed=discord.Embed(
        description="```\n{}```".format(exception),
        color=discord.Colour.red()
      ).set_author(name="Slash Command Error")
    )
  
def setup(bot: commands.Bot):
  bot.add_cog(OnCommandError(bot))