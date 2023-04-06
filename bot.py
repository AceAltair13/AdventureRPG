import typing

from classes.character import Player
from discord.ui import View
from discord import User, Member, Interaction, Bot, ApplicationContext
from data import load_data


# Custom View to prevent non-authors to grief
class ProtectedView(View):
    '''Prevent unauthorized interaction'''

    def __init__(self, author: typing.Union[User, Member], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id == self.author.id

    async def on_check_failure(self, interaction: Interaction) -> None:
        await interaction.response.send_message(
            'You are not permitted to interact with that.', ephemeral=True
        )


# Custom ApplicationContext to store player data
class PlayerApplicationContext(ApplicationContext):
    def __init__(self, bot, interaction):
        super().__init__(bot, interaction)
        self.player = None

    def set_player(self, player: Player):
        self.player = player


class AdventureRPG(Bot):
    '''Custom subclass of discord.Bot for AdventureRPG'''

    def __init__(self, version: str):
        super().__init__()
        self.version = version
        self.game_data = load_data()

    async def on_ready(self):
        print('---=---=---=---=---=---=---=---')
        print(f'AdventureRPG v{self.version}')
        print(f'{self.user} is up and running!')
        print('---=---=---=---=---=---=---=---')

    async def get_application_context(
        self, interaction: Interaction, cls=PlayerApplicationContext
    ):
        return await super().get_application_context(interaction, cls=cls)

    def load_cogs(self, cog_list: list[str]):
        print('Adding cogs ....')
        for cog in cog_list:
            print(f' + {cog} is loaded')
            super().load_extension(f'cogs.{cog}')
        print(f'{len(cog_list)} cog(s) loaded successfully')
