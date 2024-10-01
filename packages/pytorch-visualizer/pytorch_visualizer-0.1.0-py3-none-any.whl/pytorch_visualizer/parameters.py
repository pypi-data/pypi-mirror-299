from __future__ import annotations
import pygame 
from typing import Dict, TYPE_CHECKING
from .generators_and_utility_functions import convert_list_to_generator, map_to_comp_weights
from .constants import String_Constants

if TYPE_CHECKING:
    from .persistent_vars import Persistent_Variables

class GlobalParameters(String_Constants):
    """A class containing global parameters and methods"""

    @classmethod
    def initialize_core_params(cls):
        pygame.init()
        cls.display_info = pygame.display.Info()
        cls.adjust_size_by = 100 
        cls.screen_width = cls.display_info.current_w - cls.adjust_size_by
        cls.screen_height = cls.display_info.current_h - cls.adjust_size_by

        display_surface_width = 3000

        cls.screen =  pygame.display.set_mode((cls.screen_width, cls.screen_height))
        cls.display_surface = pygame.Surface((display_surface_width, cls.screen_height))

        cls.surface_x_pos = 0
        cls.surface_y_pos = 0
        cls.scroll_speed = 5
        cls.scroll_camera_x = 0

        # Animation properties
        cls.clock = pygame.time.Clock()

        # Initialize font
        pygame.font.init()

        try:
            cls.font = pygame.font.Font('./pytorch_visualizer/ARIAL.TTF', 18)
        except:
            cls.font = pygame.font.SysFont(None, 20)

        # set window caption
        pygame.display.set_caption('Neural Network Visualization')

        # Layer and component properties
        cls.spaces_between_layers = [150]
        cls.node_radius = 40
        cls.initial_x = 100

        # --------------------------Execution Properties---------------------------------#
        cls.execution_order:list[str] = []
        cls.execution_function_objects:Dict[str, Persistent_Variables]
        cls.all_nn_data = [] # TODO i am not need this variable any longer
        cls.all_target_data = [] # The target data
        cls.update_once = True # General tracker for update a class variable once
        cls.extracted_nn_structure = [] # nn structure gotten from the model forward function.
        cls.main_nn_structure = []
        cls.current_func_id_idx:int = 0
        cls.is_func_id_changed = False

        cls.start_execution_order_gen = None
        cls.serialise_all_target_data_gen = None
        cls.curr_target_data = None

        cls.pause = False

        # -----------------------Weight grad parameters---------------------------#
        """These parameters should be stored directly here, not via some child class"""
        cls.line_idx_to_weight_map:dict[str, list] = None

        cls.line_idx_to_grad_map:dict[str, list] = None

        cls.node_idx_to_bias_map:dict[str, list] = None 

        cls.node_idx_to_grad_map:dict[str, list] = None

        cls.line_weight_idx = (None, None) # the first element is the line idx, while the second is the func_id_name 

        cls.node_bias_idx = (None, None) # the first element is the Node idx, while the second is the func_id_name

        cls.node_color_before_click = (0, 0, 0) # defaultly set to black

        cls.line_weight = 0

        cls.line_grad = 0

        cls.node_grad = 0

        cls.node_bias = 0

        cls.curr_num_iterations = 1

        cls.total_num_iterations = None
        # --------------------------------General time-----------------------------------#
        cls.last_update_time = None

    @classmethod
    def get_last_update_time(cls):
        cls.last_update_time = pygame.time.get_ticks()

    @classmethod
    def initialise_target_data(cls):
        if cls.all_target_data:
            cls.serialise_all_target_data_gen = convert_list_to_generator(cls.all_target_data)
            cls.curr_target_data = next(cls.serialise_all_target_data_gen)

    @classmethod
    def execution_order_gen(cls):
        for idx, func_id in enumerate(cls.execution_order):
            yield func_id, idx

    @classmethod
    def initialise_exec_order(cls):
        cls.start_execution_order_gen = cls.execution_order_gen()
        _, cls.current_func_id_idx = next(cls.start_execution_order_gen)
        GlobalParameters.is_func_id_changed = True
    
    @classmethod
    def update_line_weight_and_grad(cls, line_idx:str, weight_idx:int):
        weight = map_to_comp_weights(line_idx, weight_idx, cls.line_idx_to_weight_map)
        grad = map_to_comp_weights(line_idx, weight_idx, cls.line_idx_to_grad_map)
        cls.line_weight = weight
        cls.line_grad = grad

        
    
    @classmethod
    def update_node_grad_and_bias(cls, node_idx:str, weight_idx:int):
        bias = map_to_comp_weights(node_idx, weight_idx, cls.node_idx_to_bias_map)
        node_grad = map_to_comp_weights(node_idx, weight_idx, cls.node_idx_to_grad_map)

        cls.node_bias = bias
        cls.node_grad = node_grad
            



            


