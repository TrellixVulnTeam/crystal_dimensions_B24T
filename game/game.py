#!/bin/python3
# Game characters
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
from game.universe import Destination, Object, Item
from game.character import NonPlayerCharacter
from game.utils import clear
from config import commands, intro, objects, items, conversation

# pip install chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new trainer for the chatbot
from chatterbot.trainers import ListTrainer

class Game:
#main game class object, complete with heler functions, help, quit, restart, move etc..
    
    def __init__(self, title, author, mission, player_characters, destinations, transport, player, commands, msg):
        self.title = title
        self.author = author
        self.mission = mission
        self.player_characters = player_characters
        self.destinations = destinations
        self.transport = transport
        self.player = player
        self.msg = msg
        self.commands = commands
        self.msg = msg

        #start a new chatbot
        self.chatbot = ChatBot("Dilly")
        trainer = ListTrainer(self.chatbot)
        trainer.train(conversation)

    def help(self):
        #print all the moves
        self.msg.clear()
        self.msg.append("Useful commands\n")
        for command in self.commands:
            if self.commands[command]['hidden'] is False:
                self.msg.append(stylize(command + " [ " + self.commands[command]['input'] + " ]", colored.fg(84)))
        self.msg.append(stylize("\nTip: there are all some hidden moves...\n", colored.fg(1)))
    
    def quit(self):
        clear()
        ascii_banner = pyfiglet.figlet_format("BYE BYE!")
        print(ascii_banner)
        print('{0}'.format('='*75))
        print(self.title + " by " + self.author)
        print('{0}'.format('='*75))
        exit()

    #Restarts the current program.
    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def show_intro(self):
        clear()
        # ascii banner
        ascii_banner = pyfiglet.figlet_format(self.title)
        print(stylize(ascii_banner, colored.fg(84)))
        time.sleep(1)
        # print an introduction to the game
        print('{0}'.format('='*75))
        print("Designed by " + self.author)
        print('{0}'.format('='*75))
        time.sleep(1)
        print(self.mission) 

    def show_welcome(self):
        self.msg.append(str('''
Hey there {name} there's no time to waste...    
Looks like your super power - {power} 
- will be key to saving humanity.    
{intro}''').format(name = self.player.name, power = self.player.power, intro = intro))
       
    def show_status(self):
        clear()
        # print the player's current status
        ascii_banner = pyfiglet.figlet_format(self.player.destination.name)
        print(stylize(ascii_banner, colored.fg(self.player.destination.colour)))

        #if beginning of the game print welcome message
        if not self.player.moves and (self.player.destination == self.destinations[0]):
            self.show_welcome()

        if self.player.weapon:
            weapon =  self.player.weapon.name
        else: 
            weapon = ""

        # print player
        print(stylize("Player : " + self.player.name, colored.fg(84)))
        # print powers
        print(stylize("Power : " + self.player.power, colored.fg(84)))
        # print weapon
        print(stylize("Weapon : " + weapon, colored.fg(84)))
        # print health
        print(stylize("Health :" + str(self.player.show_health()), colored.fg(15) + colored.bg(1)))

        #print destination scenario if just arrived
        if not self.player.moves:
            self.msg.append(self.player.destination.scenario)
            self.player.destination.scenario is None
        
        # print the quick look script - if there is an item

        if self.player.health > 0 and ((self.player.zone.items == False) and not self.msg):
            self.msg.append(str('''
You have a quick look around you and see what appears to be a {item} 
on the ground in front of you.
            ''').format(item = self.player.zone.items[0].name))
                
        if self.msg:
            print("{0}".format("="*75))
            for m in self.msg:
                print (m)
                time.sleep(.500)
            print("{0}".format("="*75))
        print(stylize("What next!?!", colored.fg(84)))

    def show_vehicle(self):
        #print out details of the chosen transport for this game
        name = self.transport.name.upper()
        name = "*".join(name)
        self.msg.append(stylize(name, colored.fg(84)))
        self.msg.append(self.transport.description)
        self.msg.append(self.transport.msg['look'])  

    def show_navigator(self):
        self.msg.append(str("Vehicle category: {category}").format(category=self.transport.category.upper()))
        self.msg.append(str("Fuel: {fuel}").format(fuel=self.transport.fuel))
        self.msg.append(str("Current location: {location}").format(location=self.player.destination.name.upper()))
        self.player.destination.voyage_list(self, "list")
        
    def players(self):
        
        for key, value in self.player_characters.items():
           print(str(key) + ") " + value['name'] + " ( " + value['power'] + " )")

    def select_weapon(self):
        print('''There's a big stack of weapons on the floor in front of you!''')
        i = 1
        for weapon in self.player.zone.weapons:
            print(str(i) + ") " + weapon.name)
            print(weapon.description)
            i += 1
        print(stylize("Pick up one of these weapons? Type a number:", colored.fg(84)))
        weapon_select = input('>')
        try:
            val = int(weapon_select)
        except ValueError:
            print(stylize("Doesn't look like there is a weapon like that...", colored.fg(1)))
            time.sleep(1)
            print(stylize("Try again...", colored.fg(84)))
            weapon_select = input('>')
        if int(weapon_select) in items['weapons']:
            self.player.weapon =  self.player.zone.weapons[int(weapon_select)]   

    def command(self, command):

        command = command.lower().split(" ", 1)
        if self.player.health == 0:
            # tell player they are dead and need to restart the game
            clear()
            ascii_banner = pyfiglet.figlet_format("GAME OVER")
            print(ascii_banner)
            print(stylize("Hey - Im afraid you're not longer with us. Type restart to play again.", colored.fg(1)))

        elif command[0] in self.commands:
            
            #'quit' command - available throughout game
            if command[0] == 'quit':
                clear()
                ascii_banner = pyfiglet.figlet_format("BYE BYE!")
                print(ascii_banner)
                print('{0}'.format('='*75))
                print(str("{title} by {author}").format(title = self.title, author = self.author))
                print('{0}'.format('='*75))
                exit()
            
            #'help' command - available throughout game
            if command[0] == 'help':
                self.msg.clear()
                self.player.moves.append(command[0])
                self.help()

            #'restart' command - available throughout game
            if command[0] == 'restart':
                self.restart()

            #'fly' command
            if command[0] == 'fly':
                self.msg.clear()
                self.player.moves.append(command[0])

                if "spaceship" in self.player.moves:
                    self.player.moves.append(command[0])
                     # check that can go to their desired destination

                    if command[1] in self.player.destination.voyages:
                        directional_move = command[1]
                        voyages = self.player.destination.voyages
                        new_destination = voyages[directional_move]
                        self.player.destination = self.destinations[new_destination]
                        self.player.zone = self.destinations[new_destination].zones[0]
                        
                        self.msg.append(str('''
After a quick interstellar hop through the universe you've arrived on {destination}
                        ''').format(destination = self.player.destination.name))            
                        self.player.moves.clear()
                    else:
                        self.msg.append(stylize("You can't go in that direction - you'll get lost!", colored.fg(1)))
                else:
                    self.msg.clear()
                    self.msg.append(stylize(commands['fly']['error'], colored.fg(1)))
                    if not self.player.transport:
                        self.msg.append("But it must be your lucky day as you happen to have a ")
                        self.show_vehicle()

            #'items' command
            if command[0] == 'items':
                self.msg.clear()
                self.player.moves.append(command[0])
                self.player.list_inventory(self, "", "list")

            #'get' command
            if command[0] == 'get':
                self.msg.clear()
                self.player.moves.append(command[0])
                if command[1] == self.player.zone.items.name:
                    self.player.zone.items.get(self, command[1])
                else:
                    self.msg.clear()
                    self.msg.append(stylize(commands['get']['error'], colored.fg(1))) 
            
            #'drop' command
            if command[0] == 'drop':
                self.msg.clear()
                self.player.moves.append(command[0])
                if self.player.list_inventory(self, command[1], "check") == True:
                    for itm in self.player.inventory:
                        if itm.name == command[1]:
                            itm.drop(self, command[1])  

            #'eat' command
            if command[0] == 'eat':
                self.msg.clear()
                self.player.moves.append(command[0])
                if self.player.list_inventory(self, command[1], "check") == True:
                    for itm in self.player.inventory:
                        if itm.name == command[1]:
                            itm.eat(self, command[1])

            #'drink' command
            if command[0] == 'drink':
                self.player.moves.append(command[0])
                if self.player.list_inventory(self, command[1], "check") == True:
                    for itm in self.player.inventory:
                        if itm.name == command[1]:
                            itm.drink(self, command[1])

            # 'attack' command
            if command[0] == 'fight':
                self.msg.clear()
                self.player.moves.append(command[0])
                if self.player.destination.thing and self.player.destination.thing.health > 0:
                    #launch an attack
                    self.player.destination.thing.fight(self)
                else:
                    self.msg.clear()
                    self.msg.append(stylize(commands['fight']['error'], colored.fg(1)))
                    
            # 'talk' move
            if command[0] == 'talk':      
                self.player.moves.append(command[0]) 
                
                if self.player.destination.thing:
                    #have a chat
                    self.player.destination.talk(self.chatbot)
                else:
                    self.msg.append(stylize("There's no one here to talk to!", colored.fg(1)))


            # 'look' command
            if command[0] == 'look':   
                self.msg.clear()     
                self.player.moves.append(command[0]) 
                if self.player.list_inventory(self, command[1], "check") == True:
                    self.show_navigator()
                else:    
                    self.player.look(self, command[1])    

            # 'go' command
            if command[0] == 'go':
                self.msg.clear()
                self.player.moves.append(command[0])
                self.player.moves.append(command[1])
                self.player.go(self, command[1])
                
            # 'fart' command
            if command[0] == 'fart':
                self.player.moves.append(command[0])
                self.player.fart(self)

            # 'open' command
            if command[0] == 'open':      
                self.player.moves.append(command[0]) 
                if "key" in self.player.inventory:
                    self.msg.clear()
                    self.msg.append("You open the box with your key and in the bottom you see the " + self.player.destination.crystal)
                else:
                    self.msg.clear()
                    self.msg.append(stylize("You don't have anything to open " + command[1] + " with...perhaps you need to find a key", colored.fg(1)))
        else:
            self.msg.clear()
            self.msg.append(stylize("Sorry, but you can't do that!", colored.fg(1)))

