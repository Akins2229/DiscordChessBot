import discord, errors
from discord.ext import commands

class OnCommandError(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name=""

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    await ctx.send(
      embed=discord.Embed(
        description=f"```py\n{error}```",
        color=discord.Colour.dark_blue()
      ).set_author(
        name="Bot Error"
      )
    )

def setup(bot):
  bot.add_cog(OnCommandError(bot))