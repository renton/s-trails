from ship import *
from name_reader import *

class Sim:

    INIT_STARTING_YEAR = 5029
    INIT_STARTING_DAY = 1
    INIT_DAYS_IN_YEAR = 365
    INIT_NUM_FACTIONS = 200

    def __init__(self):
        self.name_reader = NameReader()
        self.ship = Ship(self.name_reader)
        self.year = Sim.INIT_STARTING_YEAR
        self.day = Sim.INIT_STARTING_DAY
        self.days_elapsed = 0

        self.faction_types={
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
                'Survivors'
            ],
        }
        
        self.factions = self._generate_random_factions()

    def step_day(self):
        print "\n----------------- "+str(self.day)+" "+str(self.year)+" -------------------"
        
        self.ship.daily_step(self.day)

        if self.day >= Sim.INIT_DAYS_IN_YEAR:
            self.year += 1
            self.day = 1
        else:
            self.day += 1
        self.days_elapsed += 1

    def main_loop(self):
        while(1):
            #self.step_day()
            for faction in self.factions:
                print faction['name']
            break

    def _generate_random_factions(self):

        #promise,pact,star,hammer
        #east,west,upper,lower,first,second
        # the optional
        # <noun> of the <adj> <group>
        # <adj><noun> of the <noun>
        # <adj> <noun> <group>
        # <adj> <noun> of the <adj> <group>
        # <adj> <group> <noun>
        # <person>s <adj> <group>
        # <adj> <person>s <group>
        # <person>s <group>
        # <title> <person>s <group>
        # <noun> of the <adj> <noun>
        # <> of the <> <>
        factions=[]

        for i in range(Sim.INIT_NUM_FACTIONS):
            f_type = choice(self.faction_types.keys())
            factions.append({
                "name":self._generate_faction_name(f_type),
                "power":randint(1,5),
                "type":f_type})
        return factions

    def _generate_faction_name(self,f_type):

        word = self.name_reader.get_random_name
        group = choice(self.faction_types[f_type])
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
