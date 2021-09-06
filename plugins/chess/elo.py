import discord, utils
from discord.ext import commands
from replit import db

class Elo(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Elo category:\n=============="

  @commands.command(
    name="register",
    aliases=[
      'reg',
      'register-user', 
      'ru',
      'register_user'
    ],
    brief="Registers a user",
    description="Attempts to register a user for the bot.",
    usage="<avatar: png: attach>"
  )
  async def register(self, ctx):
    if ctx.guild:
      await ctx.message.delete()
      return await ctx.send("You must use this command in direct messages with the bot")
    await ctx.send("What would you like your username to be")
    username_state = False
    while username_state==False:
      input = await self.bot.wait_for('message', check=lambda message: message.channel==ctx.channel and message.author==ctx.author)
      username=input.content
      try:
        utils.Users.create_username(username)
        username_state = True
        continue
      except Exception as err:
        return await ctx.send(
          embed = discord.Embed(
            description=f"```{err}```",
            color = discord.Colour.dark_purple()
          ).set_author(name="Bot Error")
        )
        continue
    await ctx.send("What would you like your password to be?")
    password_state = False
    while password_state==False:
      input = await self.bot.wait_for('message', check=lambda message: message.channel==ctx.channel and message.author == ctx.author)
      password=input.content
      try:
        utils.Users.create_password(password)
        password_state = True
        continue
      except Exception as err:
        return await ctx.send(
          embed = discord.Embed(
            description=f"```{err}```",
            color = discord.Colour.dark_purple()
          ).set_author(name="Bot Error")
        )
        continue
    token = utils.Users.get_token()
    if len(ctx.message.attachments) == 0:
      avatar_path = 'assets/avatars/default.png'
    else:
      if str(ctx.message.attachments[0]).endswith('.png'):
        await ctx.message.attachments[0].save(fp=f"assets/avatars/{token}.png")
        avatar_path = f"assets/avatars/{token}.png"
      else:
        return await ctx.send("You did not attach a valid png file.")
      try:
        user = utils.User(
          token,
          username,
          password,
          avatar_path
          )
      except Exception as e:
        raise utils.UnknownError()
      try:
        utils.Users.register_user(ctx.author, user)
      except Exception as e:
        raise utils.UnknownError()
      await ctx.send("User successfully registered.")

  @commands.command(
    name="get_user",
    aliases=[
      'get-user',
      'getuser',
      'gu',
      'ge',
      'elo',
      'get-elo',
      'get_elo'
    ],
    brief="Return data about a user.",
    description="Returns data about a specific user.",
    usage="<member: discord.Member: optional>"
  )
  async def get_user(self, ctx, member: discord.Member=None):
    if member==None:
      member = ctx.author
    string = ''
    if str(member.id) not in db:
      return await ctx.send("This user has no registered accounts.")
    else:
      accounts = {}
      account_usernames = {}
      for token in db[str(member.id)]['tokens'].split():
        accounts[token] = db[str(token)]['username']
        account_usernames[db[str(token)]['username']] = token
      for token in accounts:
        string+=f"\n{accounts[token]}"
      message = await ctx.send(
        embed=discord.Embed(
          description=f"```{string}```",
          color = discord.Colour.dark_purple()
        ).set_footer(
          text="Select an account"
        )
      )
      input_state = True
      while input_state == True:
        input = await self.bot.wait_for('message', check=lambda message: message.channel==ctx.channel and message.author==ctx.author, timeout=60)
        try:
          token = account_usernames[input.content]
        except:
          await ctx.send("This is not a valid account")
          continue
        input_state=False
        continue
      try:
        elo = utils.Users.get_elo(token)
      except:
        elo = "unrated"
      await ctx.send(
        file=discord.File(db[token]['avatar'], filename='avatar.png'),
        embed=discord.Embed(
          color=discord.Colour.dark_purple()
        ).set_author(name=db[token]['username'], icon_url="attachment://avatar.png").add_field(name="Elo", value=elo, inline=False).add_field(name="Wins", value=db[token]['wins'], inline=False).add_field(name="Losses", value=db[token]['losses'], inline=False)
      )

  @commands.command(
    name="delete-user",
    aliases=[
      'de',
      'delete_user',
      'delete'
    ],
    brief="Deletes a user",
    description="Deletes a given user given the token",
    usage="<token>"
  )
  async def delete_user(self, ctx):
    string=''
    member = ctx.author
    if str(member.id) not in db:
      return await ctx.send("This user has no registered accounts.")
    else:
      accounts = {}
      account_usernames = {}
      for token in db[str(member.id)]['tokens'].split():
        accounts[token] = db[str(token)]['username']
        account_usernames[db[str(token)]['username']] = token
      for token in accounts:
        string+=f"\n{accounts[token]}"
      message = await ctx.send(
        embed=discord.Embed(
          description=f"```{string}```",
          color = discord.Colour.dark_purple()
        ).set_footer(
          text="Select an account"
        )
      )
      input_state = True
      while input_state == True:
        input = await self.bot.wait_for('message', check=lambda message: message.channel==ctx.channel and message.author==ctx.author, timeout=60)
        try:
          token = account_usernames[input.content]
        except:
          await ctx.send("This is not a valid account")
          continue
        input_state=False
        continue
      del db[token]
      db [str(member.id)]['tokens'] = db[str(member.id)]['tokens'].relace(token, '')
      await ctx.send(
        embed=discord.Embed(
          description=f"```Account {input.content} has been deleted!```",
          color=discord.Colour.dark_purple()
        )
      )

  @commands.command(
    name="login",
    aliases=[
      'log-in',
      'log_in',
      'li'
      ],
      brief="Logs into an already existing account.",
      description="Will log you into an already existing account given the username and password.",
      usage=""
  )
  async def _login(self, ctx):
    usernames = {}
    if ctx.guild:
      return await ctx.send("This command must be passed in DMs")
    for token in db.keys():
      try:
        if 'username' not in db[token]:
          continue
        usernames[db[token]['username']] = token
      except:
        continue
    await ctx.send("Input your username.")
    username = await self.bot.wait_for('message', check=lambda message: message.channel==ctx.channel and message.author==ctx.author)
    if username.content not in usernames:
      return await ctx.send("There is no account under this username.")
    await ctx.send("Input your password.")
    password = await self.bot.wait_for('message', check=lambda message: message.channel==ctx.channel and message.author==ctx.author)
    if password.content != db[usernames[username.content]]['password']:
      return await ctx.send("This password is not correct.")
    else:
      if str(ctx.author.id) not in db.keys():
        db[str(ctx.author.id)] = {}
      if 'tokens' not in db[str(ctx.author.id)]:
        db[str(ctx.author.id)]['tokens'] = ''
      db[str(ctx.author.id)]['tokens'] += f' {usernames[username.content]}'

def setup(bot):
  bot.add_cog(Elo(bot))