from classes.ship_entity import *
from random import randint

class Room_Bridge(ShipRoom):

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.name = "The Bridge"
        self.type = "bridge"

        self.manager_label = "Diplomatic Captain"
        #TODO - if human stats change, make sure still capable of job - in human loop?
        self.jobs = {
            
            "Diplomatic Captain": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "eth":60,
                    "int":60,
                    "cha":80,
                    "cry":60,
                    "emp":60,
                },
                "req_awards":[]
            },
            "Signals Captain": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "eth":60,
                    "int":80,
                    "cha":20,
                    "cry":60,
                    "emp":40,
                },
                "req_awards":[]
            },
            "Air Commander": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "eth":60,
                    "int":80,
                    "cha":60,
                    "cry":60,
                    "emp":40,
                },
                "req_awards":[]
            },
            "Military Commander": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "eth":60,
                    "int":80,
                    "cha":60,
                    "cry":60,
                    "emp":40,
                },
                "req_awards":[]
            },
            "Colony Navigator": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "eth":60,
                    "int":80,
                    "cha":20,
                    "cry":60,
                    "emp":40,
                },
                "req_awards":[]
            },
            "Colony Pilot": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "eth":60,
                    "int":80,
                    "cha":20,
                    "cry":60,
                    "emp":40,
                },
                "req_awards":[]
            },
            "Weapons Captain": {
                "employees":{},
                "max_employees":1,
                "desired_stats":["str","eth","agi","int","cha"],
                "min_stats":{
                    "eth":60,
                    "int":80,
                    "cha":20,
                    "cry":60,
                    "emp":40,
                },
                "req_awards":[]
            },
        }



    def step_daily(self):
        pass
        ShipRoom.step_daily(self)
