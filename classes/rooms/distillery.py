from classes.ship_entity import *
from random import randint

class Room_Distillery(ShipRoom):

    INIT_AVG_DAYS_TILL_BREWED = 20
    INIT_AVG_YIELD_AMOUNT = 100
    INIT_ITEM_YIELD_TYPES = ['alcohol']
    INIT_DEFAULT_ITEM = 'alcohol'

    INIT_DEFAULT_BREW_REQ_ITEMS = {
        "water":1,
        "grain":2,
       

    }

    INIT_DEFAULT_STEP_REQ_ITEMS = {
         "fuel":1
    }

    INIT_DEFAULT_BREWED_REQ_ITEMS = {

    }

    #TODO % chance of losing some items

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.name = str(self.ship.name_reader.get_random_name('l')) + "'s Brewery"
        self.type = "distillery"
        self.item_type = Room_Distillery.INIT_DEFAULT_ITEM
        self.days_till_brewed = 0
        self.ready_to_brew = True
        self.yield_amount = Room_Distillery.INIT_AVG_YIELD_AMOUNT

        self.manager_label = "Distillery Manager"
        #TODO - if human stats change, make sure still capable of job - in human loop?
        self.jobs = {
            
            "Distillery Manager": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "str":10,
                    "eth":60,
                    "agi":10,
                    "int":40,
                    "cha":40
                },
                "req_awards":[]
            },
            "Distillery Labourer": {
                "employees":{},
                "max_employees":15,
                "desired_stats":["str","agi"],
                "min_stats":{
                    "str":10,
                    "agi":10,
                },
                "req_awards":[]
            },

        }

    def _brew_distillery(self):
        #TODO - yield based on employees
        #TODO - time based on employees
        #TODO - cannot start without enough employees
        #TODO - items dont remove or have a % of removing

        if not self.has_manager():
            self.ship._add_log(2,str(self.name)+" needs manager to process distillery.")
            return False

        unmet_criteria = self.ship.get_unmet_criteria(Room_Distillery.INIT_DEFAULT_BREW_REQ_ITEMS)

        if unmet_criteria:
            self.ship._add_log(2,"Cannot process distillery. Requirments not met: "+str(unmet_criteria))
            return False
        else:
            self.ship.remove_items(Room_Distillery.INIT_DEFAULT_BREW_REQ_ITEMS)
            self.ship._add_log(1,str(self.item_type)+" distillery set.")
            self.days_till_brewed = self._calc_days_till_brewed()
            self.ready_to_plant = False

    def daily_step(self,ship):
        self.get_average_employee_stats()
        if self.ready_to_brew == True:
            self._brew_distillery()
        else:
            if self.days_till_brewed <= 0:
                self._package()
            else:
                #TODO - small bonus for employees - % to increase yield
                unmet_criteria = self.ship.get_unmet_criteria(Room_Distillery.INIT_DEFAULT_STEP_REQ_ITEMS)

                if unmet_criteria:
                    self.ship._add_log(2,"Cannot brew at distillery. Requirments not met: "+str(unmet_criteria))
                    return False
                else:
                    self.ship.remove_items(Room_Distillery.INIT_DEFAULT_STEP_REQ_ITEMS)
                    self.days_till_brewed -=1
    
    def _package(self):

        if not self.has_manager():
            self.ship._add_log(2,str(self.name)+" needs manager to package at distillery")
            return False

        # % chance at affecting yield
        #TODO - yield based on employees
        #TODO - cannot start without employees
        unmet_criteria = self.ship.get_unmet_criteria(Room_Distillery.INIT_DEFAULT_BREWED_REQ_ITEMS) 

        if unmet_criteria:
            self.ship._add_warning(2,"Cannot package. Requirements not met: "+str(unmet_criteria))
            return False
        else:
            self.ship.remove_items(Room_Distillery.INIT_DEFAULT_BREWED_REQ_ITEMS)
            self.ship._add_log(1,"packaging time")
            self.ship.add_items({self.item_type:self.yield_amount})
            self.ready_to_brew = True

    def _calc_days_till_brewed(self):

        stats = self.get_average_employee_stats()
        days = Room_Distillery.INIT_AVG_DAYS_TILL_BREWED
        days -= stats['eth']['tot'] / 200
        days -= stats['str']['tot'] / 300
        days -= stats['agi']['tot'] / 300
        days -= (stats['eth']['avg'] / 10)*2
        return days
