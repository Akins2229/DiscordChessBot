import typing
import random

import discord
from discord.ext import commands

from plugins.chess.data import Game, Participant

import utils

from discord_slash import cog_ext, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

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
  def __init__(self, bot: commands.Bot):
    self.bot=bot
    
  @cog_ext.cog_slash(
    name="play",
    description="Allows you to play a match of chess against another user.",
    options = [
      {
        "name": "member",
        "description": "Member you would like to play Chess against.",
        "type": 7,
        "required": True
      } 
    ]
  )
  async def _play(
    self,
    ctx: SlashContext,
    member: discord.Member
  ) -> discord.Message:

    if member.id == ctx.author.id:
      pass

    if ctx.channel.id in games:
      pass

    action_row = create_actionrow(
          create_button(style=ButtonStyle.green, label="Yes", custom_id="yes"),
          create_button(style=ButtonStyle.red, label="No", custom_id="no"),
        )
    

    message_obj = await ctx.channel.send(
      "{0}, would you like to play chess against {1}?".format(member.mention, ctx.author.mention),
      components=[
        action_row
      ]
    )
    
    component = await wait_for_component(self.bot, components=action_row)
    
    if component.custom_id == "no":
      return await ctx.send("Request to play chess denied.")
    
    channel = await utils.get_setup_type(ctx, "play", member)
    colors = utils.get_colors(ctx.author, member)
    game = Game(
      Participant(
        colors[0]
      ),
      Participant(
        colors[1]
      ),
      channel
    )
    self.games[channel.id] = game
    
    return await channel.send(
      file=discord.File(fp=game.get_game_image(), filename="game.png"),
      embed = discord.Embed(
        color=random.choice(embed_colors)
      ).set_author(name="{}'s move".format(colors[0])).set_image(url="attachment://game.png")
    )
    
    
  @cog_ext.cog_slash(
    name="move",
    description="Allows you to move in a game of chess.",
    options=[
      {
        "name": "move",
        "description": "The move you want to move in uci format ex: e2e4",
        "type": 4,
        "required": True
      }
    ]
  )
  async def _move(
    self,
    ctx: SlashContext,
    move: str
  ) -> discord.Message:
    if games[ctx.channel.id].get_move_user().id != ctx.author.id:
      pass
    if ctx.channel.id not in games:
      pass
    game = self.games[ctx.channel.id]
    await game.move(move)
   
  
  
  @cog_ext.cog_slash(
    name="resign",
    description="Allows you to resign in a game of chess."
  )
  async def _resign(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    if games[ctx.channel.id].get_move_user().id != ctx.author.id:
      pass
    if ctx.channel.id not in games:
      pass
    game = self.games[ctx.channel.id]
    return await game.end(5, 0.0, 1.0)
  
  @cog_ext.cog_slash(
    name="draw",
    description="Allows you to draw in a game of chess."
  )
  async def _draw(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    if games[ctx.channel.id].get_move_user().id != ctx.author.id:
      pass
    if ctx.channel.id not in games:
      pass

    game = games[ctx.channel.id]
     
    action_row = create_actionrow(
      create_button(style=ButtonStyle.green, label="Yes", custom_id="yes"),
      create_button(style=ButtonStyle.red, label="No", custom_id="no"),
    )
    
    message_obj = await ctx.channel.send(
      "{0}, would you like to draw the match against {1}?".format([game.white.user, game.black.user].remove(ctx.author).mention, ctx.author.mention),
      components=[
        action_row
      ]
    )
    
    component = await wait_for_component(self.bot, components=action_row)
    
    if component.custom_id == "no":
      return await ctx.send("Request to draw denied.")
    return await game.end(2, 0.5, 0.5)

  @cog_ext.cog_slash(
    name="elo",
    description="Returns the elo of a user.",
    options = [
      {
        "name": "member",
        "description": "Member you would like to play Chess against.",
        "type": 7,
        "required": False
      } 
    ]
  )
  async def _elo(
    self,
    ctx: SlashContext,
    member: discord.Member
  ) -> discord.Message:
    if not member:
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

  @cog_ext.cog_slash(
    name="profile",
    description="Displays information on a user.",
    options = [
      {
        "name": "member",
        "description": "The user to display the information of.",
        "type": 7,
        "required": False
      }
    ]
  )
  async def _profile(
    self,
    ctx: SlashContext,
    member: discord.Member
  ) -> discord.Message:
    if not member:
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
      
      
    
    #premptive message (made in class I'll finish this later)
    
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
        name="User profile"
      ).set_thumbnail(
        url=member.avatar_url
      )
    )
  
def setup(bot: commands.Bot):
  bot.add_cog(Chess(bot))
