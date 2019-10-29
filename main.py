#!/bin/python3
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game design by Rudy Ashford

import sys
import os
import random
import time
import colored
from colored import stylize
from config import commands, title, author, mission, player_characters, destinations, zones, transport, non_player_characters, objects, items
from game.game import Game
from game.character import PlayerCharacter
from game.universe import Destination, Zone, Transport, Object, Item, Weapon, Food, Magic, Key, WinningItem
from game.utils import chunks

#setup empty new game variables
msg = []
inventory = []
game_items = []
game_weapons = []
game_winning_items = []
game_keys = []
game_magic = []
game_food = []
game_objects = []
game_zones = []
game_destinations = []

#create the destinations, zones, transport, weapons, items and objects for a new game

#create transport for game
game_transport = Transport(transport[0]['name'], transport[0]['description'], transport[0]['category'], transport[0]['capacity'], transport[0]['fuel'], transport[0]['weapon'], transport[0]['msg'])

#items are a little more copmlex as they come in a variety of shapes and sizes

#weapons
for weapon in items['weapons'].items(): 
    game_weapons.append(Weapon(weapon[1]['name'], weapon[1]['description'], weapon[1]['msg'], weapon[1]['category'], False, 0, 0, weapon[1]['player']))

#winning items
for winning_item in items['winning_items'].items():
    game_winning_items.append(WinningItem(winning_item[1]['name'], winning_item[1]['description'], winning_item[1]['msg'], winning_item[1]['category'], False))

#keys
for key in items['keys'].items():
    game_keys.append(Key(key[1]['name'], key[1]['description'], key[1]['msg'], key[1]['category'], False, ''))
game_items.extend(game_keys)
    
#magic
for magic in items['magic'].items():
    game_magic.append(Magic(magic[1]['name'], magic[1]['description'], magic[1]['msg'], magic[1]['category'], False, magic[1]['spell'], magic[1]['health'], magic[1]['strength']))
game_items.extend(game_magic)
    
#food and drink
for food in items['food'].items():
    game_food.append(Food(food[1]['name'], food[1]['description'], food[1]['msg'], food[1]['category'], False, food[1]['health']))        
game_items.extend(game_food)

#create objects for game
for game_object in objects:
    game_objects.append(Object(objects[game_object]['name'], objects[game_object]['description'], objects[game_object]['move'], objects[game_object]['msg']))

#create zones for game
for game_zone in zones:
    zone_item = random.choice(game_items)
    zone_object = random.choice(game_objects)
    game_zones.append(Zone(zones[game_zone]['name'], zone_object, zone_item, '', '', zones[game_zone]['scenario']))

n = len(zones) / (len(destinations))
game_zones = list(chunks(game_zones, int(n)))

#create destinations for game
i = 0
for game_destination in destinations:
    game_destinations.append(Destination(destinations[game_destination]['name'], destinations[game_destination]['voyages'], destinations[game_destination]['scenario'], destinations[game_destination]['colour'], game_zones[i]))
    i += 1

new_game = Game(title, author, mission, player_characters, game_destinations, game_transport, "", commands, msg)

#display inital credits and game play instructions
#new_game.show_intro()

#display help - list of moves
#new_game.help()

while True:

    if not new_game.player:
        # print the player choice instructions
        new_game.players()
        print(stylize("Please choose a player:", colored.fg(84)))
        character = input('>')
        try:
            val = int(character)
        except ValueError:
            print(stylize("I'm afraid that's not one of our player_characters", colored.fg(1)))
            time.sleep(1)
            print(stylize("Try again...", colored.fg(84)))
            character = input('>') 

        while not new_game.player:    
            if int(character) in new_game.player_characters:
                                
                #add player to game
                new_game.player = PlayerCharacter(new_game.player_characters[int(character)]['name'], new_game.player_characters[int(character)]['power'], "", new_game.player_characters[int(character)]['strength'], new_game.player_characters[int(character)]['health'], "", "", inventory, "")

                # starting destination
                new_game.player.destination = new_game.destinations[0]   
                # starting zone
                new_game.player.zone = new_game.destinations[0].zones[0]
                #add weapons to starting location
                new_game.player.zone.weapons = game_weapons
                # add navigator to back pack
                new_game.player.inventory.append(Item('Navigator', 'Handheld maps magic', 'Your faithful navigation device','tech', True))

            else:
                print(stylize("I'm afraid that's not one of our player_characters", colored.fg(1)))
                time.sleep(1)
                print("Try again...")
                character = input('>') 

    else:
        new_game.show_status()
        
        # get the player's next 'command'
        # .split() breaks it up into an list array
        # eg typing 'fly east' would give the list:
        # ['fly','east']
        command = ''
        while command == '':
            command = input('>')
        
        new_game.command(command)


