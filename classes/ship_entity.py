import uuid
from log_types import *

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
        self.occupants = {}

    def get_available_jobs(self):
        output={}
        for k,v in self.jobs.items():
            if v['max_employees'] > len(v['employees']):
                output[k] = v['max_employees'] - len(v['employees'])
        return output

    def fire_human(self,human,job):
        del self.jobs[job]['employees'][human.id]
        human.change_job(None)
        self.ship._add_log(LOG_TYPE_ROOMS,LOG_LEVEL_MED,str(human.first_name)+" "+str(human.last_name)+" no longer works as a <"+str(job)+"> at <"+str(self.name)+">")

    def employ_human(self,human,job):
        self.jobs[job]['employees'][human.id] = human
        human.change_job({"room":self,"job":job})
        self.ship._add_log(LOG_TYPE_ROOMS,LOG_LEVEL_MED,str(human.first_name)+" "+str(human.last_name)+" took a job as a <"+str(job)+"> at <"+str(self.name)+">")

    def has_manager(self):
        return len(self.jobs[self.manager_label]['employees']) == 1

    def get_average_employee_stats(self):

        stats = ['int','str','agi','cha','emp','cry','eth','loy','imm','hap']
        data = {}

        for stat in stats:
            data[stat] = {"tot":0,"avg":0,"low":9999,"high":0}
 
        employees = self.get_all_employees()

        if employees:
            for employee in employees:
                for k,v in employee.stats.items():
                    data[k]["tot"]+=v
                    if data[k]["low"] > v:
                        data[k]["low"] = v
                    if data[k]["high"] < v:
                        data[k]["high"] = v

            for stat in data:
                data[stat]["avg"] = (data[stat]["tot"]/len(employees))

        return data

    def get_all_employees(self):
        employees = []
        for k,v in self.jobs.items():
            for k_employee,v_employee in v['employees'].items():
                employees.append(v_employee)
        return employees
    
    def step_daily(self):
        # make sure all employees are still fit to work here, or else fire them
        employees = self.get_all_employees()

        for employee in employees:
            if not employee.meets_requirements(self.jobs[employee.job['job']]['min_stats']):
                self.fire_human(employee,employee.job['job'])

#can live in livingquarters,prisons,hospitals,barracks
class ShipLivableRoom(ShipRoom):

    DEFAULT_CAPACITY = 100

    def __init__(self,ship):
        ShipRoom.__init__(self,ship)
        self.type = "default_livable_room"
        self.capacity = ShipLivableRoom.DEFAULT_CAPACITY
        self.cleanliness = 100

    def is_vacant(self):
        return len(self.occupants) < self.capacity

    def add_occupant(self,human):
        if len(self.occupants) < self.capacity:

            # remove from existing home
            if human.lq:
                human.lq.remove_occupant(human)

            self.occupants[human.id] = human
            human.change_lq(self)
            self.ship._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_MED,str(human.first_name)+" "+str(human.last_name)+" now lives at <"+str(self.name)+">")
            return True
        return False

    def remove_occupant(self,human):
        self.ship._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_MED,str(human.first_name)+" "+str(human.last_name)+" no longer lives at <"+str(self.name)+">")
        if human.id in self.occupants:
            del self.occupants[human.id]
            human.change_lq(None)
            return True
        return False

    def step_daily(self):
        ShipRoom.step_daily(self)
