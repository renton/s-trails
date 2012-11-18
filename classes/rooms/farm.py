from classes.ship_entity import *
from random import randint

class Room_Farm(ShipRoom):

    INIT_AVG_DAYS_TILL_HARVEST = 10
    INIT_AVG_YIELD_AMOUNT = 100
    INIT_ITEM_YIELD_TYPES = ['grain','fruit+veg','protein']
    INIT_DEFAULT_ITEM = 'grain'

    INIT_DEFAULT_PLANT_REQ_ITEMS = {
        "water":1,
        "growth cells":2,
        "farming supplies":1,
        "farming tools":1
    }

    INIT_DEFAULT_STEP_REQ_ITEMS = {
        "water":1
    }

    INIT_DEFAULT_HARVEST_REQ_ITEMS = {
        "water":1,
        "farming supplies":2,
        "farming tools":1
    }

    #TODO % chance of losing some items

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.name = "Farm "+str(randint(0,9999))+"-"+str(randint(0,99))
        self.type = "farm"
        self.item_type = Room_Farm.INIT_DEFAULT_ITEM
        self.days_till_harvest = 0
        self.ready_to_plant = True
        self.yield_amount = Room_Farm.INIT_AVG_YIELD_AMOUNT

        self.manager_label = "Farm Manager"
        #TODO - if human stats change, make sure still capable of job - in human loop?
        self.jobs = {
            
            "Farm Manager": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "str":20,
                    "eth":60,
                    "agi":20,
                    "int":30,
                    "cha":50
                },
                "req_awards":[]
            },
            "Farm Labourer": {
                "employees":{},
                "max_employees":10,
                "desired_stats":["str","agi"],
                "min_stats":{
                    "str":10,
                    "agi":10,
                },
                "req_awards":[]
            },
            "Machine Operator": {
                "employees":{},
                "max_employees":5,
                "desired_stats":["str","agi"],
                "min_stats":{
                    "str":10,
                    "agi":10,
                },
                "req_awards":[]
            },
        }

    def _calc_days_till_harvest(self):
        #TODO - yield based on employees
        #TODO - time based on employees
        #TODO - cannot start without enough employees
        #TODO - items dont remove or have a % of removing

        unmet_criteria = self.ship.get_unmet_criteria(Room_Farm.INIT_DEFAULT_PLANT_REQ_ITEMS)

        if unmet_criteria:
            self.ship._add_log(2,"Cannot process farm. Requirments not met: "+str(unmet_criteria))
            return False
        else:
            self.ship.remove_items(Room_Farm.INIT_DEFAULT_PLANT_REQ_ITEMS)
            self.ship._add_log(1,str(self.item_type)+" farm planted.")
            self.days_till_harvest = Room_Farm.INIT_AVG_DAYS_TILL_HARVEST
            self.ready_to_plant = False

    def daily_step(self,ship):
        if self.ready_to_plant == True:
            self._calc_days_till_harvest()
        else:
            if self.days_till_harvest <= 0:
                self._harvest()
            else:
                #TODO - small bonus for employees - % to increase yield
                unmet_criteria = self.ship.get_unmet_criteria(Room_Farm.INIT_DEFAULT_STEP_REQ_ITEMS)

                if unmet_criteria:
                    self.ship._add_log(2,"Cannot grow farm. Requirments not met: "+str(unmet_criteria))
                    return False
                else:
                    self.ship.remove_items(Room_Farm.INIT_DEFAULT_STEP_REQ_ITEMS)
                    self.days_till_harvest -=1
    
    def _harvest(self):

        # % chance at affecting yield
        #TODO - yield based on employees
        #TODO - cannot start without employees
        unmet_criteria = self.ship.get_unmet_criteria(Room_Farm.INIT_DEFAULT_HARVEST_REQ_ITEMS) 

        if unmet_criteria:
            self.ship._add_warning(2,"Cannot harvest. Requirements not met: "+str(unmet_criteria))
            return False
        else:
            self.ship.remove_items(Room_Farm.INIT_DEFAULT_HARVEST_REQ_ITEMS)
            self.ship._add_log(1,"harvest time")
            self.ship.add_items({self.item_type:self.yield_amount})
            self.ready_to_plant = True
