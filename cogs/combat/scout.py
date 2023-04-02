from classes.character import Player, Enemy
from bot import ProtectedView
from .battle import NormalBattle, BattleEmbeds
from db import consume_player_energy, update_player
import discord


# Normal enemy game view
class NormalEnemyGameView(ProtectedView):
    '''View class for the normal enemy fight. Contains the game instance.'''

    def __init__(self, game: NormalBattle, author):
        super().__init__(author=author)
        self.game = game
        self.author = author

        # Attack button
        self.btn_attack = discord.ui.Button(
            label='Attack',
            emoji='⚔️',
            style=discord.ButtonStyle.success,
            row=1,
        )
        self.btn_attack.callback = self.btn_attack_callback

        # Escape button
        self.btn_escape = discord.ui.Button(
            label='Escape',
            emoji='🏃',
            style=discord.ButtonStyle.secondary,
            row=1,
        )
        self.btn_escape.callback = self.btn_escape_callback

        # Inventory button
        self.btn_inventory = discord.ui.Button(
            label='Open Inventory' if self.game.player.inventory else 'Inventory Empty',
            style=discord.ButtonStyle.primary,
            row=1,
            disabled=self.game.player.inventory == [],
        )
        self.btn_inventory.callback = self.btn_inventory_callback

        # Inventory select menu
        self.select_menu = discord.ui.Select(
            placeholder='Select an item ...',
            row=0,
            options=[],
        )
        self.select_menu.callback = self.select_menu_callback

        # Check if inventory is open
        self.show_inventory = False

        # Game embed
        self.embed = None

        # Load the components
        self.add_item(self.btn_attack)
        self.add_item(self.btn_escape)
        self.add_item(self.btn_inventory)

    async def btn_attack_callback(self, interaction: discord.Interaction):
        self.embed, game_over = self.game.attack()
        if game_over:
            update_player(self.author.id, self.game.player)
            self.children.clear()
        await interaction.response.edit_message(embed=self.embed, view=self)

    async def btn_escape_callback(self, interaction: discord.Interaction):
        self.embed = discord.Embed(title='You escaped!')
        update_player(self.author.id, self.game.player)
        self.children.clear()
        await interaction.response.edit_message(embed=self.embed, view=self)

    async def btn_inventory_callback(self, interaction: discord.Interaction):
        self.toggle_inventory()
        await interaction.response.edit_message(view=self)

    async def select_menu_callback(self, interaction: discord.Interaction):
        index = int(self.select_menu.values[0])
        item = self.game.player.inventory[index]
        self.embed, _ = self.game.use_item(item)
        self.toggle_inventory()
        await interaction.response.edit_message(embed=self.embed, view=self)

    def toggle_inventory(self):
        # Invert show_inventory state
        self.show_inventory = not self.show_inventory

        # Change inventory button properties
        if self.show_inventory:
            self.btn_inventory.label = 'Close Inventory'
            self.btn_inventory.style = discord.ButtonStyle.danger
        else:
            self.btn_inventory.label = 'Open Inventory'
            self.btn_inventory.style = discord.ButtonStyle.primary

        # Change attack and escape button properties
        btn1, btn2 = self.btn_attack, self.btn_escape
        if self.show_inventory:
            btn1.disabled = True
            btn2.disabled = True
            options = []
            for index, item in enumerate(self.game.player.inventory):
                options.append(
                    discord.SelectOption(
                        label=item.name, description=item.description, value=str(index)
                    )
                )
            self.select_menu.options = options
            self.add_item(self.select_menu)
        else:
            btn1.disabled = False
            btn2.disabled = False
            self.remove_item(self.select_menu)

        # Check if inventory is empty
        if not self.game.player.inventory:
            self.btn_inventory.label = 'Inventory Empty'
            self.btn_inventory.disabled = True


# Normal enemy scout view
class CombatScoutView(ProtectedView):
    '''View class for scouting nearby enemies'''

    def __init__(self, player: Player, author):
        super().__init__(author=author)
        self.author = author
        self.player = player
        self.enemy = Enemy.get_random_enemy('forest', self.player.level)
        self.embed = BattleEmbeds.enemy_found_embed(self.enemy, self.player.energy)

    @discord.ui.button(label='Start', style=discord.ButtonStyle.success)
    async def btn_start_fight_callback(
        self, _: discord.ui.Button, interaction: discord.Interaction
    ):
        view = NormalEnemyGameView(
            NormalBattle(player=self.player, enemy=self.enemy), author=self.author
        )
        embed, _ = view.game.start_game()
        self.children.clear()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label='Retry [ -1⚡]', style=discord.ButtonStyle.blurple)
    async def btn_retry_scout_callback(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        self.player.energy = consume_player_energy(self.author.id)
        if self.player.energy == 0:
            button.disabled = True
            button.label = 'No Energy'
            button.emoji = '⚠️'
        self.enemy = Enemy.get_random_enemy('forest', self.player.level)
        self.embed = BattleEmbeds.enemy_found_embed(self.enemy, self.player.energy)
        await interaction.response.edit_message(embed=self.embed, view=self)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger)
    async def btn_cancel_fight_callback(
        self, _: discord.ui.Button, interaction: discord.Interaction
    ):
        embed = discord.Embed(color=discord.Color.red(), title=f'You decided not to fight.')
        self.children.clear()
        await interaction.response.edit_message(embed=embed, view=self)


# Function to link scout command to logic
def combat_scout(player: Player, author):
    view = CombatScoutView(player=player, author=author)
    return view.embed, view
