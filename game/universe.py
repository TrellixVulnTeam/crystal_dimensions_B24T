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
from config import win, commands, pack_max, destinations, items, shop
from game.utils import clear

class Destination:
    """Destination class - used in conjunction with Hero to create the players destination"""

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
                game.msg.append(str(destinations[value]['name']) + str(" (direction: " + direction.upper() + ")"))   

    def fly(self):
        pass

class Zone():
    """Create a game zone to find items and fight enemies"""

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

    def __init__(self, name, description, category, capacity, fuel_tank, fuel_usage, weapon, msg):
        self.name = name
        self.description = description
        self.category = category
        self.capacity = capacity
        self.fuel_tank = fuel_tank
        self.fuel_usage = fuel_usage
        self.weapon = weapon
        self.msg = msg   

    def voyage(self, game, command):
    #take your transport on a voyage across the game...
        if "spaceship" in game.player.moves:
            #check for fuel
            if game.player.transport.fuel_tank >=10:
                game.player.moves.append(command)
                # check that can go to their desired destination
                if command in game.player.destination.voyages:
                    voyages = game.player.destination.voyages
                    new_destination = voyages[command] - 1
                    #set the new player destination and zone
                    game.player.destination = game.destinations[new_destination]
                    game.player.zone = game.destinations[new_destination].zones[0]
                    #spend the fuel
                    game.player.transport.fuel_tank = game.player.transport.fuel_tank - game.player.transport.fuel_usage

                    game.msg.append(str('''After a quick interstellar hop through the universe 
you've arrived on {destination}
    ''').format(destination = game.player.destination.name))            
                    game.player.moves.clear()
                else:
                    game.msg.append(stylize("You can't go in that direction - you'll get lost!", colored.fg(1)))
            else:
                game.msg.append(stylize("You don't have enough fuel to make the trip dude...", colored.fg(1)))    
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['fly']['error'], colored.fg(1)))
            if not game.player.transport:
                game.msg.append("But it must be your lucky day as you happen to have a ")
                game.show_vehicle()

class Object:  
    """Create physical objects in the game"""

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

class Shop(Object):
    """create a shop extending objects (place a shop in a zone and one per destination)"""
    
    def __init__(self, name, description, move, clue, msg, products=None):
        super().__init__(name, description, move, clue, msg)
        if products is None:
            self.products = []
        else: 
            self.products = products   

    def buy(self, game):
        if game.player.credits > 1:
            print("What would you like to buy?")
            for product, product_att in self.products.items():
                print(str("{id}) {name} - (CR: {credits})").format(id=product, name=product_att['name'],credits=product_att['credits']))
            print("0) Nothing")
            print(stylize('''Type a number:''', colored.fg(84)))
            product_select = input('>')
            try:
                val = int(product_select)
            except ValueError:
                print(stylize('''Doesn't look like they sell that here...''', colored.fg(1)))
                time.sleep(1)
                print(stylize('''Try again...''', colored.fg(84)))
                product_select = input('>')    
            if int(product_select) in self.products:
                if game.player.credits >= self.products[int(product_select)]['credits']:
                    game.player.credits -= self.products[int(product_select)]['credits']
                    if self.products[int(product_select)]['name'] == "fuel":
                        game.player.inventory.append(Item("fuel tank", "Not delicious but fairly nutritious", {"food": '''Actually quite filling - you feel ready for action!!'''}, "fuel", 12, True))
                    elif self.products[int(product_select)]['name'] == "food":
                        game.player.inventory.append(Food("protein pouch", "Not delicious but fairly nutritious", {"food": '''Actually quite filling - you feel ready for action!!'''}, "food", 10, True, 1))
                    elif self.products[int(product_select)]['name'] == "water":    
                        game.player.inventory.append(Food("water bottle", "Always good to quench your thirst", {"drink": '''Pretty delish - not thirsty anymore!'''}, "drink", 2, True, 0))
                    game.msg.append(self.msg['buy'])
        else:
            game.msg.append(stylize('''You need some crrrr's to buy stuff around here!!?!*!''', colored.fg(1)))

    def sell(self, game):
        print("What would you like to sell?")
        # show updated list of pack items
        for item in game.player.inventory:
            print(item.name)
        print(stylize('''Name something:''', colored.fg(84)))
        item_select = input('>')
        if game.player.list_inventory(game, item_select.lower(), "check") == True:
            check = input("Are you sure you want to sell this? y/n: ")
            if check == "y":
                for item in game.player.inventory:
                    if item.name.lower() == item_select.lower():
                        credits = item.value - 2
                        game.player.credits += credits
                        game.player.inventory.remove(item)
                        game.msg.append(str('''You have earnt yourself {credits}''').format(credits=credits))
                        game.msg.append("\n")
            else:
                print('''OK, what next then?''')



        

