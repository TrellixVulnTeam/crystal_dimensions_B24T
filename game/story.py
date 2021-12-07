#!/bin/python3
# Story
# Code by Nathaniel Ashford
# Date: 22 September 2019
# RPG game designed by Rudy Ashford

import os
import yaml
import glob

class Story:
    """Story class object, fetches and validates story data for game."""

    def __init__(self):
        self.story = 1
        self.player_characters = self.get_player_characters()
        self.destinations = self.get_destinations()
        self.zones = self.get_zones()
        self.transport = self.get_transport()
        self.shop = self.get_shop()
        self.non_player_characters = self.get_npc()
        self.objects = self.get_objects()
        self.items = self.get_items()

    story_directory = 'crystal_dimensions'

    def validate_files(self):
        story_files = ['story.yaml', 'player_characters.yaml',
            'destinations.yaml', 'zones.yaml', 'transport.yaml',
            'shop.yaml', 'non_player_characters.yaml', 'objects.yaml',
            'items.yaml'
            ]
        file_list = list(map(os.path.basename, glob.glob('story/' + self.story_directory + '/*.yaml')))

        if story_files.sort() == file_list.sort():
            return True
        else:
            msg='You have not added all the correct files to your story theme'
            return msg

    def get_player_characters(self):
        with open('story/' + self.story_directory + '/player_characters.yaml') as f:
            player_characters = yaml.load(f, Loader=yaml.FullLoader)
        return player_characters

    def get_destinations(self):
        with open('story/' + self.story_directory + '/destinations.yaml') as f:
            destinations = yaml.load(f, Loader=yaml.FullLoader)
        return destinations

    def get_zones(self):
        with open('story/' + self.story_directory + '/zones.yaml') as f:
            zones = yaml.load(f, Loader=yaml.FullLoader)
        return zones

    def get_transport(self):
        with open('story/' + self.story_directory + '/transport.yaml') as f:
            transport = yaml.load(f, Loader=yaml.FullLoader)
        return transport

    def get_shop(self):
        with open('story/' + self.story_directory + '/shop.yaml') as f:
            shop = yaml.load(f, Loader=yaml.FullLoader)
        return shop

    def get_npc(self):
        with open('story/' + self.story_directory + '/non_player_characters.yaml') as f:
            non_player_characters = yaml.load(f, Loader=yaml.FullLoader)
        return non_player_characters

    def get_objects(self):
        with open('story/' + self.story_directory + '/objects.yaml') as f:
            objects = yaml.load(f, Loader=yaml.FullLoader)
        return objects

    def get_items(self):
        with open('story/' + self.story_directory + '/items.yaml') as f:
            items = yaml.load(f, Loader=yaml.FullLoader)
        return items

