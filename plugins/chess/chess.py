"""

Copyright 2021 Akins

Apache License 2.0

ChessBot v7.1

"""

import typing
import random
import asyncio

import discord
from discord.ext import commands

from plugins.chess.data import Game, Participant

import utils

# from discord_slash.model import ButtonStyle
# from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

from replit import db

from functools import wraps

games = {}

embed_colors = [
  discord.Colour.green(),
  discord.Colour.blue(),
  discord.Colour.dark_purple(),
  discord.Colour.purple(),
  discord.Colour.blurple()
]
  
  
class Chess(commands.Cog):
  def __init__(self, bot):
    self.bot=bot


    self.games = {}
    
  @commands.command(
    name="play",
    aliases = [
      'p',
      'chess',
      'ch'
    ],
    description="Allows you to play a match of chess against another user.",
    brief="Allows you to play chess against someone.",
    usage="<member>"
  )
  async def _play(
    self,
    ctx: commands.Context,
    member: discord.Member
  ) -> discord.Message:

    if ctx.channel.id in self.games:
      pass

    # action_row = create_actionrow(
    #       create_button(style=ButtonStyle.green, label="Yes", custom_id="yes"),
    #       create_button(style=ButtonStyle.red, label="No", custom_id="no"),
    #     )
    

    message_obj = await ctx.channel.send(
      "{0}, would you like to play chess against {1}?".format(member.mention, ctx.author.mention)
    )
    
    emojis = ["✅", "❎"]
    
    for emoji in emojis:
      await message_obj.add_reaction(emoji)
    
    try:
      component = await self.bot.wait_for('reaction_add', check = lambda reaction, user: reaction.message == message_obj and reaction.emoji in emojis and user == member, timeout=180)
    except asyncio.TimeoutError:
      return await ctx.send("Request to play chess timed out.")
      
    if component[0].emoji == "❎":
      await ctx.send("Request to play chess denied.")
    
    channel = await utils.get_setup_type(ctx, "play", member)
    colors = utils.get_colors(ctx.author, member)
    game = Game(
      Participant(
        colors[0]
      ),
      Participant(
        colors[1]
      ),
      discord.utils.get(ctx.guild.channels, id=channel)
    )
    self.games[channel] = game
    
    return await discord.utils.get(ctx.guild.channels, id=channel).send(
      file=discord.File(fp=game.get_game_image(), filename="game.png"),
      embed = discord.Embed(
        color=random.choice(embed_colors)
      ).set_author(name="{}'s move".format(colors[0])).set_image(url="attachment://game.png")
    )
    
    
  @commands.command(
    name="move",
    aliases = [
      'm'
    ],
    description="Allows you to move in a game of chess.",
    brief="Allows you to move in chess.",
    usage="<move: uci>"
  )
  async def _move(
    self,
    ctx: commands.Context,
    move: str
  ) -> discord.Message:
    if self.games[ctx.channel.id].get_move_user().id != ctx.author.id:
      pass
    if ctx.channel.id not in self.games:
      pass
    game = self.games[ctx.channel.id]
    await game.make_move(move)
    return await game.channel.send(
      file=discord.File(fp=game.get_game_image(), filename="game.png"),
      embed = discord.Embed(
        color=random.choice(embed_colors)
      ).set_author(name="{}'s move".format(self.games[ctx.channel.id].get_move_user())).set_image(url="attachment://game.png")
    )
   
  
  
  @commands.command(
    name="resign",
    aliases = [
      'r'
    ],
    description="Allows you to resign in a game of chess.",
    brief="Resigns in a chess match.",
    usage=""
  )
  async def _resign(
    self,
    ctx: commands.Context
  ) -> discord.Message:
    if self.games[ctx.channel.id].get_move_user().id != ctx.author.id:
      pass
    if ctx.channel.id not in self.games:
      pass
    game = self.games[ctx.channel.id]
    return await game.end(5, 0.0, 1.0)
  
  @commands.command(
    name="draw",
    aliases = [
      'd'
    ],
    brief="Requests to draw a game of chess.",
    description="Allows you to draw in a game of chess."
  )
  async def _draw(
    self,
    ctx: commands.Context
  ) -> discord.Message:
    if self.games[ctx.channel.id].get_move_user().id != ctx.author.id:
      pass
    if ctx.channel.id not in self.games:
      pass

    game = self.games[ctx.channel.id]
     
#     action_row = create_actionrow(
#       create_button(style=ButtonStyle.green, label="Yes", custom_id="yes"),
#       create_button(style=ButtonStyle.red, label="No", custom_id="no"),
#     )
    
    message_obj = await ctx.send(
      "{0}, would you like to draw the match against {1}?".format(game.get_not_move_user().mention, ctx.author.mention)
    )
    
    emojis = ["✅", "❎"]
    
    for emoji in emojis:
      await message_obj.add_reaction(emoji)
    
    try:
      component = await self.bot.wait_for('reaction_add', check = lambda reaction, user: reaction.message == message_obj and reaction.emoji in emojis and user == game.get_not_move_user(), timeout=180)
    except asyncio.TimeoutError:
      return await ctx.send("Request to draw timed out.")
    
    if component[0].emoji == "❎":
      return await ctx.send("Request to draw denied.")
    
    return await game.end(2, 0.5, 0.5)

  @commands.command(
    name="elo",
    description="Returns the elo of a given chess user.",
    brief="Returns the elo of a user.",
    usage="<member>"
  )
  async def _elo(
    self,
    ctx: commands.Context,
    member: discord.Member = None
  ) -> discord.Message:
    if member == None:
      member=ctx.author
    
    if str(member.id) not in db["users"]:
      elo = 600
    else:
      elo = db["users"][str(member.id)]['elo']
   
    return await ctx.send(
      embed=discord.Embed(
        description="{0} - {1}".format(member.display_name, int(elo)),
        color=random.choice(embed_colors)
      ).set_author(name="Elo for user")
    ) 

  @commands.command(
    name="profile",
    description="Displays information on a user.",
    brief="Displays a user's profile.",
    usage="<member>"
  )
  async def _profile(
    self,
    ctx: commands.Context,
    member: discord.Member = None
  ) -> discord.Message:
    if member == None:
      member=ctx.author
    
    if str(member.id) not in db["users"]:
      elo = 600
      wins = 0
      losses = 0
      draws = 0
      status = "___"
      status_color = discord.Colour.green()
    else:
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

        
        # inline if else mess essentially defaults unset values.
        # elo = 600 if 'elo' not in db["users"][str(member.id)] else elo = db["users"][str(member.id)]['elo']
        # wins = 0 if 'wins' not in db["users"][str(member.id)] else wins = db["users"][str(member.id)]['wins']
        # losses = 0 if 'losses' not in db["users"][str(member.id)] else losses = db["users"][str(member.id)]['losses']
        # draws = 0 if 'draws' not in db["users"][str(member.id)] else draws = db["users"][str(member.id)]['draws']
        # status = "___" if 'status' not in db["users"][str(member.id)] else status = db["users"][str(member.id)]['status']
        # status_color = discord.Colour.green() if 'status_color' not in db["users"][str(member.id)] else status_color = db["users"][str(member.id)]['status_color']
  
    
    return await ctx.send(
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
        name="User profile"
      ).set_thumbnail(
        url=member.avatar_url
      )
    )
  
def setup(bot: commands.Bot):
  bot.add_cog(Chess(bot))
