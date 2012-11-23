class BaseWidget():

    DEFAULT_BORDER_WIDTH = 2
    DEFAULT_BORDER_COLOR = (255,255,255)

    def __init__(self,left,top,width,height,callbacks=None,text=None,border=2,bg_color=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        if bg_color:
            self.background_color = bg_color
        else:
            self.background_color = (0,0,100)

        self.sub_widgets = []
        self.border_width = border
        self.border_color = BaseWidget.DEFAULT_BORDER_COLOR

        self.text = text

        self.callbacks = {}
        if callbacks:
            for k,v in callbacks.items():
                self.callbacks[k] = v

    def draw(self,pygame,screen,font):

        border = pygame.Rect(self.left,self.top,self.width,self.height)
        pygame.draw.rect(screen,self.border_color,(border.left, border.top, border.width, border.height))

        rect = pygame.Rect(self.left+self.border_width,self.top+self.border_width,self.width-(self.border_width*2),self.height-(self.border_width*2))
        pygame.draw.rect(screen,self.background_color,(rect.left, rect.top, rect.width, rect.height))

        #based on font size
        if self.text:
            textrect = pygame.Rect(
                rect.left+10,
                rect.top+(rect.height/2),
                rect.width,
                rect.height/2)

            text = font.render(self.text, True, (255,255,255), self.background_color)
            screen.blit(text,textrect)

        for widget in self.sub_widgets:
            widget.draw(pygame,screen,font)

    def get_widgets_with_callbacks(self,callback_type):
        widgets = []
        if callback_type in self.callbacks:
            widgets.append(self)
        for widget in self.sub_widgets:
            widgets += widget.get_widgets_with_callbacks(callback_type)
        return widgets

    def fire_callback(self,event_type):
        if event_type in self.callbacks:
            if self.callbacks[event_type]:
                return self.callbacks[event_type]()
