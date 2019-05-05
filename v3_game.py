import random
import time

class item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


class weapon(item):
    def __init__(self, name, description, damage):
        super().__init__(name, description)
        self.damage = damage
        self.defense = 0


class defensive(item):
    def __init__(self, name, description, defense):
        super().__init__(name, description)
        self.defense = defense
        self.damage = 0

class read(item):
    def __init__(self, name, description, content):
        super().__init__(name, description)
        self.content = content

class entity(object):
    def __init__(self, health, attack, defence, name, equipment):
        self.health = health
        self.attack = attack
        self.defence = defence
        self.name = name
        self.equipment = equipment

staff = weapon("STAFF", "A magical staff.", 3)
magic_staff = weapon("STAFF", "A long magic staff, teeming with ancient magic.", 5)
magic_idol = defensive("IDOL", "A sacred magic goblin relic.", 4)
spear = weapon("SPEAR", "A wooden stick with a sharpened end.", 2)
sword = weapon("SWORD", "A long silver blade decorated with pulsing blue Elven runes.", 3)
shield = defensive("SHIELD", "A wooden shield, with a weathered iron border around the edge.", 3)
stone = weapon("STONE", "A sharp stone.", 1)
breath_weapon = weapon("BREATH WEAPON", "A fiery blast.", 5)

goblin = entity(5, 3, 3, "GOBLIN", spear)
player = entity(10, 5, 5, "PLAYER", None)
bat = entity(1, 0, 0,"BAT",  None)
dragon = entity(15, 5, 5, "DRAGON", breath_weapon)
goblin_mage = entity(6, 4, 4, "GOBLIN", staff)

directions = [["NORTH", "N"], ["SOUTH", "S"], ["EAST", "E"], ["WEST", "W"]]
inventory = [sword, shield]

global room_items
room_items = [sword, shield]
global room_monsters
room_monsters = []
global string_items

string_items = []


def travel():
    print("What will you do?")
    ask = input(">").upper()
    x = ask.rsplit(" ")

    if len(x) == 0:
        print("<?> - Enter actual words this time.")
    elif len == 1:
        parser(x[0], None)
    if len(x) == 2:
        parser(x[0], x[1])
        x.clear()
    return ask

def parser(verb, noun):
    if verb == "SHOW" and noun == "INVENTORY":
        for item in inventory:
            print(item.name)
    elif verb in directions[0] or verb in directions[1] or verb in directions[2] or verb in directions[3] and noun == None:
        return verb
    elif verb == "FIGHT" and noun == room_monsters[0].name:
        for x in room_monsters:
            if x.name == noun:
                battle(player, x)
    elif verb == "EXAMINE" and noun != "":
        for x in inventory:
            if x.name == noun:
                print(x.name, ": ", x.description)
            else:
                print("You don't have ", x.name)

    elif verb == "TAKE" and noun != "":
        #print("Here")

        for x in room_items:
            if x.name == noun:
                print("I can take that ", x.name)
                inventory.append(x)
                room_items.remove(x)
                #print(inventory)
                for x in inventory:
                    print(x.name)
                print(room_items)
                for x in room_items:
                    print(x.name)

    else:
        print("Not a move in this game.")
        print(":(")

