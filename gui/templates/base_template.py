from gui.widgets.base_widget import *
from gui.widgets.list import *
from gui.widgets.table import *

class BaseTemplate():
    def __init__(self):
        self.name = "base"
        self.widgets = []

    def draw(self,pygame,screen,font):
        for widget in self.widgets:
            widget.draw(pygame,screen,font)

    def get_widgets_with_callbacks(self,callback_type):
        widgets = []
        for widget in self.widgets:
            widgets += widget.get_widgets_with_callbacks(callback_type)
        return widgets
