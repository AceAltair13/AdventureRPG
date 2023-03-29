from .scout import combat_scout
from discord.ext import commands
from test import player
import discord


class Combat(commands.Cog):
    '''Cog for combat related commands'''

    def __init__(self, bot):
        self.bot = bot

    # Create command group for combat
    combat = discord.SlashCommandGroup(name='combat', description='Commands related to combat')

    # Scout command
    @combat.command(description='Scout for nearby enemies')
    async def scout(self, ctx: discord.ApplicationContext):
        embed, view = combat_scout(player=player, author=ctx.author)
        await ctx.respond(embed=embed, view=view)

    # TODO: Implement duel
    @combat.command(description='Challenge a player in a duel')
    async def duel(self, ctx: discord.ApplicationContext, opponent: discord.Member):
        await ctx.respond(
            f'You have challenged {opponent.name}! This command is a W.I.P though :)'
        )

    # TODO: Implement boss
    @combat.command(description='Challenge the boss of your current biome')
    async def boss(self, ctx: discord.ApplicationContext):
        await ctx.respond('You are not ready for the big fight yet.')

    # TODO: Implement training
    @combat.command(description='Undergo some training at the barracks')
    async def training(self, ctx: discord.ApplicationContext):
        await ctx.respond('This feature is coming soon.')


# Load the cog
def setup(bot):
    bot.add_cog(Combat(bot))
