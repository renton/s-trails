from gui.widgets.base_widget import *

#title row (top)
#control row (bottom)

class Table(BaseWidget):

    INIT_PAGE = 0
    INIT_SORT = 0

    INIT_TABLE_PADDING = 6

    INIT_TITLE_HEIGHT = 30

    INIT_CONTROLBAR_HEIGHT = 30

    INIT_ROW_HEIGHT = 24
    INIT_ROWS_PER_PAGE = 19

    INIT_HEADER_BACKGROUND_COLOR = (0,0,50)
    INIT_ALT_ROW_BACKGROUND_COLOR = (0,0,125)

    def __init__(self,left,top,width,height,callbacks=None):
        BaseWidget.__init__(self,left,top,width,height,callbacks=callbacks)
        self.current_page = Table.INIT_PAGE
        self.update_table()

    def update_table(self):
        table_data = self.fire_callback("update")
        self.sub_widgets = []

        self.pages = len(table_data['data'])/Table.INIT_ROWS_PER_PAGE
        start_record = Table.INIT_ROWS_PER_PAGE * self.current_page
        end_record = start_record + Table.INIT_ROWS_PER_PAGE
        table_data['data'] = table_data['data'][start_record:end_record]

        y_pos = self.top+self.border_width+Table.INIT_TABLE_PADDING
        x_pos = self.left+self.border_width+Table.INIT_TABLE_PADDING

        self.sub_widgets.append(BaseWidget(
                                            x_pos,
                                            y_pos,
                                            self.width - (self.border_width*2) - (Table.INIT_TABLE_PADDING*2),
                                            Table.INIT_TITLE_HEIGHT,
                                            text=(str(table_data['title'])+" "+str(self.current_page+1)+":"+str(self.pages+1)).upper(),
                                            border=0))

        y_pos += Table.INIT_TITLE_HEIGHT
        cell_width = (self.width-(self.border_width*2)-(Table.INIT_TABLE_PADDING*2))/len(table_data['header'])

        for data in table_data['header']:
            self.sub_widgets.append(BaseWidget(
                                                x_pos,
                                                y_pos,
                                                cell_width,
                                                Table.INIT_ROW_HEIGHT,
                                                text=str(data).upper(),
                                                border=0,
                                                bg_color=Table.INIT_HEADER_BACKGROUND_COLOR))
            x_pos += cell_width

        x_pos = self.left+self.border_width+Table.INIT_TABLE_PADDING
        y_pos += Table.INIT_ROW_HEIGHT

        row_count = 0
        for data in table_data['data']:
            for record in data:

                if row_count % 2:
                    row_bg_color = None
                else:
                    row_bg_color = Table.INIT_ALT_ROW_BACKGROUND_COLOR


                self.sub_widgets.append(BaseWidget(
                                                    x_pos,
                                                    y_pos,
                                                    cell_width,
                                                    Table.INIT_ROW_HEIGHT,
                                                    text=str(record).upper(),
                                                    border=0,
                                                    bg_color=row_bg_color))
                x_pos += cell_width
            x_pos = self.left+self.border_width+Table.INIT_TABLE_PADDING
            y_pos += Table.INIT_ROW_HEIGHT
            row_count +=1


        y_pos = self.top+self.border_width+(Table.INIT_TABLE_PADDING*2)+(Table.INIT_ROW_HEIGHT*Table.INIT_ROWS_PER_PAGE)+(Table.INIT_ROW_HEIGHT*2)

        if not self.is_last_page():
            self.sub_widgets.append(BaseWidget(
                                                (self.left+self.width)-Table.INIT_TABLE_PADDING-100,
                                                y_pos,
                                                100,
                                                Table.INIT_CONTROLBAR_HEIGHT,
                                                text="NEXT",
                                                border=0,bg_color=(32,32,32),
                                                callbacks={"clicked":self.inc_page}))


        if not self.is_first_page():
            self.sub_widgets.append(BaseWidget(
                                                x_pos+Table.INIT_TABLE_PADDING,
                                                y_pos,
                                                100,
                                                Table.INIT_CONTROLBAR_HEIGHT,
                                                text="PREV",
                                                border=0,
                                                callbacks={"clicked":self.dec_page}))

    def inc_page(self):
        if not self.is_last_page():
            self.current_page += 1
            self.update_table()

    def dec_page(self):
        if not self.is_first_page():
            self.current_page -= 1
            self.update_table()

    def is_last_page(self):
        return self.current_page >= self.pages

    def is_first_page(self):
        return self.current_page == 0