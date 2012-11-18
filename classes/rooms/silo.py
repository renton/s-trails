from classes.ship_entity import *

class ShipSilo(ShipRoom):
    TYPES = ['water','oxygen','fuel']
    INIT_CAPACITY = 5000

    def __init__(self,ship,silo_type):
        ShipEntity.__init__(self,ship)
        self.type = "silo"
        self.item_type = silo_type
        self.capacity = ShipSilo.INIT_CAPACITY
        self.amount = 0

    def has_room(self):
        return self.amount < self.capacity

    def is_empty(self):
        return self.amount <= 0

    def add_items(self,item,add_amount):

        if self.item_type != item:
            return (False,item,add_amount)

        # already full
        if not self.has_room():
            return (False,item,add_amount)
        else:
            space = self.capacity - self.amount
            if add_amount > space:
                self.amount = self.capacity
                add_amount -= space
            else:
                self.amount += add_amount
                add_amount = 0
            return (True,item,add_amount)

    def remove_items(self,item,remove_amount):

        if self.item_type != item:
            return (False,item,remove_amount)

        if self.is_empty():
            return (False,item,remove_amount)
        else:
            if remove_amount > self.amount:
                temp = self.amount
                self.amount = 0
                remove_amount -= temp
            else:
                self.amount -= remove_amount
                remove_amount = 0
            return (True,item,remove_amount)
