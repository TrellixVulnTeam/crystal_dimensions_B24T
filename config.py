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
        'go': {'input': 'direction or object', 'hidden': False, 'error' : "There isn't one of those to go to...*!*"},
        'get': {'input': 'item', 'hidden': False, 'error' : "Sorry you can't get that item here :("},
        'drop': {'input': 'item', 'hidden': True, 'error' : "Sorry that item doesn't exist...yet"}, 
        'items': {'input': '', 'hidden': False, 'error' : ""},
        'info': {'input': 'item', 'hidden': True, 'error' : ""},
        'help': {'input': '', 'hidden': False, 'error' : ""},
        'look': {'input': 'around or closer', 'hidden': False, 'error' : "What's that look for!?! (may have been your clumsy typing...)"}, 
        'place': {'input': 'crystal name', 'hidden': False, 'error' : '''BUT the Earth is stil not safe...
you haven't placed all the crystals yet..do you have the others?
You need to be quick!'''}, 
        'quit': {'input': '', 'hidden': False, 'error' : ""},
        'talk': {'input': '', 'hidden': False, 'error' : "There's not a soul about to talk to..."},
        'use': {'input': 'power', 'hidden': False, 'error' : ""},
        'inspect': {'input': 'planet', 'hidden': True, 'error' : "Nothing to inspect"},
        'open': {'input': 'object', 'hidden': True, 'error' : "Nothing to open"},
        'climb': {'input': 'object', 'hidden': True, 'error' : "Nothing to climb"},
        'read': {'input': 'object', 'hidden': True, 'error' : "Nothing to read"},
        'eat': {'input': 'food', 'hidden': True, 'error' : "Blueurgh! that's not edible"},
        'drink': {'input': 'item', 'hidden': True, 'error' : "Drink what!?! there's only engine fuel here..."},
        'dance': {'input': 'name', 'hidden': True, 'error' : "That's not a dance!!"},
        'fart': {'input': '', 'hidden': True, 'error' : "You can only fart smelly air dude!"},
        'buy': {'input': '', 'hidden': False, 'error' : "You'll need to find a shop before buy anything"},
        'sell': {'input': '', 'hidden': True, 'error' : "No one to sell to aroudn here..."},
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

win = '''
Amazingly you have placed the last crystal
just in time to save planet Earth. Your
mission is successful - Thank you!'''

pack_max = 6


#destinations
destinations = {
        1: {
        'name': 'Sector 9',
        'voyages': {'north': 3, 'south': 4},
        'scenario': '''You check your handy navigator, 
from here you can fly to the South, where you'll find planet Sapsa 
and it's not far or fly North to Yanus.
It occurs to you that both planets could have the crystals you
so desperately need but that you also risk bumping into trouble...''',
        'colour': 125 
    },
        2: {
        'name': 'Taiga planet',
        'voyages': {'north': 3, 'west': 5, 'south': 4},
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
        'scenario': '''You land with a bump on an empty piece of land - there's a twilight glow
to the sky and the air is dry. Stepping out of the spaceship, the ground 
is rocky, almost crunching under foot.''',
        'colour': 214
    },
        4: {
        'name': 'Sapsa planet',
        'voyages': {'east': 2, 'north': 3, 'west': 5},
        'scenario': '''You pull off a super smooth landing in a clearing and 
run towards what looks like vegetation - travelling around the solar system 
has made you hungry.''',
        'colour': 226
    },
        5: { 
        'name': 'Earth',
        'voyages': {'north': 3, 'south': 4, 'east': 2},
        'scenario': '''You've arrived on Earth, memories flood back, the summer breeze, the trees, 
the ocean but enough of this nostalgia where is the Portal?''',
        'colour': 21
    }
}

