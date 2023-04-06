class Stats:
    '''The stats of a character'''

    def __init__(
        self,
        hp: int = 100,
        max_hp: int = 100,
        attack: int = 5,
        defense: int = 0,
        cc: float = 0.0,
        cd: float = 1.5,
        luck: float = 0.0,
    ):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.cc = cc
        self.cd = cd
        self.max_hp = max_hp
        self.luck = luck
