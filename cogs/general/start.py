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
        embed = discord.Embed()
        name = self.character_name.value
        description = self.character_description.value
        result = create_player(interaction.user.id, name, description)
        if result:
            embed.color = discord.Color.green()
            embed.title = '🔱 Welcome to AdventureRPG 🔱'
            embed.description = (
                f'Your character `{name}` is now ready to embark on an epic adventure!'
            )
        else:
            embed.color = discord.Color.red()
            embed.title = 'There was an error creating your profile!'
            embed.description = 'Please try again.'
        await interaction.response.send_message(embed=embed)
