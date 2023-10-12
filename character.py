class CHARACTER():
    def __init__(self,health,inventory,defense):
        self.health = health
        self.inventory = inventory
        self.defense = defense

class PLAYER(CHARACTER):
    def __init__(self,playerClass,health,inventory,defense):
        self.playerClass = playerClass
        super().__init__(health,inventory,defense)
class ENEMY(CHARACTER):
    def __init__(self, name, type, health, defense, inventory):
        self.name = name
        self.type = type
        super().__init__(health,inventory,defense)
        self.maxHealth = health
        self.weapon = None
