"""

Copyright 2021 Akins

Apache License 2.0

ChessBot v7.0

"""

import typing
import discord
from discord.ext import commands

# from discord_slash import cog_ext, SlashContext

import chess
import chess.svg

from replit import db
import cairosvg

import utils

game_endings = {
  1: "Win by checkmate.",
  2: "Draw by agreement.",
  3: "Draw by stalemate",
  4: "Draw by fivefold repition.",
  5: "Loss by resignation"
}

#prep for possible switch to brownie point algorithm

# import typing, math

# def points(
#   i: int,
#   j: int
# ) -> typing.Tuple[int, int]:
#   k = int(math.sqrt(i + j))
#   point_factor = abs(round((i+j/((200 * k) - i + j)))-(i+j/((200 * k) - i + j)))
#   return (i + (k * point_factor), j - (k * point_factor)) # value[0] = i, value[1] = j


class InCheckError(Exception):
  def __init__(
    self,
    move: str
  ) -> None:
    self.msg = "You cannot make move {} because you are in check.".format(move)
    
  def __repr__(self) -> str:
    return self.msg

class IllegalMoveError(Exception):
  def __init__(
    self,
    move: str
  ) -> None:
    self.msg = "The move {} you attempted is not a legal move.".format(move)
    
  def __repr__(self) -> str:
    return self.msg
  
class InvalidMoveFormatError(Exception):
  def __init__(
    self,
    move: str
  ) -> None:
    self.msg = "The move {} you attempted is in an invalid move format.".format(move)
    

  def __repr__(self) -> str:
    return self.msg 

class Participant:
  def __init__(
    self,
    discord_user: discord.Member
  ) -> None:
    self.user = discord_user

    # self.id = discord_user.id
    
    self.post_elo = 0
    
  @property
  def elo(
    self
  ) -> int:
    if str(self.user.id) in db["users"]:
      return int(db["users"][str(self.user.id)]["elo"])
    
    else:
      return 600
    
  def add_points(
    self,
    points: float
  ) -> None:
    if str(self.user.id) in db["users"]:
      db["users"][str(self.user.id)]["elo"] += points
    
    else:
      db["users"][str(self.user.id)] = {}
      db["users"][str(self.user.id)]["elo"] = 600.0 + points

class Game:
  def __init__(
    self,
    white: Participant,
    black: Participant,
    channel: discord.TextChannel
  ) -> None:
    self.white=white
    self.black=black
    
    self.board=chess.Board()
    
    self.id = db["game_id"] + 1
    db["game_id"] += 1
    
    self.channel=channel
    
    self.move = True
    
  def get_game_image(
    self
  ) -> str:
    cairosvg.svg2png(bytestring=chess.svg.board(self.board, size=800), write_to="assets/games/{}.png".format(self.id))
    return 'assets/games/{}.png'.format(self.id)
  
  def validate_position(
    self
  ) -> typing.Tuple[int, float, float]:
    if self.board.is_checkmate():
      return (1, 1.0, 0.0)
    elif self.board.is_stalemate():
      return (3, 0.5, 0.5)
    elif self.board.is_fivefold_repetition():
      return (4, 0.5, 0.5)
    else:
      return (0, 0.0, 0.0)
  
  async def make_move(
    self,
    move: str
  ) -> None:
    try:
      move_obj = move=chess.Move.from_uci(move)
      if move not in self.board.legal_moves:
        raise IllegalMoveError(move)
      self.board.push(move_obj)
      self.move = not self.move
      if self.validate_position()[0] == 0:
        pass
      else:
        self.end(self.validate_position()[0], self.validate_position()[1], self.validate_position()[2])
    except:
      if self.board.is_check():
        raise InCheckError(move)
      raise InvalidMoveFormatError(move)

  def get_move_user(
   self
  ) -> discord.Member:
    if self.move == True:
      return self.white.user
    else:
      return self.black.user

  def get_not_move_user(
   self
  ) -> discord.Member:
    if self.move == False:
      return self.white.user
    else:
      return self.black.user

  def get_move_participant(
   self
  ) -> discord.Member:
    if self.move == True:
      return self.white
    else:
      return self.black

  def get_not_move_participant(
   self
  ) -> discord.Member:
    if self.move == False:
      return self.white
    else:
      return self.black

  async def end(
    self,
    type: int,
    member_1_score: float,
    member_2_score: float
  ) -> discord.Message:
    member_1 = self.get_move_participant()
    member_2 = self.get_not_move_participant()

    if str(member_1.id) not in db:
      utils.register_database_user(member_1.id)

    if str(member_2.id) not in db:
      utils.register_database_user(member_2.id)
    
    if member_1_score == 1.0: db[str(member_1.id)]['wins'] = db[str(member_1.id)]['wins'] + 1
    if member_2_score == 1.0: db[str(member_2.id)]['wins'] = db[str(member_2.id)]['wins'] + 1
    
    if member_1_score == 0.0: db[str(member_1.id)]['losses'] = db[str(member_1.id)]['losses'] + 1
    if member_2_score == 0.0: db[str(member_2.id)]['losses'] = db[str(member_2.id)]['losses'] + 1
    
    if member_1_score == 0.5: db[str(member_1.id)]['draws'] = db[str(member_1.id)]['draws'] + 1
    if member_2_score == 0.5: db[str(member_2.id)]['draws'] = db[str(member_2.id)]['draws'] + 1
    
    member_1.add_points(18.5 * (1 / (1 + 10 ** ((member_2.elo - member_1.elo) / 400))) - member_1_score)
    member_2.add_points(18.5 * (1 / (1 + 10 ** ((member_1.elo - member_2.elo) / 400))) - member_2_score)
    
    return await self.channel.send(
      file=discord.File(fp=self.get_game_image(), filename="game.png"),
      embed=discord.Embed(
        description=game_endings[type],
        color = discord.Colour.green()
      ).set_author(name="Chess Match End.").add_field(name=member_1.user.display_name, value=member_1.elo).add_field(name=member_2.user.display_name, value=member_2.elo)
    )
