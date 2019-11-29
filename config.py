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
import pyfiglet

#list of accepted commands
commands = {
        'fight': {'input': '', 'hidden': False, 'error': "There's nothing to fight here..."},
        'fly': {'input': 'direction', 'hidden': False, 'error' : "Steady on... you'll need wings to fly!"},
        'go': {'input': 'object', 'hidden': False, 'error' : "There isn't one of those to go to...*!*"},
        'get': {'input': 'item', 'hidden': False, 'error' : "Sorry you can't get that item here :("},
        'drop': {'input': 'item', 'hidden': True, 'error' : "Sorry that item doesn't exist...yet"}, 
        'items': {'input': '', 'hidden': False, 'error' : ""},
        'info': {'input': 'item', 'hidden': True, 'error' : ""},
        'help': {'input': '', 'hidden': False, 'error' : ""},
        'look': {'input': 'direction', 'hidden': False, 'error' : "What's that look for!?! (may have been your clumsy typing...)"}, 
        'quit': {'input': '', 'hidden': False, 'error' : ""},
        'talk': {'input': '', 'hidden': False, 'error' : "There's not a soul about to talk to..."},
        'use': {'input': 'power', 'hidden': False, 'error' : ""},
        'inspect': {'input': 'planet', 'hidden': True, 'error' : "Nothing to inspect"},
        'open': {'input': 'item', 'hidden': True, 'error' : "Nothing to open"},
        'eat': {'input': 'food', 'hidden': True, 'error' : "Blueurgh! that's not edible"},
        'drink': {'input': 'item', 'hidden': True, 'error' : "Drink what!?! there's only engine fuel here..."},
        'dance': {'input': 'name', 'hidden': True, 'error' : "That's not a dance!!"},
        'fart': {'input': '', 'hidden': True, 'error' : "You can only fart smelly air dude!"},
        'check': {'input': 'misc', 'hidden': True, 'error' : "Nothing to check"},
        'restart': {'input': '', 'hidden': True, 'error' : ""}
        }

#Games setup credits and mission
title = "Crystal Dimensions"
author = "Rudy Ashford"
mission = '''
Travel accross the Galagamatic Universe to find 
the three crystals that hold the key to closing 
the portal and saving planet Earth!

Your mission is to collect your weapons and use your 
super powers to get to the cystals before your time 
runs out and Earth is destoyed!*!*!
'''
intro = '''
You begin your journey in a secret bunker in Stiffkey 
deep in the Norfolk arena - sector 9 on the planet Grampsian. 

The sea is on the horizon and your spaceship 
is parked just out of sight on the mud flats.
'''


#destinations
destinations = {
        1: {
        'name': 'Sector 9',
        'voyages': {'north': 3, 'east': 2, 'south': 4, 'west': 5},
        'crystal': False,
        'scenario': '''You check your handheld navigation system, 
from here you can fly to the South, where you'll find planet Sapsa 
and it's not far or fly North to Yanus.

It occurs to you that both planets could have the crystals you
so desperately need but that you also risk bumping into trouble...''',
        'colour': 125 
    },
        2: {
        'name': 'Taiga planet',
        'voyages': {'north': 3, 'west': 5, 'south': 4},
        'crystal': True,
        'scenario': '''You struggle to find somewhere to land, 
with great skill you park in the middle of what 
appears to be the only dry land surrounded by swamp. 
You climb out into the damp air - ready to start investigating 
the new planet you've landed on.''',
    'colour': 51
    },  
        3: {
        'name': 'Yanus planet',
        'voyages': {'east': 2, 'west': 5, 'south': 4},
        'crystal': True,
        'scenario': '''You land with a bump on an empty piece of land - there's a twilight glow
to the sky and the air is dry. Stepping out of the spaceship, the ground 
is rocky, almost crunching under foot.''',
        'colour': 214
    },
        4: {
        'name': 'Sapsa planet',
        'voyages': {'east': 2, 'north': 3, 'west': 5},
        'crystal': True,
        'scenario': '''You pull off a super smooth landing in a clearing and 
run towards what looks like vegetation - travelling around the solar system 
has made you hungry.''',
        'colour': 226
    },
        5: { 
        'name': 'Earth',
        'voyages': {'north': 3, 'south': 4},
        'crystal': False,
        'scenario': '''You've arrived on Earth, memories flood back, the summer breeze, the trees, 
the ocean but enough of this nostalgia where is the Portal?''',
        'colour': 21
    }
}

