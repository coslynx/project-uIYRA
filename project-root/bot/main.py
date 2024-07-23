import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import psycopg2
import redis

from utils.config_utils import load_config
from utils.database_utils import connect_to_database

load_dotenv()
config = load_config()

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['DEFAULT_PREFIX'], intents=intents)

# Connect to PostgreSQL database
db_connection = connect_to_database(config['DATABASE_URL'])
db_cursor = db_connection.cursor()

# Connect to Redis cache
redis_client = redis.Redis.from_url(config['REDIS_URL'])

# Load cogs
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Load cogs
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Run the bot
bot.run(config['DISCORD_TOKEN'])