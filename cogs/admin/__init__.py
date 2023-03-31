from discord.ext import commands
from config import COG_LIST
from db import delete_player, player_exists
import discord


class Admin(commands.Cog):
    '''Admin only commands for bot'''

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    admin = discord.SlashCommandGroup(name='admin', description='Admin exclusive commands')

    @commands.is_owner()
    @admin.command(description='Restarts the bot')
    async def reload(
        self,
        ctx: discord.ApplicationContext,
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

    @commands.is_owner()
    @admin.command(description='Shuts down the bot')
    async def shutdown(self, ctx: discord.ApplicationContext):
        await ctx.respond(
            embed=discord.Embed(
                color=discord.Color.red(), title='Bot is now shutting down. Goodbye 👋'
            )
        )
        await self.bot.close()

    @commands.is_owner()
    @admin.command(description='Delete a player from the database')
    async def delete_player(self, ctx: discord.ApplicationContext, player: discord.Member):
        embed = discord.Embed()
        if delete_player(player.id):
            embed.color = discord.Color.green()
            embed.title = 'Player Deleted!'
            embed.description = (
                f'You have successfully deleted the data of `{player.name}` from the database.'
            )
        else:
            embed.color = discord.Color.red()
            embed.title = 'Could not find the player in the database'
        await ctx.respond(embed=embed)

    async def cog_command_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='You are not allowed to use that command', color=discord.Color.red()
            )
            await ctx.respond(embed=embed)
        else:
            raise error


def setup(bot):
    bot.add_cog(Admin(bot))
