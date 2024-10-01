from typing import Any, List, Dict, TYPE_CHECKING
import math
import pygame
from .parameters import GlobalParameters 
from .generators_and_utility_functions import *

if TYPE_CHECKING:
    from .draw_on_screen import Line, Nodes

class Persistent_Variables(GlobalParameters):
    """A class required to initialise all persistent variables"""

    def __init__(self, 
                 nodes, 
                 lines, 
                 nn_structure,
                 total_data:List[List[List[Any]]],
                 backward=False,
                 local_execution_order=None,
                 from_layer=1,
                 to_layer=None) -> None:
        
        self.nodes:Dict[str, Nodes] = nodes
        self.lines:Dict[str, Line] = lines
        self.nn_structure = nn_structure
        self.ideal_nn_structure = nn_structure # but it might be changed though in case of crossentropy loss
        self.target_node:dict[str, Nodes] = None 
        
        self.from_layer = from_layer
        self.to_layer = to_layer
        #self.func_id_name = func_id_name
        #self.num_layer = self.func_num_layers(self.func_id_name)
        

        # function call or activate counts 
        self.subsequent_throbbed_nodes_count = 0
        self.activate_forward_pass = False
        self.activate_softmax = False
        self.activate_nllloss = False 
        self.activate_main_nllloss = False
        self.activate_move_nodes = False
        self.activate_backward_pass = False
        self.activate_activation = False
        self.activate_crossentropy_loss = False
        self.activate_ce_nllloss = False
        self.activate_logsoftmax = False

        # end of functions 
        self.is_end_forward_pass = False 
        self.is_end_of_standalone_forward_pass = False
        self.standalone_end_count = 1
        self.text_finished = False

        # Temporary storage 
        self.buffer = None 
        self.extra_data:dict[str, list|Any] = {} # a store of miscelleanous data to be used during visualization
        self.local_execution_order = local_execution_order

        # general conditional
        self.run_once = True
        self.standalone_run_once = True
        self.static = False # used as a condition to determine what to view even when a function is not activated.
        self.standalone_static = False

        # Time
        #self.last_update_time = None
        #self.current_time = None
        self.elapsed_time = None
        self.total_data:list[list[list[float]]] = total_data
        self.nn_data:list[list[float]] = None
        self.all_activation_data:list[list[list[float]]] = None

        # throbbing properties 
        self.throb_speed = 0.1
        self.throb_duration = 1000
        #self.throb_value = abs(math.sin(pygame.time.get_ticks() * self.throb_speed))

        # Starting Generators
        self.backward = backward # generator order

        self.start_generators()

        if self.local_execution_order is not None:
            # ids with the same name will share the same boolean
            self.local_run_once = {func_id_name:True for func_id_name, _ in self.local_execution_order}
            self.local_static = {func_id_name:False for func_id_name, _ in self.local_execution_order}
            self.current_local_func_id_idx = None
            self.end_of_local_execution_order = False
            self.start_local_execution_order_gen = self.local_execution_order_gen()
            self.next_local_func_id()

        # output of generator
        self.lines_idxs = None
        self.nodes_idxs = None
        self.texts = None
        self.activation_data_per_epoch = None
        self.subsequent_layer_nodes_throbbing = None
        self.current_layer_nodes = None
        self.node_idx = None

        # initialise time
        self.get_last_update_time()

        # get first output of generator
        if len(self.nn_structure) > 1:
            self.next_lines_idxs()
            self.next_nodes_idxs()

            self.next_texts()
            self.next_subsequent_layer_nodes_throbbing()

    #-----------------------------------------Start Generators------------------------------------------#
    def start_generators(self):
        # Get text
        self.text_per_epoch_gen = convert_list_to_generator(self.total_data)
        self.next_text_per_epoch()

        # start nodes, lines and text generators 
        if len(self.nn_structure) > 1:
            if not self.backward:
                self.lines_throb_idxs_gen = lines_to_throb_generator(self.nn_structure, 
                                                                    from_layer=self.from_layer, 
                                                                    to_layer=self.to_layer)
            else:
                self.lines_throb_idxs_gen = backward_lines_to_throb_generator(self.nn_structure, 
                                                                            from_layer=self.from_layer, 
                                                                            to_layer=self.to_layer)


            self.nodes_throb_idxs_gen = nodes_to_throb_generator(self.nn_structure, 
                                                                from_layer=self.from_layer, 
                                                                to_layer=self.to_layer, 
                                                                backward=self.backward)
            
            self.subsequent_nodes_in_layer_gen = layer_nodes_generator(self.nn_structure, 
                                                                        generate_from_layer=2, 
                                                                        from_layer=self.from_layer, 
                                                                        to_layer=self.to_layer, 
                                                                        backward=self.backward)

            self.text_gen = text_generator(self.nn_data, backward=self.backward)
        
        if len(self.nn_structure) == 1:
            self.node_text = None
            self.node_text_gen = self.layer_node_text_generator(self.nn_data)
            self.next_node_text()


        self.current_nodes_in_layer_gen = layer_nodes_generator(self.nn_structure, 
                                                                generate_from_layer=1, 
                                                                from_layer=self.from_layer, 
                                                                to_layer=self.to_layer, 
                                                                backward=self.backward)
        self.serialise_node_gen = None 

        self.activation_data_per_epoch_gen = None

    #-------------------------update object property----------------------#
    def update_object_properties(self, state:dict[str, Any]):
        for property_name, new_val in state.items():
            if hasattr(self, property_name):
                # Use getattr to get the property value
                property_value = getattr(self, property_name)
                
                # Check if it's a dictionary
                if isinstance(property_value, dict):
                    for key, val in new_val.items():
                        property_value[key] = val
                else:
                    setattr(self, property_name, new_val)
            else:
                raise AttributeError(f"'{property_name}' does not exist on the object.")

    # -------------------------setting throb value------------------------#
    @property
    def throb_value(self):
        return abs(math.sin(pygame.time.get_ticks() * self.throb_speed))
    
    # ---------------------------getting time-----------------------------#
    @property
    def current_time(self):
        return pygame.time.get_ticks()

    # ------------------------------functions to run the generators----------------------------------#
    def next_lines_idxs(self, restart=False):
        if restart:
            if self.backward:
                self.lines_throb_idxs_gen = backward_lines_to_throb_generator(self.nn_structure, 
                                                                              from_layer=self.from_layer, 
                                                                              to_layer=self.to_layer,)
            else:
                self.lines_throb_idxs_gen = lines_to_throb_generator(self.nn_structure, 
                                                                     from_layer=self.from_layer, 
                                                                     to_layer=self.to_layer,)
        else:
            self.lines_idxs = next(self.lines_throb_idxs_gen)

    def next_nodes_idxs(self, restart=False):
        """restart: restarts the generator without generating output"""
        if restart:
            self.nodes_throb_idxs_gen = nodes_to_throb_generator(self.nn_structure, 
                                                                 from_layer=self.from_layer, 
                                                                 to_layer=self.to_layer, 
                                                                 backward=self.backward)
        else:
            self.nodes_idxs = next(self.nodes_throb_idxs_gen)

    def layer_node_text_generator(self, nn_data:list[list[float]]):
        for data in nn_data:
            gen = convert_list_to_generator(data)
            for node_text in gen:
                yield node_text
    
    def next_node_text(self, restart=False):
        if restart:
            self.node_text_gen = self.layer_node_text_generator(self.nn_data)
        else:
            self.node_text = next(self.node_text_gen)

    def next_texts(self, restart=False):
        # Generates text for throbbing
        if restart:
            self.text_gen = text_generator(self.nn_data, backward=self.backward)
        else:
            self.texts = next(self.text_gen)
    
    def next_text_per_epoch(self):
        try:
            self.nn_data = next(self.text_per_epoch_gen)
        except StopIteration:
            self.text_finished = True
            self.text_per_epoch_gen = convert_list_to_generator(self.total_data)
            self.nn_data = next(self.text_per_epoch_gen)

    def next_subsequent_layer_nodes_throbbing(self, restart=False):
        if restart:
            self.subsequent_nodes_in_layer_gen = layer_nodes_generator(self.nn_structure, 
                                                            generate_from_layer=2, 
                                                            from_layer=self.from_layer, 
                                                            to_layer=self.to_layer, 
                                                            backward=self.backward)
        else:
            self.subsequent_layer_nodes_throbbing = next(self.subsequent_nodes_in_layer_gen)
    
    def next_current_layer_nodes(self, restart=False):
        try:
            self.current_layer_nodes = next(self.current_nodes_in_layer_gen)
        except StopIteration:
            # generate from layer is two here because forward pass is not done on the output layer,
            # so after forward pass is done on the penultimate layer to the final layer, the current layer should start
            # from the beginning of the nn structure
            self.current_nodes_in_layer_gen = layer_nodes_generator(self.nn_structure, 
                                                                    generate_from_layer=1, 
                                                                    from_layer=self.from_layer, 
                                                                    to_layer=self.to_layer, 
                                                                    backward=self.backward)
            if restart:
                self.current_layer_nodes = next(self.current_nodes_in_layer_gen)
        

    def next_node_idx(self):
        self.node_idx = next(self.serialise_node_gen)

    def next_target_data(self):
        """Should be called at the end of a cycle/epoch"""
        try:
            Persistent_Variables.curr_target_data = next(Persistent_Variables.serialise_all_target_data_gen)
        except StopIteration:
            Persistent_Variables.serialise_all_target_data_gen = convert_list_to_generator(Persistent_Variables.all_target_data)
            Persistent_Variables.curr_target_data = next(Persistent_Variables.serialise_all_target_data_gen)
            
    def initialise_activation_data(self):
        if self.backward:
            for per_epoch_data in self.all_activation_data:
                per_epoch_data.reverse()
        # flatten data by one level
        self.all_activation_data = [sublist for outer_list in self.all_activation_data for sublist in outer_list]

        self.activation_data_per_epoch_gen = convert_list_to_generator(self.all_activation_data)
        #self.activation_data_per_epoch = next(self.activation_data_per_epoch_gen)
    
    def next_activation_data_per_epoch(self):
        try:
            self.activation_data_per_epoch = next(self.activation_data_per_epoch_gen)
        except StopIteration:
            self.activation_data_per_epoch_gen = convert_list_to_generator(self.all_activation_data)
            self.activation_data_per_epoch = next(self.activation_data_per_epoch_gen)
    # ---------------------------Execution order generators---------------------------------#
    def local_execution_order_gen(self):
        for idx, func_id in enumerate(self.local_execution_order):
            yield func_id, idx

    def next_local_func_id(self):
        try:
            func_id, self.current_local_func_id_idx = next(self.start_local_execution_order_gen)
        except StopIteration:
            self.end_of_local_execution_order = True
            self.start_local_execution_order_gen = self.local_execution_order_gen()
            func_id, self.current_local_func_id_idx = next(self.start_local_execution_order_gen)
        finally:
            return func_id
    
    def next_func_id(self):
        try:
            func_id, Persistent_Variables.current_func_id_idx = next(self.start_execution_order_gen)
        except StopIteration:
            Persistent_Variables.start_execution_order_gen = Persistent_Variables.execution_order_gen()
            func_id, Persistent_Variables.current_func_id_idx = next(self.start_execution_order_gen)
        finally:
            GlobalParameters.is_func_id_changed = True
            return func_id


    