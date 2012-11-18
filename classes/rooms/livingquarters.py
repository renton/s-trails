from classes.ship_entity import *

class Room_LivingQuarters(ShipLivableRoom):

    INIT_CAPACITY = 100

    def __init__(self,ship):
        ShipLivableRoom.__init__(self,ship)
        self.type = "living_quarters"
        self.capacity = Room_LivingQuarters.INIT_CAPACITY
        self.occupants = {}

    def daily_step(self,ship):
        pass
