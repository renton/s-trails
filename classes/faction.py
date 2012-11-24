from random import randint,choice
from classes.name_reader import *
import uuid

class Faction():

    FACTION_TYPES ={
        'colonist':[
            'Colonists',
            'Separatists',
            'Fanatics',
            'Exiled',
            'Survivors',
            'Pilgrims',
            'Pioneers',
            'Harvesters',
            'Farmers',
            'Travellers',
            'Merchants',
            'United',
            'Congress',
            'Cult',
        ],
        'miner':[
            'Miners',
            'Engineers',
            'Guild',
            'Masons',
            'Crafters',
            'Terraformers',
            'Grease Monkeys',
            'Union',
            'Astrofarmers',
        ],
        'soldier':[
            'Mercenaries',
            'Soldiers',
            'Crusade',
            'Militants',
            'Force',
            'Marines',
            'Rangers',
            'Brigade',
            'Templars',
            'Grenadiers',
            'Riflemen',
            'Dragoons',
            'Generals',
            'Warriors',
        ],
        'scientist':[
            'Students',
            'Academics',
            'Expedition',
            'Researchers',
            'Scientists',
            'Voyagers',
            'Explorers',
            'Research Group',
            'Sages',
            'Seers',
            'Prophets',
            'Reading Club',
            'Archivists',
            'Futurologists',
        ],
        'pirate':[
            'Bandits',
            'Pirates',
            'Looters',
            'Pillagers',
            'Raiders',
            'Defilers',
            'Warlords',
            'Mauraders',
            'Gang',
        ],
        'convict':[
            'Convicts',
            'Escapees',
            'Lifers',
            'Prisoners',
            'Slaves',
            'Survivors',
        ]}

    def __init__(self,currencies,name_reader):
        self.id = uuid.uuid1()
        self.name_reader = name_reader
        self._init_random_faction(currencies)

    def _init_random_faction(self,currencies):
        self.f_type = choice(Faction.FACTION_TYPES.keys())
        self.name = self._generate_faction_name(self.f_type)
        self.power = randint(0,100)
        self.relations = randint(0,100)
        self.currency = choice(currencies)
        self.exchange_rate = self._generate_random_exchange_rate(currencies)

    def _generate_faction_name(self,f_type):

        word = self.name_reader.get_random_name
        group = choice(Faction.FACTION_TYPES[f_type])
        name = choice([
                        word("m"),
                        word("f"),
                        word("l"),
                        word("adjective")+" "+word("m"),
                        word("adjective")+" "+word("f"),
                        word("adjective")+" "+word("l"),
                        word("m")+" the "+word("adjective"),
                        word("f")+" the "+word("adjective"),
                        word("title")+" "+word("l"),
                        word("m")+" the "+word("animal"),
                        word("f")+" the "+word("animal")])
        patterns = [
            word("noun")+" of the "+word("adjective")+" "+word("noun"),
            word("noun")+" of the "+word("adjective")+" "+group,
            name+"'s "+group,
            name+"'s "+word("adjective")+" "+group,
            name+"'s "+word("animal")+" "+group,
            word("adjective")+" "+word("noun")+" "+group,
            group+" of the "+word("noun"),
            group+" of the "+word("adjective")+" "+word("noun"),
            "The "+word("adjective")+" "+group,
            "The "+word("adjective")+" "+word("noun")+" "+group,
            "The "+word("adjective")+" "+word("animal")+"s",
            word("adjective")+" "+word("noun")+" "+word("animal")+"s",
            name+"'s "+word("animal")+"s",
            name+"'s "+word("adjective")+" "+word("animal")+"s",
            word("adjective")+" "+word("animal")+" "+group,
            word("noun")+" of the "+word("adjective"),
            "The "+word("animal")+" "+group,
            group+" of "+name,
            word("adjective")+" "+group+" of "+name
        ]

        return choice(patterns)

    def _generate_random_exchange_rate(self,currencies):
        rates = {}

        for currency in currencies:
            if currency == self.currency:
                rates[currency] = 1.0
            else:
                rates[currency] = float(float(randint(40,100))/float(100))
        return rates
