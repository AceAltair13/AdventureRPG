from .types import ItemType
from .item import Item
from .stats import Stats


class Potion(Item):
    '''Class for in-game potions'''

    def __init__(self, name: str, description: str, item_type: ItemType, stats: Stats) -> None:
        super().__init__(name, description, item_type)
        self.stats = stats
