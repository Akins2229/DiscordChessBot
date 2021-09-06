import discord, utils, chess, random
from discord.ext import commands
from replit import db

games = {}

class Chess(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Chess category:\n=============="

  @commands.command(
    name="play",
    aliases=[
      'ch',
      'chess',
      'p'
    ],
    brief="Lets you play chess against another user.",
    description="Allows you to play a match of chess against another user using a given account.",
    usage='<member: discord.Member> <type: optional: ranked or casual defaults to casual>'
  )
  async def _play(self, ctx, member: discord.Member):
      setup_type = utils.validate_guild(ctx.guild)
      if ctx.author.id == member.id:
        return await ctx.send("You cannot play a match of chess against yourself.")
      if not ctx.guild:
        return await ctx.send("This command must be passed in a server.")
      author_token = await utils.select_account(ctx, self.bot, ctx.author)
      reactions = ['✅', '❎']
      message_object = await ctx.send(f"{member.mention} - Would you like to participate in a match against {ctx.author.mention}?\n✅- YES\n❎ - NO")
      for reaction in reactions:
        await message_object.add_reaction(reaction)
      reaction = await self.bot.wait_for('reaction_add', check=lambda reaction, user:   reaction.message==message_object and user==member and reaction.emoji in reactions)
      if reaction[0].emoji == '❎':
        return
      member_token = await utils.select_account(ctx, self.bot, member)
      if member_token == author_token:
        return await ctx.send("You cannot play a match against a person using the same account")
      if setup_type == 'channel':
        channel = db[str(ctx.guild.id)]['chess']['channel']
      elif setup_type == 'category':
        category=discord.utils.get(ctx.guild.categories, name="CHESS")
        channel = await ctx.guild.create_text_channel(f'{ctx.author.display_name}-vs-{member.display_name}'.lower(), category=category)
      elif setup_type == 'threads':
        if ctx.channel.id != db[str(ctx.guild.id)]['chess']['channel']:
          return await ctx.send("You must pass play commands in the chess bot channel that was setup <#{}>".format(db[str(ctx.guild.id)]['chess']['channel']))
        else:
          message_thread = await ctx.send("Game beginning...")
          channel = await ctx.channel.create_thread("{0} v. {1}".format(ctx.author.display_name, member.display_name), message_thread)
          await channel.add_user(ctx.author)
          await channel.add_user(member)
      if str(channel.id) in db:
        return await ctx.send("There is already an active match in this channel, this one will be postponed until further notice.")
      board = utils.Board(chess.Board(), db['game_id']+1)
      db['game_id']+=1
      player_1 = utils.Player(author_token, ctx.author)
      player_2 = utils.Player(member_token, member)
      player_1_dict = {'player': player_1}
      player_2_dict = {'player': player_2}
      players = [player_1_dict, player_2_dict]
      white_dict = random.choice(players)
      players.remove(white_dict)
      black_dict = random.choice(players)
      white = white_dict['player']
      black = black_dict['player']
      game = utils.Game(white, black)
      games[str(channel.id)] = {}
      games[str(channel.id)]['board'] = board
      games[str(channel.id)]['game'] = game
      games[str(channel.id)]['move_string'] = ""
      await channel.send(
        file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
        embed = discord.Embed(
          description = f'```\n{white.member.display_name}\'s move```',
          color=discord.Colour.dark_blue()
        ).set_image(url="attachment://game_{}.png".format(board.id))
      )

  @commands.command(
    name="move",
    aliases=[
      'm'
    ],
    brief="Allows you to move in a chess game.",
    description="Allows you to move in the currently running chess game.",
    usage="<move>"
  )
  async def _move(self, ctx, move):
    
    
    if str(ctx.channel.id) not in games:
      return await ctx.send("There is not a game currently running in this channel.")
    
    
    board = games[str(ctx.channel.id)]['board']
    game = games[str(ctx.channel.id)]['game']
    move_string = games[str(ctx.channel.id)]['move_string']

    if game.move == 'white':
      
      
      if ctx.author != game.white.member:
        
        
        return await ctx.send("It is not your turn, or you are not in the game.")
      
      
      move = board.create_move(move)
      
      
      board.move(move)
      move_string+=f"{move}->"
      
      
      pos = board.validate_position()
      
      
      if pos == 1:
        move_string+=f"checkmate"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(True, game.white, game.black)
        db[game.white.token]['elo'] = elo_dict['one_elo']
        db[game.black.token]['elo'] = elo_dict['two_elo']
        game.move='black'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\n{game.white.member.display_name} win by checkmate.\n{game.white.member.display_name} - {elo_dict["one_elo"]}\n{game.black.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )
      if pos == 2:
        move_string+=f"draw"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(False, game.white, game.black)
        db[game.white.token]['elo'] = elo_dict['one_elo']
        db[game.black.token]['elo'] = elo_dict['two_elo']
        game.move='black'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\nDraw by stalemate\n{game.white.member.display_name} - {elo_dict["one_elo"]}\n{game.black.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )
      if pos == 3:
        move_string+=f"draw"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(False, game.white, game.black)
        db[game.white.token]['elo'] = elo_dict['one_elo']
        db[game.black.token]['elo'] = elo_dict['two_elo']
        game.move='black'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board 
        games[str(ctx.channel.id)]['move_string'] = move_string       
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\nDraw by fivefold repition\n{game.white.member.display_name} - {elo_dict["one_elo"]}\n{game.black.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )
      if pos == 4:
        game.move='black'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board        
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\n{game.black.member.display_name}\'s move```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id)).set_footer(text="Black you are in check.")
        )
      await ctx.send(
        file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
        embed = discord.Embed(
          description = f'```\n{game.black.member.display_name}\'s move```',
          color=discord.Colour.dark_blue()
        ).set_image(url="attachment://game_{}.png".format(board.id))
      )
      game = utils.Game(game.white, game.black)
      games[str(ctx.channel.id)]['game'] = game
      games[str(ctx.channel.id)]['board'] = board
      games[str(ctx.channel.id)]['move_string'] = move_string   
      game.move='black'
    if game.move == 'black':
      if ctx.author != game.black.member:
        return await ctx.send("It is not your turn, or you are not in the game.")
      move = board.create_move(move)
      board.move(move)
      pos = board.validate_position()
      move_string+=f"{move}->"
      if pos == 1:
        move_string+=f"checkmate"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(True, game.black, game.white)
        db[game.black.token]['elo'] = elo_dict['one_elo']
        db[game.white.token]['elo'] = elo_dict['two_elo']
        game.move='white'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\n{game.black.member.display_name} win by checkmate.\n{game.black.member.display_name} - {elo_dict["one_elo"]}\n{game.white.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )
      if pos == 2:
        move_string+=f"draw"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(False, game.black, game.white)
        db[game.black.token]['elo'] = elo_dict['one_elo']
        db[game.white.token]['elo'] = elo_dict['two_elo']
        game.move='white'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\nDraw by stalemate\n{game.black.member.display_name} - {elo_dict["one_elo"]}\n{game.white.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )
      if pos == 3:
        move_string+=f"draw"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(False, game.black, game.white)
        db[game.black.token]['elo'] = elo_dict['one_elo']
        db[game.white.token]['elo'] = elo_dict['two_elo']
        game.move='white'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\nDraw by fivefold repition\n{game.black.member.display_name} - {elo_dict["one_elo"]}\n{game.white.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )
      if pos == 4:
        game.move='white'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\n{game.white.member.display_name}\'s move```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id)).set_footer(text="White you are in check.")
        )
      await ctx.send(
        file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
        embed = discord.Embed(
          description = f'```\n{game.white.member.display_name}\'s move```',
          color=discord.Colour.dark_blue()
        ).set_image(url="attachment://game_{}.png".format(board.id))
      )
      game = utils.Game(game.white, game.black)
      games[str(ctx.channel.id)]['game'] = game
      games[str(ctx.channel.id)]['board'] = board
      games[str(ctx.channel.id)]['move_string'] = move_string   
      game.move='white'
      
  @commands.command(
    name="draw",
    aliases=[
      'd'
    ],
    brief="Draws a match of chess.",
    description="Attempts to draw a match of chess.",
    usage=""
  )
  async def draw(self, ctx):
    if str(ctx.channel.id) not in games:
      return await ctx.send("There is not a game currently running in this channel.")
    
    
    board = games[str(ctx.channel.id)]['board']
    game = games[str(ctx.channel.id)]['game']
    move_string = games[str(ctx.channel.id)]['move_string']
    if game.move == 'white':
      if ctx.author != game.white.member:
        return await ctx.send("It is not your turn, or you are not in the game.")
      reactions = ['✅', '❎']
      message_object = await ctx.send(f"{game.black.member.mention} - Would you like to draw the current match against {ctx.author.mention}?\n✅- YES\n❎ - NO")
      for reaction in reactions:
        await message_object.add_reaction(reaction)
      reaction = await self.bot.wait_for('reaction_add', check=lambda reaction, user:   reaction.message==message_object and user==game.black.member and reaction.emoji in reactions)
      if reaction[0].emoji == '❎':
        return
      else:
        move_string+=f"draw"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
            f.write(move_string)
        elo_dict = utils.calculate_elo(False, game.white, game.black)
        db[game.white.token]['elo'] = elo_dict['one_elo']
        db[game.black.token]['elo'] = elo_dict['two_elo']
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\nDraw by agreement\n{game.white.member.display_name} - {elo_dict["one_elo"]}\n{game.black.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )          

  @commands.command(
    name="resign",
    aliases=[
      'r',
      'res'
    ],
    brief="Allows you to resign in a chess game.",
    description="Will allow a user to resign in a match of chess, giving their opponent a win.",
    usage=''
  )
  async def resign(self, ctx):
    if str(ctx.channel.id) not in games:
      return await ctx.send("There is not a game currently running in this channel.")
    
    
    board = games[str(ctx.channel.id)]['board']
    game = games[str(ctx.channel.id)]['game']
    move_string = games[str(ctx.channel.id)]['move_string']
    if game.move == 'white':
        if ctx.author != game.white.member:
          return await ctx.send("It is not your turn, or you are not in this game.")
        move_string+=f"resignation"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(True, game.black, game.white)
        db[game.black.token]['elo'] = elo_dict['one_elo']
        db[game.white.token]['elo'] = elo_dict['two_elo']
        game.move='white'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\n{game.black.member.display_name} win by resignation.\n{game.black.member.display_name} - {elo_dict["one_elo"]}\n{game.white.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )
    if game.move == 'black':
        if ctx.author != game.black.member:
          return await ctx.send("It is not your turn, or you are not in this game.")
        move_string+=f"resignation"
        with open('match_data/{}.chlog'.format(board.id), 'w+') as f:
          f.write(move_string)
        elo_dict = utils.calculate_elo(True, game.white, game.black)
        db[game.white.token]['elo'] = elo_dict['one_elo']
        db[game.black.token]['elo'] = elo_dict['two_elo']
        db[game.white.token]['wins']+=1
        db[game.black.token]['losses']+=2
        game.move='white'
        game = utils.Game(game.white, game.black)
        games[str(ctx.channel.id)]['game'] = game
        games[str(ctx.channel.id)]['board'] = board
        games[str(ctx.channel.id)]['move_string'] = move_string   
        return await ctx.send(
          file = discord.File(fp=board.get_game_image(), filename='game_{}.png'.format(board.id)),
          embed = discord.Embed(
            description = f'```\n{game.white.member.display_name} win by resignation.\n{game.white.member.display_name} - {elo_dict["one_elo"]}\n{game.black.member.display_name} - {elo_dict["two_elo"]}```',
            color=discord.Colour.dark_blue()
          ).set_image(url="attachment://game_{}.png".format(board.id))
        )

def setup(bot):
  bot.add_cog(Chess(bot))