def battle(combatant_1, combatant_2):
    global inventory
    global AtkValue
    global DefValue
    AtkValue = 0
    DefValue = 0
    won = False
    turn = 1
    DefValue = combatant_2.defence
    print("ADVENTURER STATS:\n Health: ", combatant_1.health, "\n Attack: ", combatant_1.attack, "\n Defence: ", combatant_1.defence)
    print("ENEMY STATS:\n Health: ", combatant_2.health, "\n Attack: ", combatant_2.attack, "\n Defence: ", combatant_2.defence)
    while not won:
        if turn == 1:
            AtkValue = 0
            print()
            print("Will you attack(1) or block(2) this turn?")
            move = int(input(">"))
            if move == 1:
                print("What weapon will you use?")
                for weapon in inventory:
                    print("  ", weapon.name, " deals: ", weapon.damage, " damage.")
                combat_item = input(">").upper()
                string_items.clear()
                for weapon in inventory:
                    string_items.append(weapon.name)
                if combat_item in string_items:
                    print("You are using ", combat_item)
                    for item in inventory:
                        if item.name == combat_item:
                            AtkValue = combatant_1.attack + item.damage
                            x = item.name
                else:
                    print("You do not have ", combat_item)
                    AtkValue = combatant_1.attack
                print("You attack ", combatant_2.name, " with the ", combat_item,)
                if AtkValue <= DefValue or AtkValue == DefValue:
                    print("Despite your best efforts, the ", combatant_2.name, " resists your attack.")
                elif AtkValue >= DefValue:
                    print("You wound the ", combatant_2.name, ".")
                    damage = AtkValue - DefValue
                    combatant_2.health = combatant_2.health - damage
                    if combatant_2.health == 0 or combatant_2.health <= 0:
                        print("CONGRATULATIONS!")
                        print("You have slain the ", combatant_2.name, ".")
                        AtkValue = 0
                        DefValue = 0
                        if combatant_2.name == "DRAGON":
                            print("GAME OVER!")
                            print("YOU HAVE BROUGHT PEACE AND PROSPERITY TO THE LAND!")
                        won = True

                    else:
                        print("Now it is your enemies turn.")
                        turn = 2
            elif move == 2:
                print("What defense will you use?")
                for defensive in inventory:
                    print("  ", defensive.name, " protects against: ", defensive.defense, " damage.")
                combat_item = input(">").upper()
                for defensive in inventory:
                    if combat_item == defensive.name:
                        print("You are using ", combat_item)
                        DefValue = combatant_1.defence = combatant_1.defence + defensive.defense
                    else:
                        print("You do not have ", combat_item, ".")
                        DefValue = combatant_1.defence
                print("You block the ", combatant_2.name, ".")
                print("Now it is your enemies turn.")
                turn = 2
            elif move == 3:
                print("You stand your ground.")
                DefValue = combatant_1.defence
                print("Now it is your enemies turn.")
                turn = 2

        if turn == 2:
            AtkValue = 0
            print()
            move = random.randint(1,2)
            if move == 1:
                print("The ", combatant_2.name, "attacks!")
                AtkValue = combatant_2.attack + combatant_2.equipment.damage
                if AtkValue >= DefValue:
                    print("You are wounded by the ", combatant_2.name, ".")
                    damage = AtkValue - DefValue
                    combatant_1.health = combatant_1.health - damage
                    if combatant_1.health <= 0 or combatant_1.health == 0:
                        print("You have been killed. :(")
                        print("Aah well, better luck next time.")
                        ask = input(">")
                        outside_dungeon()
                elif AtkValue <= DefValue or AtkValue == DefValue:
                    print("The ", combatant_2.name, " tries, but it cannot harm you!")
            elif move == 2:
                print("The ", combatant_2.name, "stands its ground.")
            AtkValue = 0


        print()
        print("ADVENTURER STATS:\n Health: ", combatant_1.health, "\n Attack: ", combatant_1.attack, "\n Defence: ", combatant_1.defence)
        print("ENEMY STATS:\n Health: ", combatant_2.health, "\n Attack: ", combatant_2.attack, "\n Defence: ", combatant_2.defence)
        print()
        turn = 1






def outside_dungeon():
    global room_monsters
    room_monsters = None
    print("There is a cave to your NORTH here.")
    print("In every other direction you can see trees.")
    print("And more trees. And yet more trees.")
    while True:
        command = travel()
        if command in directions[0]:
            hall()
        else:
            print("You wander into the forest and soon find yourself lost in the woods.")
            forest()

def hall():
    global room_monsters
    global room_items
    room_monsters = None
    room_items = [stone]
    print("You enter the Cave.")
    print("The cave seems to be made of stone and you can see a message scratched on the wall:")
    print("/ /:\ /:\ / |:\ /|: : /.\ /.\ /:\ /|: : /| /|: /.: /.\ \:/ : \: /|: |:\ /|:")
    print("To the SOUTH is the exit.")
    print("To the NORTH is total darkness, or to an ADVENTURER such as yourself an ADVENTURE just waiting to happen")
    #print("\n\n Adventure - Noun: \n Going into a daring or risky activity \n with a huge amount of totally unearned confidence.")
    #print(("\n\n Adventurer - Noun: \n Someone who participates in adventures,\n particularly to kill monsters(In the adventurers eyes)\n such as goblins, in order to earn the title \n Monster Killer. However goblins, are people too,\n so really they seek to earn the title of \n People Killer."))
    while True:
        command = travel()
        print(command)
        if command in directions[0]:
            dark_hall()
        elif command in directions[1]:
            outside_dungeon()

def dark_hall():
    global room_monsters
    global room_items
    room_monsters = None
    room_items = None
    print("It's pitch black in here and you stumble around blindly,")
    print("To the SOUTH is a faint light. To the EAST and WEST are cool, rough stone.")
    print("To the NORTH is something that feels like wood, possibly a door.")
    while True:
        command = travel()
        if command in directions[0]:
            adventurer_room()
        if command in directions[1]:
            hall()


