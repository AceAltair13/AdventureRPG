from bot import PlayerApplicationContext, AdventureRPG
from functools import wraps
from utils.db import get_player, player_exists
from utils.errors import AdventureRPGException, NotAnAdmin, PlayerAlreadyExists
from config import ADMIN_LIST
from discord import Embed, Color


def player_command(player_should_exist: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: PlayerApplicationContext, *args, **kwargs):
            author = ctx.author

            # Get the player and pass it into the PlayerApplicationContext
            try:
                if player_should_exist:
                    player = get_player(author.id, self.bot.game_data)
                    ctx.set_player(player)
                else:
                    if player_exists(author.id):
                        raise PlayerAlreadyExists
                await func(self, ctx, *args, **kwargs)
            except AdventureRPGException as e:
                await ctx.respond(embed=e.get_embed())
            except Exception as e:
                await ctx.respond(
                    embed=Embed(
                        color=Color.red(),
                        title='Error',
                        description='Looks like something went wrong. Please try again.',
                    )
                )

        return wrapper

    return decorator


# Allow only admins to use the command
def admin_only(func):
    @wraps(func)
    async def wrapper(self, ctx, *args, **kwargs):
        try:
            if ctx.author.id not in ADMIN_LIST:
                raise NotAnAdmin
            await func(self, ctx, *args, **kwargs)
        except AdventureRPGException as e:
            await ctx.respond(embed=e.get_embed())
        except:
            await ctx.respond(
                embed=Embed(
                    color=Color.red(),
                    title='Error',
                    description='Looks like something went wrong. Please try again.',
                )
            )

    return wrapper
