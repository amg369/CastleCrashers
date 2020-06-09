from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create Element Magic
fire = Spell("Fireball", 20, 100, "Elemental")
water = Spell("Tsunami", 30, 250, "Elemental")
ice = Spell("Ice Spear", 10, 95, "Elemental")
shadow = Spell("Shadow Strike", 15, 110, "Elemental")

cure = Spell("Cure", 12, 120, "Healing")
cura = Spell("Strong Cure", 20, 200, "Healing")

# Create Items
potion1 = Item("Healing Potion", "potion", "Heals 50 HP", 50)
potion2 = Item("Strong Potion", "potion", "Heals 100 HP", 100)
potion3 = Item("Cure All Potion", "potion", "Heals 500 HP", 500)
lemonade = Item("Sandwich", "elixir", "Fully restores HP or MP", 10000)
limeade = Item("MegaSandwich", "elixir", "Fully restores party member's HP or MP", 10000)
star = Item("Throwing Stars", "attack", "Deals 150 damage", 150)

# Instantiate Characters
player_spells = [fire, water, ice, shadow, cure, cura]
player_items = [{"item": potion1, "quantity": 15}, {"item": potion2, "quantity": 5},
                {"item": potion3, "quantity": 2}, {"item": lemonade, "quantity": 5},
                {"item": limeade, "quantity": 1}, {"item": star, "quantity": 5}]
player1 = Person("Aliyah: ", 4000, 165, 360, 340, player_spells, player_items)
player2 = Person("Allison:", 3460, 455, 260, 340, player_spells, player_items)
player3 = Person("Clara:  ", 2560, 185, 160, 340, player_spells, player_items)
enemy = Person("BIG BOI", 7000, 750, 745, 250, [], [])

players = [player1, player2, player3]

run = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "A DRAGON ATTACKS!!!" + bcolors.ENDC)

while run:
    print("=============================")
    print("NAME               HP                                      MP")
    for player in players:
        player.get_stats()
    for player in players:
        player.choose_action()
        choice = input("Choose an action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_dmg()
            enemy.take_dmg(dmg)
            print("You attacked for ", dmg, "damage points.")
        elif index == 1:
            player.choose_spell()
            magic_choice = int(input("Choose magic: ")) - 1
            magic_dmg = player.magic[magic_choice].generate_dmg()
            spell = player.magic[magic_choice]
            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou don't have enough MP!" + bcolors.ENDC)
                continue

            if magic_choice == -1:
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "Healing":
                player.heal(magic_dmg)
                print(bcolors.BLUE + spell.name +
                      " heals for " + str(magic_dmg) + " HP" +
                      bcolors.ENDC)
            elif spell.type == "Elemental":
                enemy.take_dmg(magic_dmg)
                print(bcolors.BLUE + spell.name + " deals",
                      str(magic_dmg), " damage points" + bcolors.ENDC)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "There are none left." + bcolors.ENDC)
                continue

            if item_choice == -1:
                continue
            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.GREEN + item.name + " heals for", str(item.prop),
                      " HP" + bcolors.ENDC)
            elif item.type == "elixir":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.GREEN + item.name +
                      " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_dmg(item.prop)
                print(bcolors.FAIL + str(item.name) + " gave " + str(item.prop) + " damage points" + bcolors.ENDC)
        enemy_dmg = enemy.generate_dmg()
        player.take_dmg(enemy_dmg)
        print("Enemy attacks for ", enemy_dmg,
              "points of damage.")

    print("------------------------------------")
    print("Enemy HP: ", bcolors.FAIL + str(enemy.get_hp())
          + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)

    #  print("Your HP: ", bcolors.GREEN + str(player.get_hp()) + "/" +
    #        str(player.get_max_hp()) + bcolors.ENDC)
    #  print("Your MP: ", bcolors.BLUE + str(player.get_mp()) +
    #        "/" + str(player.get_max_mp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.GREEN + "You defeated the enemy!!" + bcolors.ENDC)
        run = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You died. Sorry." + bcolors.ENDC)
        run = False
