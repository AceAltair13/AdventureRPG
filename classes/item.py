import typing

from .entity import Entity
from classes.enums import ItemType


class Item(Entity):
    """
    A class representing an in-game item.
    """

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        item_type: ItemType,
        effects: typing.Union[
            list[tuple[str, str, int, bool]], None
        ] = None,  # list[(stat, operation, value, permanent?)]
        value: int = 0,
    ):
        super().__init__(id, name, description)
        self.effects = effects
        self.item_type = item_type
        self.value = value
