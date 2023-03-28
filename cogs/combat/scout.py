from classes.character import Player, Enemy, Race, get_random_enemy, EnemyType
from classes.equipment import Armor, ArmorType, Weapon, WeaponType, EquipmentInventory
from classes.view import ProtectedView
from classes.stats import Stats
import discord
import random

# Sample player
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
    level=1,
)


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
        # Check for game over condition
        if self.player.stats.hp == 0 or self.enemy.stats.hp == 0:
            return (
                CombatScoutEmbedFactory.post_fight_embed(
                    True,
                    self.player_total_damage,
                    self.enemy_total_damage,
                    100,
                ),
                True,
            )

        # Normal embed otherwise
        return (
            CombatScoutEmbedFactory.fight_embed(
                self.player,
                self.enemy,
                player_damage,
                enemy_damage,
                player_did_crit,
                enemy_did_crit,
            ),
            False,
        )

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

    def start_game(self):
        return self.outcome(0, False, 0, False)


# Normal enemy game view
class NormalEnemyGameView(ProtectedView):
    '''View class for the normal enemy fight. Contains the game instance.'''

    def __init__(self, game: NormalEnemyGame, author):
        super().__init__(author=author)
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


# Normal enemy scout view
class CombatScoutView(ProtectedView):
    '''View class for scouting nearby enemies'''

    def __init__(self, player: Player, author):
        super().__init__(author=author)
        self.author = author
        self.player = player
        self.enemy = get_random_enemy('forest', self.player.level)
        self.embed = CombatScoutEmbedFactory.enemy_found_embed(self.enemy)

    @discord.ui.button(label='Start', style=discord.ButtonStyle.success)
    async def btn_start_fight_callback(
        self, _: discord.ui.Button, interaction: discord.Interaction
    ):
        view = NormalEnemyGameView(
            NormalEnemyGame(player=self.player, enemy=self.enemy), author=self.author
        )
        embed, _ = view.game.start_game()
        self.children.clear()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label='Retry', style=discord.ButtonStyle.blurple)
    async def btn_retry_scout_callback(
        self, _: discord.ui.Button, interaction: discord.Interaction
    ):
        self.enemy = get_random_enemy('forest', self.player.level)
        self.embed = CombatScoutEmbedFactory.enemy_found_embed(self.enemy)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger)
    async def btn_cancel_fight_callback(
        self, _: discord.ui.Button, interaction: discord.Interaction
    ):
        embed = discord.Embed(color=discord.Color.red(), title=f'You decided not to fight.')
        self.children.clear()
        await interaction.response.edit_message(embed=embed, view=self)


# Factory class with static embed generators
class CombatScoutEmbedFactory:
    '''Embed factory for all combat scout related embeds'''

    @staticmethod
    def enemy_found_embed(enemy: Enemy):
        embed = discord.Embed()

        if enemy:
            embed.color = discord.Color.gold()
            embed.title = enemy.name
            embed.description = f'Type: `{enemy.race.capitalize()}`'

            # Check if the boss is a mini-boss
            if enemy.enemy_type == EnemyType.MINI_BOSS:
                embed.set_footer(text='⚠️ Mini-Boss Detected ⚠️')

            # Add stats fields
            embed.add_field(inline=True, name='Max HP', value=f'💖 `{enemy.stats.max_hp}`')
            embed.add_field(inline=True, name='Attack', value=f'⚔️ `{enemy.stats.attack}`')
            embed.add_field(inline=True, name='Defense', value=f'🛡️ `{enemy.stats.defense}`')
        else:
            embed.color = discord.Color.dark_orange()
            embed.title = 'No enemies nearby. Try scouting again.'

        return embed

    @staticmethod
    def fight_embed(
        player: Player,
        enemy: Enemy,
        player_damage,
        enemy_damage,
        player_did_crit,
        enemy_did_crit,
    ):
        # Embed to be returned
        embed = discord.Embed(color=discord.Color.blurple())

        # Function to render health
        def render_hearts(health, max_health):
            white_squares = round((health / max_health) * 10)
            black_squares = 10 - white_squares
            return f'❤️ `{health}` ' + '`' + '⬜' * white_squares + '⬛' * black_squares + '`'

        # Send normal embed
        embed.title = 'Fight Begins!'
        embed.add_field(inline=False, name=enemy.name, value=f'Type: `{enemy.race.capitalize()}`')
        player_message = f'You dealt `{player_damage}` damage to {enemy.name} '
        enemy_message = f'{enemy.name} strikes back with `{enemy_damage}` damage '

        if player_did_crit:
            player_message += '[CRITICAL!]'
        if enemy_did_crit:
            enemy_message += '[CRITICAL!]'

        embed.add_field(
            inline=False,
            name=render_hearts(enemy.stats.hp, enemy.stats.max_hp),
            value='',
        )
        embed.add_field(inline=True, name='Max HP', value=f'💖 `{enemy.stats.max_hp}`')
        embed.add_field(inline=True, name='Attack', value=f'⚔️ `{enemy.stats.attack}`')
        embed.add_field(inline=True, name='Defense', value=f'🛡️ `{enemy.stats.defense}`')
        embed.add_field(inline=False, name='═══════════( v/s )═══════════', value='')
        embed.add_field(inline=False, name=player.name, value=f'Level `{player.level}`')
        embed.add_field(
            inline=False,
            name=render_hearts(player.stats.hp, player.stats.max_hp),
            value='',
        )
        embed.add_field(inline=True, name='Max HP', value=f'💖 `{player.stats.max_hp}`')
        embed.add_field(inline=True, name='Attack', value=f'⚔️ `{player.stats.attack}`')
        embed.add_field(inline=True, name='Defense', value=f'🛡️ `{player.stats.defense}`')
        embed.add_field(inline=False, name='\n', value='')

        if not (player_damage == enemy_damage == 0):
            embed.add_field(inline=False, name=player_message, value='')
            embed.add_field(inline=False, name=enemy_message, value='')

        return embed

    @staticmethod
    def post_fight_embed(win, player_total_damage, enemy_total_damage, xp_received):
        embed = discord.Embed()

        if win:
            embed.color = discord.Color.green()
            embed.title = '🏆 Victory'
        else:
            embed.color = discord.Color.red()
            embed.title = '☠️ Defeat'

        embed.add_field(
            inline=False,
            name='Damage Dealt',
            value=f'⚔️ `{player_total_damage}`',
        )
        embed.add_field(
            inline=False,
            name='Damage Received',
            value=f'📛 `{enemy_total_damage}`',
        )
        embed.add_field(
            inline=False,
            name='XP Earned',
            value=f'🔅 `{xp_received}`',
        )
        return embed


# Function to link scout command to logic
def combat_scout(player: Player, author):
    view = CombatScoutView(player=player, author=author)
    return view.embed, view
