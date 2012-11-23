from classes.ship_entity import *
from random import randint,choice

class Room_Prison(ShipLivableRoom):

    INIT_CAPACITY = 100
    INIT_NAME_VARIETY = ['Correctional Facility','Detention Center','Prison']

    def __init__(self,ship):
        ShipLivableRoom.__init__(self,ship)
        self.type = "prison"
        self.name = str(ship.name_reader.get_random_name("l"))+" "+str(choice(Room_Prison.INIT_NAME_VARIETY))
        self.capacity = Room_Prison.INIT_CAPACITY

        self.manager_label = "Prison Warden"
        self.jobs = {
            
            "Prison Warden": {
                "employees":{},
                "max_employees":1,
                "desired_stats":[],
                "min_stats":{
                    "emp":10,
		    "str":20,
                    "int":40,
                    "cha":40,
                },
                "req_awards":[]
            },
            "Prison Guard": {
                "employees":{},
                "max_employees":15,
                "desired_stats":[],
                "min_stats":{
                    "agi":10,
                    "cha":10,
                    "str":40,
                    "eth":10,
                },
                "req_awards":[]
            },
            "Prison Medical Staff": {
                "employees":{},
                "max_employees":5,
                "desired_stats":[],
                "min_stats":{
                    "int":50,
                    "agi":20,
                    "emp":10,
                    "cha":20,
                    "eth":10,
                },
                "req_awards":[]
            },
   
          
        }

    def daily_step(self):
        ShipLivableRoom.daily_step(self)
