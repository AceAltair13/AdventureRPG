from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Bot version
BOT_VERSION = '0.0.1'

# List of cogs to be loaded
COG_LIST = ['admin', 'fight']

# Get the bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Get the super admin ID list
SUPER_ADMIN_ID_LIST = list(map(int, os.getenv("SUPER_ADMIN_ID_LIST").split(",")))
