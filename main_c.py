from gui import gui_c
from gui.templates.events import *
from gui.templates.home_location import *
from random import randint
from classes.sim import *

class TestGui():

    def __init__(self):

        self.main_menu = [

            {
                "name":"LOCATION",
                "clicked":lambda:self.load_home(self.main_menu)
            },
            {
                "name":"LOGS",
                "clicked":lambda:self.load_table(self.logs_menu,lambda: self.get_logs(-1,0))
            },
            {
                "name":"ROOMS",
                "clicked":lambda:self.load_table(self.rooms_menu,self.get_rooms)
            },
            {
                "name":"INVENTORY",
                "clicked":lambda:self.load_table(self.inventory_menu,self.get_inventory)

            },
            {
                "name":"POPULATION",
                "clicked":lambda:self.load_table(self.main_menu,self.get_humans)

            },
            {
                "name":"STEP",
                "clicked":self.step_day,

            },

        ]

        self.inventory_menu = [
            {
                "name":"ITEMS",
                "clicked":lambda:self.load_table(self.inventory_menu,self.get_inventory)
            },
            {
                "name":"STORES",
                "clicked":lambda:self.load_table(self.inventory_menu,self.get_stores)
            },
            {
                "name":"SILOS",
                "clicked":lambda:self.load_table(self.inventory_menu,self.get_silos)
            },
            {
                "name":"BACK",
                "clicked":lambda: self.load_home(self.main_menu),
            },
        ]

        self.rooms_menu = [
            {
                "name":"ALL ROOMS",
                "clicked":lambda:self.load_table(self.rooms_menu,self.get_rooms)
            },
            {
                "name":"ROOM TYPES",
                "clicked":lambda:self.load_table(self.rooms_menu,self.get_room_types)
            },
            {
                "name":"BACK",
                "clicked":lambda: self.load_home(self.main_menu),
            },
        ]

        self.logs_menu = [
            {
                "name":"WARNINGS",
                "clicked":lambda:self.load_table(self.logs_menu,lambda: self.get_logs(-1,0))
            },
            {
                "name":"INVENTORY LOGS",
                "clicked":lambda:self.load_table(self.logs_menu,lambda: self.get_logs(0,-1))
            },
            {
                "name":"ROOM LOGS",
                "clicked":lambda:self.load_table(self.logs_menu,lambda: self.get_logs(1,-1))
            },
            {
                "name":"HUMAN LOGS",
                "clicked":lambda:self.load_table(self.logs_menu,lambda: self.get_logs(2,-1))
            },
            {
                "name":"BACK",
                "clicked":lambda: self.load_home(self.main_menu),
            },
        ]

        self.gui = gui_c.Gui()
        self.sim = Sim()
        self.load_home(self.main_menu)

    def main_loop(self):
        self.gui.main_loop()

    ###################################################################################

    def load_home(self,menu):
        home = HomeLocation(menu,self.get_overview())
        self.gui.load_template(home)

    def load_loading(self):
        pass

    def load_splash(self):
        pass

    def load_table(self,menu,tdata_callback):
        home = HomeTable(menu,self.get_overview(),{"update":tdata_callback})
        self.gui.load_template(home)

    #next could be useful to string multiple popups
    def load_event_popup(self,next=None):

        t = EventPopupTemplate(
                                {
                                    "clicked":next,
                                },
                                image=(randint(0,255),randint(-1,255),randint(0,255)))

        self.gui.load_template(t)

    ################################################################################################

    def get_inventory(self):
        data = {}
        data['title'] = "INVENTORY"
        data['header'] = ['name','quantity']
        data['data'] = []

        inventory = self.sim.ship.get_inventory()
        for k,v in inventory.items():
            data['data'].append([k,v])
        return data

    def get_stores(self):
        data = {}
        data['title'] = "STORES"
        data['header'] = ['name','amount','capacity']
        data['data'] = []

        stores = self.sim.ship.get_all_storages()
        for k,v in stores.items():
            data['data'].append([v.name,v.get_total_items(),v.capacity])

        return data

    def get_silos(self):
        data = {}
        data['title'] = "SILOS"
        data['header'] = ['name','type','amount','capacity']
        data['data'] = []

        silos = self.sim.ship.get_all_silos()
        for k,v in silos.items():
            data['data'].append([v.name,v.item_type,v.amount,v.capacity])
        return data

    def get_humans(self):
        data = {}
        data['title'] = "CITIZENS"
        data['header'] = ['first','last','age','job']
        data['data'] = []

        humans = self.sim.ship.humans
        for k,v in humans.items():
            if v.job:
                job = v.job['job']
            else:
                job = "NONE"

            data['data'].append([v.first_name,v.last_name,v.age,job])
        return data

    def get_logs(self,log_type=-1,log_level=-1):
        data = {}
        data['title'] = "DAILY LOGS"
        data['header'] = ['level','log']
        data['data'] = []


        print self.sim.ship.daily_logs[0]

        for k_type,v_type in self.sim.ship.daily_logs.items():
            if log_type == -1 or k_type == log_type:
                for k_level,v_level in v_type.items():
                    if log_level == -1 or k_level == log_level:
                        for log in v_level:
                            data['data'].append([k_level,log])
        return data

    # room type breakdown
    def get_rooms(self):
        data = {}
        data['title'] = "ROOMS"
        data['header'] = ['name','type','cond']
        data['data'] = []

        for k,v in self.sim.ship.rooms.items():
            data['data'].append([v.name,v.type,0])
        return data

    def get_room_types(self):
        data = {}
        data['title'] = "ROOM TYPES"
        data['header'] = ['type','amount']
        data['data'] = []

        types = {}
        for k,v in self.sim.ship.rooms.items():
            if v.type not in types:
                types[v.type] = 0
            types[v.type] += 1

        for k,v in types.items():
            data['data'].append([k,v])
        return data

    def step_day(self):
        self.sim.step_day()
        self.load_home(self.main_menu)

    def get_overview(self):
        overview = []
        date = str(self.sim.day)+" "+str(self.sim.year)
        overview.append({"name":"Date: "+str(date),"clicked":None})
        overview_items = self.sim.ship.get_overview()
        for k,v in overview_items.items():
           overview.append({"name":str(k)+": "+str(v[0])+" "+str(v[2]),"clicked":None})
        overview.append({"name":"POPULATION: "+str(len(self.sim.ship.humans)),"clicked":None})
        return overview

t = TestGui()
t.main_loop()
