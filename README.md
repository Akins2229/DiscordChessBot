# DiscordChessBot
A Chess Bot Made in Python using discord.py and python-chess.

## Usage

### Commands

**Chess**

- play `[member: discord.Member]` - allows you to play a match of chess against a given user; chess_channels_only
- move `[move: str (uci)]` - allows you to move in a currently running match of chess; in_game, chess_channels_only
- resign - allows you to resign from the current match of chess; in_game, chess_channels_only
- draw - allows you to offer the opponent a draw in a match of chess; in_game, chess_channels_only
- elo `[member: discord.Member]` - allows you to get the elo of another user.
- profile `[member: discord.Member]` - displays the ChessBot profile of another user.

**General**

- setup `[type: int (choices)]` `[channel: discord.Channel (optional)]` - sets up the server for Chess Bot usage.
- github - returns a link to this Github repository
- set-status `[status: str]` - sets your status to appear on your Chess Bot profile. 

### Prefix

This bot does not have a prefix. It uses only slash commands.

## TODO - v7.0.1

- better account system
- global elo leaderboard
- guild system to increase reasoning for competition
- add voice channel support
