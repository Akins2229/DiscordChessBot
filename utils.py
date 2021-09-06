from __future__ import division
import chess, chess.svg, cairosvg, discord, secrets
from replit import db

def expected(A, B):
    return 1 / (1 + 10 ** ((B - A) / 400))
  
def elo(old, exp, score, k=32):
    return old + k * (exp-score)

class NotSetupError(Exception):
  def __init__(self):
    self.message="This guild is not setup to use Chess Bot yet."
  def __str__(self):
    return self.message

class NotRatedError(Exception):
  def __init__(self):
    self.exc="User is not rated."
  def __str__(self):
    return self.exc

class NotRegisteredError(Exception):
  def __init__(self):
    self.exc="An unexpected error occured. The given token does not have a registered username"
  def __str__(self):
    return self.exc

class TokenExistsError(Exception):
  def __init__(self):
    self.exc="This token already exists"
  def __str__(self):
    return self.exc

class UsernameTakenError(Exception):
  def __init__(self):
    self.exc="This username is taken."
  def __str__(self):
    return self.exc

class InvalidCharacters(Exception):
  def __init__(self):
    self.exc="This username contains invalid characters."
  def __str__(self):
    return self.exc

class WeakPasswordError(Exception):
  def __init__(self):
    self.exc="This password is weak. It must be 8 characters or more."
  def __str__(self):
    return self.exc

class PasswordTooCommonError(Exception):
  def __init__(self):
    self.exc="This password is too common."
  def __str__(self):
    return self.exc

class AlreadyRegisteredError(Exception):
  def __init__(self):
    self.exc="This user is already registered."
  def __str__(self):
    return self.exc

class UnknownError(Exception):
  def __init__(self):
    self.exc="An Unknown error occured."
  def __str__(self):
    return self.exc

class MoveIllegalError(Exception):
  def __init__(self, move: chess.Move):
    self.message=f"Move \"{move}\" is not a legal move."
  def __str__(self):
    return self.message

class InvalidFormatError(Exception):
  def __init__(self):
    self.message="The format you attempted to use when making your move is not valid."
  def __str__(self):
    return self.message

class User():
  def __init__(self, token, username, password, avatar):
    self.username=Users.create_username(username)
    self.password=Users.create_password(password)
    self.token=token
    self.avatar=avatar

class Users():
  def __init__(self):
    self=self

  #gets a members elo
  def get_elo(token: str):
    if str(token) not in db:
      raise NotRegisteredError()
    else:
      if 'elo' not in db[str(token)]:
        return 600
      else:
        return db[str(token)]['elo']

  #creates a valid token
  def get_token():
    token_state = False
    while token_state == False:
      try:
        token = secrets.token_urlsafe(20)
        if token in db['tokens'].value:
          raise TokenExistsError()
        else:
          token_state=True
          continue
      except TokenExistsError:
        continue
    return token

  #checks if a username is valid
  def create_username(username: str):
    usernames = []
    for token in db.keys():
      try:
        if 'username' not in db[token]:
          continue
        usernames.append(token['username'])
      except:
        continue
    if username in usernames:
      raise UsernameTakenError()
    else:
      if '✅' in username:
        raise InvalidCharacters()
      else:
        return username

  def create_password(password: str):
    passwords = []
    for token in db:
      try:
        if 'password' not in db[str(token)]:
          continue
        passwords.append(db[token]['password'])
      except:
        continue
    n = 0
    for value in passwords:
      if value == password:
        n+=1
      else:
        continue
    if n > 5:
      raise PasswordTooCommonError()
    else:
      if len(password) < 8:
        raise WeakPasswordError()
    return password

  def delete_user(token):
    del db[str(token)]

  #registers a user
  def register_user(member: discord.Member, user: User):
    if str(user.token) in db:
      raise AlreadyRegisteredError()
    if str(member.id) not in db:
      db[str(member.id)] = {}
    if 'tokens' not in db:
      db['tokens'] = []
    if 'tokens' not in db[str(member.id)]:
      db[str(member.id)]['tokens'] = ''
    db[str(member.id)]['tokens'] += f' {user.token}'
    db[user.token] = {}
    db[user.token]['username'] = str(user.username)
    db[user.token]['password'] = str(user.password)
    db[user.token]['avatar'] = str(user.avatar)
    db[user.token]['wins'] = 0
    db[user.token]['losses'] = 0
    return "User registered successfully!"

