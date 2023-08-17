import colour, room, item, enemy, colour
import time, random, copy, atexit, os

# Create the items
fists = item.WEAPON("Fists","fists",1)
boneDagger = item.WEAPON("Bone Dagger","dagger",2)
rustyHalberd = item.WEAPON("Rusty Halberd","spear",5)
bronzeHalberd = item.WEAPON("Bronze Halberd","spear",11)
rustyGreatsword = item.WEAPON("Rusty Greatsword","claymore",15)

# Create the armour
leather = item.ARMOUR("Leather",1)
chainmail = item.ARMOUR("Chainmail",3)

# Create the enemies
skeleton = enemy.ENEMY("Skeleton","undead",8,1,boneDagger)
necromancer = enemy.ENEMY("Necromancer","humanoid",13,3,rustyHalberd)

# Create the rooms
library = room.ROOM("library","You are in a library. There is a door to the north and a door to the south.", "NS")
barracks = room.ROOM("barracks","You are in a barracks. There is a door to the north.", "N", items={"Leather":leather})
weaponsRoom = room.ROOM("weaponRoom","You are in a weapons room, there are weapons strewn upon the floor. There is a door to the south as well as one to the west.", "SW", items={"Rusty Halberd":rustyHalberd,"Bronze Halberd":bronzeHalberd,"Rusty Greatsword":rustyGreatsword})
cage = room.ROOM("cage","You are in a large cage like room, in front of you lies an animated skeleton, there are doors to the east and to the north.","NE","You are in a cage like room, in front of you lies the body of a defeated animated skeleton",enemies={"S1":copy.copy(skeleton)})
ritualRoom = room.ROOM("ritualRoom","You are in a room with a large pentagram on the floor, there is a door to the south, a necromancer and three animated skeletons are within.","S","You are in a room with a large pentagram on the floor, there is a door to the south, the bodies of a defeated necromancer and three animated skeletons are within",enemies={"N1":copy.copy(necromancer),"S1":copy.copy(skeleton),"S2":copy.copy(skeleton),"S3":copy.copy(skeleton)})


import pickle

rooms = [library,barracks,weaponsRoom,cage,ritualRoom]
roomsDict = {"library":library,"barracks":barracks,"weaponsRoom":weaponsRoom,"cage":cage,"ritualRoom":ritualRoom}

try:
    loadedInstances = []
    for instance in room:
        filename = f'rooms\\{instance.name}.pickle'
        with open(filename, 'rb') as file:
            loadedInstance = pickle.load(file)
            loadedInstances.append(loadedInstance)

    for instance in rooms:
        filename = f'{instance.name}.pickle'
        with open(filename, 'rb') as file:
            loadedInstance = pickle.load(file)
            roomsDict[loadedInstance.name] = loadedInstance

    library = roomsDict["library"]
except:
    pass





# Set the exits for the rooms
library.nRoom=weaponsRoom 
library.sRoom=barracks

barracks.nRoom=library

weaponsRoom.sRoom=library
weaponsRoom.wRoom=cage

cage.eRoom=weaponsRoom
cage.nRoom=ritualRoom

ritualRoom.sRoom=cage

currentRoom = barracks

visitedRooms = []

health = 20
defense = 0
inventory = {}

def start():
    folderPath = "rooms"

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        
    global inventory
    global currentRoom
    global hp
    global visitedRooms

    try:
        inventory = pickle.load(open("inv.json","rb"))
    except:
        inventory = {}
    try:
        currentRoom = pickle.load(open("currentRoom.json","rb"))
    except:
        currentRoom = barracks
    try:
        hp = int(pickle.load(open("hp.json","rb")))
    except:
        hp = 20
    try:
        visitedRooms = pickle.load(open("prevRooms.json","rb"))
    except:
        visitedRooms = []

def close():
    global inventory
    global currentRoom
    global hp
    global visitedRooms
    #Saves the information regarding inventory, health, current room and visited rooms
    try:
            inv = open("inv.json","xb")
    except:
            inv = open("inv.json","wb")
    try:
            hp = open("hp.json","xb") 
    except:
            hp = open("hp.json","wb")
    try:
            cR = open("currentRoom.json","xb") 
    except:
            cR = open("currentRoom.json","wb")
    try:
            pR = open("prevRooms.json","xb")
    except:
            pR = open("prevRooms.json","wb")
    pickle.dump(inventory,inv)
    pickle.dump(health,hp)
    pickle.dump(currentRoom,cR)
    pickle.dump(visitedRooms,pR)

    # Saves information regarding rooms
    for instance in rooms:
            filename = f'rooms\\{instance.name}.pickle'
            with open(filename, 'wb') as file:
                pickle.dump(instance, file)
    inv.close()
    hp.close()
    cR.close()
    pR.close()



