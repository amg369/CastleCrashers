from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random
import re

# Create Element Magic
fire = Spell("Fireball", 50, 670, "Elemental")
water = Spell("Tsunami", 70, 750, "Elemental")
ice = Spell("Ice Spear", 30, 895, "Elemental")
shadow = Spell("Shadow Strike", 115, 910, "Elemental")

# Enemy's Element Magic
darkness = Spell("Darkness", 50, 800, "Elemental")
acid = Spell("Acid Breath", 70, 900, "Elemental")
sand = Spell("Sand Attack", 30, 400, "Elemental")
scorch = Spell("Scorched Earth", 100, 1000, "Elemental")

# Healing Magic
cure = Spell("Cure", 22, 320, "Healing")
cura = Spell("Strong Cure", 40, 200, "Healing")
bigcure = Spell("Power Cure", 40, 2000, "Healing")

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
player1 = Person("Knight: ", 4500, 100, 360, 340, player_spells, player_items)
player2 = Person("Mage:   ", 3000, 200, 260, 340, player_spells, player_items)
player3 = Person("Rogue:  ", 3500, 140, 160, 340, player_spells, player_items)
enemy1 = Person("Tiny    ", 1000, 90, 745, 250, [darkness, shadow, cura], [])
enemy2 = Person("DRAGON  ", 7000, 550, 745, 250, [sand, scorch, darkness, shadow, bigcure], [])
enemy3 = Person("Mini    ", 1000, 90, 745, 250, [acid, darkness, cura], [])
players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
run = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "A DRAGON ATTACKS!!!" + bcolors.ENDC)

while run:
    print("=============================")
    print("NAME                      HP                                      MP")
    for enemy in enemies:
        enemy.get_enemy_stats()
    for player in players:
        player.get_stats()
    for player in players:
        player.choose_action()
        choice = input("Choose an action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_dmg()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)
            print("You attacked", re.sub('[" "]', "", str(enemies[enemy].name)), "for ", dmg, "damage points.")
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ","") + "has died")
                del enemies[enemy]
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
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolors.BLUE + spell.name + " deals",
                      str(magic_dmg), " damage points to " + bcolors.ENDC + bcolors.FAIL + re.sub('[" "]', "", str(
                        enemies[enemy].name)))
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + "has died")
                    del enemies[enemy]
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

                if item.name == "MegaSandwich":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.GREEN + item.name +
                          " fully restores the party's HP/MP" + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.GREEN + item.name +
                          " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item.prop)
                print(bcolors.FAIL + str(item.name) + " dealt " + re.sub('[" "]', "", str(enemies[enemy].name)) +
                      str(item.prop) + " damage points" + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + "has died")
                    del enemies[enemy]
    # Ending the game
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 3:
        print(bcolors.GREEN + "You defeated the enemy!!" + bcolors.ENDC)
        run = False
    elif defeated_players == 3:
        print(bcolors.FAIL + "Your party died. Sorry." + bcolors.ENDC)
        run = False

    # An Enemy Attacks
    for enemy in enemies:
        enemy_choice = random.randrange(0, 3)

        if enemy_choice == 0:
            # Enemy chooses Attack
            target = random.randrange(0, 2)
            enemy_dmg = enemies[0].generate_dmg()
            print(bcolors.FAIL + enemies[0].name.replace(" ", "") + bcolors.ENDC + " attacked " +
                  players[target].name.replace(": ", "") + " for " + str(enemy_dmg))
            players[target].take_dmg(enemy_dmg)


        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == "Healing":
                enemy.heal(magic_dmg)
                print(bcolors.BLUE + spell.name +
                      " heals " + enemy.name + " for " + str(magic_dmg) + " HP" +
                      bcolors.ENDC)
            elif spell.type == "Elemental":
                target = random.randrange(0, 3)
                players[target].take_dmg(magic_dmg)
                print(bcolors.FAIL + enemy.name.replace(" ",
                                                        "") + "'s " + bcolors.BLUE + spell.name + bcolors.ENDC + " deals",
                      str(magic_dmg), " damage points to " + bcolors.ENDC + bcolors.FAIL + re.sub('[" ":]', "", str(
                        players[target].name)))

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + "has died")
                    del players[target]