#game zones
zones = {
        1: {
        'name': 'Forest',
        'scenario': '''A copse of tall rigid trees zig zagged across the hill. 
Their silky green leaves drift down from their spikey branches onto the 
damp forest floor.'''
        },
        2: {
        'name': 'Graveyard',
        'scenario': '''Uneven rows of massive tombs stretch into the distance.
There is a path weaving through the graves of a thousand dead bodies...
But it is overgrown and riddled with potholes. Night or day this 
place has an atmosphere - dark, always dark.'''
        },
        3: {
        'name': 'Town of nothing',
        'scenario': '''Destroyed and hollow, rows of abandoned homes 
lay quiet and eerie. Roads weave through the buildings and debris, 
in the distance you can make out hundreds if not thousand of candles 
flickering in the ancient ruins, maybe despite the deserted appearance 
there is life...'''
        },
        4: {
        'name': 'Lost lake',
        'scenario': '''The cold clear water shimmers like molten glass 
on the surface of the forgotten lake. The marshy banks surrounding the dark
lake is covered in a glowing green moss - you've seen this vegetation before 
and recall it to be the home to poisonous balck and red beatles. Where they live
nothing else does...'''
        },
        5: {
        'name': 'Rainbow falls',
        'scenario': '''A flowing torrent of candy colours descends from 
the sky, crashing into the rock pools hundreds of feet below. A multi-coloured 
mist that's warm and tingly stops you fomr seeing much but despite this 
it's somehow magical'''
        },
        6: {
        'name': 'Alien Corp',
        'scenario': '''Three sky scrapers, all glass and carbon fibre 
tower climb high into the nights sky. Each with a matrix of illumination - 
they look like alien spaceships just landed 
- a bright neon sign reads "ALIEN CORP PLC"'''
        },
        7: {
        'name': 'Stone statue',
        'scenario': '''The sand is whipping up off the dessert floor, 
partly hiding the giant stone statue in front of you. It must be at least 
20 feet tall. It looks like a fierce warrior going into battle - it's 
wielding an emormous sharp scord above it's head. The statue looks like 
granite but it has a fur coat of moss'''
        },
        8: {
        'name': 'Rocky mountain',
        'scenario': '''The kilometer high peak looks over many towns, 
the spectacular views attracts thousands of visitors from all over the 
Galagamatic Universe. It takes a lot of effort to climb this high above 
the clouds and there isn't much in the way of buildings when you reach 
the summit, just rocks and the occasional lookout post.'''
        },
        9: {
        'name': 'Crazy camp',
        'scenario': '''This is weirdest alien retreat camp you've seen. 
The stripy tents are full of the Universe's most wildiest warriors, 
drinking, eating messily and brawling. It's total chaos and very noisey 
so fairly easy to keep a low profile aorund here...'''
        },
        10: {
        'name': 'Market place',
        'scenario': '''A shop standing on its own in what appears to be 
the middle of nowhere. Inside there are endless aisles of random things 
- pretty much everything from food to weapons to playing cards. You'll be 
able to buy pretty much anything here - for sure you'''
        },
        11: {
        'name': 'Cranky cave',
        'scenario': '''The mysterious dark openning leads to an orange 
chamber full of stalactites and stalagmites. There is a hole in the roof 
of the cave providing the only light - luminescent light like an underwater 
world. You can see a giant rock blocking the exit from the cave.'''
        },
        12: {
        'name': 'Square',
        'scenario': '''A bustling lively place - more activity than you've seen for a while.
There are market stalls and people seeling street food - 
the smell is making you hungry. It is easy to get lost in the crowd...
and it would be easy to hide important things here!
'''
        },
        13: {
        'name': 'Forbidden desert',
        'scenario': '''This is avast arid area - srtretching furhter than a thousand days of travelling,
it's a hostile place with deep crators that remind you of a 
planet you once visited. The sand whips up in you face 
making it hard to see'''
        },
        14: {
        'name': 'Frosty plains',
        'scenario': '''Bright white everywhere and a fierce blinding light 
relecting off the ice - it takes a proper explorer to make it through 
the Frosty plains -  suriving any amount of time here is super tough 
so it better be worth your while!!'''
        },
        15: {
        'name': 'Control tower',
        'scenario': '''An architectural wonder - it travels up up up up into the sky, 
a gloriously oval concrete column crowned with a spacehsip like control centre. 
The better be a lift as there's not a hope in hell of climbing to the top. You can just 
about make out small space shuttles coming and going from what must be a 
landing pad near the top.'''
        },
        16: {
        'name': 'Dino jungle',
        'scenario': '''Is that a leg or a tree moving ahead of you, as your eys scan up you see 
it's the leg of an enormous dinosaur of the likes you don't recognise 
from the picture books. The jungle is dense and steamy and there are loud exotic sounds 
coming from the tree tops. This is an exicing and dangerous place you find yourself, you will
need to keep a low profile...'''
        },
        17: {
        'name': 'Battle bridge',
        'scenario': '''Standing at the edge of the ravine - in front of you is a wire bridge 
creating a fragile border territory between the two enemy districts. Looking far down the 
vertical rock face you can see there is no option but to cross the bridge, you might want to 
close your eyes!!'''
        },
        18: {
        'name': 'Smelly swamp',
        'scenario': '''Nothing can prepare you for the stench - the smell of a thoudands 
eggy farts fills your nostrills. You navigator tells you this is a swamp but it looks 
deceptively firm under foot so beware. The plants that are able to grow in this smelly
atmosphere ar elike none you have ever seen, vidid colours, ouzing slimey sap.
It could have magce healing properties, then again it could just as easily 
be deadly poison...'''
        },
        19: {
        'name': 'The crossroads',
        'scenario': '''A neat sign reads North, South, East and West - pointing off
down each of the four dusty roads. There are vehicle tracks crossing paths, this crossroads
feels strangely familiar despite having never been here before - which way next...?*!?'''
        },
        20: {
        'name': 'Portal',
        'scenario': '''You have reached the portal - the end of your mission is in sight.
The chamber of crystals is backlight with a throbing glow. You must place each one
carefully and pray to the Galagamatic gods that you're not too late...''',
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
        "name": "Gabaloni",
        "species": "Dankans",
        "appearance": '''
big green slimey hairy lizzard with a long spikey tail. They're really 
strong and fierce fighters.
        ''',
        "art": ''' ''',
        "weakness": "stupidity",
        "status": "dangerous",
        "strength": 6,
        "health": 3,
        "msg": {"encounter": '''A tall shadow moves quickly across the floor and before you know it 
- you are face to face with a mean looking monster!''', "fight": '''
Are you ready for serious brawl, he screams "I will play with you, then smash you into a pulp!*!*!"''', "lose": '''
It's hard to imagine something so strong falling like this - 
seeing is believing - all the life drains from him and his tail 
becomes flappy and shrivelled like a salt soaked slug.''', "win": '''He stands over your dead body - tail swiping from left to right, 
erasing any memory of your failed heroics'''} 
    },
    2 : {
        "name": "Pancini",
        "species": "Scepti",
        "appearance": '''
small and fast with a cunning smile. They carry daggers in each hand. 
Be careful as these guys are super intelligent.
        ''',
        "art": '''''',
        "weakness": "greed",
        "status": "dangerous",
        "strength": 5,
        "health": 3,
        "msg": {"encounter": '''Something darts about in the corner of your vision, then speeds past you, 
too fast to make out. Then whatever it is calls out - "I'll fight you for 
the crystal"''', "fight": '''Are you ready for serious brawl, he screams "I will play with you, 
then smash you into a pulp!*!*!"''', "lose": '''
And just as quickly as he appeared - pooofff - 
his body evaporates in a puff of smoke''', "win": '''Grinning, he wipes his blades clean of your blood 
- not the easiest battle but a win none the less!'''} 
    },
    3 : {
        "name": "Dilly",
        "species": "Labadu",
        "appearance": '''
two and half feet high with delicate features, pointy ears and pink hair. 
You know them to be loyal and really chatty.
        ''',
        "art": '',
        "weakness": "clumsy",
        "status": "friendly",
        "strength": 2,
        "health": 2,
        "msg": {"encounter": '''There's a russle behind you, sounds like someone tripping over and then you 
get a tap on the shoulder - turning round you see it and smile.''', "fight": '''"I'm friendly folk - I really don;t want to fight with you..."''', "lose": '''
It's hard to imagine something so strong falling like this - 
seeing is believing - all the life drains from him and his tail 
becomes flappy and shrivelled like a salt soaked slug.''', "win": '''He stands over your dead body - tail swiping from left to right, erasing any memory of your failed heroics'''}
    },
    4 : {
        "name": "Sapdeez",
        "species": "Calltee",
        "appearance": '''
heavy build with wings and a beak. It has armoured scales and they like to 
destroy everything in their path.
        ''',
        "art": '''''',            
        "weakness": "slow",
        "status": "dangerous",
        "strength": 5,
        "health": 2,
        "msg": {"encounter": '''Loud swooshing and squarking screaches in your ears 
and you dive for shelter, it swoops over your head once more before landing 
four feet away and you get a proper look.''', "fight": '''Are you ready for serious brawl, he screams "I will play with you, then smash you into a pulp!*!*!"''', "lose": '''
How you beat this guy is a bit of a mystery - but now it lies fallen in front of you - 
you start to breath more normally, relieved and greatful it isn't you lying dead on the floor.''', "win": '''Flappy his wings he sores up into the sky - he's left your body for the night demons...'''}
    },
    5 : {
        "name": "Lord Devilhanger",
        "species": "Galati",
        "appearance": '''
deathly pale, 8 feet tall human like creature. He carries a blunderbuss riffle on his back 
and shoots anything that gets in his way.
        ''',
        "art": '''''',               
        "weakness": "vanity",
        "status": "boss",
        "strength": 8,
        "health": 5,
        "msg": {"encounter": '''As you feared the mission is not quite in the bag - 
standing between you and the portal is the fiercest of the foes that you have faced so far...''', "fight": '''The earth shakes beneath your feet as 
he thunder towards you...you know you don't have a choice but to stay and fight
- lets hope you survive this one''', "lose": '''
in a swirl of dust and debris, Lord D starts to disintegrate - 
his flesh turning into black particals and spinning into 
the vortex of pure darkness that's opended up in front of you. 
You did it - the ultimate evil one has been vanquished''', "win": '''You came so close but he has done his job and done away with
you like you were a piece of muck on his shoe. He kicks your dead body into orbit
and walks away...planet Earth is now doomed'''}
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
        "fuel_tank": 40,
        "fuel_usage": 17,
        "weapon": "Lazers",
        "msg": {"go": '''You stroll up to your spaceship, with a push of a button 
you open the hatch, then you climb aboard and fire up the engines - 
you're ready to fly out into the Galagamatic Universe...

Might be worth having a look at your navigator 
to see where to go next!''', 
"look": '''You can see it neatly parked just behind you, it's all fueled up 
and ready to go - whenever you are...'''
        }
    },
}

