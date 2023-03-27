from discord.ext import commands
from config import COG_LIST
import discord


class Admin(commands.Cog):
    '''Admin only commands for bot'''

    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.is_owner()
    @discord.slash_command(description='Restarts the bot')
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


def setup(bot):
    bot.add_cog(Admin(bot))
