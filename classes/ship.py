from human import *
from items import *
from ship_entity import *

class Ship:

    INIT_POPULATION_SIZE = 200
    INIT_NUM_INTERNAL_COMPONENTS = 0
    INIT_NUM_EXTERNAL_COMPONENTS = 0

    INIT_ROOMS = [
        {
            "obj":Room_Storage,
            "num":20
        },
        {
            "obj":Room_LivingQuarters,
            "num":20
        },
        {
            "obj":Room_Farm,
            "num":20
        },

    ]

    INIT_SILOS = {
        "water":10,
        "oxygen":8,
        "fuel":8
    }

    INIT_ITEMS = {
        "water":30230,
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

    def __init__(self):
        self.humans = {}
        self.rooms = {}
        self.internal_components = {}
        self.external_components = {}
        self.silos = {}
        self.daily_logs = {}
        self.is_game_over = False

        for i in range(Ship.INIT_POPULATION_SIZE):
            new_human = Human()
            self.humans[new_human.id]=new_human
        for i in range(Ship.INIT_NUM_INTERNAL_COMPONENTS):
            new_component = ShipComponent()
            self.internal_components[new_component.id]=new_component
        for i in range(Ship.INIT_NUM_EXTERNAL_COMPONENTS):
            new_component = ShipComponent()
            self.external_components[new_component.id]=new_component

        for v in Ship.INIT_ROOMS:
            for i in range(v['num']):
                new_room = v['obj'](self)
                self.rooms[new_room.id]=new_room

        for k,v in Ship.INIT_SILOS.items():
            for i in range(v):
                if ITEM[k]['type'] == "resource":
                    new_silo = ShipSilo(self,k)
                    self.silos[new_silo.id]=new_silo

        self.add_items(Ship.INIT_ITEMS)
    
        self.find_homes_for_homeless()

    # =============== DAILY ITERATION =========================

    def daily_step(self):

        self._clear_logs()

        self._daily_use_oxygen()
        self._daily_feed_humans()
        self._daily_use_fuel()

        # step humans
        for k,v in self.humans.items():
            a_human = v
            v.daily_step()

        # step rooms+employees
        for k,v in self.rooms.items():
            v.daily_step(self)

        # step jobfinder
    
        # step homefinder

        self.print_stats_silos()
        self.print_stats_stores()
        self.print_overview_stats()
        self.print_daily_logs()
        self.print_inventory()

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

        (status,remainder) = self.remove_items(resources)

        if status == False:
            self._add_log(2,"Not enough foods")

    def _daily_use_fuel(self):
        #TODO - based on current settings and upgrades
        amount = self.get_resource_daily_required()["fuel"]
        (status,remainder) = self.remove_items({"fuel":amount})

        if status == False:
            self._add_log(2,"Not enough fuel. Need "+str(remainder))

    def _daily_use_oxygen(self):
        #TODO - based on current settings and upgrades
        amount = self.get_resource_daily_required()["oxygen"]
        (status,remainder) = self.remove_items({"oxygen":amount})

        if status == False:
            self._add_log(2,"Not enough oxygen. Need "+str(remainder))
            #TODO start using oxygen tank items to survive

    # =================== INVENTORY SYSTEM ================================

    def add_items(self,item_amount_array):
        #TODO - filling strats - fill complete, spread
        #TODO - if in item list

        stores = self.get_all_storages(only_has_room=True)
        silos = {}

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


        for k_item,v_item in item_amount_array.items():
            if v_item>0:
                self._add_log(1,"Produced Waste - Couldn't Store: "+str(v_item)+" "+str(k_item))
            else:
                self._add_log(1,"Added "+str(init_amounts[k_item])+" "+str(k_item))

    def remove_items(self,item_amount_array):
        #TODO - filling strats - fill complete, spread

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
                #TODO - should there be a message or will we let client caller handle response?
                is_success = False
            else:
                self._add_log(1,"Removed: "+str(init_amounts[k_item])+" "+str(k_item))
        return (is_success,item_amount_array)

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
            estimate_days = total/self.get_resource_daily_required()[item_type]
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
            "water":(len(self.humans)),
            "oxygen":(len(self.humans)*len(self.rooms)/20),
            "grain":(len(self.humans)),
            "protein":(len(self.humans)),
            "fruit+veg":(len(self.humans)),
        }

        return daily_required


    # ============== LOGGING SYSTEM ===============
    # TODO - rather than have log/warning, just have one system
    # with multiple levels of importance

    def _add_log(self,level,message):
        if level not in self.daily_logs:
            self.daily_logs[level] = []
        self.daily_logs[level].append(message)

    def _clear_logs(self):
        self.daily_logs = {}

    # ============= HOUSING SYSTEM  ===================

    def get_all_living_quarters(self,only_vacant=False):
        lq = {}
        for k,v in self.rooms.items():
            if v.type == "living_quarters":
                if only_vacant:
                    if v.is_vacant:
                        lq[v.id] = v
                else:
                    lq[v.id] = v
        return lq

    def find_homes_for_homeless(self):
        homeless = []
        for k,v in self.humans.items():
            if v.lq is None:
                homeless.append(v)

        lq = self.get_all_living_quarters(only_vacant=True)
        lq_keys = lq.keys()

        counter = 0
        for human in homeless:
            while(1):
                iters = len(lq_keys)
                if len(lq_keys) <= (counter):
                    counter = 0

                if lq[lq_keys[counter]].add_occupant(human):
                    counter += 1
                    break
                else:
                    counter += 1
                    iters -= 1
                    if iters <= 0:
                        #WARNING - no vacancies, still homeless
                        break
                    continue


    # =============== PRINT DEBUGGING =======================

    def print_stats_living_quarter(self):
        output = []
        lq = self._get_all_living_quarters()
        for k,v in lq.items():
            output.append(len(v.occupants))
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