#game zones
zones = {
        1: {
        'name': 'The forest',
        'scenario': '''A copse of tall rigid trees zig zagged across the hill. 
Their silky green leaves drift down from their spikey branches onto the damp forest floor.'''
        },
        2: {
        'name': 'The graveyard',
        'scenario': '''Uneven rows of massive tombs stretch into the distance.
There is a path weaving through the graves of a thousand dead bodies...
But it is overgrown and riddled with potholes. Night or day this 
place has an atmosphere - dark, always dark.'''
        },
        3: {
        'name': 'The town of nothing',
        'scenario': '''Destroyed and hollow, rows of abandoned homes 
lay quiet and eerie. Roads weave through the buildings and debris, 
in the distance you can make out hundreds if not thousand of candles 
flickering in the ancient ruins, maybe despite the deserted appearance 
there is life...'''
        },
        4: {
        'name': 'The lost lake',
        'scenario': '''The cold clear water shimmers like molten glass 
on the surface of the forgotten lake. The marshy banks surrounding the dark
lake is covered in a glowing green moss - you've seen this vegetation before 
and recall it to be the home to poisonous balck and red beatles. Where they live
nothing else does...'''
        },
        5: {
        'name': 'Rainbow falls',
        'scenario': '''A flowing torrent of candy colours descends form the sky, 
crashing into the rock pools hundreds of feet below. A multi-coloured mist that's
warm and tingly stops you fomr seeing much but despite this it's somehow magical'''
        },
        6: {
        'name': 'Alien Corp',
        'scenario': '''Three sky scrapers, all glass and carbon fibre tower climb high
into the nights sky. Each with a matrix of illumination - they look like alien spaceships 
just landed - a bright neon sign reads "ALIEN CORP PLC"'''
        },
        7: {
        'name': 'Stone statue',
        'scenario': '''The sand is whippin gup off the dessert floor, partly hiding
the giant stone statue in fornt of you. It must be at least 20 feet tall. It looks
like a fierce warrior going into battle. It is wielding an emormous sharp scord above
it's head. The statue looks like granite but it has a fur coat of moss''
        },
        8: {
        'name': 'Zone 8',
        'scenario': '''zone 8 lorem ipsum.'''
        },
        9: {
        'name': 'Zone 9',
        'scenario': '''zone 9 lorem ipsum.'''
        },
        10: {
        'name': 'Zone 10',
        'scenario': '''zone 10 lorem ipsum.'''
        },
        11: {
        'name': 'Zone 11',
        'scenario': '''zone 11 lorem ipsum.'''
        },
        12: {
        'name': 'Zone 12',
        'scenario': '''zone 12 lorem ipsum.'''
        },
        13: {
        'name': 'Zone 13',
        'scenario': '''zone 13 lorem ipsum.'''
        },
        14: {
        'name': 'Zone 14',
        'scenario': '''zone 14 lorem ipsum.'''
        },
        15: {
        'name': 'Zone 15',
        'scenario': '''zone 15 lorem ipsum.'''
        },
        16: {
        'name': 'Zone 16',
        'scenario': '''zone 16 lorem ipsum.'''
        },
        17: {
        'name': 'Zone 17',
        'scenario': '''zone 13 lorem ipsum.'''
        },
        18: {
        'name': 'Zone 18',
        'scenario': '''zone 14 lorem ipsum.'''
        },
        19: {
        'name': 'Zone 19',
        'scenario': '''zone 15 lorem ipsum.'''
        },
        20: {
        'name': 'Zone 20',
        'scenario': '''zone 16 lorem ipsum.'''
        },
}
#player characters
player_characters = {
    1: {
        'name': 'Rampage', 
        'power': 'Superhuman strength', 
        'strength': 7,
        'health': 5
        },

    2: {
        'name': 'Springing Tiger', 
        'power': 'Mega jump (30m)', 
        'strength': 5,
        'health': 5
        },

    3: {
        'name': 'Armoured Soldier', 
        'power': 'Laser eyes', 
        'strength': 6,
        'health': 5
        }
}

#non player characters
non_player_characters = {
    1 : {
        'name': 'gabaloni',
        'species': 'Dankans',
        'appearance': '''
big green slimey hairy lizzard with a long spikey tail. They're really 
strong and fierce fighters.
        ''',
        'art': ''' ''',
        'encounter': '''
A tall shadow moves quickly across the floor and before you know it 
- you are face to face with a mean looking monster!
        ''',
        'weakness': 'stupidity',
        'status': 'foe',
        'strength': 6,
        'health': 3
    },
    2 : {
        'name': 'pacini',
        'species': 'Scepti',
        'appearance': '''
small and fast with a cunning smile. They carry daggers in each hand. 
Be careful as these guys are super intelligent.
        ''',
        'art': '''

        ''',
        'encounter': '''
Something darts about in the corner of your vision, then speeds past you, 
too fast to make out. Then whatever it is calls out - "I'll fight you for 
that spaceship"
        ''',
        'weakness': 'greed',
        'status': 'foe',
        'strength': 5,
        'health': 3
    },
    3 : {
        'name': 'dilly',
        'species': 'Labadu',
        'appearance': '''
two and half feet high with delicate features, pointy ears and pink hair. 
You know them to be loyal and really chatty.
        ''',
        'art': '',
        'encounter': '''
There's a russle behind you, sounds like someone tripping over and then you 
get a tap on the shoulder - turning round you see it and smile.
        ''',
        'weakness': 'clumsy',
        'status': 'friend',
        'strength': 2,
        'health': 2
    },
    4 : {
        'name': 'sapdeez',
        'species': 'Calltee',
        'appearance': '''
heavy build with wings and a beak. It has armoured scales and they like to 
destroy everything in their path.
        ''',
        'art': '',            
        'encounter': '''
Loud swooshing and squarking screaches in your ears and you dive for shelter, 
it swoops over your head once more before landing 4 feet away and you get a 
proper look.
        ''',
        'weakness': 'slow',
        'status': 'foe',
        'strength': 5,
        'health': 2
    },
    5 : {
        'name': 'lord devilhanger',
        'species': 'Galati',
        'appearance': '''
deathly pale, 8 feet tall human like creature. He carries a blunderbuss riffle on his back 
and shoots anything that gets in his way.
        ''',
        'art': '',               
        'encounter': '''
As you have feared the mission is not quite in the bag - standing between you and the portal 
is the fiercest of the foes that you have faced so far...
        ''',
        'weakness': 'vanity',
        'status': 'foe',
        'strength': 8,
        'health': 5
        }
}

#transport
transport = {
        0: {
        "name": "spaceship",    
        "description": '''It's a sporty looking, lightweight ship with no frills. 
It can carry a couple of passangers and enough fuel 
to get you to the local shops and back...''',
        "category": "spaceship",
        "capacity": 3,
        "fuel": 100,
        "weapon": "Lazers",
        "msg": {"go": '''You stroll up to your spaceship, with a push of a button 
you open the hatch, then you climb aboard and fire up the engines - 
you're ready to fly out into the Galagamtic Universe...

Might be worth having a look at your navigator 
to see where to go next!''', 
"look": '''You can see it neatly parked just behind you, it's all fueled up 
and ready to go - whenever you are...'''
        }
    },
}

#objects
objects = {
    1: {
        "name": "portal",
        "description": "Large black metal container with no obvious markings",
        "move": {"enter"},
        "msg": {"go": '''You're now inches away from the portal.''', "look": '''
You see something you think might be the portal'''} 
    },
    2: {
        "name": "box",
        "description": "Large black metal container with no obvious markings",
        "move": {"open"},
        "msg": {"go": '''The box is much bigger than it looked from a distance. 
It has a door but it's firmly shut - locked by the looks of it...''', "look": '''
A square metal container is lying on the ground up ahead of you''' 
        }
    },
    3: {
        "name": "treehouse",
        "description": '''High up in the trees there is a platform with a hideawy camouflaged 
in the branches of the big oak tree''',
        "move": {"climb"},
        "msg": {"go": '''You're standing below the treehouse - wondering how to get up to it and 
inside to have a look around - could be hiding something interesting''', "look": '''Up high above you can make out a treetop hideaway'''
        }
    },
    4: {
        "name": "table",
        "description": '''It's a long wooden table covered in elaborate carvings. 
It look like it has been prepared for a feast 
but there is no one around it''',
        "move": {"under"},
        "msg": {"go": '''You run up to the table keen to see if there are any signs of life...''', "look": '''There in front of you is a long wooden table'''
       }
    }
}

