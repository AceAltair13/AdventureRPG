from classes.character import Character, Player, Enemy, EnemyType
from classes.item import Item
import discord
import random


# Game engine for normal enemy fights
class NormalBattle:
    '''Class for a normal enemy fight'''

    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.player_total_damage = 0
        self.enemy_total_damage = 0

    def calculate_damage(self, attacker: Character, defender: Character):
        # Check if crit occurred
        crit = False

        # Calculate damage
        if attacker.stats.attack >= defender.stats.defense:
            damage = (attacker.stats.attack * 2) - defender.stats.defense
        else:
            damage = attacker.stats.attack * attacker.stats.attack / defender.stats.defense

        # Check for crits
        if random.random() < attacker.stats.cc:
            damage *= attacker.stats.cd
            crit = True

        # Return the damage and crit
        return round(damage), crit

    def outcome(
        self, player_damage, player_did_crit, enemy_damage, enemy_did_crit, item_used=None
    ):
        # Check for game over condition
        if not self.player.is_alive() or not self.enemy.is_alive():
            return (
                BattleEmbeds.post_fight_embed(
                    True,
                    self.player_total_damage,
                    self.enemy_total_damage,
                    100,
                ),
                True,
            )

        # Normal embed otherwise
        return (
            BattleEmbeds.fight_embed(
                self.player,
                self.enemy,
                player_damage,
                enemy_damage,
                player_did_crit,
                enemy_did_crit,
                item_used,
            ),
            False,
        )

    def attack(self):
        # Player attacks first
        player_damage, player_did_crit = self.calculate_damage(self.player, self.enemy)
        self.enemy.take_damage(player_damage)
        self.player_total_damage += player_damage

        # Enemy strikes next
        enemy_damage, enemy_did_crit = self.calculate_damage(self.enemy, self.player)
        self.player.take_damage(enemy_damage)
        self.enemy_total_damage += enemy_damage

        # Check the outcome
        return self.outcome(player_damage, player_did_crit, enemy_damage, enemy_did_crit)

    def use_item(self, item: Item):
        self.player.use_item(item)
        return self.outcome(0, False, 0, False, item)

    # Start the game with a pre-defined outcome
    def start_game(self):
        return self.outcome(0, False, 0, False)


# Factory class with static embed generators
class BattleEmbeds:
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
        item_used: Item = None,
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
        stat_max_hp = f'`{enemy.stats.max_hp}`'
        stat_attack = f'`{enemy.stats.attack}`'
        stat_defense = f'`{enemy.stats.defense}`'
        embed.add_field(
            inline=True,
            name=f'Max HP : {stat_max_hp}'
            + '\n'
            + f'Attack : {stat_attack}'
            + '\n'
            + f'Defense : {stat_defense}',
            value='',
        )
        embed.add_field(inline=False, name='═══════════( v/s )═══════════', value='')
        embed.add_field(inline=False, name=player.name, value=f'Level `{player.level}`')
        embed.add_field(
            inline=False,
            name=render_hearts(player.stats.hp, player.stats.max_hp),
            value='',
        )
        stat_max_hp = f'`{player.stats.max_hp}`'
        stat_attack = f'`{player.stats.attack}`'
        stat_defense = f'`{player.stats.defense}`'
        embed.add_field(
            inline=True,
            name=f'Max HP : {stat_max_hp}'
            + '\n'
            + f'Attack : {stat_attack}'
            + '\n'
            + f'Defense : {stat_defense}',
            value='',
        )
        embed.add_field(inline=False, name='\n', value='')

        if item_used is not None:
            embed.add_field(
                inline=False, name=f'You used a {item_used.name} {item_used.description}', value=''
            )
        elif not (player_damage == enemy_damage == 0):
            embed.add_field(inline=False, name=player_message + '\n' + enemy_message, value='')

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
