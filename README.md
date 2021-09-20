# ChessBot



A Chess Bot Made in Python using discord.py and python-chess.

## Usage

### Commands

**Chess**

- [play](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L76) `[member: discord.Member]` - allows you to play a match of chess against a given user; [no_current_games](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L25), [not_against_self](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L37)
- [move](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L133) `[move: str (uci)]` - allows you to move in a currently running match of chess; [in_game](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L48), chess_channels_only
- [resign](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L157) - allows you to resign from the current match of chess; [in_game](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L48), chess_channels_only
- [draw](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L170) - allows you to offer the opponent a draw in a match of chess; [in_game](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L48), chess_channels_only
- [elo](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L200) `[member: discord.Member]` - allows you to get the elo of another user.
- [profile]() `[member: discord.Member]` - displays the ChessBot profile of another user.

**General**

- [setup]() `[type: int (choices)]` `[channel: discord.Channel (optional)]` - sets up the server for Chess Bot usage.
- [github]() - returns a link to this Github repository
- [set-status]() `[status: str]` - sets your status to appear on your Chess Bot profile. 

### Prefix

This bot does not have a prefix. It uses only slash commands.

## TODO - v7.0.1

- better account system
- global elo leaderboard
- guild system to increase reasoning for competition
- add voice channel support
