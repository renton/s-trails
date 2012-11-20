from classes.ship_entity import *
from random import randint,choice

class Room_Hospital(ShipLivableRoom):

    INIT_CAPACITY = 100
    INIT_NAME_VARIETY = ['General','Memorial','Public']

    def __init__(self,ship):
        ShipLivableRoom.__init__(self,ship)
        self.type = "hospital"
        self.name = str(ship.name_reader.get_random_name("l"))+" "+str(choice(Room_Hospital.INIT_NAME_VARIETY))+" Hospital"
        self.capacity = Room_Hospital.INIT_CAPACITY

        self.manager_label = "Chief"
        self.jobs = {
            
            "Chief": {
                "employees":{},
                "max_employees":1,
                "desired_stats":[],
                "min_stats":{
                    "emp":50,
                    "int":90,
                    "cha":40,
                },
                "req_awards":[]
            },
            "Nurse": {
                "employees":{},
                "max_employees":10,
                "desired_stats":[],
                "min_stats":{
                    "int":60,
                    "agi":20,
                    "cha":20,
                    "emp":20,
                    "eth":20,
                },
                "req_awards":[]
            },
            "Doctor": {
                "employees":{},
                "max_employees":10,
                "desired_stats":[],
                "min_stats":{
                    "int":80,
                    "agi":20,
                    "emp":20,
                    "cha":20,
                    "eth":20,
                },
                "req_awards":[]
            },
            "Specialist": {
                "employees":{},
                "max_employees":5,
                "desired_stats":[],
                "min_stats":{
                    "int":85,
                    "emp":20,
                    "cha":20,
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
            "Receptionist": {
                "employees":{},
                "max_employees":10,
                "desired_stats":[],
                "min_stats":{
                    "int":10,
                },
                "req_awards":[]
            },
        }

    def daily_step(self):
        ShipLivableRoom.daily_step(self)
