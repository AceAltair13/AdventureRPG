from functools import wraps
from db import player_exists
import discord


# Custom decorator to allow only players to use command
def player_command(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        author = args[1].author
        if not player_exists(author.id):
            embed = discord.Embed(
                color=discord.Color.green(),
                title=f'Welcome, {author.name}',
                description="It looks like you haven't started playing yet. Use the `/start` command to start playing AdventureRPG now!",
            )
            await args[1].respond(embed=embed)
        else:
            await func(*args, **kwargs)

    return wrapper
