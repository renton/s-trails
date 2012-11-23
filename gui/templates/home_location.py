from gui.templates.base_template import *

class HomeLocation(BaseTemplate):
    def __init__(self,main_menu_data):
        BaseTemplate.__init__(self)
        self.name = "home location"
        self.widgets.append(BaseWidget(20,20,200,100))
        self.widgets.append(List(main_menu_data,20,140,200,320))
        self.widgets.append(BaseWidget(20,480,200,100))

class HomeTable(BaseTemplate):
    def __init__(self,main_menu_data,table_callbacks):
        BaseTemplate.__init__(self)
        self.name = "home table"
        self.widgets.append(BaseWidget(20,20,200,100))
        self.widgets.append(List(main_menu_data,20,140,200,320))
        self.widgets.append(BaseWidget(20,480,200,100))
        self.widgets.append(Table(240,20,540,560,callbacks=table_callbacks))
