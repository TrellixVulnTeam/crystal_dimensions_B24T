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
from config import commands, title, author, mission, player_characters, destinations, transport, non_player_characters, objects, items
from game.game import Game
from game.character import PlayerCharacter
from game.universe import Destination, Transport, Object, Item 

#setup empty new game variables
player = ""
msg = []
inventory = []
player_moves = []

new_game = Game(title, author, mission, player_characters, destinations, non_player_characters, objects, items, "", player, commands, player_moves, msg)

#add transport to game
new_game.transport = Transport(transport[0]['name'], transport[0]['description'], transport[0]['category'], transport[0]['capacity'], transport[0]['fuel'], transport[0]['weapon'], transport[0]['msg'])

#display inital credits and game play instructions
#new_game.showIntro()

#display help - list of moves
#new_game.help()

while True:

    if not new_game.player:
        # print the player choice instructions
        new_game.players()
        character = input('>')
        
        while not new_game.player:    
            if int(character) in new_game.player_characters:
                                
                #add player to game
                new_game.player = PlayerCharacter(new_game.player_characters[int(character)]['name'], new_game.player_characters[int(character)]['power'], new_game.player_characters[int(character)]['weapon'], False, new_game.player_characters[int(character)]['strength'], new_game.player_characters[int(character)]['health'], "", inventory, "")

                # starting location
                for place in destinations:
                    if destinations[place]['order'] == 1:

                        destination_objects = []
                        destination_items = []
                        
                        #create objects
                        for obj in destinations[place]['object']:
                            ob = Object(objects[obj]['name'], objects[obj]['description'], objects[obj]['move'], objects[obj]['msg'])
                            destination_objects.append(ob)

                        #create items
                        for itm in destinations[place]['item']:
                            it = Item(items[itm]['name'], items[itm]['description'], items[itm]['type'], items[itm]['msg'])
                            destination_items.append(it)

                        new_game.player.destination = Destination(destinations[place]['name'], destinations[place]['order'], destinations[place]['voyage'], destination_objects, destination_items, destinations[place]['thing'], destinations[place]['scenario'], destinations[place]['colour'])
                        

            else:
                print(stylize("I'm afraid that's not one of our player_characters", colored.fg(1)))
                time.sleep(1)
                print("Try again...")
                character = input('>') 

    else:
        new_game.showStatus()
        
        # get the player's next 'command'
        # .split() breaks it up into an list array
        # eg typing 'fly east' would give the list:
        # ['fly','east']
        command = ''
        while command == '':
            command = input('>')
        
        new_game.command(command)