class Item:
    """create items (pick-ups) in the game"""

    def __init__(self, name, description, msg, category, value, collected):
        self.name = name
        self.description = description
        self.msg = msg
        self.category = category
        self.value = value
        self.collected = collected
    
    def get(self, game, command):
        if command.lower() == self.name.lower():
            # check the number of items pack
            pack_total = len(game.player.inventory)
            if pack_total < pack_max:
                # display a helpful message
                game.msg.append(str("Yay - you've got the " + self.name))
                game.msg.append(self.msg['get'])
                game.player.inventory.append(self)
                self.collected = True
            else:
                game.msg.append(stylize('''You can't pick up this item as your pack is full!!''', colored.fg(1)))
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
    """create weapons for the player"""
    def __init__(self, name, description, msg, category, value, collected, damage, rounds, player):
        super().__init__(name, description, msg, category, value, collected)
        self.damage = damage
        self.rounds = rounds
        self.player = player

    def use(self):
        pass    

class Food(Item):
    """Create edible items"""
    def __init__(self, name, description, msg, category, value, collected, health):
        super().__init__(name, description, msg, category, value, collected)
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
    """create magic potion items"""
    def __init__(self, name, description, msg, category, value, collected, spell, health, strength):
        super().__init__(name, description, msg, category, value, health, collected)
        self.spell = spell
        self.strength = strength

    def drink(self, game, command):

        if command == self.name and self.category == "drink":
            game.msg.append(self.msg['drink'])
            game.msg.append(self.msg['magic'])
            game.player.health = game.player.health + self.health
            game.player.strength = game.player.strength + self.strength
            game.player.inventory.remove(self)
        else:
            game.msg.clear()
            game.msg.append(stylize(commands['magic']['error'], colored.fg(1)))  

class Key(Item):
    """Create key items"""
    def __init__(self, name, description, msg, category, value, collected, object=None):
        super().__init__(name, description, msg, category, value, collected)
        if object is None:
            self.object = []
        else: 
            self.object = object     
        
class WinningItem(Item):
    """create winning items - these must be collected to win game!"""
    
    def __init__(self, name, description, msg, category, value, collected, non_player_character=None):
        super().__init__(name, description, msg, category, value, collected)
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
                game.msg.append(ascii_banner)
            else:
                game.msg.append(stylize(commands['place']['error'], colored.fg(1))) 


class Credit(Item):
    """Create credits"""

    def __init__(self, name, description, msg, category, value, collected):
        super().__init__(name, description, msg, category, value, collected)

    def get(self, game, command):
        if command.lower() == self.name.lower():
            game.player.credits = game.player.credits + self.value
            game.msg.append(str("Yay - you've got the " + self.name))
            game.msg.append(self.msg['get'])
            game.msg.append(stylize(str("You've just added {value} credits to your wallet!").format(value=self.value), colored.fg(1)))
            self.collected = True
            
        else:
            # otherwise, if the item isn't there to get
            # tell them they can't get it
            game.msg.clear()
            game.msg.append(stylize(commands['get']['error'], colored.fg(1)))
            
class Clue():
    """create cluses to be hidden in objects"""
    
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
