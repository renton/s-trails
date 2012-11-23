from classes.ship_entity import *
from random import randint

class Room_Bar(ShipRoom):

    INIT_DEFAULT_ITEM = 'alcohol' #Well being? people with higher 'cha' get bigger affect (more social)

    INIT_DEFAULT_SERVICE_REQUIREMENTS = {
        "alcohol":50
        
    }

    #TODO % chance of losing some items

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        #TODO - Better randomization of Bar names
        self.name = "(Bar) "+str(self.ship.name_reader.get_random_name('verb'))+" "+str(self.ship.name_reader.get_random_name('animal'))
        self.type = "bar"
        self.item_type = Room_Bar.INIT_DEFAULT_ITEM
        self.open_for_business = True

        self.manager_label = "Bar Owner"
        #TODO - if human stats change, make sure still capable of job - in human loop?
        self.jobs = {
            
            "Bar Owner": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "str":30,
                    "eth":60,
                    "agi":20,
                    "int":20,
                    "cha":60
                },
                "req_awards":[]
            },
            "Bartender": {
                "employees":{},
                "max_employees":4,
                "desired_stats":["cha","agi"],
                "min_stats":{
                    "cha":20,
                    "agi":10,
                },
                "req_awards":[]
            },
            "Security": {
                "employees":{},
                "max_employees":2,
                "desired_stats":["str","agi"],
                "min_stats":{
                    "str":20,
                    "agi":10,
                },
                "req_awards":[]
            },
        }

    #TODO - Bar Service, effects % of human well being
    def _bar_service(self):
        pass
    
    def step_daily(self):
        self.get_average_employee_stats()
        if self.open_for_business == True:
             self._bar_service()

        else:
            
            unmet_criteria = self.ship.get_unmet_criteria(Room_Bar.INIT_DEFAULT_SERVICE_REQUIREMENTS)

            if unmet_criteria:
                self.ship._add_log(Ship.LOG_TYPE_ROOMS,Ship.LOG_LEVEL_HIGH,"Bar cannot open. Requirments not met: "+str(unmet_criteria))
                return False
            else:
                self.ship.remove_items(Room_Bar.INIT_DEFAULT_SERVICE_REQUIREMENTS)
        ShipRoom.step_daily(self)
