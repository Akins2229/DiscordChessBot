echo "Installing Libraries..."

echo -en "------\r"
pip install discord.py &> /dev/null
echo  -en "x-----\r"
pip install discord-py-interactions &> /dev/null  
echo  -en "xx----\r"
pip install python-chess &> /dev/null 
echo  -en "xxx---\r"
pip install DiscordUtils &> /dev/null 
echo  -en "xxxx--\r"
pip install replit &> /dev/null 
echo  -en "xxxxx-\r"
pip install cairosvg &> /dev/null 
echo  -en "xxxxxx\r"
echo "      "

echo "Libraries Installed."
echo "-------------------------"

python3 main.py