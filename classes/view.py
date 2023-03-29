from discord import User, Member, Interaction, Embed
from discord.ui import View
import typing


class ProtectedView(View):
    '''Prevent misauthorized interaction'''

    def __init__(self, author: typing.Union[User, Member], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id == self.author.id

    async def on_check_failure(self, interaction: Interaction) -> None:
        await interaction.response.send_message(
            'You are not permitted to interact with that.', ephemeral=True
        )
