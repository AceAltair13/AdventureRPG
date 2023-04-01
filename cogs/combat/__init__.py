from .scout import combat_scout
from discord.ext import commands
from decorators import player_command
from bot import PlayerApplicationContext
import discord


class Combat(commands.Cog):
    '''Cog for combat related commands'''

    def __init__(self, bot):
        self.bot = bot

    # Create command group for combat
    combat = discord.SlashCommandGroup(name='combat', description='Commands related to combat')

    # Scout command
    @combat.command(name='scout', description='Scout for nearby enemies')
    @player_command(energy_consumed=1)
    async def _scout(self, ctx: PlayerApplicationContext):
        embed, view = combat_scout(player=ctx.player, author=ctx.author)
        await ctx.respond(embed=embed, view=view)

    # TODO: Implement duel
    @combat.command(name='challenge', description='Challenge a player in a duel')
    @player_command()
    async def _challenge(self, ctx: PlayerApplicationContext, opponent: discord.Member):
        await ctx.respond(
            f'You have challenged {opponent.name}! This command is a W.I.P though :)'
        )

    # TODO: Implement boss
    @combat.command(name='boss', description='Challenge the boss of your current biome')
    @player_command()
    async def _boss(self, ctx: PlayerApplicationContext):
        await ctx.respond('You are not ready for the big fight yet.')

    # TODO: Implement training
    @combat.command(name='training', description='Undergo some training at the barracks')
    @player_command()
    async def _training(self, ctx: PlayerApplicationContext):
        await ctx.respond('This feature is coming soon.')


# Load the cog
def setup(bot):
    bot.add_cog(Combat(bot))