start()

def type(text):
    #Slowly types text that can be changed within the same line
    lettersTyped = ""
    for letter in text:
        lettersTyped += letter
        print(lettersTyped, end= "\r")
        if(letter != " "):
            time.sleep(random.uniform(0,0.05))

    print(text+"")

def inputType(text):
    #Slowly types text that can be changed within the same line
    lettersTyped = ""
    for letter in text:
        lettersTyped += letter
        print(lettersTyped, end= "\r")
        if(letter != " "):
            time.sleep(random.uniform(0,0.05))
    return(input(text))


def Show_Inventory():
    if(len(inventory) == 0):
        type(f"{colour.reset}{colour.bold}{colour.italic}{colour.white}Your inventory is empty.")
        return
    else:
        type(f"{colour.reset}{colour.bold}{colour.italic}{colour.white}Your inventory contains:")
        for thing in inventory:
            type(f"{colour.reset}{colour.bold}{colour.italic}{colour.white}{thing.name}  -   {thing.damage}")

def Show_Commands():
    type(f"{colour.reset}{colour.bold}{colour.italic}{colour.white}Commands:{optionsList}")

optionsList = ["i","help","quit"]
options = {"i":Show_Inventory, "help":Show_Commands,"quit":close}

while True:
    enemiesTotalHealth = 0
    # Check if the current room has been visited before and then types the description, changing the colour based on whether or not it has
    if currentRoom not in visitedRooms:
        visitedRooms.append(currentRoom)
        type(colour.reset + colour.bold + colour.green + colour.italic + currentRoom.description + colour.reset)
    else:
        type(colour.reset + colour.blue + colour.italic + currentRoom.description + colour.reset)


        # Engages in combat for the enemies in the room
    enemiesTotalHealth = 0
    
    enemyOptions = []
    for roomEnemy in currentRoom.enemies:
        enemiesTotalHealth += currentRoom.enemies[roomEnemy].health
        enemyOptions.append(roomEnemy.lower())
    if(len(enemyOptions) > 0):
        enemyOptionsHigh = []
        for thing in enemyOptions:
            enemyOptionsHigh.append(thing.capitalize())

    # Player attacking
    def playerAttack():
        global enemiesTotalHealth
        global inventory
        global previousRoom
        global currentRoom
        # Player attacking
        attack = "!"
        enemyOptions = []
        enemyOptionsHigh = []
        for roomEnemy in currentRoom.enemies:
            enemyOptions.append(roomEnemy.lower())
            enemyOptionsHigh.append(roomEnemy.capitalize())

        type(f"{colour.green}{colour.bold}{colour.italic}The enemies present in this room are, {', '.join(enemyOptionsHigh)}.")
        while not (attack.lower() in enemyOptions or attack.lower() == "run"):
            attack = inputType(f"{colour.reset}{colour.purple}What would you like to do? Enter either run, or the name of the enemy you would like to attack.   -   {colour.reset}{colour.yellow}{colour.bold}")
            if(not(attack.lower() in enemyOptions or attack.lower() == "run")):   
                type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Please enter a valid input.{colour.reset}")

        
        if(attack.lower() == "run"):
            currentRoom = previousRoom
            return "ran"
        
                
        if(attack.lower() in enemyOptions):
            weapons = []
            for thing in inventory:
                if isinstance(inventory[thing], item.WEAPON):
                    weapons.append(inventory[thing].name + f", dealing {inventory[thing].damage} damage")
            weapon = "!"
            if(len(weapons) == 0):
                type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}You have no weapons!{colour.reset}")
                weapon = "fists"
            else:    
                weapon = inputType(f"{colour.reset}{colour.purple}What weapon would you like to use? Your current items are {', '.join(weapons)}  -   {colour.reset}{colour.yellow}{colour.bold}")
                weapons = []
                for thing in inventory:
                    if isinstance(inventory[thing], item.WEAPON):
                        weapons.append(inventory[thing].name.lower())
                if(not (weapon.lower() in weapons)):
                    type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Please enter a valid input.{colour.reset}")
                    playerAttack()
            weapons = []
            for thing in inventory:
                if isinstance(inventory[thing], item.WEAPON):
                    weapons.append(inventory[thing].name.lower())
            if ((weapon.lower() in weapons) or (weapon.lower() == "fists")):
                weapons = []
                for thing in inventory:
                    if isinstance(thing, item.WEAPON):
                        weapons.append(inventory[thing].name.lower())
                    
                if(weapon != "fists"):
                    if(inventory[weapon.lower()].damage >= currentRoom.enemies[attack.capitalize()].defense):
                        type(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}You attack the {attack.capitalize()} with your {weapon.lower().capitalize()}! You inflict a total of {inventory[weapon.lower()].damage} damage!{colour.reset}")
                        currentRoom.enemies[attack.capitalize()].health -= inventory[weapon.lower()].damage
                    else:
                        type(f"{colour.reset}{colour.bold}{colour.red}You were unable to hit {attack.capitalize()}, as their defense is too high compared to your weapon of choice.{colour.reset}")
                else:        
                    if(1 >= currentRoom.enemies[attack.capitalize()].defense):
                        type(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}You attack the {attack.capitalize()} with your fists! You inflict a total of 1 damage!{colour.reset}")
                        currentRoom.enemies[attack.capitalize()].health -= 1
                    else:
                        type(f"{colour.reset}{colour.bold}{colour.red}You were unable to hit {attack.capitalize()}, as their defense is too high compared to your weapon of choice.{colour.reset}")
                        
            if(currentRoom.enemies[attack.capitalize()].health <= 0):
                type(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}{attack.capitalize()} falls to the floor!")
                enemiesTotalHealth -= currentRoom.enemies[attack.capitalize()].maxHealth
                if(random.randint(1,10) < 5):
                    type(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}{attack.capitalize()} dropped their {currentRoom.enemies[attack.capitalize()].weapon.name}!{colour.reset}")
                    currentRoom.items[currentRoom.enemies[attack.capitalize()].weapon.name] = currentRoom.enemies[attack.capitalize()].weapon
                currentRoom.enemies.pop(attack.capitalize())

    # Lets players and enemies attack
    while enemiesTotalHealth > 0 and health > 0:
        command = playerAttack()
        if(command == "ran"):
            if currentRoom not in visitedRooms:
                visitedRooms.append(currentRoom)
                type(colour.reset + colour.bold + colour.green + colour.italic + currentRoom.description + colour.reset)
            else:
                type(colour.reset + colour.blue + colour.italic + currentRoom.description + colour.reset)
            break
        for creature in currentRoom.enemies:
            type(f"{colour.reset}{colour.bold}{colour.red}{creature} swings at you with their {currentRoom.enemies[creature].weapon.name}{colour.reset}")
            if(currentRoom.enemies[creature].weapon.damage >= defense):
                health -=currentRoom.enemies[creature].weapon.damage
                if(health <= 0):
                    type(f"{colour.reset}{colour.italic}{colour.bold}{colour.red}YOU DIED")
                    time.sleep(3)
                    quit()
                type(f"{colour.reset}{colour.bold}{colour.red}You took {currentRoom.enemies[creature].weapon.damage} damage. You're at {health} health!{colour.reset}")
            else:
                type(f"{colour.reset}{colour.bold}{colour.green}{creature} were unable to hit you, as your defense is too high compared to their weapon of choice.{colour.reset}")    
            # Attack Player
            # Check if players defense is lower or equal to the weapons attack damage
    if(currentRoom.clearDescription != None):
        currentRoom.description = currentRoom.clearDescription
    



    # Check if the current room has any items and then asks if they want them
    itemsInRoom = []
    for object in currentRoom.items:
        itemsInRoom.append(object)
    oldInventory = inventory
    toRemove = []

    for object in itemsInRoom:
        take = "!"
        while not (take == "y" or take == "n"):
            if isinstance(currentRoom.items[object], item.WEAPON):
                type(f"{colour.reset}{colour.purple}There is a {object} in this room. Would you like to take it?{colour.reset}")
            if isinstance(currentRoom.items[object], item.ARMOUR):
                type(f"{colour.reset}{colour.purple}There is {object} armour in this room. Would you like to take it?{colour.reset}")
            take = inputType(f"{colour.reset}{colour.purple}Y/N?   -   {colour.bold}{colour.yellow}").lower()
            if take == "y":
                if isinstance(currentRoom.items[object], item.WEAPON):
                    type(f"{colour.reset}{colour.white}{colour.underlined}{colour.bold}You have picked up a {currentRoom.items[object].name}! It does {currentRoom.items[object].damage} damage!{colour.reset}")

                    # Check if the player already has a weapon of the same type
                    weaponType = currentRoom.items[object].type
                    existingWeapon = None
                    for thing in oldInventory:
                        if isinstance(oldInventory[thing], item.WEAPON):
                            if oldInventory[thing].type == weaponType:
                                existingWeapon = oldInventory[thing]
                                break

                    if existingWeapon != None:
                        takeReplace = "!"
                        while not (takeReplace == "y" or takeReplace == "n"):
                            type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}You already have a {weaponType}! It is the {existingWeapon.name}, it deals {colour.underlined}{existingWeapon.damage}{colour.reset}{colour.reset}{colour.red}{colour.bold}{colour.italic} damage.{colour.reset}")
                            type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Are you sure you want to take it, leaving your {existingWeapon.name} behind?")
                            takeReplace = inputType(f"{colour.reset}{colour.purple}Y/N?   -   {colour.bold}{colour.yellow}").lower()
                            if takeReplace == "y":
                                currentRoom.items[existingWeapon.name] = existingWeapon
                                inventory.pop(existingWeapon.name.lower())
                                inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                                currentRoom.items.pop(object)
                            elif takeReplace == "n":
                                break
                            else:
                                type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Please enter a valid input.{colour.reset}")
                    else:
                        inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                        currentRoom.items.pop(object)
                elif isinstance(currentRoom.items[object], item.ARMOUR):
                    type(f"{colour.reset}{colour.white}{colour.underlined}{colour.bold}You have picked up {currentRoom.items[object].name} armour! It has a defense of {currentRoom.items[object].defense}!{colour.reset}")

                    # Check if the player already has a weapon of the same type
                    existingArmour = None
                    for thing in oldInventory:
                        if isinstance(oldInventory[thing], item.ARMOUR):
                            existingArmour = oldInventory[thing]
                            break

                    if existingArmour != None:
                        takeReplace = "!"
                        while not (takeReplace == "y" or takeReplace == "n"):
                            type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}You already have armour! Your current armour is {existingArmour.name}, it has a defense of {colour.underlined}{existingArmour.defense}{colour.reset}")
                            type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Are you sure you want to take it, leaving your {existingArmour.name} armour behind?")
                            takeReplace = inputType(f"{colour.reset}{colour.purple}Y/N?   -   {colour.bold}{colour.yellow}").lower()
                            if takeReplace == "y":
                                currentRoom.items[existingArmour.name] = existingArmour
                                defense = currentRoom.items[object].defense
                                inventory.pop(existingArmour.name.lower())
                                inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                                currentRoom.items.pop(object)
                            elif takeReplace == "n":
                                break
                            else:
                                type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Please enter a valid input.{colour.reset}")
                    else:
                        defense = currentRoom.items[object].defense
                        inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                        currentRoom.items.pop(object)
            
            elif take == "n":
                break
            else:
                type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Please enter a valid input.{colour.reset}")
   
 

    # Asks the user which direction they want to go, repeating if it is not a valid input
    direction = "!"
    while not (direction in currentRoom.exits.lower() or direction in options):
        direction = inputType(f"{colour.reset}{colour.purple}Which direction would you like to head or command you would like to call?  -   {colour.reset}{colour.italic}{colour.yellow}").lower()
        # Checks if the inputType is a command and then runs it
        if direction in optionsList:
            options[direction]()
        # Check if the direction is valid and then changes the current room
        elif direction in currentRoom.exits.lower():
            previousRoom = currentRoom
            if direction == "n":
                currentRoom = currentRoom.nRoom
                break
            elif direction == "s":
                currentRoom = currentRoom.sRoom
                break
            elif direction == "e":
                currentRoom = currentRoom.eRoom
                break
            elif direction == "w":
                currentRoom = currentRoom.wRoom
                break
        else:
            type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}You can't go that way!{colour.reset}")
    



    atexit.register(close)