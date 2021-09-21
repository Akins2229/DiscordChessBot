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
          create_choice(
            name="Categories",
            value=3
          )
        ],
        option_type=4,
        required=True
      ),
      create_option(
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
    channel: discord.TextChannel
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
        title="Github repository",
        url="https://github.com/Akins2229/DiscordChessBot/",
        color=discord.Colour.blue()
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
    
    member = ctx.author
    
    if 'elo' in db["users"][str(member.id)]:
      elo = db["users"][str(member.id)]['elo']
    else:
      elo = 600

    if 'wins' in db["users"][str(member.id)]:
      wins = db["users"][str(member.id)]['wins']
    else:
      wins = 0

    if 'losses' in db["users"][str(member.id)]:
      losses = db["users"][str(member.id)]['losses']
    else:
      losses = 0

    if 'draws' in db["users"][str(member.id)]:
      draws = db["users"][str(member.id)]['draws']

    else: 
      draws = 0

    if 'status' in db["users"][str(member.id)]:
      status = db["users"][str(member.id)]['status']
    else:
       status = "___"

    if 'status_color' in db["users"][str(member.id)]:
      status_color = db["users"][str(member.id)]['status_color']
    else:
      status_color = discord.Colour.green()
    
    return await ctx.channel.send(
      embed=discord.Embed(
        description=status,
        color=status_color
      ).add_field(
        name="Elo",
        value=elo
      ).add_field(
        name="Wins",
        value=wins
      ).add_field(
        name="Losses",
        value=losses
      ).add_field(
        name="Draws",
        value=draws
      ).set_author(
        name="Changed Status!"
      ).set_thumbnail(
        url=ctx.author.avatar_url
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
            value=0x2ECC71
          ),
          create_choice(
            name="Red",
            value=0xE74C3C
          ),
          create_choice(
            name="Purple",
            value=0x71368A
          ),
          create_choice(
            name="Gold",
            value=0xF1C40F
          )
        ],
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
    
    member = ctx.author

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
    
    
    if 'elo' in db["users"][str(member.id)]:
      elo = db["users"][str(member.id)]['elo']
    else:
      elo = 600

    if 'wins' in db["users"][str(member.id)]:
      wins = db["users"][str(member.id)]['wins']
    else:
      wins = 0

    if 'losses' in db["users"][str(member.id)]:
      losses = db["users"][str(member.id)]['losses']
    else:
      losses = 0

    if 'draws' in db["users"][str(member.id)]:
      draws = db["users"][str(member.id)]['draws']

    else: 
      draws = 0

    if 'status' in db["users"][str(member.id)]:
      status = db["users"][str(member.id)]['status']
    else:
       status = "___"

    if 'status_color' in db["users"][str(member.id)]:
      status_color = db["users"][str(member.id)]['status_color']
    else:
      status_color = discord.Colour.green()
    
    return await ctx.channel.send(
      embed=discord.Embed(
        description=status,
        color=status_color
      ).add_field(
        name="Elo",
        value=elo
      ).add_field(
        name="Wins",
        value=wins
      ).add_field(
        name="Losses",
        value=losses
      ).add_field(
        name="Draws",
        value=draws
      ).set_author(
        name="Changed Status!"
      ).set_thumbnail(
        url=ctx.author.avatar_url
      )
    )
  
def setup(bot: commands.Bot):
  bot.add_cog(Commands(bot))
