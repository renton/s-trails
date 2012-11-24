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
                "clicked":lambda:self.load_table(self.population_menu,self.get_humans)

            },
            {
                "name":"DIPLOMACY",
                "clicked":lambda:self.load_table(self.main_menu,self.get_factions)

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

        self.station_location_menu = [
            {
                "name":"BACK",
                "clicked":lambda: self.load_home(self.main_menu),
            },
        ]

        self.population_menu = [
            {
                "name":"ALL PEOPLE",
                "clicked":lambda:self.load_table(self.population_menu,self.get_humans)
            },
            {
                "name":"LIVING QUARTERS",
                "clicked":lambda:self.load_table(self.population_menu,lambda: self.get_housing("living_quarters"))
            },
            {
                "name":"HOSPITALS",
                "clicked":lambda:self.load_table(self.population_menu,lambda: self.get_housing("hospital"))
            },
            {
                "name":"PRISONS",
                "clicked":lambda:self.load_table(self.population_menu,lambda: self.get_housing("prison"))
            },
            {
                "name":"OCCUPATION TYPES",
                "clicked":lambda:self.load_table(self.population_menu,self.get_occupation_types)
            },
            {
                "name":"BACK",
                "clicked":lambda: self.load_home(self.main_menu),
            },
        ]

        self.gui = gui_c.Gui()
        self.sim = Sim()
        self.load_event_popup(lambda: self.load_home(self.main_menu),"oh hi! welcome to an adventure.")

    def main_loop(self):
        self.gui.main_loop()

    ###################################################################################

    def load_home(self,menu):

        print len(self.sim.cur_events)
        if len(self.sim.cur_events) > 0:
            event = self.sim.cur_events.pop()
            self.load_event_popup(lambda: self.load_home(self.main_menu),event.text)
        else:
            home = HomeLocation(menu,self.get_overview(),self.get_locations())
            self.gui.load_template(home)

    def load_loading(self):
        pass

    def load_splash(self):
        pass

    def load_table(self,menu,tdata_callback):
        home = HomeTable(menu,self.get_overview(),{"update":tdata_callback})
        self.gui.load_template(home)

    def load_station_location(self,menu,location):
        #% random event (hostile, welcome, quest etc.)
        if randint(0,10) == 11:
            location_callback = self.get_station_location_lambda(location)
            self.load_event_popup(location_callback,"")
        else:
            station = HomeStationLocation(menu,self.get_overview(),self.get_station_location(location))
            self.gui.load_template(station)

    #next could be useful to string multiple popups
    def load_event_popup(self,next=None,text=""):

        t = EventPopupTemplate(
                                {
                                    "clicked":next,
                                },
                                image=(randint(0,255),randint(-1,255),randint(0,255)),
                                text=text)

        self.gui.load_template(t)

    ################################################################################################

    def get_inventory(self):
        data = {}
        data['title'] = "INVENTORY"
        data['header'] = ['name','quantity']
        data['rows'] = []
        data['width'] = [90,10]

        inventory = self.sim.ship.get_inventory()
        for k,v in inventory.items():
            row_data = [k,v]
            data['rows'].append({"data":row_data})
        return data

    def get_stores(self):
        data = {}
        data['title'] = "STORES"
        data['header'] = ['name','amount','capacity']
        data['rows'] = []
        data['width'] = [80,10,10]

        stores = self.sim.ship.get_all_storages()
        for k,v in stores.items():
            row_data = [v.name,v.get_total_items(),v.capacity]
            data['rows'].append({"data":row_data})
        return data

    def get_silos(self):
        data = {}
        data['title'] = "SILOS"
        data['header'] = ['name','type','amount','capacity']
        data['rows'] = []
        data['width'] = [50,30,10,10]

        silos = self.sim.ship.get_all_silos()
        for k,v in silos.items():
            row_data = [v.name,v.item_type,v.amount,v.capacity]
            data['rows'].append({"data":row_data})
        return data

    def get_housing(self,by_type=False):
        data = {}
        data['title'] = "LIVING QUARTERS"
        data['header'] = ['name','occupants','capacity']
        data['rows'] = []
        data['width'] = [50,30,20]

        rooms = self.sim.ship.get_all_livable_rooms(room_type=by_type)
        for k,v in rooms.items():
            row_data = [v.name,len(v.occupants),v.capacity]

            lq_callback = self.get_lq_id_filter_lambda(v.id)
            callbacks = [{"clicked":lq_callback},None,None]
            data['rows'].append({"data":row_data,"callbacks":callbacks})
        return data

    def get_humans(self,job_filter=False,lq_id_filter=False,job_room_id_filter=False):
        data = {}
        data['title'] = "CITIZENS"
        data['header'] = ['first','last','hp','hap','age','int','str','agi','cha','emp','cry','eth','job','home']
        data['rows'] = []
        data['width'] = [13,13,4,4,4,4,4,4,4,4,4,4,17,17]

        humans = self.sim.ship.humans
        for k,v in humans.items():
            if v.job:
                job = v.job['job']
                job_room_id = v.job['room'].id
            else:
                job = "NONE"
                job_room_id = None

            if v.lq:
                lq = v.lq.name
                lq_id = v.lq.id
            else:
                lq = "NONE"
                lq_id = None

            if (job_filter == False or job_filter == job) and (lq_id_filter == False or lq_id_filter == lq_id) and (job_room_id_filter == False or job_room_id_filter == job_room_id):
                row_data= [v.first_name,v.last_name,v.hp,v.stats['hap'],v.age,v.stats['int'],v.stats['str'],v.stats['agi'],v.stats['cha'],v.stats['emp'],v.stats['cry'],v.stats['eth'],job,lq]

                if lq_id:
                    lq_id_callback = self.get_lq_id_filter_lambda(lq_id)
                else:
                    lq_id_callback = None

                if job_room_id:
                    job_room_id_callback = self.get_job_room_id_filter_lambda(job_room_id)
                else:
                    job_room_id_callback = None
                callbacks = [None,None,None,None,None,None,None,None,None,None,None,None,{"clicked":job_room_id_callback},{"clicked":lq_id_callback}]

                data['rows'].append({"data":row_data,"callbacks":callbacks})
        return data

    def get_logs(self,log_type=-1,log_level=-1):
        data = {}
        data['title'] = "DAILY LOGS"
        data['header'] = ['level','log']
        data['rows'] = []
        data['width'] = [10,90]


        for k_type,v_type in self.sim.ship.daily_logs.items():
            if log_type == -1 or k_type == log_type:
                for k_level,v_level in v_type.items():
                    if log_level == -1 or k_level == log_level:
                        for log in v_level:
                            row_data = [k_level,log]
                            data['rows'].append({"data":row_data})
        return data

    # room type breakdown
    def get_rooms(self,type_filter=False):
        data = {}
        data['title'] = "ROOMS"
        data['header'] = ['name','occupants','employees','type','cond']
        data['rows'] = []
        data['width'] = [30,20,20,20,10]

        for k,v in self.sim.ship.rooms.items():
            if type_filter == False or type_filter == v.type:

                all_emps = len(v.get_all_employees())
                #TODO should distinguish between n/a and 0
                row_data = [v.name,len(v.occupants),all_emps,v.type,0]

                if len(v.occupants)>0:
                    occupant_filter = self.get_lq_id_filter_lambda(v.id)
                else:
                    occupant_filter = None

                if all_emps > 0:
                    emp_filter = self.get_job_room_id_filter_lambda(v.id)
                else:
                    emp_filter =None

                callbacks = [None,{"clicked":occupant_filter},{"clicked":emp_filter},None,None]
                data['rows'].append({"data":row_data,"callbacks":callbacks})
        return data

    def get_room_types(self):
        data = {}
        data['title'] = "ROOM TYPES"
        data['header'] = ['type','amount']
        data['rows'] = []
        data['width'] = [80,20]

        types = {}
        for k,v in self.sim.ship.rooms.items():
            if v.type not in types:
                types[v.type] = 0
            types[v.type] += 1

        for k,v in types.items():
            row_data = [k,v]
            room_filter = self.get_room_type_filter_lambda(k)
            callbacks = [{"clicked":room_filter},None]
            data['rows'].append({"data":row_data,"callbacks":callbacks})
        return data

    def get_occupation_types(self):
        data = {}
        data['title'] = "OCCUPATION TYPES"
        data['header'] = ['occupation','num']
        data['rows'] = []
        data['width'] = [80,20]
        data['callbacks'] = []

        types = {}
        for k,v in self.sim.ship.humans.items():
            if v.job:
                if v.job['job'] not in types:
                    types[v.job['job']] = 0
                types[v.job['job']] += 1

        for k,v in types.items():
            row_data = [k,v]
            job_filter = self.get_job_filter_lambda(k)
            callbacks = [{"clicked":job_filter},None]
            data['rows'].append({'data':row_data,'callbacks':callbacks})

        return data

    def get_factions(self):
        data = {}
        data['title'] = "FACTIONS"
        data['header'] = ['name','type','relations','power','currency']
        data['rows'] = []
        data['width'] = [50,20,10,10,10]

        for k,v in self.sim.factions.items():
            row_data = [v.name,v.f_type,v.relations,v.power,v.currency]
            data['rows'].append({"data":row_data})
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
        overview.append({"name":"DENSITY: "+str(self.sim.cur_density),"clicked":None})
        return overview

    def get_station_location(self,location):
        overview = []
        location = self.sim.cur_locations[location]
        overview.append({"name":"Name: "+str(location.name),"clicked":None})
        overview.append({"name":"Population: "+str(location.population),"clicked":None})
        overview.append({"name":"Faction: "+str(location.faction.name),"clicked":None})
        overview.append({"name":"Faction Power: "+str(location.faction.power),"clicked":None})
        overview.append({"name":"Trade Swindle Factor: "+str(location.trade_swindle_factor),"clicked":None})

        item_string = ""
        for k,v in location.demand_items.items():
            item_string += k +", "
        overview.append({"name":"Demand Items: "+str(item_string),"clicked":None})

        item_string = ""
        for k,v in location.surplus_items.items():
            item_string += k +", "
        overview.append({"name":"Surplus Items: "+str(item_string),"clicked":None})

        overview.append({"name":"Military Size: "+str(location.military_size),"clicked":None})
        overview.append({"name":"Relations: "+str(self.sim.factions[location.faction.id].relations),"clicked":None})
        overview.append({"name":"Currency Type: "+str(self.sim.factions[location.faction.id].currency),"clicked":None})
        return overview

    def get_locations(self):
        locations = []
        count = 0
        for location in self.sim.cur_locations:
            location_callback = self.get_station_location_lambda(count)
            locations.append({"name":str(location.name),"clicked":location_callback})
            count += 1
        return locations

    def get_station_location_lambda(self,location_index):
        return lambda:self.load_station_location(self.station_location_menu,location_index)

    def get_job_filter_lambda(self,job_type):
        return lambda:self.load_table(self.population_menu,lambda: self.get_humans(job_filter=job_type))

    def get_lq_id_filter_lambda(self,lq_id):
        return lambda:self.load_table(self.population_menu,lambda: self.get_humans(lq_id_filter=lq_id))

    def get_job_room_id_filter_lambda(self,job_room_id):
        return lambda:self.load_table(self.population_menu,lambda: self.get_humans(job_room_id_filter=job_room_id))

    def get_room_type_filter_lambda(self,room_type):
        return lambda:self.load_table(self.rooms_menu,lambda: self.get_rooms(type_filter=room_type))

t = TestGui()
t.main_loop()
