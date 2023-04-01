from classes.character import Player
import discord


# Custom ApplicationContext to store player data
class PlayerApplicationContext(discord.ApplicationContext):
    def __init__(self, bot, interaction):
        super().__init__(bot, interaction)
        self.player = None

    def set_player(self, player: Player):
        self.player = player


class AdventureRPG(discord.Bot):
    '''Custom subclass of discord.Bot for AdventureRPG'''

    def __init__(self, version: str):
        super().__init__()
        self.version = version

    async def on_ready(self):
        print('---=---=---=---=---=---=---=---')
        print(f'AdventureRPG v{self.version}')
        print(f'{self.user} is up and running!')
        print('---=---=---=---=---=---=---=---')

    async def get_application_context(
        self, interaction: discord.Interaction, cls=PlayerApplicationContext
    ):
        return await super().get_application_context(interaction, cls=cls)

    def load_cogs(self, cog_list: list[str]):
        print('Adding cogs ....')
        for cog in cog_list:
            print(f' (+) {cog} is loaded')
            super().load_extension(f'cogs.{cog}')
        print(f'{len(cog_list)} cog(s) loaded successfully')
