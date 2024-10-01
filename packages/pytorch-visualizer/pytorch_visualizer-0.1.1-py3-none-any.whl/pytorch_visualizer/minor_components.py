from __future__ import annotations
from .parameters import GlobalParameters
from .persistent_vars import Persistent_Variables
from .draw_on_screen import Triangle, Text, Rect, Line
from .screen_operations import mass_update_component_state, display_all_componenets
import pygame 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screen_components import Components
class func_minor_components(GlobalParameters):

    func_minor_components_dict:dict[str, Components] = {}

    def __init__(self) -> None:
        self.initialise_components()
    
    def initialise_components(self):
        self.func_heading_text()
        self.vertical_seperator()

    @classmethod
    def func_heading_text(cls):
        cls.func_minor_components_dict[Persistent_Variables.FUNC_HEADING_TEXT] = Text(GlobalParameters.display_surface, GlobalParameters.font)

    @classmethod
    def vertical_seperator(cls):
        cls.func_minor_components_dict[Persistent_Variables.VERTICAL_BAR] = Line(Persistent_Variables.display_surface)

class Iteration_Count(GlobalParameters):

    def __init__(self) -> None:
        super().__init__()
        self.create_iter_count_text()

    @classmethod
    def initialize_iter_count_params(cls):
        cls.x = 50
        cls.y = 40

    @classmethod
    def create_iter_count_text(cls):
        cls.iteration_text = Text(GlobalParameters.display_surface, GlobalParameters.font)
        cls.iteration_text.mass_update_state({'text':f"Epoch: {GlobalParameters.curr_num_iterations}",
                                         'x':cls.x,
                                         'y':cls.y})
        
    def display_iter_count(self):
        self.iteration_text.mass_update_state({'text':f"Iteration: {GlobalParameters.curr_num_iterations}"})
        self.iteration_text.display()

# creating pause button
class Pause_button(GlobalParameters):

    def __init__(self) -> None:
        super().__init__()
        self.prev_surface_x_pos = 0
        self.create_button()

    @classmethod
    def initialize_pause_button_params(cls):
        cls.pause_button:pygame.Rect = None
        cls.rect_obj:Rect = None
        
        cls.x = GlobalParameters.screen_width/2
        cls.y = 40
        cls.rect_width = 80
        cls.rect_height = 30

        cls.button_color = (200, 200, 200)
        cls.button_hover_color = (170, 170, 170)
        cls.text_color = (0, 0, 0)

    @classmethod
    def create_button(cls):
        cls.rect_obj = Rect(cls.display_surface, cls.font)
        cls.rect_obj.text = Persistent_Variables.PAUSE_TEXT
        cls.rect_obj.mass_update_state({'text':Persistent_Variables.PAUSE_TEXT, 
                                         'x':cls.x,
                                         'y':cls.y,
                                         'rect_width':cls.rect_width,
                                         'rect_height':cls.rect_height,
                                         'text_color':cls.text_color})
        
        cls.pause_button = cls.rect_obj()
        
    def display_button(self):
        # to make the button to be stuck at the center
        if GlobalParameters.surface_x_pos != self.prev_surface_x_pos:
            x = self.x - GlobalParameters.surface_x_pos
            self.rect_obj.mass_update_state({'x':x})

        self.prev_surface_x_pos = GlobalParameters.surface_x_pos

        self.rect_obj.display()
        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        if self.pause_button.collidepoint(mouse_pos):
            current_color = self.button_hover_color
        else:
            current_color = self.button_color
        
        self.rect_obj.mass_update_state({'color':current_color})


