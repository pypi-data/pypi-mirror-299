import pygame
from abc import ABC, abstractmethod
from .screen_state import ScreenState
from .screen_operations import *

class Components(ScreenState, ABC):
    def __init__(self, window, font=None, visible=True, throbbing=False) -> None:

        super().__init__()

        # Gui parameters 
        self.window = window
        self.font = font
        self.visible= visible
        self.throbbing = throbbing 
        self.color = (0, 0, 0) # colour is set to black by default
        self.node_radius = 40
        self.move_component_gen = None
        #self.node_width = 3

    @abstractmethod
    def get_component():
        """Abstract method that must be implemented by subclasses"""
        pass

    def move_component(self, end_coor:tuple[float], factor:int=30):

        x = self.x
        y = self.y

        x_end_coor, y_end_coor = end_coor

        if x_end_coor == None:
            x_end_coor = self.x
        if y_end_coor == None:
            y_end_coor = self.y

        diff_x = x_end_coor - x
        diff_y = y_end_coor - y

        fraction_dist_x = diff_x/factor

        fraction_dist_y = diff_y/factor

        for _ in range(factor):
            #self.window.fill((255, 255, 255)) # clear streaks
            self.x += fraction_dist_x
            self.y += fraction_dist_y

            self.display()
            pygame.display.flip() # update the display
            pygame.time.delay(15)


    def move_component_generator(self, end_coor:tuple[float], factor:int=30):

        x = self.x
        y = self.y

        x_end_coor, y_end_coor = end_coor

        if x_end_coor == None:
            x_end_coor = self.x
        if y_end_coor == None:
            y_end_coor = self.y

        diff_x = x_end_coor - x
        diff_y = y_end_coor - y

        fraction_dist_x = diff_x/factor

        fraction_dist_y = diff_y/factor


        for _ in range(factor):
            #self.window.fill((255, 255, 255)) # clear streaks
            self.x += fraction_dist_x
            self.y += fraction_dist_y

            yield
    






