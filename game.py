import random
from .magic import Spell


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[95m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkh = atk + 10
        self.atkl = atk - 10
        self.df = df
        self.magic = magic
        self.items = items
        self.action = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_dmg(self):
        return random.randrange(self.atkl, self.atkh)

    # def generate_spelldmg(self, i):
    #    mgl = self.magic[i]["dmg"] - 5
    #    mgh = self.magic[i]["dmg"] + 5
    #    return random.randrange(mgl, mgh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
            return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    #  def get_spell_name(self, i):
    #       return self.magic[i]["name"]

    #  def get_spell_mp_cost(self, i):
    #      return self.magic[i]["cost"]

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def choose_action(self):
        i = 1
        print("\n" + bcolors.BOLD + bcolors.WARNING + str(self.name) + bcolors.ENDC)
        for item in self.action:
            print("    " + str(i) + ":", item)
            i += 1

    def choose_spell(self):
        i = 1
        print("Magic")
        for spell in self.magic:
            print("    " + str(i) + ":",
                  spell.name,
                  "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("Items")
        "\n"
        for item in self.items:
            print("    " + str(i) + ".",
                  item["item"].name, ":",
                  str(item["item"].description) + "(x" + str(item["quantity"]) + ")")
            i += 1

    def get_stats(self):
        hp_bar = ""
        bar_num = (self.hp / self.maxhp) * (100 / 4)

        mp_bar = ""
        bar_num_mp = (self.mp / self.maxmp) * (100 / 4)
        while bar_num > 0:
            hp_bar += "█"
            bar_num -= 1
            mp_bar += "█"
            bar_num_mp -= 1

        while len(hp_bar) < 25:
            hp_bar += " "
            mp_bar += " "

        print(
            bcolors.BOLD + self.name + "   " +
            str(self.hp) + "/" + str(self.maxhp) + "   |" + bcolors.GREEN +
            hp_bar + bcolors.ENDC +
            "|   " + str(self.mp) + "/" + str(self.maxmp) +
            "  |" + bcolors.BLUE + mp_bar + bcolors.ENDC + "|")