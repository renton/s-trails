from human import *
from items import *
from ship_entity import *
from name_reader import *

from rooms.silo import *
from rooms.livingquarters import *
from rooms.farm import *
from rooms.storage import *
from rooms.bar import *
from rooms.distillery import *
from rooms.hospital import *
from rooms.prison import *
from rooms.bridge import *

from copy import deepcopy

from log_types import *

class Ship:

    INIT_POPULATION_SIZE = 500
    INIT_NUM_INTERNAL_COMPONENTS = 0
    INIT_NUM_EXTERNAL_COMPONENTS = 0

    STARTING_JOB_AGE = 16

    INIT_ROOMS = [
		{
            "obj":Room_Bridge,
            "num":1
        },
        {
            "obj":Room_Storage,
            "num":5
        },
        {
            "obj":Room_LivingQuarters,
            "num":2
        },
        {
            "obj":Room_Farm,
            "num":1
        },
        {
            "obj":Room_Bar,
            "num":1
        },
        {
            "obj":Room_Distillery,
            "num":1
        },
        {
            "obj":Room_Hospital,
            "num":1
        },
		{
            "obj":Room_Prison,
            "num":1
        },


    ]

    INIT_SILOS = {
        "water":10,
        "oxygen":8,
        "fuel":8
    }

    INIT_ITEMS = {
        "water":3,
        "fuel":12233,
        "oxygen":93820,
        "grain":2000,
        "protein":1000,
        "fruit+veg":2000,
        "farming supplies":1000,
        "farming tools":100,
        "growth cells":1000,
        "oxygen canister":1000,
        "oxygen mask":100
    }

    def __init__(self,name_reader):
        self.humans = {}
        self.rooms = {}
        self.internal_components = {}
        self.external_components = {}
        self.silos = {}
        self.daily_logs = {}
        self.is_game_over = False
        self.name_reader = name_reader

        print "Creating population..."
        for i in range(Ship.INIT_POPULATION_SIZE):
            new_human = Human(self)
            self.humans[new_human.id]=new_human
        for i in range(Ship.INIT_NUM_INTERNAL_COMPONENTS):
            new_component = ShipComponent()
            self.internal_components[new_component.id]=new_component
        for i in range(Ship.INIT_NUM_EXTERNAL_COMPONENTS):
            new_component = ShipComponent()
            self.external_components[new_component.id]=new_component

        print "Creating rooms..."
        for v in Ship.INIT_ROOMS:
            for i in range(v['num']):
                new_room = v['obj'](self)
                self.rooms[new_room.id]=new_room

        print "Creating silos..."
        for k,v in Ship.INIT_SILOS.items():
            for i in range(v):
                if ITEM[k]['type'] == "resource":
                    new_silo = ShipSilo(self,k)
                    self.silos[new_silo.id]=new_silo

        print "Adding initial items..."
        self.add_items(Ship.INIT_ITEMS)

        print "Finding homes for homeless..."
        self.find_homes_for_homeless()

        print "Finding jobs for homeless..."
        self.find_jobs_for_unemployed()

    # =============== DAILY ITERATION =========================

    def daily_step(self,day):

        self._clear_logs()

        self._daily_use_oxygen()
        self._daily_feed_humans()
        self._daily_use_fuel()

        print "---"
        # step humans
        print len(self.humans)
        for k,v in self.humans.items():
            if not v.daily_step(day):
                #passed away
                self.remove_human(v,is_death=True)

        # step rooms+employees
        for k,v in self.rooms.items():
            v.step_daily()

        self.find_homes_for_hospitalized()
        self.find_homes_for_homeless()
        self.find_jobs_for_unemployed()
        self.find_prison_for_prisoners()

        #self.print_stats_living_quarters()
        #self.print_stats_silos()
        #self.print_stats_stores()
        #self.print_overview_stats()
        #self.print_daily_logs()
        #self.print_inventory()
        #self.print_humans()
        #self.print_rooms()

        return self.is_game_over

    #TODO - all daily req in one function ?

    def _daily_feed_humans(self):
        # food / water
        #TODO - setting to change diet

        daily_required = self.get_resource_daily_required()
        resources = {
            'water':daily_required['water'],
            'grain':daily_required['grain'],
            'protein':daily_required['protein'],
            'fruit+veg':daily_required['fruit+veg'],
        }

        print resources

        (status,remainder) = self.remove_items(resources)

        if remainder['protein'] == 0 and remainder['water'] == 0 and remainder['fruit+veg'] == 0 and remainder['grain'] == 0:
            for k,v in self.humans.items():
                v.eat_balanced_diet()

        # suffer thirst - hp loss
        if remainder['water'] > 0:
            self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"No water: The colony is suffering from major thirst.")
            for k,v in self.humans.items():
                v.suffer_thirst()

        # suffer imm loss
        if remainder['fruit+veg'] > 0:
            self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"The colony is suffering from vitamin deficiency")
            for k,v in self.humans.items():
                v.suffer_vitamin_loss()

        # suffer agi loss
        if remainder['protein'] > 0:
            self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"The colony is suffering from protein deficiency")
            for k,v in self.humans.items():
                v.suffer_protein_loss()

        # suffer hunger - hp loss
        if (remainder['protein'] > 0 and remainder['grain'] > 0 and remainder['fruit+veg'] > 0):
            self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"No food: The colony is suffering from major starvation.")
            for k,v in self.humans.items():
                v.suffer_hunger()

    def _daily_use_fuel(self):
        #TODO - based on current settings and upgrades
        amount = self.get_resource_daily_required()["fuel"]
        (status,remainder) = self.remove_items({"fuel":amount})

        if status == False:
            self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"Not enough fuel. Need "+str(remainder))

    def _daily_use_oxygen(self):
        #TODO - based on current settings and upgrades
        amount = self.get_resource_daily_required()["oxygen"]
        (status,remainder) = self.remove_items({"oxygen":amount})

        if status == False:
            for k,v in self.humans.items():
                v.suffocate()
            self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"No oxygen: The colony is suffocating.")

    # =================== INVENTORY SYSTEM ================================

    def add_items(self,item_amount_array_input):
        #TODO - filling strats - fill complete, spread
        #TODO - if in item list

        item_amount_array = deepcopy(item_amount_array_input)

        stores = self.get_all_storages(only_has_room=True)

        init_amounts = {}
        for k,v in item_amount_array.items():
            init_amounts[k] = v

        for k_item,v_item in item_amount_array.items():

            container = stores

            if ITEM[k_item]['type'] == "resource":
                container = self.get_all_silos(with_item=k_item,only_has_room=True)

            for k_container,v_container in container.items():
                if v_item <= 0:
                    break
                (add_status,k_item,v_item) = v_container.add_items(k_item,v_item)
            item_amount_array[k_item]=v_item


        no_waste = True
        for k_item,v_item in item_amount_array.items():
            if v_item>0:
                self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"Produced Waste - Couldn't Store: "+str(v_item)+" "+str(k_item))
                no_waste = False
            else:
                self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_LOW,"Added "+str(init_amounts[k_item])+" "+str(k_item))

        return (no_waste,item_amount_array)

    def remove_items(self,item_amount_array_input):
        #TODO - filling strats - fill complete, spread

        item_amount_array = deepcopy(item_amount_array_input)

        #TODO - hard copy?
        init_amounts = {}
        for k,v in item_amount_array.items():
            init_amounts[k] = v

        for k_item,v_item in item_amount_array.items():

            container = {}

            if ITEM[k_item]['type'] == "resource":
                container = self.get_all_silos(with_item=k_item)
            else:
                if ITEM[k_item]['type'] == "item":
                    container = self.get_all_storages(with_item=k_item)

            for k_container,v_container in container.items():
                if v_item<=0:
                    break
                (remove_status,k_item,v_item) = v_container.remove_items(k_item,v_item)
            item_amount_array[k_item]=v_item

        is_success = True
        for k_item,v_item in item_amount_array.items():
            if v_item>0:
                #self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_HIGH,"wtf: "+str(v_item)+" "+str(k_item))
                #TODO - should there be a message or will we let client caller handle response?
                is_success = False
            else:
                self._add_log(LOG_TYPE_INVENTORY,LOG_LEVEL_MED,"Removed: "+str(init_amounts[k_item])+" "+str(k_item))
        return (is_success,item_amount_array)

    def get_unmet_criteria(self,item_array_input):
        inventory = self.get_inventory()
        item_array = deepcopy(item_array_input)

        for k,v in item_array.items():
            if k in inventory:
                total = inventory[k]
                if total >= v:
                    del item_array[k]
                else:
                    item_array[k] -= total

        return item_array

    def get_total_items(self,item_type):
    #TODO refactor - ugggglllly

        total = 0
        capacity = 0
        estimate_days = 0

        if ITEM[item_type]['type'] == "resource":
            containers = self.get_all_silos(with_item=item_type)
            for k,v in containers.items():
                if v.item_type == item_type:
                    total+=v.amount
                    capacity+=v.capacity
        else:
            if ITEM[item_type]['type'] == "item":
                containers = self.get_all_storages(with_item=item_type)
                for k,v in containers.items():
                    if item_type in v.item_store:
                        total+=v.item_store[item_type]
                    capacity+=v.capacity
            else:
                containers = {}

        if 'core' in ITEM[item_type]:
            daily_required = self.get_resource_daily_required()[item_type]
            if daily_required > 0:
                estimate_days = total/self.get_resource_daily_required()[item_type]
            else:
                estimate_days = 0
        else:
            estimate_days = None

        return (total,capacity,estimate_days)

    def get_all_silos(self,only_has_room=False,with_item=None):
        silos = {}
        for k,v in self.silos.items():
            if with_item and v.item_type == with_item:
                if only_has_room:
                    if v.has_room:
                        silos[v.id] = v
                else:
                    silos[v.id] = v
            else:
                silos[v.id] = v
        return silos

    def get_all_storages(self,only_has_room=False,with_item=None):
        stores = {}
        for k,v in self.rooms.items():
            if v.type=="storage":
                if with_item and with_item in v.item_store:
                    if only_has_room:
                        if not v.is_full():
                            stores[v.id] = v
                    else:
                        stores[v.id] = v
                else:
                    stores[v.id] = v
        return stores

    def get_ship_weight(self):
        return 1000

    def get_inventory(self,count_silos=True,count_stores=True):

        inventory = {}

        if count_stores:
            stores = self.get_all_storages()
            for k,v in stores.items():
                for k_item,v_item in v.item_store.items():
                    if k_item not in inventory:
                        inventory[k_item] = 0
                    inventory[k_item]+=v_item
        if count_silos:
            silos = self.get_all_silos()
            for k,v in silos.items():
                if v.item_type not in inventory:
                    inventory[v.item_type] = 0
                inventory[v.item_type]+=v.amount
        return inventory

    def get_resource_daily_required(self):

        daily_required = {

            "fuel":(self.get_ship_weight()/10),
            "water":(len(self.humans)/10),
            "oxygen":(len(self.humans)*len(self.rooms)/20),
            "grain":(len(self.humans)/10),
            "protein":(len(self.humans)/10),
            "fruit+veg":(len(self.humans)/10),
        }

        # always requires at least 1 of each type
        if len(self.humans) >= 1:
            for k,v in daily_required.items():
                if v == 0:
                    daily_required[k] = 1

        return daily_required


    # ============== LOGGING SYSTEM ===============
    # TODO - differnet types for topics (farming,housing,inventory,population,etc.)

    def _add_log(self,log_type,level,message,archive=False):

        if not archive:
            if log_type not in self.daily_logs:
                self.daily_logs[log_type] = {}
            if level not in self.daily_logs[log_type]:
                self.daily_logs[log_type][level] = []
            self.daily_logs[log_type][level].append(message)
        else:
           outFile = open('Archived Log.txt', 'a+')
           outFile.write(message)
           outFile.close()

    def _clear_logs(self):
        self.daily_logs = {}

    # ============= WORKFORCE =========================

    def find_jobs_for_unemployed(self):
        #TODO - smart placment system
        unemployed = []
        for k,v in self.humans.items():
            if v.job is None and not v.old_age_immobile and not v.should_be_hospitalized() and v.age >= Ship.STARTING_JOB_AGE:
                unemployed.append(v)

        for k_room_id,v_room in self.rooms.items():
            for k_job_title,v_job in v_room.get_available_jobs().items():
                for i in range(v_job):
                    for human in unemployed:
                        if human.meets_requirements(v_room.jobs[k_job_title]['min_stats']) and human.job is None:
                            v_room.employ_human(human,k_job_title)
                            unemployed.remove(human)
                            break

        if len(unemployed) > 0:
            self._add_log(LOG_TYPE_ROOMS,LOG_LEVEL_HIGH,str(len(unemployed))+" civilians could not find work.")

        if len(self.get_available_jobs_simple()) > 0:
            self._add_log(LOG_TYPE_ROOMS,LOG_LEVEL_HIGH,"Unfilled jobs: "+str(self.get_available_jobs_simple()))
        

    #TODO maybe job db like in items for same jobs / mult rooms
    def get_available_jobs_simple(self):

        jobs = {}
        for k_room_id,v_room in self.rooms.items():
            for k_job_title,v_job in v_room.get_available_jobs().items():
                if k_job_title not in jobs:
                    jobs[k_job_title]=0
                jobs[k_job_title]+=v_job
        return jobs

    # ============= HOUSING SYSTEM  ===================

    def get_all_livable_rooms(self,only_vacant=False,room_type=False):
        lq = {}
        for k,v in self.rooms.items():
            if room_type == False or v.type == room_type:
                if only_vacant:
                    if v.is_vacant:
                        lq[v.id] = v
                else:
                    lq[v.id] = v
        return lq

    def get_all_living_quarters(self,only_vacant=False):
        return self.get_all_livable_rooms(room_type="living_quarters")

    def get_all_hospitals(self,only_vacant=False):
        return self.get_all_livable_rooms(room_type="hospital")
		
    def get_all_prisons(self,only_vacant=False):
        return self.get_all_livable_rooms(room_type="prison")

    def find_homes_for_homeless(self):
        homeless = []
        for k,v in self.humans.items():
            if v.lq is None:
                homeless.append(v)

        lq = self.get_all_living_quarters(only_vacant=True)
        lq_keys = lq.keys()

        counter = 0
        count_found_home = 0
        for human in homeless:
            iters = len(lq_keys)
            while(1):
                if len(lq_keys) <= (counter):
                    counter = 0

                if lq[lq_keys[counter]].add_occupant(human):
                    counter += 1
                    count_found_home +=1
                    break
                else:
                    counter += 1
                    iters -= 1
                    if iters <= 0:
                        #WARNING - no vacancies, still homeless
                        break
                    continue

        if len(homeless) > 0:
            self._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_HIGH,str(len(homeless)-count_found_home)+" civilians could not find a home.")

    def find_homes_for_hospitalized(self):
        hospitalized = []
        for k,v in self.humans.items():
            if v.should_be_hospitalized() and v.lq and v.lq.type != "hospital":
                hospitalized.append(v)

        lq = self.get_all_hospitals(only_vacant=True)
        lq_keys = lq.keys()

        counter = 0
        count_found_home = 0
        for human in hospitalized:
            iters = len(lq_keys)
            while(1):
                if len(lq_keys) <= (counter):
                    counter = 0

                if lq[lq_keys[counter]].add_occupant(human):
                    counter += 1
                    count_found_home +=1
                    break
                else:
                    counter += 1
                    iters -= 1
                    if iters <= 0:
                        #WARNING - no vacancies, still homeless
                        break
                    continue

        if count_found_home > 0:
            self._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_HIGH,str(count_found_home)+" civlians were hospitalized.")

        if (len(hospitalized)-count_found_home) > 0:
            self._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_HIGH,str(len(hospitalized)-count_found_home)+" civlians could not be hospitalized.")

    def find_prison_for_prisoners(self):
	imprisoned = []
        for k,v in self.humans.items():
            if v.should_be_imprisoned() and v.lq and v.lq.type != "prison" and v.lq.type != "hospital":
                imprisoned.append(v)

        lq = self.get_all_prisons(only_vacant=True)
        lq_keys = lq.keys()

        counter = 0
        count_found_prison = 0
        for human in imprisoned:
            iters = len(lq_keys)
            while(1):
                if len(lq_keys) <= (counter):
                    counter = 0

                if lq[lq_keys[counter]].add_occupant(human):
                    counter += 1
                    count_found_prison +=1
                    break
                else:
                    counter += 1
                    iters -= 1
                    if iters <= 0:
                        #WARNING - no vacancies, still homeless
                        break
                    continue

        if count_found_prison > 0:
            self._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_HIGH,str(count_found_prison)+" wanted criminals were imprisoned.")

        if (len(imprisoned)-count_found_prison) > 0:
            self._add_log(LOG_TYPE_HUMANS,LOG_LEVEL_HIGH,str(len(imprisoned)-count_found_prison)+" wanted criminals could not be imprisoned.")
		
    # =============== HUMAN MGMT ============================
    
    def remove_human(self,human,is_death=False):

        if human.lq:
            human.lq.remove_occupant(human)
        if human.job:
            human.job['room'].fire_human(human,human.job['job'])

        del self.humans[human.id]

        if is_death:
            self.add_items({"corpse":1})

    # ============== GENERAL ================================

    def get_overview(self):
        items = ['oxygen','water','fuel','protein','grain','fruit+veg']
        overview = {}

        for item in items:
            overview[item] = self.get_total_items(item)

        return overview

    # =============== PRINT DEBUGGING =======================

    def print_rooms(self):
        for k,v in self.rooms.items():
            print v.name

    def print_stats_living_quarters(self):
        output = []
        lq = self.get_all_living_quarters()
        for k,v in lq.items():
            output.append({v.name:len(v.occupants)})
        print output

    def print_stats_silos(self):
        print "======= SILOS ====="
        for k,v in self.silos.items():
            print "("+str(v.item_type)+") "+str(v.amount)

    def print_stats_stores(self):
        print "======== STORES ======"
        stores = self.get_all_storages()
        for k,v in stores.items():
            print v.item_store

    def print_total_resources(self):
        #TODO - use core value from item table
        items = ['oxygen','water','fuel','protein','grain','fruit+veg']

        for item in items:
            print str(item)+": "+str(self.get_total_items(item))

    def print_overview_stats(self):
        print "\n=== Overview ==="
        print "population: "+str(len(self.humans))
        print "rooms: "+str(len(self.rooms))
        print "silos: "+str(len(self.silos))
        self.print_total_resources()

    def print_daily_logs(self):
        print "\n=== Daily Log ==="
        if not self.daily_logs:
            print "(None)"
        else:
            for k,v in self.daily_logs.items():
                print "\n===== LEVEL "+str(k)+" ======"
                for log in v:
                    print str(log)

    def print_inventory(self):
        print self.get_inventory()

    def print_humans(self):
        for k,v in self.humans.items():
            print v.first_name,v.last_name,v.age,v.hp

    def print_bars(self):
       for k,v in self.rooms.items():
        print v.name
#this is a comment