def inverse_bool(value: bool):
  if value == True:
    response = False

  if value == False:
    response = True

  return response

class Player():
  def __init__(self, token: str, member: discord.Member):
    self.token = token
    self.name = db[token]['username']
    self.avatar = db[token]['avatar']
    self.wins = db[token]['wins']
    self.losses = db[token]['losses']
    self.elo = Users.get_elo(token)
    self.member = member

class Game():
  def __init__(self, white: Player, black: Player):
    self.white=white
    self.black=black
    self.move='white'

class Board():
  def __init__(self, board: chess.Board, id: int):
    self.board=board
    self.id=id

  def move(self, move: chess.Move):
    if move not in self.board.legal_moves:
      raise MoveIllegalError(move)
    else:
      self.board.push(move)

  def create_move(self, move: str):
    try:
      move = chess.Move.from_uci(move)
    except:
      raise InvalidFormatError()
    return move

  def validate_position(self):
    if self.board.is_checkmate():
      result = 1
      return result
    elif self.board.is_stalemate():
      result = 2
      return result
    elif self.board.is_fivefold_repetition():
      result = 3
      return result
    elif self.board.is_check():
      result = 4
      return result
    else:
      return
    
    
  def get_game_image(self):
    image = chess.svg.board(self.board, size=600)
    cairosvg.svg2png(bytestring=image, write_to='assets/games/{}.png'.format(self.id))
    return 'assets/games/{}.png'.format(self.id)

async def select_account(ctx, bot, member: discord.Member):
  string = ''
  if str(member.id) not in db:
    return await ctx.send("You have no registered accounts.")
  else:
    accounts = {}
    account_usernames = {}
    for token in db[str(member.id)]['tokens'].split():
      accounts[token] = db[str(token)]['username']
      account_usernames[db[str(token)]['username']] = token
    for token in accounts:
      string+=f"\n{accounts[token]}"
    message = await member.send(
      embed=discord.Embed(
        description=f"```{string}```",
        color = discord.Colour.dark_purple()
      ).set_footer(
        text="Select an account"
      )
    )
  account_state = False
  while account_state==False:
    input = await bot.wait_for('message', check=lambda message: not message.guild and message.author == member)
    try:
      token = account_usernames[input.content]
    except:
      await member.send("This is not a valid account")
      continue
    account_state=True
    continue
  return token

def validate_guild(guild: discord.Guild):
  if str(guild.id) not in db:
    raise NotSetupError()
  if 'chess' not in db[str(guild.id)]:
    raise NotSetupError()
  return db[str(guild.id)]['chess']['type']

def get_prefix(bot, message):
  if message.guild:
    try:
      prefix = db[str(message.guild.id)]['prefix']
    except:
      prefix = 'ch!'
  else:
    prefix = "ch!"
  return prefix

def calculate_elo(state: bool, player_1: Player, player_2: Player):
  if state == True:
    one_expected = expected(player_1.elo, player_2.elo)
    two_expected = expected(player_2.elo, player_1.elo)
    one_new_elo = elo(player_1.elo, one_expected, 1.0, k=32)
    two_new_elo = elo(player_2.elo, two_expected, 0, k=32)
    response = {
      'one_elo': int(one_new_elo),
      'two_elo': int(two_new_elo)
    }
    return response
  if state == False:
    one_expected = expected(player_1.elo, player_2.elo)
    two_expected = expected(player_2.elo, player_1.elo)
    one_new_elo = elo(player_1.elo, one_expected, 0.5, k=32)
    two_new_elo = elo(player_2.elo, two_expected, 0.5, k=32)
    response = {
      'one_elo': int(one_new_elo),
      'two_elo': int(two_new_elo)
    }    
    return response