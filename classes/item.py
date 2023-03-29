from .entity import Entity
from .types import ItemType
import typing


class Item(Entity):
    """
    A class representing an in-game item.

    Attributes:
    - name (str): The name of the item.
    - description (str): A description of the item.
    - type (ItemType): The type of the item, such as ARMOR, WEAPON, or POTION.
    - effects (tuple[str, str, int] or None): The effects of the item on a player's stats,
      represented as a tuple containing the name of the stat, the operation to perform (+, -, *, /),
      and the value to apply to the stat. If the item has no effects, this attribute is None.
    - buying_price (int): Buying price of the item
    - selling_price (int): Selling price of the item
    """

    def __init__(
        self,
        name: str,
        description: str,
        item_type: ItemType,
        effects: typing.Union[
            list[tuple[str, str, int]], None
        ] = None,  # list[(stat, operation, value)]
        duration: int = 0,  # 0 = Permanent effect
        buying_price: int = 0,
        selling_price: int = 0,
    ) -> None:
        super().__init__(name=name, description=description)
        self.effects = effects
        self.duration = duration
        self.type = item_type
        self.buying_price = buying_price
        self.selling_price = selling_price
