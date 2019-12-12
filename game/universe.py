#!/bin/python3
# Game planets
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game designed by Rudy Ashford

import sys
import os
import random
import time
import colored
from colored import stylize
import pyfiglet
from config import win, commands, destinations, items
from game.utils import clear

class Destination:
#destination class - used in conjunction with Hero to create the players destination

    def __init__(self, name, voyages, scenario, colour, zones):
        self.name = name
        self.voyages = voyages
        self.scenario = scenario
        self.colour = colour
        self.zones = zones

    def title(self):
        print('{0}'.format('-'*65))
        ascii_banner = pyfiglet.figlet_format(self.name)
        print(stylize(ascii_banner, colored.fg(self.colour)))
        print('{0}'.format('-'*65))

    def voyage_list(self, game, task):
        if task == "list":
            game.msg.append(str("Suggested destinations:"))
            for direction, value in self.voyages.items():
                game.msg.append(str(destinations[value]['name']) + str(" ( direction: " + direction + " )"))   
        game.msg.append(stylize(str("Remember you'll need enough fuel to reach your destination!").format(capacity=10), colored.fg(1)))

    def fly(self, game, command):
        if "spaceship" in game.player.moves:
            game.player.moves.append(command)
            # check that can go to their desired destination

            if command in game.player.destination.voyages:
                voyages = game.player.destination.voyages
                new_destination = voyages[command] - 1
                game.player.destination = game.destinations[new_destination]
                game.player.zone = game.destinations[new_destination].zones[0]
                game.msg.append(str('''After a quick interstellar hop through the universe 
you've arrived on {destination}
''').format(destination = game.player.destination.name))            
                game.player.moves.clear()
            else:
                game.msg.append(stylize("You can't go in that direction - you'll get lost!", colored.fg(1)))
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['fly']['error'], colored.fg(1)))
            if not game.player.transport:
                game.msg.append("But it must be your lucky day as you happen to have a ")
                game.show_vehicle()

class Zone():
#create a game zone to find items and fight enemies
    def __init__(self, name, objects, items, winning_items, scenario, weapons=None, non_player_characters=None):
        self.name = name 
        self.objects = objects 
        self.items = items
        self.winning_items = winning_items
        self.scenario = scenario
        if weapons is None:
            self.weapons = []
        else: 
            self.weapons = weapons
        if non_player_characters is None:
            self.non_player_characters = []
        else: 
            self.non_player_characters = non_player_characters    
        
class Transport:
#create a vehicle to carry the player  + non player characters around the game

    def __init__(self, name, description, category, capacity, fuel, weapon, msg):
        self.name = name
        self.description = description
        self.category = category
        self.capacity = capacity
        self.fuel = fuel
        self.weapon = weapon
        self.msg = msg   

    def voyage(self):
        pass

class Object:  
#create physical objects in the game

    def __init__(self, name, description, move, clue, msg):
        self.name = name
        self.description = description
        self.move = move
        self.clue = clue
        self.msg = msg

    def open(self, game):
        if game.player.list_inventory(self, "key", "check") == True:
            if self.clue:
                game.msg.clear()
                game.msg.append('''The key fits, you turn it anti-clockwise...
bingo, it opens without so much as a creeeeek...
''')
                self.clue.read(game)
            else:
                game.msg.clear()
                game.msg.append(str('''Alas the {item} is empty''').format(item=self.name))    
        else:
            self.msg.append(stylize(str('''You don't have anything to open {item} with...perhaps you need to find a key''').format(item=self.name), colored.fg(1)))

    def climb(self, game):
        if self.clue:
                game.msg.clear()
                game.msg.append('''You scramble up and up and up
''')
                self.clue.read(game)
        else:
            game.msg.clear()
            game.msg.append(str('''Alas there's nothing to see up there...''').format(item=self.name))

    def read(self, game):
        if self.clue:
                game.msg.clear()
                game.msg.append('''Taking a step back you start to read the words one by one...
''')
                self.clue.read(game)
        else:
            game.msg.clear()
            game.msg.append(str('''Alas not a language you understand...''').format(item=self.name))        

    def smash(self):
        pass

