class WEAPON():
    def __init__(self,name,type,damage,preferedClass):
        self.name = name
        self.type = type
        self.damage = damage
        self.preferedClass = preferedClass
class POTION():
    def __init__(self,name,type,effect):
        self.name = name
        self.type = type
        self.effect = effect
class ARMOUR():
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense