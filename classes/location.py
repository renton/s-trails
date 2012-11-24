from random import choice, randint
from classes.items import *

#TODO system relations between factions
#TODO hidden info - based on spying/scanning/intel
#TODO unexplored location

class Location():

    def __init__(self):
        self.explored = False
        self.name = "Base Location"

class PlanetLocation(Location):
    
    FACTION_OWNER_PROBABILITY = 20

    def __init__(self,factions):
        self.type = "planet"
        Location.__init__(self)
        self.name = "Planet "+str(randint(100,999))

        if randint(0,100) <= PlanetLocation.FACTION_OWNER_PROBABILITY:
            faction = choice(factions)
        else:
            faction = None

        self._gen_planet()

    def _gen_planet(self):
        pass

class SocialLocation(Location):
    
    MIN_POPULATION_SIZE = 10
    POPULATION_MULTIPLIER = 100

    MAX_DEMAND_ITEMS = 4
    MAX_SURPLUS_ITEMS = 4

    def __init__(self,faction):
        self.faction = faction
        Location.__init__(self)
        self._gen_social_location()

    def _gen_social_location(self):

        #TYPES
        #scientists - rarer items, high int humans
        #warriors - strong military
        #pirates - strong military, bad swindle rates, easy to piss off
        #colonists - good trading
        #prisoners
        #miner - trade mineral types

        self.population = randint(SocialLocation.MIN_POPULATION_SIZE,SocialLocation.MIN_POPULATION_SIZE+(self.faction.power*SocialLocation.POPULATION_MULTIPLIER))
        self.air_hanger = {}
        self.external_components = {} #ground to air missiles etc. (components have type/quality/struct hp, plus methods to use)
        self.trade_swindle_factor = randint(0,30) #deviation from base prices of items, pirate type higher
        self.trade_inventory = {} #items to buy/sell
        self.personal_inventory = {} #items only obtained by pillaging/assualting

        self._gen_random_demand_items([])
        self._gen_random_surplus_items(self.demand_items.keys())

        self.will_trade = True #based on relations
        self.is_hostile = False #based on relations

        #this should be based off faction type, power and population size
        self.military_size = randint(0,self.population)

    def _gen_random_demand_items(self,not_in_list):
        self.demand_items = {}

        # num items
        num_items = randint(0,SocialLocation.MAX_DEMAND_ITEMS)

        item_set = set()
        for i in range(num_items):
            item = choice(ITEM.keys())
            if item not in not_in_list:
                item_set.add(item)

        for item in item_set:
            self.demand_items[item] = True #TODO this should be a value factor on price

    def _gen_random_surplus_items(self,not_in_list):
        self.surplus_items = {}

        # num items
        num_items = randint(0,SocialLocation.MAX_DEMAND_ITEMS)

        item_set = set()
        for i in range(num_items):
            item = choice(ITEM.keys())
            if item not in not_in_list:
                item_set.add(item)

        for item in item_set:
            self.surplus_items[item] = True #TODO this should be a value factor on price

    def _gen_random_inventories(self):
        #TODO make sure they have surplus items, and no demand items
        pass

class FleetLocation(SocialLocation):
    def __init__(self,factions):
        self.type = "fleet"
        SocialLocation.__init__(self,choice(factions))
        self.name = "Fleet "+str(randint(100,999))
        self._gen_fleet()

    def _gen_fleet(self):
        pass

class StationLocation(SocialLocation):
    def __init__(self,factions):
        self.type = "station"
        SocialLocation.__init__(self,choice(factions))
        self.name = "Station "+str(randint(100,999))
        self._gen_station()

    def _gen_station(self):
        self.vehicle_hanger = {}
