from gui.templates.base_template import *

class HomeLocation(BaseTemplate):
    def __init__(self,main_menu_data,overview_data,location_data):
        BaseTemplate.__init__(self)
        self.name = "home location"
        self.widgets.append(List(overview_data,20,20,200,300))
        self.widgets.append(List(main_menu_data,20,340,200,320))
        self.widgets.append(List(location_data,1146,340,200,320))

class HomeTable(BaseTemplate):
    def __init__(self,main_menu_data,overview_data,table_callbacks):
        BaseTemplate.__init__(self)
        self.name = "home table"
        self.widgets.append(List(overview_data,20,20,200,300))
        self.widgets.append(List(main_menu_data,20,340,200,320))
        self.widgets.append(Table(240,20,1106,730,callbacks=table_callbacks))

class HomeStationLocation(BaseTemplate):
    def __init__(self,main_menu_data,overview_data,station_data):
        BaseTemplate.__init__(self)
        self.name = "home station location"
        self.widgets.append(List(overview_data,20,20,200,300))
        self.widgets.append(List(main_menu_data,20,340,200,320))
        self.widgets.append(List(station_data,240,20,1106,730))