def adventurer_room():
    global room_items
    global room_monsters
    room_monsters = None
    room_items = None
    print("This room is well lit and the walls are made out of fine flagstones. A dozen torches hang in brackets on the wall.")
    print("However, in one corner lies a rotten decaying corpse.")
    print("The stench is terrible.")
    print("To the EAST is a dark passage.")
    print("To the SOUTH is a wooden door.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_hall()
        if command in directions[1]:
            hall()

def goblin_hall():
    global room_items
    global room_monsters
    room_items = None
    room_monsters = [goblin]
    print("This hall is spartan and empty. To the WEST is a brightly lit room. To the EAST is a door.")
    print("However, standing at the end of the hall, is a ", room_monsters[0].name)
    while True:
        command = travel()
        if command in directions[2]:
            goblin_walkway1()
        if command in directions[3]:
            adventurer_room()

def goblin_walkway1():
    global room_items
    global room_monsters
    room_monsters = [bat]
    room_items = None
    print("There is a rickety wooden bridge here at the edge of a great cavern.")
    print("Beneath the bridge is jagged rocks sinking into the darkness.")
    print("To the WEST is a door. To the EAST is a pillar with a well lit building upon it.")
    print("There is a bat here.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_hut1()
        if command in directions[3]:
            goblin_hall()

def goblin_hut1():
    global room_items
    global room_monsters
    room_monsters = [goblin]
    room_items = [stone]
    print("This is a small hut, made of stalictites and staligmites forming the walls, and a fire in the centre.")
    print("A goblin stands guard.")
    print("To the EAST and WEST are bridges.")
    print("The WEST one leads towards the wall of the cave. The EAST one goes further into it.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_walkway2()
        if command in directions[3]:
            goblin_walkway1()

def goblin_walkway2():
    global room_items
    global room_monsters
    room_monsters = None
    room_items = None
    print("There is a rickety wooden bridge here.")
    print("Beneath the bridge is jagged rocks sinking into the darkness.")
    print("To the WEST is a hut. To the EAST is a pillar with a pulsing blue light upon it")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_pool()
        if command in directions[3]:
            goblin_hut1()



def goblin_pool():
    global room_items
    global room_monsters
    room_monsters = [bat]
    room_items = None
    print("Here there is a rectangular pool, a few inches deep.")
    print("In the pool is a pulsing, glowing blue liquid, and a goblin skeleton, arms spread out facing the ceiling.")
    print("To the EAST and WEST are rickety bridges to other pillars.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_walkway3()
        if command in directions[3]:
            goblin_walkway2()

def goblin_walkway3():
    global room_items
    global room_monsters
    room_monsters = None
    room_items = None
    print("There is a rickety wooden bridge here.")
    print("Beneath the bridge is jagged rocks sinking into the darkness.")
    print("To the WEST is a pillar with a pulsing blue light upon it. To the EAST is a hut.")
    print("There is a bat here.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_hut2()
        if command in directions[3]:
            goblin_pool()

def goblin_hut2():
    global room_items
    global room_monsters
    room_monsters = [goblin]
    room_items = [stone]
    print("This is a small hut, made of stalictites and staligmites forming the walls, and a table in the centre.")
    print("A goblin stands guard.")
    print("To the EAST and WEST are bridges.")
    print("The WEST one leads out of the cave. The EAST one goes further into it.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_walkway4()
        if command in directions[3]:
            goblin_walkway3()

def goblin_walkway4():
    global room_items
    global room_monsters
    room_monsters = None
    room_items = None
    print("There is a rickety wooden bridge here.")
    print("Beneath the bridge is jagged rocks sinking into the darkness.")
    print("To the WEST is a pillar with a hut upon it. To the EAST is a is a temple formed out of stalictites.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_temple1()
        if command in directions[3]:
            goblin_hut2()

def goblin_temple1():
    global room_items
    global room_monsters
    room_items = [magic_idol]
    room_monsters = [goblin]
    print("Nightmarish images adorn the walls of this room, of demons...")
    print("... And Dragons!")
    print("A goblin guards a sacred idol.")
    print("To the WEST is a rickety bridge. To the EAST is a stone bridge with ornate carvings. To the NORTH is another stone bridge.")
    while True:
        command = travel()
        if command in directions[0]:
            goblin_temple_bridge1()
        if command in directions[2]:
            goblin_temple_bridge2()
        if command in directions[3]:
            goblin_walkway4()

def goblin_temple_bridge1():
    global room_items
    global room_monsters
    room_monsters = None
    room_items = None
    print("This is a bridge with detailed carvings of tales from goblin myth and legend.")
    print("To the NORTH is a small part of the temple that is isolated.")
    print("To the SOUTH is the main body of the temple.")
    while True:
        command = travel()
        if command in directions[0]:
            goblin_temple2()
        if command in directions[1]:
            goblin_temple1()

def goblin_temple_bridge2():
    global room_items
    global room_monsters
    room_monsters = None
    room_items = None
    print("This is a bridge with detailed carvings of tales from goblin myth and legend.")
    print("To the EAST is much more of the temple.")
    print("To the WEST is the temple entrance.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_temple3()
        if command in directions[3]:
            goblin_temple1()

def goblin_temple2():
    global room_items
    global room_monsters
    room_monsters = [goblin]
    room_items = None
    print("A small fire burns in the centre of this room. A goblin sits by it.")
    print("To the SOUTH is a bridge.")
    while True:
        command = travel()
        if command in directions[1]:
            goblin_temple_bridge1()

def goblin_temple3():
    global room_items
    global room_monsters
    room_monsters = [goblin_mage]
    room_items = [magic_staff]
    print("A great statue is in this room. It shows goblins ruling over the known realms.")
    print("To the EAST and WEST are bridges.")
    print("A goblin mage twirls his staff expectantly.")
    print("There is a staff here, pulsing with ancient and powerful magic.")
    while True:
        command = travel()
        if command in directions[2]:
            goblin_temple_bridge3()
        if command in directions[3]:
            goblin_temple_bridge2()

def goblin_temple_bridge3():
    global room_items
    global room_monsters
    room_items = None
    room_monsters = [dragon]
    print("This bridge is at the edge of the cavern.")
    print("To the WEST is the main temple.")
    print("To the EAST is a door bearing an inscription above it which reads:")
    print("     Here Be Dragons")
    while True:
        command = travel()
        if command in directions[2]:
            treasure_room()
        if command in directions[3]:
            goblin_temple3()

def treasure_room():
    global room_items
    global room_monsters
    room_items = None
    room_monsters = [dragon]
    print("This room has piles and piles of gold.")
    print("However, it is guarded by a ", room_monsters[0].name)
    while True:
        command = travel()
        if command in directions[3]:
            goblin_temple_bridge3()

def forest():
    global room_items
    global room_monsters
    room_monsters = None
    room_items = None
    descriptions = ["After a short while you find a clearing, with a stream of muddy water in it.", "The trees get denser here, and you look at the sunlight speckled on the ground amidst pine needles.", "The forest is vibrant and alive here, and you see a bird eating berries.", "You come to a clearing with a solitary stump in the middle."]
    print(random.choice(descriptions))
    while True:
        command = travel()
        if command in directions[0] or command in directions[1] or command in directions[2] or command in directions[3] :
            forest()

def choice(option1, option2, option3):
    print("(1) ", option1)
    print("(2) ", option2)
    print("(3) ", option3)
    ask = int(input("> "))
    return ask
def start():
    print("Welcome to a world of Swords, Sorcery, and Adventure...")
    time.sleep(1)
    print("Welcome to the world of...")
    time.sleep(1)
    print()
    print("================================")
    print("          DRAGON BORNE")
    print("================================")
    print("Licensed under CC BY-NC.")
    start_input = choice("Play Dragon Borne game", "Backstory of Dragon Borne", "How to play Dragon Borne.")

    if start_input == 1:
        outside_dungeon()
    elif start_input == 2:
        print("Tales spread far and wide about the existence of the last dragon.")
        print("Most dismissed the tales as mere rumours, or were too afraid to confront their fears.")
        print("But you didn't dismiss them or fear them. ")
        print("You knew that slaying the dragon would bring peace and prosperity throughout the land.")
        print("And so you resolved to slay the dragon.")
        print("So you packed your sword and shield and embarked on a mission of epic proportions.")
        print("But you knew that a dragon wouldn't be all you'd face.")
        print("For where dragons be, gold be. And where gold be, goblins be...")
        x = input(">")
        start()
    elif start_input == 3:
        print("Play the game by entering 1 or 2 word commands like:")
        print(" To move a direction: Direction or initial letter of Direction")
        print(" To fight a monster: Fight (Monsters name)")
        print(" To take something from a room: Take (Item)")
        x = input(">")
        start()
    else:
        print("Improper statement.")
        x = input(">")
        start()

start()