#!/usr/bin/env python3
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game design by Rudy Ashford

# TODO chat with Dilly to get crystal (not fight)
# TODO clear game after win
# TODO remove crystals when placed
# TODO add artwork for NPC's and destinations
# TODO add view health and other stats for NPC
# TODO superpower can only be used when full health

import sys
import os
import random
import time
import yaml
# from config import commands, title, author, soundtrack, mission, player_characters, destinations, zones, transport, shop, non_player_characters, objects, items
from game.story import Story
from game.game import Game
from game.character import Hero, NonPlayerCharacter, Boss
from game.universe import Destination, Zone, Transport, Object, Shop, Item, Weapon, Food, Magic, Key, Credit, WinningItem, Clue
from game.utils import chunks
from termcolor import colored, cprint

#game config
config_file = open('story/crystal_dimensions/story.yaml')
config = yaml.load(config_file, Loader=yaml.FullLoader)

#commands
commands_file = open('game/commands.yaml')
commands = yaml.load(commands_file, Loader=yaml.FullLoader)

new_story = Story()

#setup empty new game lists
msg = []
inventory = []
game_items = []
game_weapons = []
game_non_player_characters = []
game_boss = ""
game_winning_items = []
game_keys = []
game_credits = []
game_magic = []
game_food = []
game_clues = []
game_objects = []
game_zones = []
game_destinations = []

#create the destinations, zones, non-player characters, transport, weapons, items and objects for a new game

#create transport for game
game_transport = Transport(new_story.transport[0]['name'], new_story.transport[0]['description'], new_story.transport[0]['category'], new_story.transport[0]['capacity'], new_story.transport[0]['fuel_tank'], new_story.transport[0]['fuel_usage'], new_story.transport[0]['weapon'], new_story.transport[0]['msg'])

#items are a little more complex as they come in a variety of shapes and sizes

#weapons
for weapon in new_story.items['weapons'].items():
    game_weapons.append(Weapon(weapon[1]['name'], weapon[1]['description'], weapon[1]['msg'], weapon[1]['category'], weapon[1]['value'], False, 0, 0, weapon[1]['player']))

#create non player characters for game
for game_non_player_character in new_story.non_player_characters:
    if new_story.non_player_characters[game_non_player_character]['status'] == "boss":
        game_boss = Boss(new_story.non_player_characters[game_non_player_character]['name'], new_story.non_player_characters[game_non_player_character]['species'], new_story.non_player_characters[game_non_player_character]['appearance'], new_story.non_player_characters[game_non_player_character]['weakness'], new_story.non_player_characters[game_non_player_character]['status'], new_story.non_player_characters[game_non_player_character]['strength'], new_story.non_player_characters[game_non_player_character]['speed'], new_story.non_player_characters[game_non_player_character]['health'], new_story.non_player_characters[game_non_player_character]['msg'])
    else:
        game_non_player_characters.append(NonPlayerCharacter(new_story.non_player_characters[game_non_player_character]['name'], new_story.non_player_characters[game_non_player_character]['species'], new_story.non_player_characters[game_non_player_character]['appearance'], new_story.non_player_characters[game_non_player_character]['weakness'], new_story.non_player_characters[game_non_player_character]['status'], new_story.non_player_characters[game_non_player_character]['strength'], new_story.non_player_characters[game_non_player_character]['speed'], new_story.non_player_characters[game_non_player_character]['health'], new_story.non_player_characters[game_non_player_character]['msg']))

#create a shop for the game
game_shop = Shop(new_story.shop[0]['name'], new_story.shop[0]['description'], 'buy/sell', '', new_story.shop[0]['msg'], new_story.shop[0]['products'])

#winning items
for winning_item in new_story.items['winning_items'].items():
    game_winning_items.append(WinningItem(winning_item[1]['name'], winning_item[1]['description'], winning_item[1]['msg'], winning_item[1]['category'], winning_item[1]['value'], False))

#keys
for key in new_story.items['keys'].items():
    game_keys.append(Key(key[1]['name'], key[1]['description'], key[1]['msg'], key[1]['category'], key[1]['value'], False, ''))
game_items.extend(game_keys)

