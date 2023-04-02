class Stats:
    '''The stats of a character'''

    def __init__(
        self,
        hp: int,
        attack: int,
        defense: int,
        cc: float,
        cd: float,
        max_hp: float,
        luck: float = 0.0,
    ):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.cc = cc
        self.cd = cd
        self.max_hp = max_hp
        self.luck = luck
