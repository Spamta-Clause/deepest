import playerScript, colour, room, item, enemy
import time, random, copy, os

# Create the items
fists = item.WEAPON("Fists","fists",1,"None")
boneDagger = item.WEAPON("Bone Dagger","dagger",3,"bladewarden")

holyHammer = item.WEAPON("Holy Hammer","claymore",12,"aurorion",["undead","fiend"])
fireball = item.SPELL("Fireball","spell",18,45,"arcanist")
rustyDagger = item.WEAPON("Rusty Dagger","sword",6,"bladewarden")
rustyHalberd = item.WEAPON("Rusty Halberd","spear",4,"celestrik")
rustyGreatsword = item.WEAPON("Rusty Greatsword","claymore",10,"aurorion")

# Create the armour
leather = item.ARMOUR("Leather",1)
chainmail = item.ARMOUR("Chainmail",3)

# Create the enemies
skeleton = enemy.ENEMY("Skeleton","undead",6,1,boneDagger)
necromancer = enemy.ENEMY("Necromancer","humanoid",18,3,rustyHalberd)

# Create the rooms
library = room.ROOM("library","You are in a library. There is a door to the north and a door to the south.", "NS")
barracks = room.ROOM("barracks","You are in a barracks. There is a door to the north.", "N", items={"Leather":leather})
weaponsRoom = room.ROOM("weaponRoom","You are in a weapons room, there are weapons strewn upon the floor. There is a door to the south as well as one to the west.", "SW", items={"Holy Hammer":holyHammer,"Rusty Halberd":rustyHalberd,"Rusty Dagger":rustyDagger,"Rusty Greatsword":rustyGreatsword,"Fireball":fireball})
cage = room.ROOM("cage","You are in a large cage like room, in front of you lies an animated skeleton, there are doors to the east and to the north.","NE","You are in a cage like room, in front of you lies the body of a defeated animated skeleton",enemies={"S1":copy.copy(skeleton)})
ritualRoom = room.ROOM("ritualRoom","You are in a room with a large pentagram on the floor, there is a door to the south, a necromancer and three animated skeletons are within.","S","You are in a room with a large pentagram on the floor, there is a door to the south, the bodies of a defeated necromancer and three animated skeletons are within",enemies={"N1":copy.copy(necromancer),"S1":copy.copy(skeleton),"S2":copy.copy(skeleton),"S3":copy.copy(skeleton)})

# Create the Player
player = playerScript.PLAYER("None",20,{},0)

import pickle

rooms = [library,barracks,weaponsRoom,cage,ritualRoom]
roomsDict = {"library":library,"barracks":barracks,"weaponsRoom":weaponsRoom,"cage":cage,"ritualRoom":ritualRoom}

error = colour.red + colour.bold + colour.italic
information =  colour.bold + colour.italic + colour.white
# Checks if there is the room file, if not it makes one
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
library.connectedRooms = {"n":weaponsRoom,"s":barracks}
barracks.connectedRooms = {"n":library}
weaponsRoom.connectedRooms = {"s":library,"w":cage}
cage.connectedRooms = {"e":weaponsRoom,"n":ritualRoom}
ritualRoom.connectedRooms = {"s":cage}

currentRoom = barracks
visitedRooms = []

player.health = 20
player.defense = 0
player.inventory = {}


def slowPrint(text, delay=0.03):
    totalTime = len(text)/80 + 1.8
    isCode = False
    for letter in text:
        print(letter.replace("~",""), end="", flush=True)
        if(letter != "~" and not isCode):
            time.sleep(random.uniform(totalTime/len(text),(totalTime + 0.2)/len(text)))
        elif(letter == "~"):
            isCode = not isCode
    print()

def slowInput(text, delay=0.03):
    totalTime = len(text)/80 + 1.8
    isCode = False  # Initialize isCode to False
    
    for letter in text:
        print(letter.replace("~",""), end="", flush=True)
        if(letter != "~" and not isCode):
            time.sleep(random.uniform(totalTime/len(text),(totalTime + 0.2)/len(text)))
        elif(letter == "~"):
            isCode = not isCode
        
    return input()

