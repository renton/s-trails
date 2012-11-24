from ship import *
from name_reader import *
from faction import *
from location import *
from event import *

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
        self.cur_events = []

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

            for i in range(Sim.MAX_FACTIONS_PER_SYSTEM):
                faction = choice(self.factions.values())
                self.system_factions[faction.id] = faction

            #generate x num locations based off current density
            num_location_calc = (self.cur_density/(100/Sim.MAX_LOCATIONS))
            if num_location_calc < 1:
                num_location_calc = 1

            for i in range(randint(1,num_location_calc)):
                self.cur_locations.append(choice(Sim.LOCATION_TYPES)(self.system_factions.values()))

    def _gen_events(self):
        self.cur_events = []

        if self.days_elapsed > 0 and self.day == 1:
            self.cur_events.append(Event("The colony celebrates the New Year!"))

        if randint(0,40) == 0:
            self.cur_events.append(Event("RANDOMNESS!"))

        if self.ship.get_total_items("water")[0] <= 0:
            self.cur_events.append(Event("The colony is dying of thirst."))

        if self.ship.get_total_items("grain")[0] <= 0 and self.ship.get_total_items("protein")[0] <= 0 and self.ship.get_total_items("fruit+veg")[0] <= 0:
            self.cur_events.append(Event("The colony is dying of hunger."))

        if len(self.ship.humans) <= 0:
            self.cur_events.append(Event("The colony has vanquished. Game Over."))

    def step_day(self):

        print "\n----------------- "+str(self.day)+" "+str(self.year)+" -------------------"

        if self.days_in_cur_density >= Sim.INIT_DAYS_IN_DENSITY_ZONE:
            self._gen_new_density()

        if self.day >= Sim.INIT_DAYS_IN_YEAR:
            self.year += 1
            self.day = 1
        else:
            self.day += 1

        self.days_elapsed += 1
        self.days_in_cur_density += 1

        self.ship.daily_step(self.day)

        #LOCATIONS
        self._gen_locations()

        #EVENTS
        self._gen_events()

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
