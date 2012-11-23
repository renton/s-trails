import pygame, sys
from pygame.locals import *

from gui.templates.base_template import *

class Gui():

    WINDOW_SIZE_X = 800
    WINDOW_SIZE_Y = 600
    WINDOW_BACKGROUND_COLOR = (0,0,0)
    WIDGET_BACKGROUND_COLOR = (255,0,0)
    FONT_COLOR = (255,255,255)
    FONT_SIZE = 8

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((Gui.WINDOW_SIZE_X, Gui.WINDOW_SIZE_Y), 0, 32)
        pygame.display.set_caption('Hello world!')

        # set up fonts
        self.font = pygame.font.Font("gui/nintendo_nes.ttf", Gui.FONT_SIZE)

        # set up the text
        #text = self.font.render('Hello world!', True, WHITE, BLUE)
        #textRect = text.get_rect()
        #textRect.centerx = windowSurface.get_rect().centerx
        #textRect.centery = windowSurface.get_rect().centery

        # draw the white background onto the surface
        self.screen.fill(Gui.WINDOW_BACKGROUND_COLOR)

        # draw a green polygon onto the surface
        #pygame.draw.polygon(windowSurface, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

        # draw some blue lines onto the surface
        #pygame.draw.line(windowSurface, BLUE, (60, 60), (120, 60), 4)
        #pygame.draw.line(windowSurface, BLUE, (120, 60), (60, 120))
        #pygame.draw.line(windowSurface, BLUE, (60, 120), (120, 120), 4)

        # draw a blue circle onto the surface
        #pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)

        # draw a red ellipse onto the surface
        #pygame.draw.ellipse(windowSurface, RED, (300, 250, 40, 80), 1)

        # draw the text's background rectangle onto the surface
        #pygame.draw.rect(windowSurface, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

        # get a pixel array of the surface
        #pixArray = pygame.PixelArray(windowSurface)
        #pixArray[480][380] = WHITE
        #del pixArray

        # draw the text onto the surface
        #windowSurface.blit(text, textRect)

        # draw the window onto the screen

    def load_template(self,template):
        self.current_template = template
        self.update()

    def update(self):
        self.screen.fill(Gui.WINDOW_BACKGROUND_COLOR)
        self.current_template.draw(pygame,self.screen,self.font)
        pygame.display.update()

    def main_loop(self):
        # run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    (m_x,m_y) = pygame.mouse.get_pos()
                    for widget in self.current_template.get_widgets_with_callbacks("clicked"):
                        rect = pygame.Rect(widget.left, widget.top, widget.width, widget.height)
                        if rect.collidepoint(m_x,m_y):
                            widget.fire_callback("clicked")
                            self.update()
                        del rect
