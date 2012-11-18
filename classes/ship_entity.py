import uuid

class ShipEntity:
    def __init__(self,ship):
        self.id = uuid.uuid1() 
        self.max_hp = 100
        self.cur_hp = 100
        self.ship = ship

class ShipComponent(ShipEntity):
    def __init__(self,ship):
        ShipEntity.__init__(self,ship)

class ShipRoom(ShipEntity):

    def __init__(self,ship):
        ShipEntity.__init__(self,ship)
        self.type = "default_room"
        self.name = "A Room"
        self.jobs = {}
        self.manager_label = "ShipRoom Manager"

    def get_available_jobs(self):
        output={}
        for k,v in self.jobs.items():
            if v['max_employees'] > len(v['employees']):
                output[k] = v['max_employees'] - len(v['employees'])
        return output

    def assign_manager(self):
        pass

    def employ_human(self,human,job):
        self.jobs[job]['employees'][human.id] = human
        human.job = {"room":self,"job":job}
        #self.ship._add_log(1,str(human.first_name)+" "+str(human.last_name)+" took a job as a <"+str(job)+"> at <"+str(self.name)+">")

    def has_manager(self):
        return len(self.jobs[self.manager_label].employees) == 1

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
