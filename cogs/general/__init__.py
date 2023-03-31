from discord.ext import commands
from .start import PlayerCreateModal
from db import player_exists
import discord


class General(commands.Cog):
    '''General cog for general game commands'''

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Starts a new game')
    async def start(self, ctx: discord.ApplicationContext):
        if player_exists(ctx.author.id):
            embed = discord.Embed(
                color=discord.Color.red(),
                title='Player Exists',
                description=f'Hey, {ctx.author.name}! It looks like you have already created a character before. This command is only for new players 😀',
            )
            await ctx.respond(embed=embed)
        else:
            await ctx.send_modal(PlayerCreateModal(title='AdventureRPG'))


def setup(bot):
    bot.add_cog(General(bot))
