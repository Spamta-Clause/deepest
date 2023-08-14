import colour, room, item, enemy, colour
import time, random

# Create the items
fists = item.WEAPON("Fists","fists",1)
rustyHalberd = item.WEAPON("Rusty Halberd","spear",6)
bronzeHalberd = item.WEAPON("Bronze Halberd","spear",13)
rustyGreatsword = item.WEAPON("Rusty Greatsword","claymore",15)

leather = item.ARMOUR("Leather",1)
chainmail = item.ARMOUR("Chainmail",3)
# Create the enemies
skeleton = enemy.ENEMY("Skeleton","undead",10,1,rustyHalberd)


# Create the rooms
library = room.ROOM("You are in a library. There is a door to the north and a door to the south.", "NS", items={"Chainmail":chainmail})
barracks = room.ROOM("You are in a barracks. There is a door to the north.", "N", items={"Leather":leather})
weaponsRoom = room.ROOM("You are in a weapons room, there are weapons strewn upon the floor. There is a door to the south as well as one to the west.", "SW", items={"Rusty Halberd":rustyHalberd,"Bronze Halberd":bronzeHalberd,"Rusty Greatsword":rustyGreatsword})
cage = room.ROOM("You are in a large cage like room, in front of you lies an animated skeleton","E",enemies={"S1":skeleton})


# Set the exits for the rooms
library.nRoom=weaponsRoom 
library.sRoom=barracks

barracks.nRoom=library

weaponsRoom.sRoom=library
weaponsRoom.wRoom=cage

currentRoom = weaponsRoom

visitedRooms = []

health = 10
defense = 0
inventory = {}



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

optionsList = ["i","help"]
options = {"i":Show_Inventory, "help":Show_Commands}

while True:
    # Check if the current room has been visited before and then types the description, changing the colour based on whether or not it has
    if currentRoom not in visitedRooms:
        visitedRooms.append(currentRoom)
        type(colour.reset + colour.bold + colour.green + colour.italic + currentRoom.description + colour.reset)
    else:
        type(colour.reset + colour.blue + colour.italic + currentRoom.description + colour.reset)

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
                    weapon_type = currentRoom.items[object].type
                    existingWeapon = None
                    for thing in oldInventory:
                        if isinstance(oldInventory[thing], item.WEAPON):
                            if oldInventory[thing].type == weapon_type:
                                existingWeapon = oldInventory[thing]
                                break

                    if existingWeapon != None:
                        takeReplace = "!"
                        while not (takeReplace == "y" or takeReplace == "n"):
                            type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}You already have a {weapon_type}! It is the {existingWeapon.name}, it deals {colour.underlined}{existingWeapon.damage}{colour.reset}{colour.reset}{colour.red}{colour.bold}{colour.italic} damage.{colour.reset}")
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
                    if(not (weapon.lower in weapons)):
                        type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Please enter a valid input.{colour.reset}")
                        playerAttack()
                weapons = []
                for thing in inventory:
                    if isinstance(inventory[thing], item.WEAPON):
                        weapons.append(inventory[thing].name.lower())
                if(currentRoom.enemies[attack.capitalize()].health <= 0):
                    type(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}{attack.capitalize()} falls to the floor!")
                    enemiesTotalHealth -= currentRoom.enemies[attack.capitalize()].maxHealth
                    currentRoom.enemies.pop(attack.capitalize())
                if ((weapon.lower() in weapons) or (weapon.lower() == "fists")):
                    weapons = []
                    for thing in inventory:
                        if isinstance(thing, item.WEAPON):
                            weapons.append(inventory[thing].name.lower())
                    
                    if(weapon != "fists"):
                        if(inventory[weapon.lower()].damage >= currentRoom.enemies[attack.capitalize()].defense):
                            type(f"{colour.reset}{colour.green}{colour.bold}{colour.italic}You attack the {attack.capitalize()} with your {weapon}! You inflict a total of {inventory[weapon.lower()].damage} damage!{colour.reset}")
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
                    currentRoom.enemies.pop(attack.capitalize())
            else:   
                type(f"{colour.reset}{colour.red}{colour.bold}{colour.italic}Please enter a valid input.{colour.reset}")
                playerAttack()

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