#credits
for credit in new_story.items['credits'].items():
    game_credits.append(Credit(credit[1]['name'], credit[1]['description'], credit[1]['msg'], 'credits', credit[1]['value'], False))
game_items.extend(game_credits)

#magic
for magic in new_story.items['magic'].items():
    game_magic.append(Magic(magic[1]['name'], magic[1]['description'], magic[1]['msg'], magic[1]['category'], magic[1]['value'], False, magic[1]['spell'], magic[1]['health'], magic[1]['strength']))
game_items.extend(game_magic)

#food and drink
for food in new_story.items['food'].items():
    game_food.append(Food(food[1]['name'], food[1]['description'], food[1]['msg'], food[1]['category'], food[1]['value'], False, food[1]['health']))
game_items.extend(game_food)

#create physical objects for game
for game_object in new_story.objects:
    game_objects.append(Object(new_story.objects[game_object]['name'], new_story.objects[game_object]['description'], new_story.objects[game_object]['move'], '', new_story.objects[game_object]['msg']))

#create zones for game
for game_zone in new_story.zones:
    zone_item = random.choice(game_items)
    zone_object = random.choice(game_objects)
    game_zones.append(Zone(new_story.zones[game_zone]['name'], zone_object, zone_item, '', new_story.zones[game_zone]['scenario']))

final_zone = game_zones.pop()
final_zone.non_player_characters = game_boss

random.shuffle(game_zones)

x = len(game_winning_items)

while x > 0:
    game_zones[x-1].winning_items = game_winning_items[x-1]
    game_zones[x-1].non_player_characters = game_non_player_characters[x-1]
    game_clues.append(Clue(game_zones[x-1], "unread"))
    x -= 1

#hide clues in objects
i = 0
for clue in game_clues:
    game_objects[i].clue = clue
    i += 1

n = len(new_story.zones) / (len(new_story.destinations))
random.shuffle(game_zones)
game_zones.append(final_zone)
game_zones_group = list(chunks(game_zones, int(n)))

for z in game_zones_group:
   z[random.randint(0,3)].objects = game_shop

#create destinations for game
i = 0
for game_destination in new_story.destinations:
    game_destinations.append(Destination(new_story.destinations[game_destination]['name'], new_story.destinations[game_destination]['voyages'], new_story.destinations[game_destination]['scenario'], new_story.destinations[game_destination]['colour'], new_story.destinations[game_destination]['artwork'], game_zones_group[i]))
    i += 1

new_game = Game(config['title'], config['author'], config['mission'], new_story.player_characters, game_destinations, game_transport, "", commands, msg)

#play soundtrack
if config['soundtrack'] is not None:
    new_game.play_soundtrack()

#display inital credits and game play instructions
new_game.show_intro()

#display help - list of moves
new_game.help()

while True:

    if not new_game.player:
        # print the player choice instructions
        new_game.players()
        cprint("Please choose a player (by entering the number):", 'green')
        character = input('>')
        try:
            val = int(character)
        except ValueError:
            cprint("I'm afraid that's not one of our players", 'red')
            time.sleep(1)
            cprint("Try again...", 'green')
            character = input('>')

        while not new_game.player:
            if int(character) in new_game.player_characters:
                #add player to game
                new_game.player = Hero(new_game.player_characters[int(character)]['name'], new_game.player_characters[int(character)]['power'], "", new_game.player_characters[int(character)]['strength'], new_game.player_characters[int(character)]['speed'], new_game.player_characters[int(character)]['health'], new_game.player_characters[int(character)]['health'], "", "", inventory, game_transport, 0)
                # starting destination
                new_game.player.destination = new_game.destinations[0]
                # starting zone
                new_game.player.zone = new_game.destinations[0].zones[0]
                #add weapons to starting location
                new_game.player.zone.weapons = game_weapons
                # add navigator to back pack
                new_game.player.inventory.append(Item('Navigator', 'Handheld maps magic', 'Your faithful navigation device','tech', 25, True))

            else:
                print("I'm afraid that's not one of our player_characters")
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

        while command == '' and new_game.player.health > 0 and len(new_game.player.winning_items) != len(new_story.items['winning_items']):
            command = input('>')

        new_game.command(command)




