#!/bin/python3
# Game characters
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game design by Rudy Ashford

import sys
import os
import random
import time
import colored
from colored import stylize
import pyfiglet
from game.utils import spinning_cursor
from config import commands
from game.universe import Item, WinningItem

# pip install chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new trainer for the chatbot
from chatterbot.trainers import ListTrainer


class PlayerCharacter:
#create a choice of hero players to play the game
    def __init__(self, name, power, weapon, strength, health, destination, zone, inventory, transport, winning_items=None, moves=None):
        self.name = name
        self.power = power
        self.weapon = weapon
        self.strength = strength
        self.health = health   
        self.destination = destination
        self.zone = zone
        self.inventory = inventory
        self.transport = transport
        if winning_items is None:
            self.winning_items = []
        else: 
            self.winning_items = winning_items
        if moves is None:
            self.moves = []
        else: 
            self.moves = moves

    def show_health(self):
        health = self.health
        h = 1
        health_hearts = ""

        while h <= health:
            health_hearts += " \u2764 "
            h += 1   
        return health_hearts
        
    def go(self, game, command):
        go_directions = {"north": 2, "south": 0, "west": 1, "east": 3}
        go_styles = ["swagger over to the", "jog over to the", "walk cautiously in the direction of the", "sprint towards the ", "do a ninja roll to get to the"]
        obj_name = ""
        
        obj_name = game.player.zone.objects.name  
        go_msg = game.player.zone.objects.msg['go']

        if command in go_directions:
            game.player.zone = game.player.destination.zones[go_directions[command]]
            game.msg.append(str("Travelling {direction} you reach the {zone}").format(direction=command.title(), zone=game.player.zone.name))
            game.msg.append(game.player.zone.scenario)

        elif command == obj_name:
            go_style = random.choice(go_styles)
            game.msg.append(str("You {go} {object}").format(go = go_style, object = obj_name))
            game.msg.append(go_msg)         

        elif command == game.transport.name:
            if game.player.transport == "":
                game.player.transport = game.transport    
            game.msg.append(game.player.transport.msg['go'])

        else:
            game.msg.append(stylize(commands['go']['error'], colored.fg(1)))


    def look(self, game, command):
        if command == "closer" and "look" in game.player.moves:
            if game.player.zone.items.collected == False or game.player.zone.winning_items.collected == False:
                game.msg.append("You get closer and see that...")
                if game.player.zone.items.collected == False:
                    game.msg.append("the item you could see looks a lot like a " + game.player.zone.items.name)
                    game.msg.append(game.player.zone.items.description)
                if isinstance(game.player.zone.winning_items, WinningItem):
                    if game.player.zone.winning_items.collected == False:
                        game.msg.append("Wow!! You see what appears to be a " + game.player.zone.winning_items.name)
                        game.msg.append(game.player.zone.winning_items.description)
            else:
                game.msg.append("You look closer but there doesn't appear to be anything here to see...")  
        elif command == "around":
            if game.player.zone == game.destinations[0].zones[0] and game.player.weapon == "":
                game.select_weapon()
            else:
                game.msg.append("You have a good look around...")
            tip = ""
            tip = stylize(" (tip: go " + game.player.zone.objects.name + ")", colored.fg(1))
            game.msg.append(game.player.zone.objects.msg['look'] + tip)
            if game.player.zone.items.collected == False:
                game.msg.append(game.player.zone.items.msg['look'])
            
            if isinstance(game.player.zone.winning_items, WinningItem):
                if game.player.zone.winning_items.collected == False:
                    game.msg.append(game.player.zone.winning_items.msg['look'])    
        else:
            game.msg.append(stylize(commands['look']['error'], colored.fg(1)))
    
    def dance(self, game, command):
        pass

    def fart(self, game):
        fart = {
            1: '''
You ease and squeeze - a dense dark smell
oouzes from your buttocks. A nearby bird falls from her perch,
has the smell killed her!?!
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
            game.msg.append("Your back pack items:")
            if self.inventory:
                for item in self.inventory:
                    game.msg.append(str(item.name.title()) + " (" + str(item.category) + ")",)       
                game.msg.append(stylize(str("Remember you can only hold {capacity} items in your pack").format(capacity=8), colored.fg(1)))
            else:
                game.msg.append(stylize("[ No items in your inventory. ]", colored.fg(1)))
        elif task == "check":
            if self.inventory:
                for item in self.inventory:
                    if item.name.lower() == command:
                        return True


class NonPlayerCharacter:
#create npc, friends and foe to populate the game and spice it up!
    def __init__(self, name, species, appearance, weakness, status, strength, health, msg):
        self.name = name
        self.species = species
        self.appearance = appearance
        self.weakness = weakness
        self.status = status
        self.strength = strength
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

    def fight(self, game):
    #dice based fighting engine

        attack = 'n'

        #intro to fight
        print(self.msg['fight'])   
        print(stylize(str('''{name} are you ready to commence battle with {npc}?''').format(name=game.player.name, npc=self.name), colored.fg(1)))   

        attack = input("Start fight (y/n) > ")

        if attack == 'y':
            if game.player.weapon:
                print(str('''You have your trusty {weapon} - this will add strength to your attack''').format(weapon=game.player.weapon.name))
                player_strength = game.player.strength + 1
            else:
                player_strength = game.player.strength
            powers = input(str("Do you want to use {power} to fight {npc}? (y/n)").format(power=game.player.power, npc=self.name))
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
                print(stylize("Health :" + str(health_hearts), colored.fg(15) + colored.bg(1)))

                attack = 'n'    

                if game.player.health == 0:
                    game.msg.append("Oh no you have just died at the hands of " + self.name)
                    game.msg.append(self.msg['win'])
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
                print("There is strength in not fighting.")
                time.sleep(1)
                print(self.name + " from the " + self.species + " species...")
                time.sleep(1)
                print("Do you have a mobile? If so why not google it?")
                time.sleep(2)

        return


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
    def __init__(self, name, species, appearance, weakness, status, strength, health, encounter):
        super().__init__(name, species, appearance, weakness, status, strength, health, encounter)

    
   

