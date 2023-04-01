from config import BOT_TOKEN, COG_LIST, BOT_VERSION
from bot import AdventureRPG


# Create custom bot instance
bot = AdventureRPG(version=BOT_VERSION)

# Load the cogs
bot.load_cogs(COG_LIST)

# Start the bot
bot.run(BOT_TOKEN)