def start():
    # Assigns the values to the variables from the files
    folderPath = "rooms"

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    global player
    global currentRoom
    global visitedRooms

    # Load the information regarding the player's class, or asks them via an input statement
    try:
        player = pickle.load(open("player.sp@mta","rb"))
    except:
        classOptions = ["aurorion","celestrik","bladewarden","arcanist"]
        playerClass = "!"
        while playerClass not in classOptions:  # Keep asking until a valid input is given
            playerClass = slowInput(f"{colour.reset}{colour.purple}What class would you like to play? Aurorion / Bonus damage with claymores, Celestrik / Attacks multiple times with spears, Bladewarden / Bonus damage and two attacks with shortsword, Arcanist / Higher chance to hit with spells     -     {colour.italic}{colour.yellow}").lower()
            
            if playerClass not in classOptions:
                slowInput(f"{colour.reset}{error}Please enter a valid input.{colour.reset}")
        

        player = playerScript.PLAYER(playerClass,20,{},0)
    
    # Load the information regarding the current room and visited rooms, or assigns them to the default values
    try:
        currentRoom = pickle.load(open("currentRoom.sp@mta","rb"))
    except:
        currentRoom = barracks
    try:
        visitedRooms = pickle.load(open("prevRooms.sp@mta","rb"))
    except:
        visitedRooms = []


def close():
    slowPrint(f"{colour.reset}{information}As you rest by your campfire, your game begins saving.")
    # Saves the information regarding inventory, health, current room and visited rooms
    global player
    global currentRoom
    global visitedRooms
    #Saves the information regarding inventory, health, current room and visited rooms
    try:
            plyr = open("player.sp@mta","xb")
    except:
            plyr = open("player.sp@mta","wb")
    try:
            cR = open("currentRoom.sp@mta","xb") 
    except:
            cR = open("currentRoom.sp@mta","wb")
    try:
            pR = open("prevRooms.sp@mta","xb")
    except:
            pR = open("prevRooms.sp@mta","wb")
    pickle.dump(player,plyr)
    pickle.dump(currentRoom,cR)
    pickle.dump(visitedRooms,pR)

    # Saves information regarding rooms
    for instance in rooms:
            filename = f'rooms\\{instance.name}.pickle'
            with open(filename, 'wb') as file:
                pickle.dump(instance, file)
    plyr.close()
    cR.close()
    pR.close()
    slowPrint(f"{colour.reset}{information}Your game has been saved.")

start()

def Show_Inventory():
    if(len(player.inventory) == 0):
        slowPrint(f"{colour.reset}{information}Your inventory is empty.")
        return
    else:
        slowPrint(f"{colour.reset}{information}Your inventory contains:")
        for thing in player.inventory:
            if(isinstance(player.inventory[thing], item.WEAPON)):
                slowPrint(f"{colour.reset}{information}{player.inventory[thing].name}  -   {player.inventory[thing].damage} damage")
            elif(isinstance(player.inventory[thing], item.ARMOUR)):
                slowPrint(f"{colour.reset}{information}{player.inventory[thing].name} Armour  -   {player.inventory[thing].defense} defense")
def Show_Commands():
    slowPrint(f"{colour.reset}{information}Commands:{optionsList}")

optionsList = ["i","help","save"]
options = {"i":Show_Inventory, "help":Show_Commands,"save":close}