class Item:
#create items (pick-ups) in the game

    def __init__(self, name, description, msg, category, collected):
        self.name = name
        self.description = description
        self.msg = msg
        self.category = category
        self.collected = collected
    
    def get(self, game, command):
        if command.lower() == self.name.lower():
            # display a helpful message
            game.msg.append(str("Yay - you've got the " + self.name))
            game.msg.append(self.msg['get'])
            game.player.inventory.append(self)
            self.collected = True

        else:
            # otherwise, if the item isn't there to get
            # tell them they can't get it
            game.msg.clear()
            game.msg.append(stylize(commands['get']['error'], colored.fg(1)))

    def drop(self, game, command):
        check = input("Are you sure you want to drop it? y/n: ")
        if check == "y":
            game.player.inventory.remove(self)
            game.msg.append(str('''You fling the {item} to the ground, freeing up some space in your pack''').format(item=self.name))
            game.msg.append("\n")
            # show updated list of pack items
            game.player.list_inventory(game, "", "list")
            # restore the item to the current destination as if dropped on the ground
            game.destination.item.append(self)  

class Weapon(Item):
#create weapons for the player
    def __init__(self, name, description, msg, category, collected, damage, rounds, player):
        super().__init__(name, description, msg, category, collected)
        self.damage = damage
        self.rounds = rounds
        self.player = player

    def use(self):
        pass    

class Food(Item):
#create edible items
    def __init__(self, name, description, msg, category, collected, health):
        super().__init__(name, description, msg, category, collected)
        self.health = health

    def eat(self, game, command):
        if command == self.name and self.category == "food":
            game.msg.append(self.msg['food'])
            
            if self.health > 0:
                game.player.health = game.player.health + self.health
                game.msg.append((stylize("Yum that food just gave you more health.", colored.fg(201))))
            else:
                game.player.health = game.player.health + self.health
                game.msg.append((stylize("Ouch that food was junk dude - you lose some health.", colored.fg(201))))   
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['food']['error'], colored.fg(1))) 

    def drink(self, game, command):

        if command == self.name and self.category == "drink":
            game.msg.clear()
            game.msg.append(self.msg['drink'])
            game.player.health = game.player.health + self.health
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['food']['error'], colored.fg(1)))  

class Magic(Food):
#create magic potion items
    def __init__(self, name, description, msg, category, collected, spell, health, strength):
        super().__init__(name, description, msg, category, health, collected)
        self.spell = spell
        self.strength = strength

    def drink(self, game, command):

        if command == self.name and self.category == "drink":
            game.msg.append(self.msg['drink'])
            game.player.strength = game.player.strength + self.strength
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['magic']['error'], colored.fg(1)))  


class Key(Item):
#create key items
    def __init__(self, name, description, msg, category, collected, object=None):
        super().__init__(name, description, msg, category, collected)
        if object is None:
            self.object = []
        else: 
            self.object = object
        
class WinningItem(Item):
#create winning items - these must be collected to win game!
    def __init__(self, name, description, msg, category, collected, non_player_character=None):
        super().__init__(name, description, msg, category, collected)
        if non_player_character is None:
            self.non_player_character = []
        else: 
            self.non_player_character = non_player_character

    def place_to_win(self, game, command):
        if command.lower() == self.name.lower():
            game.msg.clear()
            game.msg.append(self.msg['place'])
            game.player.winning_items.append(self)
            winning_items_total = len(items['winning_items'])
            if len(game.player.winning_items) == winning_items_total:
                clear()
                game.msg.append(win)
                ascii_banner = pyfiglet.figlet_format("YOU WIN!")
                print(ascii_banner)
            else:
                game.msg.clear()
                game.msg.append(stylize(commands['place']['error'], colored.fg(1))) 

class Clue():
#create cluses to be hidden in objects
    def __init__(self, zone, status):
        self.zone = zone
        self.status = status 

    def read(self, game):
        if self.status == "unread":
            clue_discovery_msg = {"Looks suspiciously like a clue...", "Just what you've looking for, a hint", "Finding anything around here was going to be tricky without a clue..."}
            game.msg.append(random.choice(list(clue_discovery_msg)))
            game.msg.append(str('''It's going to be important to get to THE {zone} on your travels''').format(zone=self.zone.name))
        else:
            game.msg.append('''It looks like you already read and binned this clue''')
