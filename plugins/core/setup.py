import discord
from discord.ext import commands
from replit import db

class Setup(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Setup category:\n=============="

  @commands.command(
    name="setup",
    brief="Sets up the server to use chess bot",
    description="Decides how Chess bot is used within the server based on a given type.",
    usage="<type>"
  )
  async def setup(self, ctx, type, *, channel: discord.TextChannel=None):
    if type == 'channel':
      if channel == None:
        return await ctx.send("You must provide a channel for the bot to use.")
      else:
        if str (ctx.guild.id) not in db:
          db[str(ctx.guild.id)] = {}
        
        if 'chess' not in db[str(ctx.guild.id)]:
          db[str(ctx.guild.id)]['chess'] = {}
        if 'type' not in db[str(ctx.guild.id)]['chess']:
          db[str(ctx.guild.id)]['chess']['type'] = type
        db[str(ctx.guild.id)]['chess']['type'] = type
        db[str(ctx.guild.id)]['chess']['channel'] = str(channel.id)
        await channel.send("This channel will now be used for chess bot activities.")
    if type == 'category':
          if str(ctx.guild.id) not in db:
            db[str(ctx.guild.id)] = {}
          if 'chess' not in db[str(ctx.guild.id)]:
            db[str(ctx.guild.id)]['chess'] = {}
          if 'type' not in db[str(ctx.guild.id)]['chess']:
              db[str(ctx.guild.id)]['chess']['type'] = type
          category = await ctx.guild.create_category("Chess")
          channel = await ctx.guild.create_text_channel('commands', category=category)
          db[str(ctx.guild.id)]['chess']['category'] = str(category.id)
          await channel.send("This category will now be used for chess bot activites.")
    if type == 'threads':
      if channel == None:
        return await ctx.send("You must provide a channel for the bot to use.")
      else:
        if str(ctx.guild.id) not in db:
          db[str(ctx.guild.id)] = {}
        if 'chess' not in db[str(ctx.guild.id)]:
            db[str(ctx.guild.id)]['chess'] = {}
        
        if 'type' not in db[str(ctx.guild.id)]['chess']:
            db[str(ctx.guild.id)]['chess']['type'] = type
        else:
            db[str(ctx.guild.id)]['chess']['type'] = type
        db[str(ctx.guild.id)]['chess']['channel'] = channel.id
        await channel.send("This channel will now be the home for all threads created by the chess bot.")

def setup(bot):
  bot.add_cog(Setup(bot))