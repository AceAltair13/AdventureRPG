from classes.character import Character, Player, Enemy, EnemyType
from classes.item import Item
from classes.stats import Stats
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
            player_alive = self.player.is_alive()
            return (
                BattleEmbeds.post_fight_embed(
                    player_alive,
                    self.player_total_damage,
                    self.enemy_total_damage,
                    100,
                    self.enemy.loot_table if player_alive else None,
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
    def enemy_found_embed(enemy: Enemy, energy: int):
        embed = discord.Embed()
        if energy:
            embed.set_footer(text=f'Energy Remaining: {energy}⚡')

        if enemy:
            embed.color = discord.Color.gold()
            embed.title = enemy.name
            embed.description = f'```❤️{enemy.stats.max_hp} ⚔️{enemy.stats.attack} 🛡️{enemy.stats.defense} \n\n{enemy.description}```'

            # Check if the boss is a mini-boss
            if enemy.enemy_type == EnemyType.MINI_BOSS:
                embed.set_author(name='⚠️ Mini-Boss Detected ⚠️')
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
        def render_stats(stats: Stats):
            green_squares = round((stats.hp / stats.max_hp) * 10)
            orange_squares = 10 - green_squares
            line_1 = f'`❤️ {"🟩" * green_squares}{"🟧" * orange_squares}` `{stats.hp}`'
            line_2 = f'`⚔️ {stats.attack} 🛡️ {stats.defense}`'
            return line_1 + ' \n' + line_2

        def render_actions():
            # Player action information
            player_message = f'🔹 You dealt {player_damage} damage to {enemy.name} '
            if player_did_crit:
                player_message += ' \n    [ Critical! ]'

            # Enemy action information
            enemy_message = f'🔸 {enemy.name} strikes back with {enemy_damage} damage '
            if enemy_did_crit:
                enemy_message += ' \n    [ Critical! ]'

            if item_used is not None:
                action_message = f'🔹 You used a {item_used.name} {item_used.description}'
            elif not (player_damage == enemy_damage == 0):
                action_message = player_message + '\n' + enemy_message
            else:
                action_message = f'🔹 You have started a fight with {enemy.name}'

            return '```' + action_message + '```'

        # Render enemy and player
        embed.add_field(name=enemy.name, value=render_stats(enemy.stats), inline=False)
        embed.add_field(name=f'🧑 {player.name}', value=render_stats(player.stats), inline=False)

        # Render actions
        embed.add_field(name='Actions', value=render_actions(), inline=False)

        # Return the embed
        return embed

    @staticmethod
    def post_fight_embed(win, player_total_damage, enemy_total_damage, xp_received, loot: None):
        embed = discord.Embed()

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

        if win:
            embed.color = discord.Color.green()
            embed.title = '🏆 Victory'
            if loot:
                list_loot = '\n'.join(f'{item[2]}x {item[1]}' for item in loot)
                embed.add_field(name='🎉 Loot', value=list_loot, inline=False)
        else:
            embed.color = discord.Color.red()
            embed.title = '☠️ Defeat'
        return embed
