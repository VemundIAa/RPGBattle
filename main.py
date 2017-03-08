from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 30, 730, "black")


# Create White Magic
cure = Spell("Cure", 15, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")


# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, curaga]

player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item":  hielixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Valos", 3250, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick ", 4150, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Magus", 18220, 721, 525, 25, enemy_spells, [])
enemy2 = Person("Imp  ", 1250, 130, 560, 350, enemy_spells, [])
enemy3 = Person("Imp  ", 1250, 130, 560, 350, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
        print("===========================")
        print("\n\n")
        print(bcolors.BOLD + "NAME               HP                                    MP"+bcolors.ENDC)
        for player in players:
            player.get_stats()

        print("\n")
        print(bcolors.BOLD + "NAME               HP" + bcolors.ENDC)
        for enemy in enemies:
            enemy.get_enemy_stats()

        for player in players:

            player.choose_action()
            choice = input("    Choose action:")
            if choice == "":
                print(bcolors.FAIL + "\n" + player.name.replace(" ","") , "skips the round.\n" + bcolors.ENDC)
                continue
            index = int(choice) - 1
            if index == 0:
                dmg = player.generate_damage()
                enemy = player.choose_target(enemies)
                if enemy > len(enemies):
                    print(bcolors.FAIL + "\n"+ player.name.replace(" ","") +  " Strikes at the air, and misses.\n" + bcolors.ENDC)
                    continue
                enemies[enemy].take_damage(dmg)
                print("\n"+player.name.replace(" ","") +" attacked",enemies[enemy].name.replace("  ",""),"for", dmg, "points of damage.\n")
            elif index == 1:
                player.choose_magic()
                magic_choice = int(input("    Chose magic:")) - 1
                if magic_choice > len(player.magic):
                    print(bcolors.FAIL + "\nChoose a valid action.\n" + bcolors.ENDC)
                    continue
                if magic_choice == -1:
                    continue

                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()
                current_mp = player.get_mp()

                if spell.cost > current_mp:
                    print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                    continue

                player.reduce_mp(spell.cost)

                if spell.type == "white":
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg), "HP\n" + bcolors.ENDC)
                elif spell.type == "black":
                    enemy = player.choose_target(enemies)

                    enemies[enemy].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to "+ enemies[enemy].name.replace("  ","") + "\n"+ bcolors.ENDC)

            elif index == 2:
                player.choose_item()
                item_choice = int(input("    Choose Item: ")) - 1

                if item_choice > len(player.items):
                    print(bcolors.FAIL + "\nChoose a valid action" + bcolors.ENDC)
                    continue

                if item_choice == -1:
                    continue

                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\n" + "None left.." + bcolors.ENDC)
                    continue

                item = player.items[item_choice]["item"]
                player.items[item_choice]["quantity"] -= 1

                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
                elif item.type == "elixir":

                    if item.name == "MegaElixir":
                        for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
                elif item.type == "attack":
                    enemy = player.choose_target(enemies)

                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name.replace("  ","") + bcolors.ENDC)

            elif index > 3:
                print(bcolors.FAIL + "\nChoose a valid action" + bcolors.ENDC)
                continue

        # Enemy attack phase
        for enemy in enemies:
            enemy_choice = random.randrange(0, 2)
            range = len(players)
            target = random.randrange(0, range)

            if enemy_choice == 0:
                enemy_dmg = enemy.generate_damage()
                players[target].take_damage(enemy_dmg)
                print(bcolors.FAIL + enemy.name.replace("  ","") + " attacks", players[target].name.replace(" ","") + " for", enemy_dmg, "points of damage." + bcolors.ENDC)

            elif enemy_choice == 1:
                spell, magic_dmg = enemy.choose_enemy_spell()
                if spell == None:
                    print("FAAAAAAAIIIIL")
                    continue
                enemy.reduce_mp(spell.cost)
                if spell.type == "black":
                    players[target].take_damage(magic_dmg)
                    print (bcolors.OKBLUE + enemy.name.replace("  ",""), "casts", spell.name+ ",", players[target].name.replace(" ","") + " takes " + str(magic_dmg), "points of damage." + bcolors.ENDC)
                elif spell.type == "white":
                    enemy.heal(magic_dmg)
                    print(bcolors.OKBLUE + enemy.name.replace("  ",""), "casts", spell.name + ", heals for " + str(magic_dmg) + bcolors.ENDC)



 # check if people are defeated
        i = 0
        for enemy in enemies:
            if enemy.get_hp() == 0:
                print(bcolors.FAIL + "\n" + enemy.name.replace("  ", "") + " has been defeated" + bcolors.ENDC)
                del enemies[i]
            i += 1

        i = 0
        for player in players:
            if player.get_hp() == 0:
                print(bcolors.FAIL + "\n" + player.name.replace(" ", "") + " has been defeated" + bcolors.ENDC)
                del players[i]
            i += 1
        # check if battle is over
        if players == []:
            print(bcolors.FAIL + bcolors.BOLD + "\nYou have been defeated!" + bcolors.ENDC)
            running = False
        if enemies == []:
            print(bcolors.OKGREEN + "\nYou Win!" + bcolors.ENDC)
            running = False









