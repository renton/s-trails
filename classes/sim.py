from ship import *

class Sim:

    INIT_STARTING_YEAR = 5029
    INIT_STARTING_DAY = 1
    INIT_DAYS_IN_YEAR = 365

    def __init__(self):
        self.ship = Ship()
        self.year = Sim.INIT_STARTING_YEAR
        self.day = Sim.INIT_STARTING_DAY
        self.days_elapsed = 0

    def step_day(self):
        print "\n----------------- "+str(self.day)+" "+str(self.year)+" -------------------"
        
        self.ship.daily_step()

        if self.day >= Sim.INIT_DAYS_IN_YEAR:
            self.year += 1
            self.day = 1
        else:
            self.day += 1
        self.days_elapsed += 1

    def main_loop(self):
        while(1):
            self.step_day()
            break
