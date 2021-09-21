"""

Copyright 2021 Akins

Apache License 2.0

ChessBot v7.0

"""

import random
import typing

import discord

from discord_slash import SlashContext
from replit import db

class MustBePassedInGuild(Exception):
  def __init__(self, command_name: str) -> None:
    self.message="Command {} must be passed within a guild (server)."
  
  def __repr__(self) -> str:
    return self.message
    
async def get_setup_type(
  ctx: SlashContext,
  command_name: str,
  member: str
) -> int:
  if not ctx.guild:
    raise MustBePassedInGuild(command_name)
  
  else:
    if str(ctx.guild.id) not in db["guilds"]:
      return ctx.channel.id
    
    elif db["guilds"][str(ctx.guild.id)]["type"] == 1:
      channel = discord.get_channel(db["guilds"][str(ctx.guild.id)]["channel"])
      thread = await channel.create_thread(name="{0} v. {1}".format(ctx.author.display_name, member.display_name))
      return thread
    
    elif db["guilds"][str(ctx.guild.id)]["type"] == 2:
      channel = discord.get_channel(db["guilds"][str(ctx.guild.id)]["channel"])
      return channel
    
    elif db["guilds"][str(ctx.guild.id)]["type"] == 3:
      category = discord.utils.get(ctx.guild.categories, id=db["guilds"][str(ctx.guild.id)]["category"])
      channel = await ctx.guild.create_text_channel("{} v. {}".fromat(ctx.author.display_name, member.display_name), category=category)
      return channel

    
def get_colors(
  member_one: discord.Member,
  member_two: discord.Member
) -> typing.Tuple[discord.Member, discord.Member]:
  choices = [member_one, member_two]
  black = random.choice(choices)
  for choice in choices:
    if choice.id == black.id:
      choices.remove(choice)
  return (choices[0], black)
