class ITEM():
    def __init__(self,name,type,damage,preferedClass,proficiency,weakness,dropchance):
        self.name = name
        self.type = type
        self.damage = damage
        self.preferedClass = preferedClass
        self.proficiency = proficiency
        self.weakness = weakness
        self.dropchance = dropchance
        
class WEAPON(ITEM):
    def __init__(self,name,type,damage,preferedClass,proficiency=[],weakness=[],dropchance=50):
        super().__init__(name,type,damage,preferedClass,proficiency,weakness,dropchance)
class SPELL(ITEM):
    def __init__(self,name,type,damage,chance,preferedClass,proficiency=[],weakness=[],dropchance=50):
        super().__init__(name,type,damage,preferedClass,proficiency,weakness,dropchance)
        self.chance = chance
class POTION():
    def __init__(self,name,type,effect):
        self.name = name
        self.type = type
        self.effect = effect
class ARMOUR():
    def __init__(self, name, defense,dropchance=50):
        self.name = name
        self.defense = defense
        self.dropchance = dropchance