from config import BOT_TOKEN, COG_LIST, BOT_VERSION
import discord


class AdventureRPG(discord.Bot):
    '''Custom subclass of discord.Bot for AdventureRPG'''

    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print('===================================')
        print(f'AdventureRPG v{BOT_VERSION}')
        print(f'{self.user} is up and running!')
        print('===================================')

    def load_cogs(self, cog_list: list[str]):
        print('Loading cogs ....')
        for cog in cog_list:
            print(f' + {cog} is loaded')
            super().load_extension(f'cogs.{cog}')
        print(f'{len(cog_list)} cog(s) loaded successfully')


# Create custom bot instance
bot = AdventureRPG()

# Load the cogs
bot.load_cogs(COG_LIST)

# Start the bot
bot.run(BOT_TOKEN)
