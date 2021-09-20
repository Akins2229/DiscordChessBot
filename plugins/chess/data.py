import discord
from discord.ext import commands

from discord_slash import cog_ext, SlashContext

import chess
import chess.svg

from replit import db
from cairosvg import svg2png

class IllegalMoveError:
  def __init__(
    self,
    move: str
  ) -> None:
    self.msg = "The move {} you attempted is not a legal move.".format(move)
    
  def __repr__(self) -> str:
    return self.msg
  
class InvalidMoveFormatError:
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
    
  @property
  def elo(
    self
  ) -> int:
    if str(self.user.id) in db["users"]:
      return int(db["users"][str(self.user.id)]["elo"])
    
    else:
      return 600
    
  def add_elo(
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
    channel: discord.Channel
  ) -> None:
    self.white=white
    self.black=black
    
    self.board=chess.Board()
    
    id = db["game_id"] += 1
    
    self.channel=channel
    
  def get_game_image(
    self
  ) -> str:
    cairosvg.svg2png(bytestring=chess.svg.board(self.board, size=800), write_to="assets/games/{}.png".format(self.id))
    return 'assets/games/{}.png'.format(self.id)
  
  
  def move(
    self,
    move: str
  ) -> None:
    try:
      move_obj = move=chess.Move.from_uci(move)
      if move not in self.board.legal_moves:
        raise IllegalMoveError(move)
      self.board.push(move_obj)
    except:
      raise InvalidMoveFormatError(move)
