class ENEMY():
    def __init__(self, name, type, health, defense, weapon):
        self.name = name
        self.type = type
        self.health = health
        self.maxHealth = health
        self.defense = defense
        # Will be an actual WEAPON class passed in
        self.weapon = weapon
