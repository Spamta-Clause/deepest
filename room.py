class ROOM():
    def __init__(self,name=None,description=None,exits=None,clearDescription=None,items={},enemies={}):
        self.description = description
        self.name = name
        self.connectedRooms = {}
        self.exits = exits
        self.items = items
        self.enemies = enemies
        self.clearDescription = clearDescription