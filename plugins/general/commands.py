import discord
from discord.ext import commands

from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from replit import db


class InvalidTypeError(Exception):
  def __init__(self, type: int) -> None:
    self.msg="Type of {} is not a valid type. Please use option choices or an integer less than 4.".format(type)
    
  def __repr__(self) -> str:
    return self.msg


class Commands(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot=bot
    
  @cog_ext.cog_slash(
    name="setup",
    description="Allows you to set up a server for ChessBot usage.",
    options = [
      create_option(
        name="type",
        description="Type of setup you would like to do.",
        choices = [
          create_choice(
            name="Threads",
            value=1
          ),
          create_choice(
            name="Channels",
            value=2
          ),
          create_option(
            name="Categories",
            value=3
          )
        ],
        option_type=4,
        required=True
      ),
      create_options(
        name="channel",
        description="The channel you want to use when using ChessBot (for use in Threads and Channels types.",
        option_type=7,
        required=False
      )
    ]
  )
  async def _setup(
    self,
    ctx: SlashContext,
    type: int,
    channel: discord.Channel
  ) -> discord.Message:
    if channel:
      if type == 1:
        db["guilds"][str(ctx.guild.id)] = {}
        db["guilds"][str(ctx.guild.id)]["channel"] = channel.id
        db["guilds"][str(ctx.guild.id)]["type"] = type
        
        return await channel.send(
          "Guild set up for ChesBot usage! Use this channel for chess bot commands."
        )
      elif type == 2:
        db["guilds"][str(ctx.guild.id)] = {}
        db["guilds"][str(ctx.guild.id)]["channel"] = channel.id
        db["guilds"][str(ctx.guild.id)]["type"] = type
        
        return await channel.send(
          "Guild set up for ChesBot usage! Use this channel for chess bot commands."
        )
      else:
        raise InvalidTypeError(type)
        
    else:
      if type == 3:
        category = await ctx.guild.create_category_channel("ChessBot")
        db["guilds"][str(ctx.guild.id)] = {}
        db["guilds"][str(ctx.guild.id)]["category"] = category.id
        db["guilds"][str(ctx.guild.id)]["type"] = type
        
        return await channel.send(
          "Guild set up for ChesBot usage! Use this channel for chess bot commands."
        )
      else:
        raise InvalidTypeError(type)
        

  @cog_ext.cog_slash(
    name="github",
    description="Returns a link to the bot's github repository."
  )
  async def _github(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    return await ctx.send(
      embed=discord.Embed(
        color=discord.Colour.blue()
      ).set_author(
        name="Github.com/Akins2229/DiscordChessBot",
        url="https://github.com/Akins2229/DiscordChessBot"
      ).set_image(
        url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
      )
    )
  
  @cog_ext.cog_slash(
    name="set-status",
    description="Allows you to set your status to appear on your profile.",
    options = [
      create_option(
        name="status",
        description="The status you want to appear on your ChessBot profile.",
        option_type=3,
        required=True
      )
    ]
  )
  async def _set_status(
    self,
    ctx: SlashContext,
    status: str
  ) -> discord.Message:
    if str(ctx.author.id) not in db["users"]:
      db["users"][str(ctx.author.id)] = {}
      db["users"][str(ctx.author.id)]['elo'] = 600
      db["users"][str(ctx.author.id)]['wins'] = 0
      db["users"][str(ctx.author.id)]['losses'] = 0
      db["users"][str(ctx.author.id)]['draws'] = 0
      db["users"][str(ctx.author.id)]['status_color'] = discord.Colour.green()
    db["users"][str(ctx.author.id)]['status'] = status
    
    #
    # Return Profile
    #
    
    
    #inline if mess to set non-existing values to default values
    elo = db["users"][str(member.id)]['elo'] if 'elo' in db["users"][str(member.id)] else elo = 600
    wins = db["users"][str(member.id)]['wins'] if 'wins' in db["users"][str(member.id)] else wins = 0
    losses = db["users"][str(member.id)]['losses'] if 'losses' in db["users"][str(member.id)] else losses = 0
    draws = db["users"][str(member.id)]['draws'] if 'draws' in db["users"][str(member.id)] else draws = 0
    status = db["users"][str(member.id)]['status'] if 'status' in db["users"][str(member.id)] else status = "___"
    status_color = db["users"][str(member.id)]['status_color'] if 'status_color' in db["users"][str(member.id)] else status_color = discord.Colour.green()
    
    return await ctx.channel.send(
      embed=discord.Embed(
        description=status,
        color=status_color
      ).add_field(
        title="Elo",
        value=elo
      ).add_field(
        title="Wins",
        value=wins
      ).add_field(
        title="Losses",
        value=losses
      ).add_field(
        title="Draws",
        value=draws
      ).set_author(
        name="Changed Status!"
      ).set_thumbnail(
        url=member.avatar_url
      )
    )
  
  @cog_ext.cog_slash(
    name="set-status-color",
    description="Allows you to set the color that appears on your status.",
    options = [
      create_option(
        name="color",
        description="The color you want to appear on your profile (int 0x format)",
        option_type=4,
        choices = [
          create_choice(
            name="Green",
            value=discord.Colour.green()
          ),
          create_choice(
            name="Red",
            value=discord.Colour.red()
          ),
          create_choice(
            name="Purple",
            value=discord.Colour.dark_purple()
          ),
          create_option(
            name="Gold",
            value=discord.Colour.gold()
          )
        ]
        required=False
      )
    ]
  )
  async def _set_status_color(
    self,
    ctx: SlashContext,
    color: int
  ) -> discord.Message:
    if not color:
      color=discord.Colour.green()
    
        if str(ctx.author.id) not in db["users"]:
      db["users"][str(ctx.author.id)] = {}
      db["users"][str(ctx.author.id)]['elo'] = 600
      db["users"][str(ctx.author.id)]['wins'] = 0
      db["users"][str(ctx.author.id)]['losses'] = 0
      db["users"][str(ctx.author.id)]['draws'] = 0
      db["users"][str(ctx.author.id)]['status'] = "___"
    db["users"][str(ctx.author.id)]['status_color'] = color
    
    
    #
    # Return Profile
    #
    
    
    #inline if mess to set non-existing values to default values
    elo = db["users"][str(member.id)]['elo'] if 'elo' in db["users"][str(member.id)] else elo = 600
    wins = db["users"][str(member.id)]['wins'] if 'wins' in db["users"][str(member.id)] else wins = 0
    losses = db["users"][str(member.id)]['losses'] if 'losses' in db["users"][str(member.id)] else losses = 0
    draws = db["users"][str(member.id)]['draws'] if 'draws' in db["users"][str(member.id)] else draws = 0
    status = db["users"][str(member.id)]['status'] if 'status' in db["users"][str(member.id)] else status = "___"
    status_color = db["users"][str(member.id)]['status_color'] if 'status_color' in db["users"][str(member.id)] else status_color = discord.Colour.green()
    
    return await ctx.channel.send(
      embed=discord.Embed(
        description=status,
        color=status_color
      ).add_field(
        title="Elo",
        value=elo
      ).add_field(
        title="Wins",
        value=wins
      ).add_field(
        title="Losses",
        value=losses
      ).add_field(
        title="Draws",
        value=draws
      ).set_author(
        name="Changed Status!"
      ).set_thumbnail(
        url=member.avatar_url
      )
    )
  
def setup(bot: commands.Bot):
  bot.add_cog(Commands(bot))
