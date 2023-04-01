from discord.ext import commands
from .start import PlayerCreateModal
from decorators import player_command
from bot import PlayerApplicationContext
import discord


class General(commands.Cog):
    '''General cog for general game commands'''

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='start', description='Starts a new game')
    @player_command(player_should_exist=False)
    async def _start(self, ctx: PlayerApplicationContext):
        await ctx.send_modal(PlayerCreateModal(title='AdventureRPG'))


def setup(bot):
    bot.add_cog(General(bot))
