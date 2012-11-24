from ship import *
from name_reader import *
from faction import *
from location import *

#TODO - settings file with constants

class Sim:

    INIT_STARTING_YEAR = 5029
    INIT_STARTING_DAY = 1
    INIT_DAYS_IN_YEAR = 365
    INIT_NUM_FACTIONS = 20
    INIT_NUM_CURRENCIES = 3
    INIT_DAYS_IN_DENSITY_ZONE = 20
    DENSITY_DIVISION_ROLL_CONSTANT = 4

    #TODO % and max in area
    #LOCATION_TYPES = [PlanetLocation, FleetLocation, StationLocation]
    LOCATION_TYPES = [StationLocation]
    MAX_LOCATIONS = 6
    MAX_FACTIONS_PER_SYSTEM = 3

    def __init__(self):
        self.name_reader = NameReader()
        self.ship = Ship(self.name_reader)
        self.year = Sim.INIT_STARTING_YEAR
        self.day = Sim.INIT_STARTING_DAY
        self.days_elapsed = 0
        self.days_in_cur_density = 0
        self._gen_new_density()
        self.currencies = self._generate_random_currencies()
        self.factions = self._generate_random_factions()
        self.cur_locations = []

    def _gen_new_density(self):
        self.days_in_cur_density = 0
        self.cur_density = randint(10,100)
        #self.cur_density = 100

    #TODO use density
    def _gen_locations(self):
        self.cur_locations = []
        self.system_factions = {}

        #roll for empty locations or system with locations
        if randint(0,100) <= (self.cur_density/Sim.DENSITY_DIVISION_ROLL_CONSTANT):

            print self.cur_density

            #TODO this logic isnt great... be cool for there to at least be prob. of more factions in low density area
            num_faction_calc = (self.cur_density/(100/Sim.MAX_FACTIONS_PER_SYSTEM))
            if num_faction_calc < 1:
                num_faction_calc = 1

            #num factions operating in this location TODO use this
            num_factions = randint(1,num_faction_calc)

            self.system_factions = {}
            for i in range(num_factions):
                faction = choice(self.factions.values())
                self.system_factions[faction.id] = faction

            print len(self.system_factions)

            #generate x num locations based off current density
            num_location_calc = (self.cur_density/(100/Sim.MAX_LOCATIONS))
            if num_location_calc < 1:
                num_location_calc = 1

            for i in range(randint(1,num_location_calc)):
                self.cur_locations.append(choice(Sim.LOCATION_TYPES)(self.system_factions.values()))

    def step_day(self):

        print "\n----------------- "+str(self.day)+" "+str(self.year)+" -------------------"

        if self.days_in_cur_density >= Sim.INIT_DAYS_IN_DENSITY_ZONE:
            self._gen_new_density()

        #LOCATIONS
        self._gen_locations()

        print self.cur_locations
        #EVENTS
        
        self.ship.daily_step(self.day)

        if self.day >= Sim.INIT_DAYS_IN_YEAR:
            self.year += 1
            self.day = 1
        else:
            self.day += 1
        self.days_elapsed += 1
        self.days_in_cur_density += 1

    def _generate_random_factions(self):
        factions={}
        for i in range(Sim.INIT_NUM_FACTIONS):
            new_faction = Faction(self.currencies,self.name_reader)
            factions[new_faction.id] = new_faction
        return factions

    def _generate_random_currencies(self):
        currencies=[]
        for i in range(Sim.INIT_NUM_CURRENCIES):
            currencies.append(str(randint(100,999)))
        return currencies
