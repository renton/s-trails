from gui.templates.base_template import *

class EventPopupTemplate(BaseTemplate):
    def __init__(self,pass_event_callback=None,image=None,text=None):
        BaseTemplate.__init__(self)
        self.name = "event"
        self.text = text
        widget1 = BaseWidget(500,500,200,50,callbacks=pass_event_callback)
        widget2 = BaseWidget(200,40,400,300)
        self.widgets = [widget1,widget2]
