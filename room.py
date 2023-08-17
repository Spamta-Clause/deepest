class ROOM():
    def __init__(self,name=None,description=None,exits=None,clearDescription=None, nRoom=None, sRoom=None, eRoom=None, wRoom=None,items={},enemies={}):
        self.description = description
        self.name = name
        self.nRoom = nRoom
        self.sRoom = sRoom
        self.eRoom = eRoom
        self.wRoom = wRoom
        self.exits = exits
        self.items = items
        self.enemies = enemies
        self.clearDescription = clearDescription