#shop
shop = {
        0: {
        "name": "Shop",    
        "description": '''Basic looking counter with a local standing behind it 
waiting to take your credits...''',
        "msg": {"go": '''You go up to the counter and start a conversation with the shop keeper...''', "look": '''You can see that there is a small shop - 
have you got anything you need to buy...or maybe even sell''', "buy": '''Great to do business with you'''},
        "products": {
                1: {
                "name": "fuel",
                "credits": 12
                },
                2: {
                "name": "food",
                "credits": 10
                },
                3: {
                "name": "water",
                "credits": 2
                }
        }
        }
        }

#objects
objects = {
    1: {
        "name": "computer console",
        "description": "Two meter high navy pillar box with a screen illuminated on one side.",
        "move": {"read"},
        "msg": {"go": '''Standing in front of the screen you can read some info in a language 
you don't understand...''', "look": '''
You see what looks like a telephone boothe...is it doctor who?'''}
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
        "name": "bunker",
        "description": '''It has a tough outer shell - looks bomb proof. There's
a door on one side, its slightly ajar.''',
        "move": {"enter"},
        "msg": {"go": '''The door is open and you can make out a desk
with some files on it...''', "look": '''There in the distance what looks like a bunker...'''
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
        "value": 20,
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
        "value": 15,
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
        "value": 18,
        "player": 3
        }},
        "winning_items": {
    1: {
        "name": "Collapse Crystal",
        "description": '''A very thin, sheet like crystal with shards of shiny black 
material running through the middle.''',
        "msg": {"get": '''Nice work, another precious crystal and 
another step closer to completing your mission''', "look": '''You spot what looks like a stone but something tells 
you it is more than that''', "place": '''Placing the crystal into the slot carefully so as not to damage it - 
as it slots into position the black material at it's centre 
turns to gold!'''},
        "category": "crystal",
        "value": 60
    },
    2: {
        "name": "Build Crystal",
        "description": '''A dense perfect square. Purple and very shiny, 
when you look into this crystal you see your reflection
but wear your eyes would be, there are black holes.''',
        "msg": {"get": '''It's the build crystal, this one creeps you right out but 
you're pleased it's safely in your possession''', "look": '''What's that shiny thing reflecting the light a little way off, 
you can just about see the light bouncing off - deep purple 
- the build crystal is purple...''', "place": '''Holding it in both hands you drop it lightly into place -
it changes colour as it lowers into the portal - 
now a million shade so '''},
        "category": "crystal",
        "value": 50
        
    },
    3: {
        "name": "Unite Crystal",
        "description": '''This is the most beautiful thing you have ever seen.
Radiating warmth and energy, the Unite Crystal has an 
iridescent glow that lights up it's surroundings.''',
        "msg": {"get": '''Wow you barely manage to take your eyes off the crystal as you stow it away safely.
The rumours were right this is the most powerful crystal and you've got it!!''', "look": '''There's glow coming up from somewhere in the undergrowth.
It could be some kind of energy source - its worth a closer look.''', "place": '''Oh precious, it's hard to let go of this one - it has a magnetic beauty,
giving it away is like parting with the hobbit's ring. You close your eyes and thrust it into the portal
- a flash of bright light shoots out and it's sucked out of your 
hands and out of sight forever...'''},
        "category": "crystal",
        "value": 75
    }},
        "keys": {
    1: {
        "name": "key",
        "description": '''It's a Large iron key with a Ruby encrusted bit and a 
ornate looking blade.''',
        "msg": {"get": '''You pocket the skeleton key - this will unlock anything''', "look": '''Is that a key you can see, looks like someone has tried to hide it 
- but failed as there it is bold as brass, right in front of you!'''},
        "category": "key",
        "value": 10
    }},
        "credits": {
    1: {
        "name": "Two Galag-Zags",
        "description": '''Credits to spend if you can find a shop to spend them in...''',
        "msg": {"look": '''Shiny crrrr's - need some of that''', 
        "get": '''Watch the Zags and the Zigs will look after themselves!''', 
        "spend": '''Well its what it was intended for...''' },
        "value": 2
        },
    2: {
        "name": "Ten Galag-Zigs",
        "description": '''Credits to spend if you can find a shop to spend them in...''',
        "msg": {"look": '''what's on the floor, is that some free crrrrr's?''', 
        "get": '''This has got a reassuring weight about it - should buy some tings''', 
        "spend": '''hmmm I hope that was worth it...''' },
        "value": 10
        },
    3: {
        "name": "A Galag-Zig-Zag",
        "description": '''Credits to spend if you can find a shop to spend them in...''',
        "msg": {"look": '''Bling! Looks like some credits kicking around in front of you''', 
        "get": '''CHING CHING - I'm in the CRrrrr's''', 
        "spend": '''Ouch that hurt''' },
        "value": 25
        }    
        },
        "magic": {
    1: {
        "name": "potion",
        "description": '''A small leather flask with clear liquid inside.
Smells like vanilla pods.''',
        "msg": {"get": '''Supplies always come in handy - you wonder if the potion has a kick to it?''', "look": '''There's a bottle - looks too special to be water...''',
"drink": '''With a gulp and a slurp you down the potion.
A few moments later the hallucinations kick in -
you might need to lie down for while...''', "magic": '''But miraculously this potion has hidden powers and your strength increases!!!'''},
        "category": "drink",
        "spell": "",
        "health": 0,
        "strength": 2,
        "value": 12,
    }},
        "food": {
    1: {
        "name": "cake",
        "description": '''That's one big slice of sticky chocolate cake.''',
        "msg": {"get": '''Save this food in case of hunger or the need for a boost!''', "look": '''Your eyes must be decieving you - 
it looks like cake ****chocolate cake!?!****''', "food": '''You gobble it down so quickly it's like it has evapourated - and then
you start to feel bloated, you really need to fart dude
 or you might explode...'''},
        "category": "food",
        "health": -1,
        "value": 2,
    },
    2: {
        "name": "water",
        "description": '''Blue. Cold. Wet. Delicious''',
        "msg": {"get": '''Water seems precious around here - you might get thirsty!''', 
        "look": '''A small bamboo flask holding what looks like water''', 
        "drink": '''You take a couple of big gulps,
it is water and it's as refreshing as you'd hoped it would be...
Your health increase :) '''},
        "category": "drink",
        "health": 0,
        "value": 2,
    },
    3: {
        "name": "bagel",
        "description": '''Looks like a cream cheese bagel, fancy that, your favourite''',
        "msg": {"get": '''Keep this bread in case you need an energy boost!''', 
        "look": '''A brown paper bag is lying on the floor in front of you keeping something 
safe, looks like a food bag of some sort.''', 
        "food": '''You feel lucky to have found your favourite snack out here - you savour
each mouthful - its a good one, chewy with plenty of cream cheese.'''},
        "category": "food",
        "health": 1,
        "value": 10
    },
    4: {
        "name": "energy bar",
        "description": '''Looks like a vegan fruity energy bar''',
        "msg": {"get": '''You've heard of these - even Super Heroes need a boost from time to time.
Could be useful in a fight - The advert says it boosts your health 
and your strength...double whammy!!!''', "look": '''A bar of something has been discarded inches from your feet...
could be a tasty treat''', "food": '''A zing in your mouth lets you know your body has scored some energy - it's pretty tasty too'''},
        "category": "food",     
        "health": 1,
        "strength": 1,  
        "value": 15,
    },
    5: {
        "name": "wild berries",
        "description": '''They look like raspberries - you love fresh berries but what was it that your mum told you about picking 
wild fruit!?!?''',
        "msg": {"get": '''Going to be hard not just to scoff these fruity gems''', 
        "look": '''There are berries hanging off a plant just in front of you...''',
        "food": '''Not bad tasting but they do have really glooopy texture - 
it's made you feel a bit sick...And then you are sick, 
really sick, you lose health and strength :('''},
        "category": "food",             
        "health": -1,
        "strength": -1,
        "value": 5,
    }
}
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