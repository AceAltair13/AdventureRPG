from db import create_player
import discord


class PlayerCreateModal(discord.ui.Modal):
    '''Modal to create a new user'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.character_name = discord.ui.InputText(label='Character Name')
        self.character_description = discord.ui.InputText(
            label='Character Description', style=discord.InputTextStyle.paragraph
        )
        self.add_item(self.character_name)
        self.add_item(self.character_description)

    async def callback(self, interaction: discord.Interaction):
        name = self.character_name.value
        description = self.character_description.value
        create_player(interaction.user.id, name, description)
        embed = discord.Embed(
            color=discord.Color.green(),
            title='🔱 Welcome to AdventureRPG 🔱',
            description=f'Your character `{name}` is now ready to embark on an epic adventure!',
        )
        await interaction.response.send_message(embed=embed)
