from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Bot version
BOT_VERSION = '0.0.1'

# List of cogs to be loaded
COG_LIST = ['admin', 'general', 'combat']

# Get the bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Get the super admin ID list
ADMIN_LIST = list(map(int, os.getenv("ADMIN_LIST").split(",")))

# MongoDB Credentials
MONGODB_URI = os.getenv('MONGODB_URI')

# Game config
MINI_BOSS_SPAWN_CHANCE = 0.1  # 10% chance for miniboss to spawn
