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
                "clicked":lambda:self.load_table(self.main_menu,self.get_logs)
            },
            {
                "name":"ROOMS",
                "clicked":lambda:self.load_table(self.main_menu,self.get_rooms)
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

        self.gui = gui_c.Gui()
        self.load_home(self.main_menu)
        self.sim = Sim()

    def main_loop(self):
        self.gui.main_loop()

    def load_home(self,menu):
        home = HomeLocation(menu)
        self.gui.load_template(home)

    def load_loading(self):
        pass

    def load_splash(self):
        pass

    def refresh(self):
        self.gui.update()

    def load_table(self,menu,tdata_callback):
        home = HomeTable(menu,{"update":tdata_callback})
        self.gui.load_template(home)

    #next could be useful to string multiple popups
    def load_event_popup(self,next=None):

        t = EventPopupTemplate(
                                {
                                    "clicked":next,
                                },
                                image=(randint(0,255),randint(-1,255),randint(0,255)))

        self.gui.load_template(t)

    ###

    def get_empty_data(self):
        return {"header":[],"data":[]}

    def get_sample_data(self):

        data = []

        for i in range(100):
            data.append([randint(0,100),randint(0,100),randint(0,100),randint(0,100)])

        return {
                "title":"SAMPLE DATA",
                "header":[
                    "COL1",
                    "COL2",
                    "COL3",
                    "COL4",
                ],
                "data":data
                }

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

    def get_logs(self):
        data = {}
        data['title'] = "DAILY LOGS"
        data['header'] = ['log']
        data['data'] = []

        for k,v in self.sim.ship.daily_logs.items():
            for log in v:
                data['data'].append([log])
        return data

    def get_rooms(self):
        data = {}
        data['title'] = "ROOMS"
        data['header'] = ['name','type','cond']
        data['data'] = []

        for k,v in self.sim.ship.rooms.items():
            data['data'].append([v.name,v.type,0])
        return data

    def step_day(self):
        self.sim.step_day()
        self.load_home(self.main_menu)

t = TestGui()
t.main_loop()