# creating Navigation button
class Nav_Buttons(GlobalParameters):

    def __init__(self) -> None:
        super().__init__()
        self.prev_surface_x_pos = 0
        self.create_weight_grad_text()
        self.create_nav_arrows()

        self.text.update_default_state(var_dict=['x'], update_all=False)
        for _, button in self.nav_arrows.items():
            button.update_default_state(var_dict=['vertex1', 'vertex2', 'vertex3'], update_all=False)
    
    @classmethod
    def initialize_nav_buttons_params(cls):
        cls.animation_duration = 60

        cls.clicked_button = None 

        cls.last_update_time = None

        cls.gap = 120
        cls.triangle_height = 10
        cls.base = 20
        cls.height_from_base_of_screen = 20 # height from base of screen to lowest vertex

        cls.text:Text = None
        cls.animate_text = False
        cls.nav_arrows:dict[str, Triangle] = None 

        cls.curr_text_idx = 0

    def display_buttons_and_text(self):
        # to make the button and text stuck at the center
        if GlobalParameters.surface_x_pos != self.prev_surface_x_pos:
            self.update_button_pos()
            self.text.x = self.text.default_state['x'] - GlobalParameters.surface_x_pos
        
        self.prev_surface_x_pos = GlobalParameters.surface_x_pos

        self.text.display()
        display_all_componenets(self.nav_arrows)
        self.click_animation()

    def update_button_pos(self):
        for id, button in self.nav_arrows.items():

            x, y = button.default_state['vertex1']
            new_x = x - GlobalParameters.surface_x_pos
            button.vertex1 = new_x, y

            x, y = button.default_state['vertex2']
            new_x = x - GlobalParameters.surface_x_pos
            button.vertex2 = new_x, y

            x, y = button.default_state['vertex3']
            new_x = x - GlobalParameters.surface_x_pos
            button.vertex3 = new_x, y

    

    @classmethod
    def update_curr_text_idx(cls, back=False):
        if back:
            if cls.curr_text_idx - 1 >= 0:
                cls.animate_text = True
                cls.curr_text_idx -= 1
            else:
                cls.animate_text = False
        else:
            if cls.curr_text_idx < cls.total_num_iterations-1:
                cls.animate_text = True
                cls.curr_text_idx += 1
            else:
                cls.animate_text = False

    @classmethod
    def current_time(self):
        return pygame.time.get_ticks()
    
    @classmethod
    def create_nav_arrows(cls):
        # generate left and right triangles 
        
        # for left arrow 
        # Top vertex
        l_vertex1 = cls.screen_width/2 - cls.gap - cls.triangle_height, cls.screen_height - cls.height_from_base_of_screen - cls.base/2
        # lower base vertex
        l_vertex2 = cls.screen_width/2 - cls.gap, cls.screen_height - cls.height_from_base_of_screen
        # upper base vertex
        l_vertex3 = cls.screen_width/2 - cls.gap, cls.screen_height - cls.height_from_base_of_screen - cls.base

        # for Right arrow
        # Top vertex
        r_vertex1 = cls.screen_width/2 + cls.gap + cls.triangle_height, cls.screen_height - cls.height_from_base_of_screen - cls.base/2
        # lower base vertex
        r_vertex2 = cls.screen_width/2 + cls.gap, cls.screen_height - cls.height_from_base_of_screen
        # upper base vertex
        r_vertex3 = cls.screen_width/2 + cls.gap, cls.screen_height - cls.height_from_base_of_screen - cls.base

        # create the triangles 

        prev_arrow = Triangle(cls.display_surface, l_vertex1, l_vertex2, l_vertex3)
        next_arrow = Triangle(cls.display_surface, r_vertex1, r_vertex2, r_vertex3)
        cls.nav_arrows = {Persistent_Variables.PREV_ARROW:prev_arrow, Persistent_Variables.NEXT_ARROW:next_arrow}

        return cls.nav_arrows
    
    @classmethod
    def create_weight_grad_text(cls):
        # create text
        weight_grad_text = Text(cls.display_surface, cls.font)
        weight_grad_text.mass_update_state({'x':cls.screen_width/2, 
                                            'y':cls.screen_height-cls.height_from_base_of_screen-cls.base/2, 
                                            'text':f'weight = {GlobalParameters.line_weight}, grad = {GlobalParameters.line_grad}'})
        cls.text = weight_grad_text
        return cls.text
    
    @classmethod
    def update_line_weight_grad_text(cls):
        cls.text.mass_update_state({'text':f'weight = {GlobalParameters.line_weight}, grad = {GlobalParameters.line_grad}'})
    
    @classmethod
    def update_node_bias_grad_text(cls):
        cls.text.mass_update_state({'text':f'bias = {GlobalParameters.node_bias}, grad = {GlobalParameters.node_grad}'})
    
    @classmethod
    def click_animation(cls):
        nav_arrows = cls.nav_arrows
        if cls.clicked_button:
            duration = cls.current_time() - cls.last_update_time
            if duration < cls.animation_duration:
                mass_update_component_state(nav_arrows[cls.clicked_button], {'color':(128, 128, 128)})
                if cls.animate_text:
                    cls.text.mass_update_state({'color':(128, 128, 128)})
            else:
                mass_update_component_state(nav_arrows[cls.clicked_button], {'color':(0, 0, 0)})
                if cls.animate_text:
                    cls.text.mass_update_state({'color':(0, 0, 0)})
    