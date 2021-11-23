#!/bin/python3
# Game characters
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game design by Rudy Ashford

#todo
#TODO create character class - and amend PC and NPC to inherit
#TODO add fight method to character class
#TODO update fight method to include specific moves form PC and NPC
#TODO research new AI chat thats less random
#TODO create friend NPC
#TODO create character with money and puzzles

import sys
import os
import random
import time
from termcolor import colored, cprint
import pyfiglet
from game.utils import spinning_cursor
from config import commands, pack_max
from game.universe import Item, WinningItem

class Character:
    #Game characters
    def __init__(self, name, species, appearance, weakness, strength, speed, health, zone):
        self.name = name
        self.species = species
        self.appearance = appearance
        self.weakness = weakness
        self.strength = strength
        self.speed = speed
        self.health = health
        self.zone = zone

    def show_health(self):
        health = self.health
        h = 1
        health_hearts = ""

        while h <= health:
            health_hearts += " \u2764 "
            h += 1
        return health_hearts

    def show_info(self, game):
        #NPC name
        game.msg.append("Name : " + self.name)
        #NPC species
        cprint("Species : " + self.species, 'green')
        #NPC strength
        cprint("Strength : " + str(self.strength), 'green')
        #NPC speed
        cprint("Speed : " + str(self.speed), 'green')
        #NPC health
        cprint("Health :" + str(self.show_health()), 'white', 'on_red')


class Hero(Character):
    #Create the hero players

    def __init__(self, name, power, weapon, strength, speed, health, full_health, destination, zone, inventory, transport, credits, winning_items=None, moves=None):
        self.name = name
        self.power = power
        self.weapon = weapon
        self.strength = strength
        self.speed = speed
        self.health = health
        self.full_health = full_health
        self.destination = destination
        self.zone = zone
        self.inventory = inventory
        self.transport = transport
        self.credits = credits
        if winning_items is None:
            self.winning_items = []
        else:
            self.winning_items = winning_items
        if moves is None:
            self.moves = []
        else:
            self.moves = moves

    def show_navigator(self, game):
        if self.transport == "":
            category = ""
            fuel_tank = ""
        else:
            category = self.transport.category
            fuel_tank = self.transport.fuel_tank

        game.msg.append(str("Vehicle category: {category}").format(category=category.upper()))
        game.msg.append(str("Fuel: {fuel}").format(fuel=fuel_tank))
        game.msg.append(str("Current location: {location}").format(location=self.destination.name.upper()))
        game.msg.append(str("Zone: {zone}").format(zone=self.zone.name.upper()))
        game.player.destination.voyage_list(game, "list")

    def go(self, game, command):
        go_directions = {"north": 2, "south": 0, "west": 1, "east": 3}
        go_styles = ["swagger over to the", "jog over to the", "walk cautiously in the direction of the", "sprint towards the ", "do a ninja roll to get to the"]

        if command in go_directions:
            game.player.zone = game.player.destination.zones[go_directions[command]]
            game.msg.append(str("Travelling {direction} you reach the {zone}").format(direction=command.title(), zone=game.player.zone.name))
            game.msg.append(game.player.zone.scenario)
            if game.destinations[-1].zones[-1] == self.zone:
                self.zone.non_player_characters.encounter(game)

        elif command == game.player.zone.objects.name.lower():
            go_style = random.choice(go_styles)
            game.msg.append(str("You {go} {object}").format(go = go_style, object = game.player.zone.objects.name))
            game.msg.append(game.player.zone.objects.msg['go'])

        elif command == game.transport.name:
            if self.list_inventory(game, "fuel tank", "check") == True:
                    for itm in self.inventory:
                        if itm.name == "fuel tank":
                            game.player.transport.fuel_tank += 15
                            game.player.inventory.remove(itm)
            game.msg.append(game.player.transport.msg.get('go'))
        else:
            game.msg.append(commands['go']['error'])

    def look(self, game, command):
        if command == "closer" and "look" in game.player.moves:
            game.msg.append("You shuffle a little closer and...")
            if game.player.zone.items.collected == False:
                if game.player.zone.items.collected == False:
                    game.msg.append("see that the item in front of you looks a lot like a " + game.player.zone.items.name)
                    if hasattr(game.player.zone.items, 'description'):
                        game.msg.append(game.player.zone.items.description)
            if game.player.zone.winning_items != "":
                if game.player.zone.winning_items.collected == False:
                    game.msg.append("Wow!! You see what appears to be a " + game.player.zone.winning_items.name)
                    game.msg.append(game.player.zone.winning_items.description)
            else:
                game.msg.append("...but there doesn't appear to be anything here to see...")
        elif command == "around":
            if game.player.zone == game.destinations[0].zones[0] and game.player.weapon == "":
                game.select_weapon()
            else:
                game.msg.append("You have a good look around...")
                tip = ""
                tip = '''\n(tip: go ''' + game.player.zone.objects.name + ''')'''

                if game.player.zone.items.collected == False:
                    game.msg.append(game.player.zone.items.msg['look'])

                if isinstance(game.player.zone.winning_items, WinningItem):
                    if game.player.zone.winning_items.collected == False:
                        game.msg.append(game.player.zone.winning_items.msg['look'])

                game.msg.append(game.player.zone.objects.msg['look'] + tip)

        else:
            game.msg.append(commands['look']['error'])

    def dance(self, game, command):
        pass

    def fart(self, game):
        fart = {
            1: '''
You ease and squeeze - a dense dark smell
oouzes from your buttocks. A nearby bird falls from her perch,
I think the smell has killed her!**!!
''',
            2: '''
PARP PARP PARP - your but cheeks sing and
then there's the smell - wow it's a tuneful killa. You chuckle
loudly - thoroughly impressed with your bottom skills''',
            3: '''
A high pitch SCREEEECH is coming from somewhere
nearby, then you realise its your bum, seconds later the smell
confirms it. ***Deadly***'''
        }
        fart_choice = random.randint(1,3)
        game.msg.clear()
        game.msg.append(fart[fart_choice])

    def list_inventory(self, game, command, task):
        if task == "list":
            game.msg.append("Your pack items:")
            if self.inventory:
                for item in self.inventory:
                    game.msg.append(str(item.name.title()) + " (" + str(item.category) + ")",)
                game.msg.append(str("Remember you can only hold {capacity} items in your pack").format(capacity=pack_max))
            else:
                game.msg.append("[ No items in your inventory. ]")
        elif task == "check":
            if self.inventory:
                for item in self.inventory:
                    if item.name.lower() == command:
                        return True


