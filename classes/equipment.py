from .item import Item
from .enums import ArmorType, WeaponType, ItemType


class Equipment(Item):
    '''Base class for all equipments'''

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        item_type: ItemType,
        required_level: int,
        current_level: int = 1,
    ):
        super().__init__(id, name, description, item_type)
        self.required_level = required_level
        self.current_level = current_level


class Armor(Equipment):
    '''Model class for armors'''

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        required_level: int,
        armor_type: ArmorType,
        item_type: ItemType,
        defense: int,
        set_bonus_id: str,
        current_level: int = 1,
    ):
        super().__init__(
            id=id,
            name=name,
            description=description,
            item_type=item_type,
            required_level=required_level,
            current_level=current_level,
        )
        self.armor_type = armor_type
        self.defense = defense
        self.set_bonus_id = set_bonus_id


class Weapon(Equipment):
    '''Model class for weapons'''

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        required_level: int,
        weapon_type: WeaponType,
        item_type: ItemType,
        attack: int,
        current_level: int = 1,
    ):
        super().__init__(
            id=id,
            name=name,
            description=description,
            item_type=item_type,
            required_level=required_level,
            current_level=current_level,
        )
        self.weapon_type = weapon_type
        self.attack = attack
