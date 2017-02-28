from classes.game import Person, bcolors
from classes.magic import Spell

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 12, 130, "black")

# Create White Magic

cure = Spell("Cure", 12, 120,"white")
cura = Spell("Cura",18, 200, "white")



#Instantiate People
player = Person(450, 80, 60, 34, [fire,thunder,blizzard,meteor, cure, cura])
enemy = Person(1220, 65, 45, 25, [])

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!"+ bcolors.ENDC)

while running:
        print("=====================================")
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1
        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("\nYou attacked for", dmg, "points of damage." )
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Chose magic:")) - 1
            if magic_choice > len(player.magic):
                print(bcolors.FAIL + "\nChoose a valid action" + bcolors.ENDC)
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n"+ bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE+ "\n" + spell.name + " heals for " + str(magic_dmg), "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index > 2:
            print( bcolors.FAIL + "\nChoose a valid action" + bcolors.ENDC)
            continue

        enemy_choice = 1
        enemy_dmg = enemy.generate_damage()
        player.take_damage(enemy_dmg)
        print(bcolors.FAIL + "Enemy attacks for", enemy_dmg,"points of damage." + bcolors.ENDC)

        print("=====================================")
        print("Enemy HP:", bcolors.FAIL+ str(enemy.get_hp())+ "/"+ str(enemy.maxhp) + bcolors.ENDC, "\n")

        print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.maxhp)+ bcolors.ENDC)
        print("Your MP:", bcolors.OKBLUE + str(player.get_mp())+ "/"+ str(player.get_maxmp()) + bcolors.ENDC)
        if enemy.get_hp() == 0:
            print(bcolors.OKGREEN + "\nYou Win!" + bcolors.ENDC)
            running = False
        elif player.get_hp() == 0:
            print(bcolors.FAIL + "\nYour enemy has defeated you!" + bcolors.ENDC)
            running = False







