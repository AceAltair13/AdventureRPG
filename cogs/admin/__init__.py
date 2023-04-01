from discord.ext import commands
from config import COG_LIST
from db import delete_player
from bot import PlayerApplicationContext
from decorators import admin_only
import discord


class Admin(commands.Cog):
    '''Admin only commands for bot'''

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    admin = discord.SlashCommandGroup(name='admin', description='Admin exclusive commands')

    @admin.command(name='reload', description='Restarts the bot')
    @admin_only
    async def _reload(
        self,
        ctx: PlayerApplicationContext,
        cog: discord.Option(str, 'Select a cog to reload', choices=COG_LIST),
    ):
        try:
            self.bot.reload_extension(f'cogs.{cog}')
            await ctx.respond(
                embed=discord.Embed(
                    title=f'`{cog}` cog reloaded successfully.', color=discord.Color.green()
                )
            )
        except:
            await ctx.respond(
                embed=discord.Embed(
                    title=f'There was a problem loading `{cog}`. Please try again.',
                    color=discord.Color.red(),
                )
            )

    @admin.command(name='shutdown', description='Shuts down the bot')
    @admin_only
    async def _shutdown(self, ctx: PlayerApplicationContext):
        await ctx.respond(
            embed=discord.Embed(
                color=discord.Color.red(), title='Bot is now shutting down. Goodbye 👋'
            )
        )
        await self.bot.close()

    @admin.command(name='delete_player', description='Delete a player from the database')
    @admin_only
    async def _delete_player(self, ctx: PlayerApplicationContext, player: discord.Member):
        delete_player(player.id)
        embed = discord.Embed(
            color=discord.Color.green(),
            title='Player Deleted!',
            description=(
                f'You have successfully deleted the data of `{player.name}` from the database.'
            ),
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
