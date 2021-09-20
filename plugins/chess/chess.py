import typing

import discord
from discord.ext import commands

from plugins.chess.data import Game, Participant

import utils

from discord_slash import cog_ext, SlashContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component

embed_colors = [
  discord.Colour.green(),
  discord.Colour.blue(),
  discord.Colour.dark_purple(),
  discord.Colour.purple(),
  discord.Colour.blurple()
]

# decoraters
def no_current_games(
  func,
  class: Chess
) -> typing.Any:
  def wrapper(*args, **kwargs) -> None:
    if args[1].channel.id in class.games:
      pass
    else:
      func(*args, **kwargs)
  return wrapper
 
# decoraters
def not_against_self(
  func
) -> typing.Any:
  def wrapper(*args, **kwargs) -> None:
    if args[2].id == args[1].author.id:
      pass
    else:
      func(*args, **kwargs)
  return wrapper
  

def in_game(
  func,
  class: Chess
) -> typing.Any:
  def wrapper(*args, **kwargs) -> None:
    if args[1].channel.id not in class.games:
      pass
    else:
      func(*args, **kwargs)
  return wrapper  
  
def is_turn(
  func,
  class: Chess
) -> typing.Any:
  def wrapper(*args, **kwargs) -> None:
    if class.games[args[1].channel.id].get_move_user().id != args[1].author.id:
      pass
    else:
      func(*args, **kwargs)
  return wrapper
  
  
class Chess(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot=bot
    self.games = {}
    
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
  @no_current_games(self)
  @not_against_self
  async def _play(
    self,
    ctx: SlashContext,
    member: discord.Member
  ) -> discord.Message:
    action_row = create_actionrow(
          create_button(style=ButtonStyle.green, label="Yes", custom_id="yes"),
          create_button(style=ButtonStyle.red, label="No", custom_id="no"),
        )
    
    message_obj = await message.channel.send(
      "{0}, would you like to play chess against {1}?".format(member.mention, ctx.author.mention),
      components=[
        action_row
      ]
    )
    
    component = await wait_for_component(self.bot, components=action_row)
    
    if component.custom_id == "no":
      return await ctx.send("Request to play chess denied.")
    
    channel = await get_setup_type(ctx, "play", member)
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
        "required"=True
      }
    ]
  )
  @in_game(self)
  @is_turn(self)
  async def _move(
    self,
    ctx: SlashContext,
    move: str
  ) -> discord.Message:
    game = self.games[ctx.channel.id]
    await game.move(move)
   
  
  
  @cog_ext.cog_slash(
    name="resign",
    description="Allows you to resign in a game of chess."
  )
  @in_game(self)
  @is_turn(self)
  async def _resign(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    game = games[ctx.channel.id]
    return await game.end(5, 0.0, 1.0)
  
  @cog_ext.cog_slash(
    name="draw",
    description="Allows you to draw in a game of chess."
  )
  @in_game(self)
  @is_turn(self)
  async def _draw(
    self,
    ctx: SlashContext
  ) -> discord.Message:
    game = games[ctx.channel.id]
     
    action_row = create_actionrow(
      create_button(style=ButtonStyle.green, label="Yes", custom_id="yes"),
      create_button(style=ButtonStyle.red, label="No", custom_id="no"),
    )
    
    message_obj = await message.channel.send(
      "{0}, would you like to draw the match against {1}?".format(member.mention, ctx.author.mention),
      components=[
        action_row
      ]
    )
    
    component = await wait_for_component(self.bot, components=action_row)
    
    if component.custom_id == "no":
      return await ctx.send("Request to draw denied.")
    return await game.end(2, 0.5, 0.5)

def setup(bot: commands.Bot):
  bot.add_cog(Chess(bot))
