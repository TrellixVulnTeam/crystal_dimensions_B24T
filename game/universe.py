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

    def __init__(self, name, order, voyage, object, item, non_player_character, scenario, colour):
        self.name = name
        self.order = order
        self.voyage = voyage
        self.object = object
        self.item = item
        self.non_player_character = non_player_character
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
            for direction, value in self.voyage.items():
                game.msg.append(str(destinations[value]['name']) + str(" ( direction: " + direction + " )"))   
        game.msg.append(stylize(str("Remember you'll need enough fuel to reach your destination!").format(capacity=10), colored.fg(1)))

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

    def __init__(self, name, description, category, msg):
        self.name = name
        self.description = description
        self.category = category
        self.msg = msg
    
    def get(self, game, command):

        if command == self.name:
            # display a helpful message
            game.msg.append(str("Yay - you've got the " + self.name))
            game.msg.append(self.msg['get'])

            # check if its a weapon or not and add the item to player's inventory
            if self.category == "weapon":
                game.player.collected_weapon = True
            else:
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
    
    def eat(self, game, command):

        if command == self.name and self.category == "food":
            game.msg.append(self.msg['eat'])
            game.player.health = game.player.health + 1
            game.msg.append((stylize("Yum that food just gave you an more health.", colored.fg(201))))
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['eat']['error'], colored.fg(1))) 

    def drink(self, game, command):

        if command == self.name and self.category == "drink":
            game.msg.append(self.msg['drink'])
            game.player.health = game.player.health + 1
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['eat']['error'], colored.fg(1)))

    