#items
items = {
        "weapons": {
        1: {
        "name": "Rhino horn daggers",
        "description": "Nothing is sharper or cuts deaper than fossilized rhino horn.",
        "damage": 3,
        "rounds": 18,
        "msg": {"get": '''You're now armed with your trusty weapon - 
ready to do battle with the bad guys...''', "look": '''Right by your feet is your weapon. 
Where you're going - you're defintely going to need a weapon!'''},
        "category": "weapon",
        "player": 1
        },
        2: {
        "name": "Two swords and a pistol",
        "description": '''Ready for close and long range combat. 
The swords are your favourite but you are happy to finish the job with a pistol if need be...''',
        "damage": 4,
        "rounds": 14,
        "msg": {"get": '''You're now armed with your trusty weapon - 
ready to do battle with the bad guys...''', "look": '''Right by your feet is your weapon. 
Where you're going - you're defintely going to need a weapon!'''},
        "category": "weapon",
        "player": 2
        },
        3: {
        "name": "Rifle",
        "description": '''You need to get up out of the way with this weapon,
its leathal but you need some cover to use it range effectively''',
        "damage": 5,
        "rounds": 10,
        "msg": {"get": '''You're now armed with your trusty weapon - 
ready to do battle with the bad guys...''', "look": '''Right by your feet is your weapon. 
Where you're going - you're defintely going to need a weapon!'''},
        "category": "weapon",
        "player": 3
        }},
        "winning_items": {
    1: {
        "name": "Collapse Crystal",
        "description": '''A very thin, sheet like crystal with shards of shiny black 
material running through the middle.''',
        "msg": {"get": '''Nice work, another precious crystal and 
another step closer to completing your mission''', "look": '''You spot what looks like a stone but something tells 
you it is more than that'''},
        "category": "crystal"
    },
    2: {
        "name": "Build Crystal",
        "description": '''A dense perfect square. Purple and very shiny, 
when you look into this crystal you see your reflection
but wear your eyes would be, there are black holes.''',
        "msg": {"get": '''It's the build crystal, this one creeps you right out but 
you're pleased it's safely in your possession''', "look": '''What's that shiny thing relfecting the light a little way off, 
you can just about see the light bouncing of it is purple - the build crystal is purple...'''},
        "category": "crystal"
        
    },
    3: {
        "name": "Unite Crystal",
        "description": '''This is the most beautiful thing you have ever seen.
Radiating warmth and energy, the Unite Crystal has an 
iridescent glow that lights up it's surroundings.''',
        "msg": {"get": '''Wow you barely manage to take your eyes off the Crsytal as you stow it away safely.
The rumours were right this is the most powerful crystal and you've got it!!''', "look": '''There's glow coming up from somewhere in the undergrowth.
It could be some kind of energy source - its worth a closer look.'''},
        "category": "crystal"
    }},
        "keys": {
    1: {
        "name": "skeleton key",
        "description": '''It's a Large iron key with a Ruby encrusted bit and a 
ornate looking blade.''',
        "msg": {"get": '''You pocket the skeleton key - this will unlock anything''', "look": '''Is that a key you can see, looks like someone has tried to hide it 
- but failed as there it is bold as brass, right in front of you!'''},
        "category": "key"
    }},
        "magic": {
    1: {
        "name": "potion",
        "description": '''A small leather flask with clear liquid inside.
Smells like vanilla pods.''',
        "type": "drink",
        "msg": {"get": '''Supplies always come in handy - I wonder if the potion has any kick to it?''', "look": '''There's a bottle - looks too special to be water...''',
"drink": '''With a gulp and a slurp you down the potion.
A few moments later the hallucinations kick in -
you might need to lie down for while...'''},
        "category": "magic",
        "spell": "",
        "health": -1,
        "strength": 0
    }},
        "food": {
    1: {
        "name": "cake",
        "description": '''That's one big slice of sticky chocolate cake.''',
        "type": "food",
        "msg": {"get": '''Save this food in case of hunger or the need for a boost!''', "look": '''Your eyes must be decieving you - 
it looks like cake ****chocolate cake!?!****''', "food": '''You gobble it down so quickly it's like it has evapourated - and then
you start to feel bloated, you really need to fart dude
 or you might explode...'''},
        "category": "food",
        "health": 0,
    },
    2: {
        "name": "water",
        "description": '''Blue. Cold. Wet. Delicious''',
        "type": "food",
        "msg": {"get": '''Water seems precious around here - you might get thirsty!''', "look": '''A small bamboo flask holding what looks like water''', "drink": '''You take a couple fo big gulps,
it is water and it's as refreshing as you'd hoped it would be...'''},
        "category": "drink",
        "health": 0,
    }}
}

conversation = [
            "How are you?",
            "I am good.",
            "That is good to hear.",
            "Thank you",
            "You are welcome.",
            "What is your name?",
            "My name is Dilly - what is yours?",
            "Where are you from?",
            "I was born on a planet to the South of here - Sapsa - do you know of it?",
            "Will you help me?",
            "Yes of course - how can I help?",
            "Where are the crystals?",
            "I hear you'll find them on the planets in the nearby solar system",
            "but where exactly?",
            "riddle me dee riddle mee do - the collapse crytal is right in front of you!",
            "I like your hair",
            "Thanks - pink is my favourite colour",
            "what is you favourite colour?",
            "Green",
            "Will you come in my spaceship to find the crystals?",
            "Why not - but I have to be back by 5pm tomorrow to watch Strictly!!",
            "Bye",
            "Bye Bye (press ctrl + d)",
            "Can you fight?",
            "No I am a peaceful, loving soul",
            "Can you fly a spaceship?",
            "Yes - been flying across the Universe all my life"
        ]