#!/bin/python3
# Game characters
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game designed by Rudy Ashford

import sys
import os
import random
import time
import pygame
from termcolor import colored, cprint
import pyfiglet
from game.universe import Destination, Object, Item, WinningItem
from game.character import NonPlayerCharacter
from game.utils import clear
from config import commands, intro, soundtrack, objects, items, conversation

class Game:
    """Main game class object, complete with heler functions, help, quit, restart, move etc.."""

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


    def help(self):
        #print all the moves
        self.msg.clear()
        self.msg.append("Useful commands:\n")
        for command in self.commands:
            if self.commands[command]['hidden'] is False:
                self.msg.append(command + " [ " + self.commands[command]['input'] + " ]")
        self.msg.append("\nTip: there are hidden moves...\n")

    def quit(self):
        clear()
        ascii_banner = pyfiglet.figlet_format("BYE BYE!")
        print(ascii_banner)
        print('{0}'.format('='*95))
        print(self.title + " by " + self.author)
        print('{0}'.format('='*95))
        exit()


    def restart(self):
    #Restarts the current program.
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def play_soundtrack(self):
    #plays soundtrack in background
        pygame.mixer.init()
        pygame.mixer.music.load("music/" + soundtrack)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)


    def show_intro(self):
        clear()
        # ascii banner
        ascii_banner = pyfiglet.figlet_format(self.title)
        cprint(ascii_banner, 'green')
        time.sleep(1)
        # print an introduction to the game
        print('{0}'.format('='*95))
        print("Designed by " + self.author)
        print('{0}'.format('='*95))
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
        #print the player's current status
        ascii_banner = pyfiglet.figlet_format(self.player.destination.name)
        cprint(ascii_banner, 'green')

        #show destination artwork
        if self.player.destination.artwork is not None:
            a = open(self.player.destination.artwork, 'r')
            artwork = a.read()
            a.read()
            cprint(artwork, 'white')
            a.close()


        #if beginning of the game print welcome message
        if not self.player.moves and (self.player.destination == self.destinations[0]):
            self.show_welcome()

        if self.player.weapon:
            weapon =  self.player.weapon.name
        else:
            weapon = ""

        # print player
        print ("\n")
        cprint("Player : " + self.player.name, 'green')
        # print powers
        cprint("Power : " + self.player.power, 'green')
        #print strength
        cprint("Strength : " + str(self.player.strength), 'green')
        #print speed
        cprint("Speed : " + str(self.player.speed), 'green')
        # print weapon
        cprint("Weapon : " + weapon, 'green')
        # print credits
        cprint("Credits : " + str(self.player.credits), 'green')
        # print health
        cprint("Health :" + str(self.player.show_health()), 'green')

        #print destination scenario if just arrived
        if not self.player.moves:
            self.msg.append(self.player.destination.scenario)
            self.player.destination.scenario is None

        if self.player.health > 0 and ((self.player.zone.items == False) and not self.msg):
            self.msg.append(str('''
You have a quick look around you and see what appears to be a {item}
on the ground in front of you.
            ''').format(item = self.player.zone.items[0].name))

        if self.msg:
            print ("\n")
            print("{0}".format("="*95))
            for m in self.msg:
                print (m)
                print("")
                time.sleep(.500)

        print("{0}".format("="*95))
        print ("")
        cprint("What next!?!", 'white', 'on_magenta', attrs=['bold'])

    def show_vehicle(self):
        #print out details of the chosen transport for this game
        name = self.transport.name.upper()
        name = "*".join(name)
        self.msg.append(name)
        self.msg.append(self.transport.description)
        self.msg.append(self.transport.msg.get('look'))

    def players(self):

        for key, value in self.player_characters.items():
           print(str(key) + ") " + value['name'] + " ( " + value['power'] + " )")

    def over(self):
        # tell player they are dead and need to restart the game
        clear()
        ascii_banner = pyfiglet.figlet_format("GAME OVER")
        self.msg.append(ascii_banner)
        self.msg.append("Hey - Im afraid you're not longer with us. Type restart to play again.")


    def select_weapon(self):
        print('''There's a big stack of weapons on the floor in front of you!''')
        i = 1
        for weapon in self.player.zone.weapons:
            print(str(i) + ") " + weapon.name)
            print(weapon.description)
            i += 1
        cprint("Pick up one of these weapons? Type a number:", 'green')
        weapon_select = input('>')
        try:
            val = int(weapon_select)
        except ValueError:
            cprint("Doesn't look like there is a weapon like that...", 'green')
            time.sleep(1)
            cprint("Try again...", 'green')
            weapon_select = input('>')
        if int(weapon_select) in items['weapons']:
            self.player.weapon =  self.player.zone.weapons[int(weapon_select)-1]
            self.msg.append(self.player.weapon.msg.get('get'))

    def command(self, command):

        command = command.lower().split(" ", 1)
        if self.player.health <= 0:
            # tell player they are dead and need to restart the game
            clear()
            ascii_banner = pyfiglet.figlet_format("GAME OVER")
            print(ascii_banner)
            cprint('''Hey - Im afraid you're not longer with us. Type restart to play again.''', 'red')

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
            # end quit

            #'help' command - available throughout game
            if command[0] == 'help':
                self.msg.clear()
                self.player.moves.append(command[0])
                self.help()
            # end help

            #'check' command - available throughout game
            if command[0] == 'check':
                self.msg.clear()
                self.player.moves.append(command[0])
                if command[1] == "location":
                    self.msg.append(str('''Your location: {destination}, {zone}''').format(destination=self.player.destination.name.upper(), zone=self.player.zone.name.upper()))
                elif self.player.list_inventory(self, command[1], "check") == True:
                    self.player.show_navigator(self)
            # end check

            #'restart' command - available throughout game
            if command[0] == 'restart':
                self.restart()
            # end restart

            #'fly' command
            if command[0] == 'fly':
                self.msg.clear()
                self.player.moves.append(command[0])
                if "spaceship" in self.player.moves:
                    self.player.transport.voyage(self, command[1])
                else:
                    self.msg.clear()
                    self.msg.append(commands['fly']['error'])
                    if not self.player.transport:
                        self.msg.append("But it must be your lucky day as you happen to have a ")
                        self.show_vehicle()
                        self.msg.append(str("\ntip: go {transport}\n").format(transport=self.transport.name))


            # end fly

            #'items' command
            if command[0] == 'items':
                self.msg.clear()
                self.player.moves.append(command[0])
                self.player.list_inventory(self, "", "list")
            # end items

            #'get' command
            if command[0] == 'get':
                self.msg.clear()
                self.player.moves.append(command[0])
                if len(command) > 1:
                    if command[1]:
                        if command[1].lower() == self.player.zone.items.name.lower():
                            self.player.zone.items.get(self, command[1])
                        elif isinstance(self.player.zone.winning_items, WinningItem) and command[1].lower() == self.player.zone.winning_items.name.lower():
                            if self.player.zone.non_player_characters.health > 0:
                                self.player.zone.non_player_characters.encounter(self)
                            else:
                                self.player.zone.winning_items.get(self, command[1])
                        else:
                            self.msg.clear()
                            self.msg.append(commands['get']['error'])
                else:
                    self.msg.append('You need to get an item!')
            # end get

            #'drop' command
            if command[0] == 'drop':
                self.msg.clear()
                self.player.moves.append(command[0])
                if command[1]:
                    if self.player.list_inventory(self, command[1], "check") == True:
                        for itm in self.player.inventory:
                            if itm.name == command[1]:
                                itm.drop(self, command[1])
            # end drop

            #'eat' command
            if command[0] == 'eat':
                self.msg.clear()
                self.player.moves.append(command[0])
                if len(command) >= 2:
                    if self.player.list_inventory(self, command[1], "check") == True:
                        for itm in self.player.inventory:
                            if itm.name == command[1]:
                                itm.eat(self, command[1])
                else:
                    self.msg.append("Eat what?")
            # end eat

            #'drink' command
            if command[0] == 'drink':
                self.msg.clear()
                self.player.moves.append(command[0])
                if len(command) >= 2:
                    if self.player.list_inventory(self, command[1], "check") == True:
                        for itm in self.player.inventory:
                            if itm.name == command[1]:
                                itm.drink(self, command[1])
                else:
                    self.msg.append("Drink what?")
            # end drink

            # 'fight' command
            if command[0] == 'fight':
                self.msg.clear()
                self.player.moves.append(command[0])
                if self.player.zone.non_player_characters and self.player.zone.non_player_characters.health > 0:
                    #launch an attack
                    self.player.zone.non_player_characters.fight(self)
                else:
                    self.msg.clear()
                    self.msg.append(commands['fight']['error'])
            # end fight

            # 'talk' move
            if command[0] == 'talk':
                self.player.moves.append(command[0])

                if self.player.zone.non_player_characters:
                    #have a chat
                    self.player.zone.non_player_characters.talk(self.chatbot)
                else:
                    self.msg.append("There's no one here to talk to!")
            # end talk

            # 'look' command
            if command[0] == 'look':
                self.msg.clear()
                self.player.moves.append(command[0])

                if len(command) == 1:
                        command.append("around")

                self.player.look(self, command[1])

            # end look

            # 'go' command
            if command[0] == 'go':
                self.msg.clear()
                self.player.moves.append(command[0])
                if command[1]:
                    self.player.moves.append(command[1])
                    self.player.go(self, command[1])
                else:
                    self.player.moves.append("Go where?")
            # end go

            # 'buy' command
            if command[0] == 'buy':
                self.msg.clear()
                self.player.moves.append(command[0])
                if self.player.zone.objects.name.lower() == "shop" and "shop" in self.player.moves:
                    self.player.zone.objects.buy(self)
                else:
                    self.msg.clear()
                    self.msg.append("Sorry, but you can't do that here - you need a shop!")
            # end buy

            # 'sell' command
            if command[0] == 'sell':
                self.msg.clear()
                self.player.moves.append(command[0])
                if self.player.zone.objects.name.lower() == "shop" and "shop" in self.player.moves:
                    self.player.zone.objects.sell(self)
                else:
                    self.msg.clear()
                    self.msg.append("Sorry, but you can't do that here - you need a shop!")
            # end buy


            # 'fart' command d
            if command[0] == 'fart':
                self.player.moves.append(command[0])
                self.player.fart(self)
            # end fart

            # 'open' command
            if command[0] == 'open':
                self.player.moves.append(command[0])
                self.player.zone.objects.open(self)
            # end open

            # 'climb' command
            if command[0] == 'climb':
                self.player.moves.append(command[0])
                self.player.zone.objects.climb(self)
            # end climb

            # 'read' command
            if command[0] == 'read':
                self.player.moves.append(command[0])
                self.player.zone.objects.read(self)
            # end read

            # 'place' command
            if command[0] == 'place':
                self.msg.append(command[1])
                self.player.moves.append(command[0])
                if self.destinations[-1].zones[-1] == self.player.zone and self.player.list_inventory(self, command[1], "check") == True:
                    for w_itm in self.player.inventory:
                        if w_itm.name.lower() == command[1]:
                            self.msg.append("whoops some-ting wong")
                            w_itm.place_to_win(self, command[1])
                else:
                    self.msg.append("whoops some-ting wong")
            # end place

        else:
            self.msg.clear()
            self.msg.append("Sorry, but you can't do that!")

