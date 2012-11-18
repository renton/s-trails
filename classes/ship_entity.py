import uuid

class ShipEntity:
    def __init__(self,ship):
        self.id = uuid.uuid1() 
        self.max_hp = 100
        self.cur_hp = 100
        self.ship = ship

class ShipRoom(ShipEntity):
    def __init__(self,ship):
        self.type = "default_room"
        ShipEntity.__init__(self,ship)

#can live in livingquarters,prisons,hospitals,barracks
class ShipLivableRoom(ShipRoom):

    DEFAULT_CAPACITY = 100

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.type = "default_livable_room"
        self.capacity = ShipLivableRoom.DEFAULT_CAPACITY

    def is_vacant(self):
        return len(self.occupants) < self.capacity

    def add_occupant(self,human):
        if len(self.occupants) < self.capacity:
            self.occupants[human.id] = human
            human.change_lq(self)
            return True
        return False

    def remove_occupant(self,human):
        if human.id in self.occupants:
            del self.occupants[human.id]
            human.change_lq(None)
            return True
        return False

class Room_LivingQuarters(ShipLivableRoom):

    INIT_CAPACITY = 100

    def __init__(self,ship):
        ShipLivableRoom.__init__(self,ship)
        self.type = "living_quarters"
        self.capacity = Room_LivingQuarters.INIT_CAPACITY
        self.occupants = {}

    def daily_step(self,ship):
        pass

class Room_Farm(ShipRoom):

    INIT_AVG_DAYS_TILL_HARVEST = 10
    INIT_AVG_YIELD_AMOUNT = 100
    INIT_ITEM_YIELD_TYPES = ['grain','fruit+veg','protein']
    INIT_DEFAULT_ITEM = 'grain'

    INIT_DEFAULT_PLANT_REQ_RESOURCES = {
        "water":10,
        "growth cells":2,
        "farming supplies":1,
        "farming tools":1
    }

    INIT_DEFAULT_STEP_REQ_RESOURCES = {
        "water":1
    }

    INIT_DEFAULT_HARVEST_REQ_ITEMS = {
        "farming supplies":2,
        "farming tools":1
    }

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.type = "farm"
        self.item_type = Room_Farm.INIT_DEFAULT_ITEM
        self.days_till_harvest = 0
        self.ready_to_plant = True
        self.yield_amount = Room_Farm.INIT_AVG_YIELD_AMOUNT

    def _calc_days_till_harvest(self):
        #TODO - requires water
        #TODO - use items to plan harvest
        #TODO - yield based on employees
        #TODO - time based on employees
        #TODO - cannot start without enough employees
        #TODO - items dont remove or have a % of removing

        #TODO - ship unmet criteria can be function of ship that returns the unmet criteria dict

        '''
        unmet_criteria = {}

        for k,v in Room_Farm.INIT_DEFAULT_PLANT_REQ_RESOURCES.items():
            if not self.ship._get_total_resources(k)[0] >= v:
                unmet_criteria[k] = v

        for k,v in Room_Farm.INIT_DEFAULT_PLANT_REQ_ITEMS.items():
            if not self.ship._get_total_items(k)[0] >= v:
                unmet_criteria[k] = v

        if unmet_criteria:
            message = ""
            for k,v in unmet_criteria.items():
                message += str(k)+":"+str(v)+","
            self.ship._add_warning("Cannot process farm. Requirments not met: "+str(message))
            return False

        for k,v in Room_Farm.INIT_DEFAULT_PLANT_REQ_RESOURCES.items():
            self.ship._remove_resources(k,v)
        for k,v in Room_Farm.INIT_DEFAULT_PLANT_REQ_ITEMS.items():
            self.ship._remove_items(k,v)

        self.ship._add_log(str(self.item_type)+" farm planted.")
        self.days_till_harvest = Room_Farm.INIT_AVG_DAYS_TILL_HARVEST
        self.ready_to_plant = False
        '''

    def daily_step(self,ship):
        '''
        if self.ready_to_plant == True:
            self._calc_days_till_harvest()
        else:
            if self.days_till_harvest <= 0:
                self._harvest()
            else:
                unmet_criteria = {}
                for k,v in Room_Farm.INIT_DEFAULT_PLANT_REQ_RESOURCES.items():
                    if not self.ship._get_total_resources(k)[0] >= v:
                        unmet_criteria[k] = v
                #TODO - small bonus for employees - % to increase yield

                if unmet_criteria:
                    message = ""
                    for k,v in unmet_criteria.items():
                        message += str(k)+":"+str(v)+","
                    self.ship._add_warning("Farm cannot grow. Requirements not met: "+str(message))
                    # % chance at affecting yield
                else:
                    #TODO - removing bulk items can be ship function
                    for k,v in Room_Farm.INIT_DEFAULT_PLANT_REQ_RESOURCES.items():
                        self.ship._remove_resources(k,v)
                    self.days_till_harvest -=1
        '''
        pass
    
    def _harvest(self):
        '''
        unmet_criteria = {}
        for k,v in Room_Farm.INIT_DEFAULT_HARVEST_REQ_ITEMS.items():
            if not self.ship._get_total_items(k)[0] >= v:
                unmet_criteria[k] = v

        if unmet_criteria:
            message = ""
            for k,v in unmet_criteria.items():
                message += str(k)+":"+str(v)+","
            self.ship._add_warning("Cannot harvest. Requirements not met: "+str(message))
            # % chance at affecting yield
        else:
            #TODO - removing bulk items can be ship function
            for k,v in Room_Farm.INIT_DEFAULT_HARVEST_REQ_ITEMS.items():
                self.ship._remove_resources(k,v)
            #TODO - use items to process harvest
            #TODO - yield based on employees
            #TODO - cannot start without employees
            self.ship._add_log("harvest time")
            self.ready_to_plant = True
        '''

class Room_Storage(ShipRoom):

    INIT_CAPACITY = 1000

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.type = "storage"
        self.item_store = {}
        self.capacity = Room_Storage.INIT_CAPACITY

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

    def daily_step(self,ship):
        pass

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

class ShipComponent(ShipEntity):
    def __init__(self,ship):
        ShipEntity.__init__(self,ship)