currentRoom = weaponsRoom
while True:
    enemiesTotalHealth = 0
    # Check if the current room has been visited before and then types the description, changing the colour based on whether or not it has
    names = []
    for room in visitedRooms:
        names.append(room.name)
    if currentRoom.name not in names:
        visitedRooms.append(currentRoom)
        slowPrint(f"{colour.reset}{colour.bold}{colour.green}{colour.italic}{currentRoom.description}{colour.reset}")
    else:
        slowPrint(f"{colour.reset}{colour.blue}{colour.italic}{currentRoom.description}{colour.reset}")


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
        global player
        global previousRoom
        global currentRoom
        # Player attacking
        attack = "!"
        enemyOptions = []
        enemyOptionsHigh = []
        for roomEnemy in currentRoom.enemies:
            if(currentRoom.enemies[roomEnemy].health > 0):
                enemyOptions.append(roomEnemy.lower())
                enemyOptionsHigh.append(roomEnemy.capitalize())

        slowPrint(f"{colour.green}{colour.bold}{colour.italic}The enemies present in this room are, {', '.join(enemyOptionsHigh)}.")
        while not (attack.lower() in enemyOptions or attack.lower() == "run"):
            attack = slowInput(f"{colour.reset}{colour.purple}What would you like to do? Enter either run, or the name of the enemy you would like to attack.   -   {colour.reset}{colour.italic}{colour.yellow}")
            if(not(attack.lower() in enemyOptions or attack.lower() == "run")):   
                slowPrint(f"{colour.reset}{error}Please enter a valid input.{colour.reset}")

        
        if(attack.lower() == "run"):
            currentRoom = previousRoom
            return "ran"
        
                
        if(attack.lower() in enemyOptions):
            weapons = []
            for thing in player.inventory:
                if isinstance(player.inventory[thing], item.WEAPON):
                    weapons.append(player.inventory[thing].name + f", dealing {player.inventory[thing].damage} damage")
                
                elif isinstance(player.inventory[thing], item.SPELL):
                    weapons.append(player.inventory[thing].name + f", dealing {player.inventory[thing].damage} damage, with a chance of {player.inventory[thing].chance}%")
                print(player.inventory[thing].name)
            weapon = "!"
            if(len(weapons) == 0):
                slowPrint(f"{colour.reset}{error}You have no weapons!{colour.reset}")
                weapon = "fists"
            else:    
                weapon = slowInput(f"{colour.reset}{colour.purple}What weapon would you like to use? Your current items are {', '.join(weapons)}  -   {colour.reset}{colour.italic}{colour.yellow}")
                weapons = []
                for thing in player.inventory:
                    if isinstance(player.inventory[thing], item.WEAPON):
                        weapons.append(player.inventory[thing].name.lower())
                    elif isinstance(player.inventory[thing], item.SPELL):
                        weapons.append(player.inventory[thing].name.lower())
                if(not (weapon.lower() in weapons)):
                    slowPrint(f"{colour.reset}{error}Please enter a valid input.{colour.reset}")
                    playerAttack()
            weapons = []
            for thing in player.inventory:
                if isinstance(player.inventory[thing], item.WEAPON):
                    weapons.append(player.inventory[thing].name.lower())
                elif isinstance(player.inventory[thing], item.SPELL):
                    weapons.append(player.inventory[thing].name.lower())
                    
            if ((weapon.lower() in weapons) or (weapon.lower() == "fists")):
                weapons = []
                totalDamage = 0
                for thing in player.inventory:
                    if isinstance(thing, item.WEAPON):
                        weapons.append(player.inventory[thing].name.lower())
                    elif isinstance(thing, item.SPELL):
                        weapons.append(player.inventory[thing].name.lower())
                    
                if(weapon != "fists"):
                    
                    bonus = 0
                    loop = 1
                    chanceModifier = 1
                    for weaponWeakness in player.inventory[weapon.lower()].weakness:
                        if(currentRoom.enemies[attack.capitalize()].type == weaponWeakness):
                            bonus -= (player.inventory[weapon.lower()].damage/2)
                    if(player.inventory[weapon.lower()].preferedClass == player.playerClass):
                        for weaponStrength in player.inventory[weapon.lower()].proficiency:
                            if(currentRoom.enemies[attack.capitalize()].type == weaponStrength):
                                bonus += player.inventory[weapon.lower()].damage
                        if(player.playerClass == "aurorion"):
                            bonus += 4
                            loop = 1
                        if(player.playerClass == "bladewarden"):
                            bonus += 2
                            loop = 2
                        if(player.playerClass == "celestrik"):
                            loop = random.randint(3,4)
                        if(player.playerClass == "arcanist"):
                            chanceModifier = 2
                    if(isinstance(player.inventory[weapon.lower()], item.SPELL)):
                            if(random.randint(1,100) < player.inventory[weapon.lower()].chance * chanceModifier):
                                slowPrint(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}You cast {weapon.lower().capitalize()} against {attack.capitalize()}! You inflict a total of {player.inventory[weapon.lower()].damage + bonus} damage!{colour.reset}")
                                currentRoom.enemies[attack.capitalize()].health -= player.inventory[weapon.lower()].damage + bonus
                                totalDamage += player.inventory[weapon.lower()].damage + bonus
                            else:
                                slowPrint(f"{colour.reset}{colour.bold}{colour.red}You fail to cast {weapon.lower().capitalize()}{colour.reset}")
                    else:
                        for x in range(loop):
                            if(player.inventory[weapon.lower()].damage+bonus >= currentRoom.enemies[attack.capitalize()].defense):
                                slowPrint(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}You attack {attack.capitalize()} with your {weapon.lower().capitalize()}! You inflict a total of {player.inventory[weapon.lower()].damage + bonus} damage!{colour.reset}")
                                currentRoom.enemies[attack.capitalize()].health -= player.inventory[weapon.lower()].damage + bonus
                                totalDamage += player.inventory[weapon.lower()].damage + bonus  
                            else:
                                slowPrint(f"{colour.reset}{colour.bold}{colour.red}You were unable to hit {attack.capitalize()}, as their defense is too high compared to your weapon of choice.{colour.reset}")
                else:        
                    if(1 >= currentRoom.enemies[attack.capitalize()].defense):
                        slowPrint(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}You attack {attack.capitalize()} with your fists! You inflict a total of 1 damage!{colour.reset}")
                        currentRoom.enemies[attack.capitalize()].health -= 1
                    else:
                        slowPrint(f"{colour.reset}{colour.bold}{colour.red}You were unable to hit {attack.capitalize()}, as their defense is too high compared to your weapon of choice.{colour.reset}")
                        
            if(currentRoom.enemies[attack.capitalize()].health <= 0):
                slowPrint(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}{attack.capitalize()} falls to the floor!")
                enemiesTotalHealth -= currentRoom.enemies[attack.capitalize()].maxHealth
                if(random.randint(1,10) < 5):
                    slowPrint(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}{attack.capitalize()} dropped their {currentRoom.enemies[attack.capitalize()].weapon.name}!{colour.reset}")
                    currentRoom.items[currentRoom.enemies[attack.capitalize()].weapon.name] = currentRoom.enemies[attack.capitalize()].weapon
                if(totalDamage >= currentRoom.enemies[attack.capitalize()].maxHealth * 2):
                    # Then deals overflow damage to the next enemy
                    # Player is able to choose
                    if(len(currentRoom.enemies)>1):
                        slowPrint(f"{colour.reset}{colour.bold}{colour.italic}{colour.green}You dealt massive damage, now you are able to attack again!")
                        currentRoom.enemies.pop(attack.capitalize())
                        playerAttack()
                    else:
                        currentRoom.enemies.pop(attack.capitalize())
                else:
                    currentRoom.enemies.pop(attack.capitalize())
                
    if(player.health <= 0):
        slowPrint(f"{colour.reset}{colour.italic}{colour.bold}{colour.red}YOU DIED")
        for x in os.listdir("rooms"):
            os.remove(f"rooms\\{x}")
        for x in os.listdir():
            if("sp@mta" in x):
                os.remove(x)
        quit()

    # Lets players and enemies attack
    while enemiesTotalHealth > 0 and player.health > 0:
        command = playerAttack()
        if(command == "ran"):
            if currentRoom not in visitedRooms:
                visitedRooms.append(currentRoom)
                slowPrint(f"{colour.reset + colour.bold + colour.green + colour.italic}{currentRoom.description}{colour.reset}")
            else:
                slowPrint(colour.reset + colour.blue + colour.italic + currentRoom.description + colour.reset)
            break
        for creature in currentRoom.enemies:
            slowPrint(f"{colour.reset}{colour.bold}{colour.red}{creature} swings at you with their {currentRoom.enemies[creature].weapon.name}{colour.reset}")
            if(currentRoom.enemies[creature].weapon.damage >= player.defense):
                player.health -=currentRoom.enemies[creature].weapon.damage
                if(player.health <= 0):
                    slowPrint(f"{colour.reset}{colour.italic}{colour.bold}{colour.red}YOU DIED")
                    time.sleep(3)
                    quit()
                slowPrint(f"{colour.reset}{colour.bold}{colour.red}You took {currentRoom.enemies[creature].weapon.damage} damage. You're at {player.health} health!{colour.reset}")
            else:
                slowPrint(f"{colour.reset}{colour.bold}{colour.green}{creature} were unable to hit you, as your defense is too high compared to their weapon of choice.{colour.reset}")    
            # Attack Player
            # Check if players defense is lower or equal to the weapons attack damage
    if(currentRoom.clearDescription != None):
        currentRoom.description = currentRoom.clearDescription
    



    # Check if the current room has any items and then asks if they want them
    itemsInRoom = []
    for object in currentRoom.items:
        itemsInRoom.append(object)
    oldInventory = player.inventory
    toRemove = []

    for object in itemsInRoom:
        take = "!"
        while not (take == "y" or take == "n"):
            if isinstance(currentRoom.items[object], item.WEAPON):
                slowPrint(f"{colour.reset}{colour.purple}There is a {object} in this room. Would you like to take it?{colour.reset}")
            if isinstance(currentRoom.items[object], item.SPELL):
                slowPrint(f"{colour.reset}{colour.purple}There is a {object} scroll in this room. Would you like to take it?{colour.reset}")
            if isinstance(currentRoom.items[object], item.ARMOUR):
                slowPrint(f"{colour.reset}{colour.purple}There is {object} armour in this room. Would you like to take it?{colour.reset}")
            take = slowInput(f"{colour.reset}{colour.purple}Y/N?   -   {colour.italic}{colour.yellow}").lower()
            if take == "y":
                if isinstance(currentRoom.items[object], item.SPELL):
                    slowPrint(f"{colour.reset}{colour.white}{colour.underlined}{colour.bold}You have picked up a {currentRoom.items[object].name} scroll! It does {currentRoom.items[object].damage} damage, and has an accuracy of {currentRoom.items[object].chance}%!{colour.reset}")
                    player.inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                if isinstance(currentRoom.items[object], item.WEAPON):
                    slowPrint(f"{colour.reset}{colour.white}{colour.underlined}{colour.bold}You have picked up a {currentRoom.items[object].name}! It does {currentRoom.items[object].damage} damage!{colour.reset}")

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
                            slowPrint(f"{colour.reset}{error}You already have a {weaponType}! It is the {existingWeapon.name}, it deals {colour.underlined}{existingWeapon.damage}{colour.reset}{colour.reset}{error} damage.{colour.reset}")
                            slowPrint(f"{colour.reset}{error}Are you sure you want to take it, leaving your {existingWeapon.name} behind?")
                            takeReplace = slowInput(f"{colour.reset}{colour.purple}Y/N?   -   {colour.italic}{colour.yellow}").lower()
                            if takeReplace == "y":
                                currentRoom.items[existingWeapon.name] = existingWeapon
                                player.inventory.pop(existingWeapon.name.lower())
                                player.inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                                currentRoom.items.pop(object)
                            elif takeReplace == "n":
                                break
                            else:
                                slowPrint(f"{colour.reset}{error}Please enter a valid input.{colour.reset}")
                    else:
                        player.inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                        currentRoom.items.pop(object)
                elif isinstance(currentRoom.items[object], item.ARMOUR):
                    slowPrint(f"{colour.reset}{colour.white}{colour.underlined}{colour.bold}You have picked up {currentRoom.items[object].name} armour! It has a defense of {currentRoom.items[object].defense}!{colour.reset}")

                    # Check if the player already has a weapon of the same type
                    existingArmour = None
                    for thing in oldInventory:
                        if isinstance(oldInventory[thing], item.ARMOUR):
                            existingArmour = oldInventory[thing]
                            break
                    
                    if existingArmour != None:
                        takeReplace = "!"
                        while not (takeReplace == "y" or takeReplace == "n"):
                            slowPrint(f"{colour.reset}{error}You already have armour! Your current armour is {existingArmour.name}, it has a defense of {colour.underlined}{existingArmour.defense}{colour.reset}")
                            slowPrint(f"{colour.reset}{error}Are you sure you want to take it, leaving your {existingArmour.name} armour behind?")
                            takeReplace = slowInput(f"{colour.reset}{colour.purple}Y/N?   -   {colour.italic}{colour.yellow}").lower()
                            if takeReplace == "y":
                                currentRoom.items[existingArmour.name] = existingArmour
                                player.defense = currentRoom.items[object].defense
                                player.inventory.pop(existingArmour.name.lower())
                                player.inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                                currentRoom.items.pop(object)
                            elif takeReplace == "n":
                                break
                            else:
                                slowPrint(f"{colour.reset}{error}Please enter a valid input.{colour.reset}")
                    else:
                        player.defense = currentRoom.items[object].defense
                        player.inventory[currentRoom.items[object].name.lower()] = currentRoom.items[object]
                        currentRoom.items.pop(object)
            
            elif take == "n":
                break
            else:
                slowPrint(f"{colour.reset}{error}Please enter a valid input.{colour.reset}")
   
 

    # Asks the user which direction they want to go, repeating if it is not a valid input
    direction = "!"
    while not (direction in currentRoom.exits.lower() or direction in options):
        direction = slowInput(f"{colour.reset}{colour.purple}Which direction would you like to head or command you would like to call?  -   {colour.reset}{colour.italic}{colour.yellow}").lower()
        # Checks if the slowInput is a command and then runs it
        if direction in optionsList:
            options[direction]()
        # Check if the direction is valid and then changes the current room
        elif direction in currentRoom.exits.lower():
            previousRoom = currentRoom
            currentRoom = currentRoom.connectedRooms[direction]
            break
        else:
            slowPrint(f"{colour.reset}{error}You can't go that way!{colour.reset}")
