from gui.widgets.base_widget import *

class List(BaseWidget):

    LIST_ENTRY_HEIGHT = 30
    LIST_ENTRY_PADDING = 10
    LIST_ENTRY_MARGIN = 8

    LIST_HOVER_TEXT_COLOR = (200,200,200)

    def __init__(self,list_data,left,top,width,height):
        BaseWidget.__init__(self,left,top,width,height)
        self.list_data = list_data
        self._populate_list()

    #HOVER TO CHANGE TEXT COLOR
    def _populate_list(self):
        y_pos = 0
        for entry in self.list_data:
            new_list_entry = BaseWidget(
                                        self.left+self.border_width+List.LIST_ENTRY_PADDING,
                                        self.top+y_pos+self.border_width+List.LIST_ENTRY_PADDING,
                                        self.width-(self.border_width*2)-(List.LIST_ENTRY_PADDING*2),
                                        List.LIST_ENTRY_HEIGHT,
                                        callbacks={
                                            "clicked":entry['clicked']
                                        },
                                        text=entry['name'])
            new_list_entry.border_width = 0
            self.sub_widgets.append(new_list_entry)
            y_pos += List.LIST_ENTRY_MARGIN + List.LIST_ENTRY_HEIGHT
