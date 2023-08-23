class WEAPON():
    def __init__(self,name,type,damage,preferedClass,proficiency=[],weakness=[]):
        self.name = name
        self.type = type
        self.damage = damage
        self.preferedClass = preferedClass
        self.proficiency = proficiency
        self.weakness = weakness
class SPELL():
    def __init__(self,name,type,damage,chance,preferedClass,proficiency=[],weakness=[]):
        self.name = name
        self.type = type
        self.damage = damage
        self.chance = chance
        self.preferedClass = preferedClass
        self.proficiency = proficiency
        self.weakness = weakness
class POTION():
    def __init__(self,name,type,effect):
        self.name = name
        self.type = type
        self.effect = effect
class ARMOUR():
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense