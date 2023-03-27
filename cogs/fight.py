from models.character import Player, Enemy, Race
from models.equipment import Armor, ArmorType, Weapon, WeaponType, Equipment, EquipmentInventory
from models.stats import Stats
from discord.ext import commands
import discord
import random


# Game engine for normal enemy fights
class NormalEnemyGame:
    '''Create a new game for a normal enemy fight'''

    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.player_total_damage = 0
        self.enemy = enemy
        self.enemy_total_damage = 0

    def calculate_damage(self, player_attack: bool = False):
        # Check if crit occured
        crit = False

        # Variables
        if player_attack:
            player, enemy = self.player.stats, self.enemy.stats
        else:
            player, enemy = self.enemy.stats, self.player.stats

        # Calculate damage
        if player.attack >= enemy.defense:
            damage = (player.attack * 2) - enemy.defense
        else:
            damage = player.attack * player.attack / enemy.defense

        # Check for crits
        if random.random() < player.cc:
            damage *= player.cd
            crit = True

        # return the damage and crit
        return round(damage), crit

    def outcome(self, player_damage, player_did_crit, enemy_damage, enemy_did_crit):
        # Embed to be returned
        embed = discord.Embed()

        # Function to render health
        def render_hearts(health, max_health):
            white_squares = round((health / max_health) * 10)
            black_squares = 10 - white_squares
            return f'❤️ `{health}` ' + '`' + '⬜' * white_squares + '⬛' * black_squares + '`'

        # Send post game embed
        if self.player.stats.hp == 0 or self.enemy.stats.hp == 0:
            if self.player.stats.hp == 0:
                embed.color = discord.Color.red()
                embed.title = 'Defeat  ☠️'
            else:
                embed.color = discord.Color.green()
                embed.title = 'Victory  🏆'
            embed.add_field(
                inline=False,
                name='Damage Dealt',
                value=f'⚔️ `{self.player_total_damage}`',
            )
            embed.add_field(
                inline=False,
                name='Damage Received',
                value=f'📛 `{self.enemy_total_damage}`',
            )
            embed.add_field(
                inline=False,
                name='XP Earned',
                value=f'⚜️ `100`',
            )
            return embed, True

        # Send normal embed
        embed.title = 'Fight Begins!'
        embed.add_field(inline=False, name=self.enemy.name, value=f'Level `{self.enemy.level}`')
        player_message = f'You dealt `{player_damage}` damage to {self.enemy.name} '
        enemy_message = f'{self.enemy.name} strikes back with `{enemy_damage}` damage '

        if player_did_crit:
            player_message += '[CRITICAL!]'
        if enemy_did_crit:
            enemy_message += '[CRITICAL!]'

        embed.add_field(
            inline=False,
            name=render_hearts(self.enemy.stats.hp, self.enemy.stats.max_hp),
            value='',
        )
        embed.add_field(inline=True, name='Max HP', value=f'💖 `{self.enemy.stats.max_hp}`')
        embed.add_field(inline=True, name='Attack', value=f'⚔️ `{self.enemy.stats.attack}`')
        embed.add_field(inline=True, name='Defense', value=f'🛡️ `{self.enemy.stats.defense}`')
        embed.add_field(inline=False, name='═══════════( 🆚 )═══════════', value='')
        embed.add_field(inline=False, name=self.player.name, value=f'Level `{self.player.level}`')
        embed.add_field(
            inline=False,
            name=render_hearts(self.player.stats.hp, self.player.stats.max_hp),
            value='',
        )
        embed.add_field(inline=True, name='Max HP', value=f'💖 `{self.player.stats.max_hp}`')
        embed.add_field(inline=True, name='Attack', value=f'⚔️ `{self.player.stats.attack}`')
        embed.add_field(inline=True, name='Defense', value=f'🛡️ `{self.player.stats.defense}`')
        embed.add_field(inline=False, name='\n', value='')

        # Check if game has just begun
        if player_damage == enemy_damage == 0 and player_did_crit == enemy_did_crit == False:
            return embed, False

        embed.add_field(inline=False, name=player_message, value='')
        embed.add_field(inline=False, name=enemy_message, value='')

        return embed, False

    def attack(self):
        # Player does the damage first
        player_damage, player_did_crit = self.calculate_damage(True)
        self.enemy.stats.hp -= player_damage
        self.player_total_damage += player_damage

        # Check if enemy defeated
        if self.enemy.stats.hp <= 0:
            self.enemy.stats.hp = 0
            return self.outcome(player_damage, player_did_crit, 0, False)

        # Enemy strikes next
        enemy_damage, enemy_did_crit = self.calculate_damage()
        self.player.stats.hp -= enemy_damage
        self.enemy_total_damage += enemy_damage

        # Check if player defeated
        if self.player.stats.hp <= 0:
            self.player.stats.hp = 0
            return self.outcome(player_damage, player_did_crit, enemy_damage, enemy_did_crit)

        return self.outcome(player_damage, player_did_crit, enemy_damage, enemy_did_crit)

    def start_game(self):
        return self.outcome(0, False, 0, False)


# Normal Enemy Game View
class NormalEnemyGameView(discord.ui.View):
    '''View class for the normal enemy fight. Contains the game instance.'''

    def __init__(self, game: NormalEnemyGame):
        super().__init__()
        self.game = game

    @discord.ui.button(label='Attack', emoji='⚔️', style=discord.ButtonStyle.success)
    async def btn_attack_callback(self, _: discord.ui.Button, interaction: discord.Interaction):
        embed, game_over = self.game.attack()
        if game_over:
            self.children.clear()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Escape', emoji='🏃', style=discord.ButtonStyle.secondary)
    async def btn_escape_callback(self, _: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title='You escaped!')
        self.children.clear()
        await interaction.response.edit_message(embed=embed, view=self)


# Attack command cog
class Attack(commands.Cog):
    '''Cog for combat related commands'''

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Start a fight with a normal enemy')
    async def fight(self, ctx: discord.ApplicationContext):
        # Create a new game for the user
        player = Player(
            name='You',
            race=Race.HUMAN,
            stats=Stats(100, 5, 0, 0.0, 1.5, 100),
            equipment=EquipmentInventory(
                helmet=Armor('No Helmet', 0, ArmorType.HELMET, 0),
                chestplate=Armor('No Helmet', 0, ArmorType.CHESTPLATE, 0),
                leggings=Armor('No Helmet', 0, ArmorType.LEGGINGS, 0),
                boots=Armor('No Helmet', 0, ArmorType.BOOTS, 0),
                weapon=Weapon('Fist', 0, WeaponType.BLUDGEONING, 1),
            ),
        )
        game = NormalEnemyGame(
            player=player,
            enemy=Enemy(name='Wolf', race=Race.ANIMAL, stats=Stats(50, 3, 1, 0.02, 1.2, 50)),
        )
        normal_fight_view = NormalEnemyGameView(game)

        embed, _ = normal_fight_view.game.start_game()
        await ctx.respond(embed=embed, view=normal_fight_view)


# Load the cog
def setup(bot):
    bot.add_cog(Attack(bot))
