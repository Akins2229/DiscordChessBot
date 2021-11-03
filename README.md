<h1 align="center">ChessBot for Discord</h1>
<p align="center">
    <a href="https://chessbot.readthedocs.io/en/latest/?badge=latest"><img width="100" src="https://user-images.githubusercontent.com/82357502/134055704-b7bf7cc7-f5ba-428f-811a-78567ce10669.png"/></a>
</p>
<p align="center">
    <br>
    <br>
    <a href="https://chessbot.readthedocs.io/en/latest/?badge=latest">
        <img src="https://readthedocs.org/projects/chessbot/badge/?version=latest" alt='Documentation Status'/>
    </a>
    <a href="https://discord.com/api/oauth2/authorize?client_id=864611397736726599&permissions=8&scope=bot%20applications.commands">
        <img src="https://user-images.githubusercontent.com/82357502/134057791-f9996005-b1be-47b1-8ab3-d685cf1dd905.png" alt="Bot invite"/>
    </a>

</p>
<hr>

## Usage

### Commands

**Chess**

- [play](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/chess/chess.py#L44) `[member: discord.Member]` - allows you to play a match of chess against a given user; [no_current_games](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L25), [not_against_self](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L37)
- [move](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/chess/chess.py#L106) `[move: str (uci)]` - allows you to move in a currently running match of chess; [in_game](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L48)
- [resign](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/chess/chess.py#L126) - allows you to resign from the current match of chess; [in_game](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L48)
- [draw](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/chess/chess.py#L143) - allows you to offer the opponent a draw in a match of chess; [in_game](https://github.com/Akins2229/DiscordChessBot/blob/0805751272f3339971044f4de59519eb82509d55/plugins/chess/chess.py#L48)
- [elo](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/chess/chess.py#L182) `[member: discord.Member]` - allows you to get the elo of another user.
- [profile](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/chess/chess.py#L208) `[member: discord.Member]` - displays the ChessBot profile of another user.

**General**

- [setup](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/general/commands.py#L37) `[type: int (choices)]` `[channel: discord.Channel (optional)]` - sets up the server for Chess Bot usage.
- [github](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/general/commands.py#L109) - returns a link to this Github repository
- [set-status](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/general/commands.py#L139) `[status: str]` - sets your status to appear on your Chess Bot profile.
- [set-status-color](https://github.com/Akins2229/DiscordChessBot/blob/7812b1b483c31836f961970cd64837ee7ebcf273/plugins/general/commands.py#L226) `[color: int (0x hexadecimal)]` - allows you to set the color that appears on your ChessBot profile. 

### Prefix

The bot's prefix is "ch!". 

## TODO - v7.1.0

- ~~better account system~~
- [ ] help command
- [ ] global elo leaderboard
- ~~guild system to increase reasoning for competition~~
- ~~add voice channel support~~