class NonPlayerCharacter(Character):
    #Create NPC, friends and foe to populate the game and spice it up!

    def __init__(self, name, species, appearance, weakness, status, strength, speed, health, msg):
        self.name = name
        self.species = species
        self.appearance = appearance
        self.weakness = weakness
        self.status = status
        self.strength = strength
        self.speed = speed
        self.health = health
        self.msg = msg

    def encounter(self, game):
    #encounter a npc
        game.msg.append('''Before you can get it...''')
        game.msg.append(self.msg['encounter'])
        game.msg.append(str('''
It's {name} from the species {species}''').format(name=self.name, species=self.species))
        game.msg.append(self.appearance.title())
        game.msg.append(str('''You know of these guys and you know them to be {status}''').format(status=self.status))

    def attack(self, game):
    #dice based fighting engine

        attack = 'n'

        #intro to fight
        print(self.msg['fight'])
        print(str('''{name} are you ready to commence battle with {npc}?''').format(name=game.player.name, npc=self.name))

        attack = input("Start fight (y/n) > ")

        if attack == 'y':

            if game.player.weapon:
                print(str('''You have your trusty {weapon} - this will add strength to your attack''').format(weapon=game.player.weapon.name))
                player_strength = game.player.strength + 1
            else:
                player_strength = game.player.strength
            if game.player.health >= game.player.full_health:
                powers = input(str("You have full health - do you want to use {power} to fight {npc}? (y/n) >").format(power=game.player.power, npc=self.name))
                #player strength
                if powers == 'y':
                    player_strength + 2

        #thing strength
        npc_strength = self.strength

        #attacks
        attacks = {
                1 : {
                        'name': 'bone crusher',
                        'moves': 'jump and land on their back and crush their bones!!'
                    },
                2 : {
                        'name': 'power punch',
                        'moves': 'deliver a big punch to the gut and knock them flying!'
                    },
                3 : {
                        'name': 'big bang',
                        'moves': 'bash them to the ground with earth shattering effect to making them fall unconcious!!!'
                    }
                }

        #defence
        defence = {
                1 : {
                        'name': 'block',
                        'moves': 'well timed full body block preventing any damage'
                    },
                2 : {
                        'name': 'dodge',
                        'moves': 'dogdes the attack narowly avoiding an injury...for the time being'
                    },
                3 : {
                        'name': 'counter strike',
                        'moves': 'quicker - faster - harder counter strike deflects the attack'
                    }
                }

        while attack == 'y' and game.player.health > 0:

            min = 1

            npc_attack_pts = random.randint(min,npc_strength)
            player_attack_pts = random.randint(min,player_strength)

            attack_choice = random.choice(list(attacks))
            defence_choice = random.choice(list(defence))

            if npc_attack_pts > player_attack_pts:
                spinning_cursor(3)
                print("You launch an attack but " + self.name)
                print (defence[defence_choice]['moves'])
                spinning_cursor(1)
                print ("Your health has been damaged")
                game.player.health = game.player.health - 1
                h = 1
                health_hearts = ""

                while h <= game.player.health:
                    health_hearts += " \u2764 "
                    h += 1

                # print health
                cprint("Health :" + str(health_hearts), 'white', 'on_red')

                if game.player.health == 1:
                    game.msg.append("Your health is on it's last legs - lose one more and you are dead...just saying!")

                attack = 'n'

                if game.player.health == 0:
                    game.msg.append("Oh no you have just died at the hands of " + self.name)
                    game.msg.append(self.msg['win'])
                    game.over()
                    attack = 'n'
                elif game.player.health > 0:
                    attack = input("Attack again? y/n > ")
            else:
                spinning_cursor(2)
                print ("You " + attacks[attack_choice]['moves'])
                spinning_cursor(1)
                print ("Their health has been damaged")
                self.health = self.health - 1
                if self.health == 0:
                    game.msg.append("You have just killed " + self.name)
                    game.msg.append(self.msg['lose'])
                    # set attack to no
                    attack = 'n'

        else:
            if self.health > 0:
                print("No worries - there is indeed great strength in not fighting.")
                time.sleep(1)


    def talk(self, chatbot):

        print("Say something then...")
        while True:
            try:
                bot_input = chatbot.get_response(input())
                print(bot_input)

            except(KeyboardInterrupt, EOFError, SystemExit):
                break

class Boss(NonPlayerCharacter):
    #create the boss - this character will guard the final object - they must be defeated to win the game!
    pass




