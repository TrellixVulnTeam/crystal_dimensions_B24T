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
from config import commands, destinations

class Destination:
#destination class - used in conjunction with Hero to create the players destination

    def __init__(self, name, crystal, voyages, scenario, colour):
        self.name = name
        self.voyages = voyages
        self.scenario = scenario
        self.colour = colour

    def title(self):
        print('{0}'.format('-'*65))
        ascii_banner = pyfiglet.figlet_format(self.name)
        print(stylize(ascii_banner, colored.fg(self.colour)))
        print('{0}'.format('-'*65))

    def voyage_list(self, game, task):
        if task == "list":
            game.msg.append(str("Voyages:"))
            for direction, value in self.voyages.items():
                game.msg.append(str(destinations[value]['name']) + str(" ( direction: " + direction + " )"))   
        game.msg.append(stylize(str("Remember you'll need enough fuel to reach your destination!").format(capacity=10), colored.fg(1)))

class Zone(Destination):
#create a game zone to find items and fight enemies
    def __init__(self, name, objects, items, crystal, non_player_characters, scenario):
        super().__init__(name, scenario)
        self.objects = objects 
        self.items = items
        self.crystal = crystal
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

    def __init__(self, name, description, move, msg):
        self.name = name
        self.description = description
        self.move = move
        self.msg = msg

    def open(self):
        pass

    def climb(self):
        pass

    def smash(self):
        pass

class Item:
#create items (pick-ups) in the game

    def __init__(self, name, description, msg):
        self.name = name
        self.description = description
        self.msg = msg
    
    def get(self, game, command):

        if command == self.name:
            # display a helpful message
            game.msg.append(str("Yay - you've got the " + self.name))
            game.msg.append(self.msg['get'])
            game.player.inventory.append(self)    

            # remove item from destination
            game.player.destination.item.remove(self)        
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
            #show updated list of pack items
            game.player.list_inventory(game, "", "list")
            # restore the item to the current destination as if dropped on the ground
            game.player.destination.item.append(self)  

class Weapon(Item):
#create weapons for the player
    def __init__(self, name, description, msg, damage, rounds):
        super().__init__(name, description, msg)
        self.damage = damage
        self.rounds = rounds

    def use(self):
        pass    
    
class Food(Item):
#create edible items
    def __init__(self, name, description, msg, health, category):
        super().__init__(name, description, msg)
        self.health = health
        self.category = category

    def eat(self, game, command):

        if command == self.name and self.category == "food":
            game.msg.append(self.msg['eat'])
            game.player.health = game.player.health + self.health
            if self.health > 0:
                game.msg.append((stylize("Yum that food just gave you more health.", colored.fg(201))))
            else:
                game.msg.append((stylize("Ouch that food was junk dude - you lose some health.", colored.fg(201))))   
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['food']['error'], colored.fg(1))) 

    def drink(self, game, command):

        if command == self.name and self.category == "drink":
            game.msg.append(self.msg['drink'])
            game.player.health = game.player.health + self.health
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['food']['error'], colored.fg(1)))  

class Potion(Food):
#create magic potion items
    def __init__(self, name, description, msg, health, category, magic, strength):
        super().__init__(name, description, msg, health, category)
        self.magic = magic
        self.strength = strength

class Key(Item):
#create key items
    def __init__(self, name, description, msg, object=None):
        super().__init__(name, description, msg)
        if object is None:
            self.object = []
        else: 
            self.object = object
        
class WinningItem(Item):
#create winning items - these must be collected to win game!
    def __init__(self, name, description, msg):
       super().__init__(name, description, msg)

    def place_to_win(self):
        pass

    