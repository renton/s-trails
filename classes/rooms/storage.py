from classes.ship_entity import *
from random import randint

class Room_Storage(ShipRoom):

    INIT_CAPACITY = 10000

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.name = "Store "+str(randint(0,9999))+"-"+str(randint(0,99))
        self.type = "storage"
        self.item_store = {}
        self.capacity = Room_Storage.INIT_CAPACITY
        self.manager_label = "Foreman"

        self.jobs = {
            "Foreman": {
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
            "Manual Labourer": {
                "employees":{},
                "max_employees":10,
                "desired_stats":["str","agi"],
                "min_stats":{
                    "str":10,
                    "agi":10,
                },
                "req_awards":[]
            },
            "Logistics Clerk": {
                "employees":{},
                "max_employees":5,
                "desired_stats":["int","str","agi"],
                "min_stats":{
                    "int":10,
                },
                "req_awards":[]
            },
        }
    def add_items(self,item,add_amount):
        #TODO lost due to logistic error,theft(% based on empl with lowest loy and emp),accident
        # already full
        if self.is_full():
            return (False,item,add_amount)
        else:
            cur_amount = self.get_total_items()
            space = self.capacity - cur_amount
            if add_amount > space:
                if item not in self.item_store:
                    self.item_store[item] = 0
                self.item_store[item] += space
                add_amount -= space
            else:
                if item not in self.item_store:
                    self.item_store[item] = 0               
                self.item_store[item] += add_amount
                add_amount = 0
            return (True,item,add_amount)

    def remove_items(self,item,remove_amount):
        #TODO lost due to logistic error
        if self.is_empty():
            return (False,item,remove_amount)
        else:
            if item in self.item_store:
                cur_amount = self.item_store[item]
                if remove_amount > cur_amount:
                    temp = cur_amount
                    del self.item_store[item]
                    remove_amount -= temp
                else:
                    self.item_store[item] -= remove_amount
                    if self.item_store[item] == 0:
                        del self.item_store[item]
                    remove_amount = 0
                return (True,item,remove_amount)
            else:
                return (False,item,remove_amount)

    def get_total_items(self):
        total = 0
        for k,v in self.item_store.items():
            total+=v
        return total

    def is_full(self):
        return self.capacity <= self.get_total_items()

    def is_empty(self):
        return self.get_total_items() == 0

    def step_daily(self):
        ShipRoom.step_daily(self)
