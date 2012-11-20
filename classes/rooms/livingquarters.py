from classes.ship_entity import *
from random import randint

class Room_LivingQuarters(ShipLivableRoom):

    INIT_CAPACITY = 100

    def __init__(self,ship):
        ShipLivableRoom.__init__(self,ship)
        self.type = "living_quarters"
        self.name = str(ship.name_reader.get_random_name("lq"))+"-"+str(randint(0,999))
        self.capacity = Room_LivingQuarters.INIT_CAPACITY

        self.manager_label = "Superindendent"
        self.jobs = {
            
            "Superindendent": {
                "employees":{},
                "max_employees":1,
                "desired_stats":[],
                "min_stats":{
                    "eth":20,
                    "int":20,
                    "cha":20
                },
                "req_awards":[]
            },
            "Handyman": {
                "employees":{},
                "max_employees":5,
                "desired_stats":[],
                "min_stats":{
                    "int":10,
                    "eth":10,
                },
                "req_awards":[]
            },
            "Custodian": {
                "employees":{},
                "max_employees":5,
                "desired_stats":[],
                "min_stats":{
                    "eth":10,
                },
                "req_awards":[]
            },
        }

    def daily_step(self):
        ShipLivableRoom.daily_step(self)
