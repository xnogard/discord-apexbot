import discord
from discord.ext import commands
import requests

# Replace with your actual Discord bot token
DISCORD_TOKEN = ''
# Replace with your actual Mozambique API key
API_KEY = ''
# Discord API Application ID
DISCORD_APP_ID = ''

# Initialize the bot with slash command support
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, application_id=DISCORD_APP_ID)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Function to fetch the player's rank from api.mozambiquehe.re
def get_player_rank(player_name, platform="PC"):
    # URL for Mozambique API (replace with correct platform and player name)
    url = f'https://api.mozambiquehe.re/bridge?version=1&platform={platform}&player={player_name}&auth={API_KEY}'

    # Send request to Mozambique API
    response = requests.get(url)
    rp = "No data"
    nr = "No data"
    bkill = "No data"
    gp = "No data"

    if response.status_code == 200:
        data = response.json()

        # Check if player data exists in the response
        if 'global' in data:
            # Find ranked stats in the 'segments' field
            if data['global']['rank']['rankedSeason'] == "br_ranked":

                # Extract the rank and tier information
                rank = data['global']['rank']['rankName']
                tier = data['global']['rank']['rankDiv']
                desc = f"Current rank is {rank} {tier}"

                if 'rankScore' in data['global']['rank']: 
                    rp = data['global']['rank']['rankScore']
                if 'rankScore' in data['global']['rank']: 
                    nr  = f"{data['global']['toNextLevelPercent']}%"
                if 'kills' in data['total']: 
                    bkill = data['total']['kills']['value']
                if 'games_played' in data['total']: 
                    gp = data['total']['games_played']['value']

                embed = discord.Embed(title=data['global']['name'], url="", description=desc, color=0xFF5733)
                embed.set_thumbnail(url=data['global']['rank']['rankImg'])
                embed.add_field(name="RP", value=rp, inline=True)
                embed.add_field(name="Next Rank", value=nr, inline=True)
                embed.add_field(name="Kills", value=bkill, inline=True)
                embed.add_field(name="Games", value=gp, inline=True)
                embed.set_footer(text="Last played legend is " + data['legends']['selected']['LegendName'])

                return embed
        return "Player not found or no ranked data available."
    else:
        return f"Error: Could not retrieve player data (Status Code: {response.status_code})."

def get_map():
    url = f'https://api.mozambiquehe.re/maprotation?auth={API_KEY}&version=2'

    # Send request to Mozambique API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

    embed = discord.Embed(title=data['ranked']['current']['map'], description="Current Ranked map and next rotation.", color=0xFF5733)
    embed.set_thumbnail(url=data['ranked']['current']['asset'])
    embed.add_field(name="Next Map", value=data['ranked']['next']['map'])
    embed.set_footer(text="Time Remaining: " + data['ranked']['current']['remainingTimer'])
    return embed


# Slash Command to get player's rank
@bot.slash_command(name="rank", description="Get Apex Legends player's rank")
async def rank(ctx, player_name: str, platform: str = "PC"):
    """Fetch and display Apex Legends player's rank"""
    data = get_player_rank(player_name, platform)
    await ctx.response.send_message(embed=data)

# Slash Command to get map rotation
@bot.slash_command(name="map", description="Get Apex Legends map rotation")
async def map(ctx):
    """Fetch and display Apex Legends map rotation"""
    data = get_map()
    await ctx.response.send_message(embed=data)

# Run the bot
bot.run(DISCORD_TOKEN)
