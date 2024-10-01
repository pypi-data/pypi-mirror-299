from .screen_components import Components 
from .draw_on_screen import Text
from .persistent_vars import Persistent_Variables
from .screen_operations import display_all_componenets, set_all_comoponents_to_default_state, update_defualt_states_of_components, update_set_of_components_states, mass_update_numerous_components
from .generators_and_utility_functions import *
from .generate_coordinates import *
from .parameters import GlobalParameters
from .minor_components import func_minor_components
from typing import Iterable
import pygame


def log_text_coor(nodes:dict[str, Components], window, font, distance_from_vertex=20):
    text_dict = dict()

    for node_idx in nodes:
        if node_idx != 'node11':
            text = Text(window, font)
            x = nodes[node_idx].x - nodes[node_idx].node_radius - distance_from_vertex
            y = nodes[node_idx].y
            state = {'x':x, 'y':y, 'text':'-Log'}
            text.mass_update_state(state)

            text_dict[node_idx] = text
    
    # Make text invisible
    for text in text_dict.values():
        text.visible = False

    return text_dict

def render_log_text_beside_node(obj:Persistent_Variables, log_node_idx, distance_from_vertex=20):
    window = Persistent_Variables.display_surface
    font = Persistent_Variables.font
    
    text = Text(window, font)
    nodes = obj.nodes
    x = nodes[log_node_idx].x - nodes[log_node_idx].node_radius - distance_from_vertex
    y = nodes[log_node_idx].y
    state = {'x':x, 'y':y, 'text':'-Log'}
    text.mass_update_state(state)

    text.display()

def display_func_heading_text(obj:Persistent_Variables, text:str):
    # getting the farthest point in the x direction

    max_value_x = -float('inf')
    min_value_x = float('inf')
    min_value_y = float('inf')
    for node_obj in obj.nodes.values():
        min_value_x = min(node_obj.x, min_value_x)
        max_value_x = max(node_obj.x, max_value_x)

        min_value_y = min(node_obj.y, min_value_y)

    x_pos_of_text = min_value_x + (max_value_x - min_value_x)/2

    y_pos_of_text = min_value_y - (2*node_obj.node_radius)

    text_obj = func_minor_components.func_minor_components_dict[Persistent_Variables.FUNC_HEADING_TEXT]

    state = {'x':x_pos_of_text, 'y':y_pos_of_text, 'text':text}

    text_obj.mass_update_state(state)

    text_obj.display()
    
def display_text_above_layer(obj:Persistent_Variables, layer_num:int, text:str):
    node_indices:list[str] = []
    layer_idx = layer_num - 1
    layer_gen = layer_nodes_generator(nn_structure=[obj.nn_structure[layer_idx]],from_layer=layer_num)

    for layer_indices in layer_gen:
        node_indices += layer_indices

    min_val_y = float('inf')
    for node_idx, node_obj in obj.nodes.items():
        if node_idx in node_indices:
            min_val_y = min(min_val_y, node_obj.y)
    y_pos_text = min_val_y - (2*node_obj.node_radius)
    x_pos_text = node_obj.x

    text_obj = func_minor_components.func_minor_components_dict[Persistent_Variables.FUNC_HEADING_TEXT]

    state = {'x':x_pos_text, 'y':y_pos_text, 'text':text}

    text_obj.mass_update_state(state)

    text_obj.display()



def deactivate_all_func_across_all_objects(obj:Persistent_Variables):

    obj_dict:dict[str, Persistent_Variables] = obj.execution_function_objects

    for object in obj_dict.values():
        object.activate_forward_pass = False
        object.activate_nllloss = False 
        object.activate_softmax = False
        object.activate_move_nodes = False
        object.activate_backward_pass = False
        object.activate_activation = False
        object.activate_crossentropy_loss = False
        object.activate_ce_nllloss = False
        object.activate_logsoftmax = False
        object.activate_main_nllloss = False

def deactivate_all_local_func(obj:Persistent_Variables):
    obj.activate_forward_pass = False
    obj.activate_nllloss = False 
    obj.activate_softmax = False
    obj.activate_move_nodes = False
    obj.activate_backward_pass = False
    obj.activate_activation = False
    obj.activate_crossentropy_loss = False
    obj.activate_ce_nllloss = False
    obj.activate_logsoftmax = False
    obj.activate_main_nllloss = False


def activate_next_func(obj:Persistent_Variables, func_id:tuple):
    """func_id: function ids to activate"""
    
    obj_dict:dict[str, Persistent_Variables] = obj.execution_function_objects

    deactivate_all_func_across_all_objects(obj)

    func_id_name = func_id[0]

    if func_id_name == Persistent_Variables.FORWARD_PASS:
        obj_dict[func_id].activate_forward_pass = True

    elif func_id_name == Persistent_Variables.ACTIVATION:
        obj_dict[func_id].activate_activation = True

    elif func_id_name == Persistent_Variables.SOFTMAX:
        obj_dict[func_id].activate_softmax = True
    
    elif func_id_name == Persistent_Variables.LOGSOFTMAX:
        obj_dict[func_id].activate_logsoftmax = True
    
    elif func_id_name == Persistent_Variables.NLLLOSS:
        obj_dict[func_id].activate_nllloss = True
    
    elif func_id_name == Persistent_Variables.MAIN_NLLLOSS:
        obj_dict[func_id].activate_main_nllloss = True

    elif func_id_name == Persistent_Variables.CROSSENTROPY_LOSS:
        obj_dict[func_id].activate_crossentropy_loss = True
    
    elif func_id_name == Persistent_Variables.CE_NLLLOSS:
        obj_dict[func_id].activate_ce_nllloss = True

    elif func_id_name == Persistent_Variables.MOVE_NODES:
        obj_dict[func_id].activate_move_nodes = True
    
    elif func_id_name == Persistent_Variables.BACKWARD_PASS:
        obj_dict[func_id].activate_backward_pass = True

def activate_next_local_func(obj:Persistent_Variables, func_ids:tuple|Iterable):
    """func_ids: function ids to activate"""
    if isinstance(func_ids, tuple):
        func_ids = [func_ids]

    deactivate_all_local_func(obj)

    for func_id in func_ids:
        func_id = func_id[0]

        if func_id == Persistent_Variables.FORWARD_PASS:
            obj.activate_forward_pass = True

        elif func_id == Persistent_Variables.ACTIVATION:
            obj.activate_activation = True

        elif func_id == Persistent_Variables.SOFTMAX:
            obj.activate_softmax = True
        
        elif func_id == Persistent_Variables.LOGSOFTMAX:
            obj.activate_logsoftmax = True
        
        elif func_id == Persistent_Variables.NLLLOSS:
            obj.activate_nllloss = True
        
        elif func_id == Persistent_Variables.MAIN_NLLLOSS:
            obj.activate_main_nllloss = True
        
        elif func_id == Persistent_Variables.CROSSENTROPY_LOSS:
            obj.activate_crossentropy_loss = True
        
        elif func_id == Persistent_Variables.CE_NLLLOSS:
            obj.activate_ce_nllloss = True

        elif func_id == Persistent_Variables.MOVE_NODES:
            obj.activate_move_nodes = True
        
        elif func_id == Persistent_Variables.BACKWARD_PASS:
            obj.activate_backward_pass = True


def end_of_cycle(obj:Persistent_Variables, func_id:str):
    index_of_func_id = obj.execution_order.index(func_id) - 1 # since func_id is always the next func_id not the current function
    if index_of_func_id == -1:
        return True
    else:
        return False

def disable_static():
    execution_function_objects:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects

    for obj in execution_function_objects.values():
        obj.static = False

def display_all_forward_pass_components():
    execution_function_objects:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects

    for func_id, obj in execution_function_objects.items():
        if func_id[0] == Persistent_Variables.FORWARD_PASS:
            display_all_componenets(obj.nodes)
            display_all_componenets(obj.lines)
        elif func_id[0] not in Persistent_Variables.AVAILABLE_LOSS_FUNC and func_id[0] != Persistent_Variables.BACKWARD_PASS:
            obj.static = True

def set_execution_order_components_to_default_state(obj:Persistent_Variables):
    for storage_obj in obj.execution_function_objects.values():
        set_all_comoponents_to_default_state([storage_obj.nodes, storage_obj.lines])
        if storage_obj.target_node is not None:
            set_all_comoponents_to_default_state([storage_obj.target_node])
    
    # for minor functional components like vertical bars and func text heading 
    set_all_comoponents_to_default_state(component_types=[func_minor_components.func_minor_components_dict])

def update_execution_order_components_default_states():
    for storage_obj in Persistent_Variables.execution_function_objects.values():
        update_defualt_states_of_components(component_types=[storage_obj.nodes, storage_obj.lines], var_dict=None, update_all=True)
        if storage_obj.target_node is not None:
            update_defualt_states_of_components(component_types=[storage_obj.target_node], var_dict=None, update_all=True)

    # for minor functional components like vertical bars and func text heading
    update_defualt_states_of_components(component_types=[func_minor_components.func_minor_components_dict], var_dict=None, update_all=True)


def construct_boolean_state_dict(use_local_exec_order:bool, standalone:bool, func_id_name:str, bool_properties:dict[str, bool]):
    state_dict = dict()
    for property, activate in bool_properties.items():
        if use_local_exec_order:
            if property == 'run_once':
                state_dict['local_run_once'] = {func_id_name:activate}
            elif property == 'static':
                # parent function should control what is on screen
                state_dict['local_static'] = {func_id_name:False}
        elif standalone:
            if property == 'run_once':
                state_dict['standalone_run_once'] = activate
            elif property == 'static':
                # parent function should control what is on the screen
                state_dict['standalone_static'] = False          
        else:
            state_dict[property] = activate
    
    return state_dict

def update_boolean_status(obj:Persistent_Variables, use_local_exec_order, standalone, func_id_name, bool_properties:dict[str, bool]):
    state_dict = construct_boolean_state_dict(use_local_exec_order, 
                                              standalone, 
                                              func_id_name, 
                                              bool_properties,)
    
    obj.update_object_properties(state_dict)


def map_func_to_boolean_property(obj:Persistent_Variables, 
                                  use_local_exec_order:bool, 
                                  standalone:bool, 
                                  func_id_name:str, 
                                  property_name:str):
    bool_state = None 
    if use_local_exec_order:
        if property_name == 'run_once':
            bool_state = obj.local_run_once[func_id_name]
        elif property_name == 'static':
            bool_state = obj.local_static[func_id_name]
    elif standalone:
        if property_name == 'run_once':
            bool_state = obj.standalone_run_once
        elif property_name == 'static':
            bool_state = obj.standalone_static
    else:
        if property_name == 'run_once':
            bool_state = obj.run_once
        elif property_name == 'static':
            bool_state = obj.static
    return bool_state


def forward_pass(obj:Persistent_Variables, standalone=False, use_local_exec_order=False, standalone_num_layers=None):
    """
    standalone: straight up forward pass without activation and the function does not have to call the next function.
    standalone_num_layers determines how many layers to be throbbed before end of forward pass. this is usefull when
    an object has num layers greater than the intended purpose of the use of forward_pass function
    """
    if obj.activate_forward_pass and not obj.pause:
        obj.elapsed_time = obj.current_time - obj.last_update_time
        # get current layer nodes
        run_once = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.FORWARD_PASS, property_name='run_once')

        if run_once:
            obj.next_current_layer_nodes(restart=True)
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.FORWARD_PASS, bool_properties={'run_once':False})
            
        try:
            if obj.elapsed_time > obj.throb_duration:
                # update time
                obj.get_last_update_time()

                # off throbbing of lines and nodes
                update_set_of_components_states(keys=obj.lines_idxs, components=obj.lines, state_updates={'throb_value': None})
                update_set_of_components_states(keys=obj.nodes_idxs, components=obj.nodes, state_updates={'throb_value': None})
                
                obj.subsequent_throbbed_nodes_count += 1

                # after throbbing a particular layer call next action
                if not standalone:

                    if obj.subsequent_throbbed_nodes_count == len(obj.subsequent_layer_nodes_throbbing):
                        obj.get_last_update_time()
                        if use_local_exec_order:
                            func_id = obj.next_local_func_id()
                            funcs_to_activate = [func_id, obj.execution_order[obj.current_func_id_idx]]
                            activate_next_local_func(obj, funcs_to_activate)
                        else:
                            func_id = obj.next_func_id()
                            activate_next_func(obj, func_id)

                obj.next_lines_idxs()
                obj.next_nodes_idxs()
                obj.next_texts()

        except StopIteration:
            # update flag
            obj.is_end_forward_pass = True 
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.FORWARD_PASS, bool_properties={'run_once':True})

            # restart generators
            obj.next_lines_idxs(restart=True)
            obj.next_nodes_idxs(restart=True)
            obj.next_text_per_epoch() # update text before restarting
            obj.next_texts(restart=True)

            # get outputs from generators
            obj.next_lines_idxs()
            obj.next_nodes_idxs()
            obj.next_texts()


            
        finally:
            # meaning only turn on throbbing and texting when it is not activation time 
            if obj.subsequent_throbbed_nodes_count != len(obj.subsequent_layer_nodes_throbbing):
                # Turn on throbbing
                update_set_of_components_states(keys=obj.lines_idxs, components=obj.lines, state_updates={'throb_value': int(obj.throb_value * 5) + 1})
                update_set_of_components_states(keys=obj.nodes_idxs, components=obj.nodes, state_updates={'throb_value': int(obj.throb_value * 5) + 1})

                # Turn on node text
                for key, text in zip(obj.nodes_idxs, obj.texts):
                    if key in obj.nodes:
                        if obj.nodes[key].text == '':
                            obj.nodes[key].update_state(param='text', value=text)
            
            # get the next layer
            if (obj.subsequent_throbbed_nodes_count == len(obj.subsequent_layer_nodes_throbbing)):

                obj.next_current_layer_nodes()

                if standalone:
                    obj.standalone_end_count += 1

                    if obj.standalone_end_count == standalone_num_layers:
                        obj.is_end_of_standalone_forward_pass = True
                        obj.standalone_end_count = 1

                obj.subsequent_throbbed_nodes_count = 0

                # update subsequent layer throbbing when activation function is not activated.
                try:
                    obj.next_subsequent_layer_nodes_throbbing()
                except:
                    obj.next_subsequent_layer_nodes_throbbing(restart=True)
                    obj.next_subsequent_layer_nodes_throbbing()


                    if not standalone and not use_local_exec_order:
                        # check if end of cycle
                        if end_of_cycle(obj, func_id):
                            disable_static()
                            set_execution_order_components_to_default_state(obj)
                            update_curr_num_of_iterations()
                            if obj.curr_target_data is not None:
                                obj.next_target_data()
                        
                        obj.get_last_update_time()

def activation(obj:Persistent_Variables, standalone=False, use_local_exec_order=False):
    """
    obj: should be the same object used for forward pass
    standalone: performing activation through the end while calling only the next function in the execution order after all nodes have been activated
    """
    if obj.activate_activation and not obj.pause:
        obj.elapsed_time = obj.current_time - obj.last_update_time
        run_once = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.ACTIVATION, property_name='run_once')
        if run_once:
            # create generator to know which node to activate
            obj.next_activation_data_per_epoch()
            obj.serialise_node_gen = convert_list_to_generator(zip(obj.current_layer_nodes, obj.activation_data_per_epoch))
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.ACTIVATION, bool_properties={'run_once':False})

        try:
            if obj.elapsed_time > obj.throb_duration:
                # update time 
                obj.get_last_update_time()

                # off throbbing of lines and nodes
                update_set_of_components_states(keys=obj.lines_idxs, components=obj.lines, state_updates={'throb_value': None})
                update_set_of_components_states(keys=obj.nodes_idxs, components=obj.nodes, state_updates={'throb_value': None})

                obj.next_node_idx()

                node_idx, node_activation_data = obj.node_idx

                if obj.backward:
                    obj.nodes[node_idx].update_state(param='color', value=(0, 0, 0))
                else:
                    obj.nodes[node_idx].update_state(param='color', value=(0, 200, 0))
                
                obj.nodes[node_idx].update_state(param='text', value=node_activation_data)

        except StopIteration:
            # this except block shows that activation has been done

            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.ACTIVATION, bool_properties={'run_once':True})

            if not standalone:

                obj.get_last_update_time()

                if use_local_exec_order:
                    func_id = obj.next_local_func_id()
                    funcs_to_activate = [func_id, obj.execution_order[obj.current_func_id_idx]]
                    activate_next_local_func(obj, funcs_to_activate)
                else:
                    func_id = obj.next_func_id()
                    activate_next_func(obj, func_id)

                    if end_of_cycle(obj, func_id):
                        disable_static()
                        set_execution_order_components_to_default_state(obj)
                        update_curr_num_of_iterations()
                        if obj.curr_target_data is not None:
                            obj.next_target_data()

def log_softmax(obj:Persistent_Variables, use_local_exec_order=False, standalone=False):
    """it should use a seperate persistent variable object"""
    static = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.LOGSOFTMAX, property_name='static')
    if (static or (obj.pause and obj.activate_logsoftmax)) and not use_local_exec_order:
        display_all_componenets(obj.nodes)
        display_all_componenets(obj.lines)

    if obj.activate_logsoftmax and not obj.pause:
        obj.elapsed_time = obj.current_time - obj.last_update_time
        
        run_once = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.LOGSOFTMAX, property_name='run_once')
        if run_once:
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.LOGSOFTMAX, bool_properties={'run_once':False, 'static':True})

        display_all_componenets(obj.nodes)
        display_all_componenets(obj.lines)

        if use_local_exec_order:
            if obj.current_layer_nodes is not None and Persistent_Variables.LOGSOFTMAX != obj.local_execution_order[0][0]:
                """to prevent code under run_once in forward pass from runnning if it was ran before."""
                update_boolean_status(obj, 
                                      use_local_exec_order=False, 
                                      standalone=True, 
                                      func_id_name=Persistent_Variables.LOGSOFTMAX, 
                                      bool_properties={'run_once':False})
                
        obj.activate_forward_pass = True # turn on forward pass
        forward_pass(obj, standalone=True, standalone_num_layers=3)
        obj.activate_forward_pass = False

        if obj.is_end_of_standalone_forward_pass:
            
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.LOGSOFTMAX, bool_properties={'run_once':True})
            # update flag
            obj.is_end_of_standalone_forward_pass = False
            
            if not standalone:
                if use_local_exec_order:
                    func_id = obj.next_local_func_id()
                    func_to_activate = [func_id, obj.execution_order[obj.current_func_id_idx]]
                    activate_next_local_func(obj, func_to_activate)
                else:
                    func_id = obj.next_func_id()
                    activate_next_func(obj, func_id)

                    # check if end of cycle 
                    if end_of_cycle(obj, func_id):
                        disable_static()
                        set_execution_order_components_to_default_state(obj)
                        update_curr_num_of_iterations()
                        if obj.curr_target_data is not None:
                            obj.next_target_data()
                
                obj.get_last_update_time()

def softmax(obj:Persistent_Variables, use_local_exec_order=False, standalone=False):
    """it should use a seperate persistent variable object"""
    static = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.SOFTMAX, property_name='static')
    if (static or (obj.pause and obj.activate_softmax)) and not use_local_exec_order:
        display_all_componenets(obj.nodes)
        display_all_componenets(obj.lines)

    if obj.activate_softmax and not obj.pause:
        obj.elapsed_time = obj.current_time - obj.last_update_time
        
        run_once = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.SOFTMAX, property_name='run_once')
        if run_once:
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.SOFTMAX, bool_properties={'run_once':False, 'static':True})

        display_all_componenets(obj.nodes)
        display_all_componenets(obj.lines)

        if use_local_exec_order:
            if obj.current_layer_nodes is not None and Persistent_Variables.SOFTMAX != obj.local_execution_order[0][0]:
                """to prevent code under run_once in forward pass from runnning if it was ran before."""
                update_boolean_status(obj, 
                                      use_local_exec_order=False, 
                                      standalone=True, 
                                      func_id_name=Persistent_Variables.SOFTMAX, 
                                      bool_properties={'run_once':False})
                
        obj.activate_forward_pass = True # turn on forward pass
        forward_pass(obj, standalone=True, standalone_num_layers=3)
        obj.activate_forward_pass = False

        if obj.is_end_of_standalone_forward_pass:
            
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.SOFTMAX, bool_properties={'run_once':True})
            # update flag
            obj.is_end_of_standalone_forward_pass = False
            
            if not standalone:
                if use_local_exec_order:
                    func_id = obj.next_local_func_id()
                    func_to_activate = [func_id, obj.execution_order[obj.current_func_id_idx]]
                    activate_next_local_func(obj, func_to_activate)
                else:
                    func_id = obj.next_func_id()
                    activate_next_func(obj, func_id)

                    # check if end of cycle 
                    if end_of_cycle(obj, func_id):
                        disable_static()
                        set_execution_order_components_to_default_state(obj)
                        update_curr_num_of_iterations()
                        if obj.curr_target_data is not None:
                            obj.next_target_data()
                
                obj.get_last_update_time()

def draw_nllloss_vertical_bar(obj:Persistent_Variables):
    
    for node_obj in obj.nodes.values():
        obj_x = node_obj.x
        radius = node_obj.node_radius
        break

    vertical_bar = func_minor_components.func_minor_components_dict['vertical_bar']
    point_x = obj_x - (radius + 35)
    start_point_y = Persistent_Variables.screen_height/2 - 30
    end_point_y = 30 + Persistent_Variables.screen_height/2
    vertical_bar.mass_update_state({'node_to_node':False,
                                    'start_point':(point_x, start_point_y),
                                    'end_point':(point_x, end_point_y),
                                    'thickness':5})
    
    vertical_bar.display()

def main_nllloss(obj:Persistent_Variables, use_local_exec_order=False, standalone=False):

    static = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MAIN_NLLLOSS, property_name='static')
    if (static or (obj.pause and obj.activate_main_nllloss)) and not use_local_exec_order: 
        # meaning do not display when it is using local execution order 
        #because the function that it is in will call the required components
        draw_nllloss_vertical_bar(obj)
        display_all_componenets(obj.nodes)
        display_all_componenets(obj.target_node)
        display_func_heading_text(obj, Persistent_Variables.NLLLOSS)

    if obj.activate_main_nllloss and not obj.pause:
        obj.elapsed_time = obj.current_time - obj.last_update_time
        run_once = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MAIN_NLLLOSS, property_name='run_once')
        if run_once:
            transfer_prev_node_obj_text_to_curr_obj(obj)
            obj.extra_data[Persistent_Variables.LOG_NODE_IDX] = map_target_node_to_nllloss_layer(obj, obj.curr_target_data)
            obj.extra_data[Persistent_Variables.LOSS_VAL] = -obj.nodes[obj.extra_data[Persistent_Variables.LOG_NODE_IDX]].text
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MAIN_NLLLOSS, bool_properties={'run_once':False, 'static':True})


        display_all_componenets(obj.target_node)
        
        if not use_local_exec_order:
            display_all_componenets(obj.nodes)
        
        # throb node
        log_node_idx = obj.extra_data[Persistent_Variables.LOG_NODE_IDX]
        obj.nodes[log_node_idx].mass_update_state({'color': (150, 0, 0), 'throb_value': int(obj.throb_value * 5) + 1})

        mass_update_numerous_components(obj.target_node, {'text':obj.curr_target_data, 'color': (150, 0, 0), 'throb_value': int(obj.throb_value * 5) + 1}) 

        # update logsoftmax text
        if obj.elapsed_time >= obj.throb_duration/2:
            nllloss_value = obj.extra_data[Persistent_Variables.LOSS_VAL]
            obj.nodes[log_node_idx].mass_update_state({'text':nllloss_value})   

        if obj.elapsed_time > obj.throb_duration+500:

            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MAIN_NLLLOSS, bool_properties={'run_once':True})

            # default state for throb value is None
            mass_update_numerous_components(obj.target_node, {'throb_value':None})
            obj.nodes[log_node_idx].mass_update_state({'throb_value':None})

            if not standalone:
                if use_local_exec_order:
                    func_id = obj.next_local_func_id()
                    func_to_activate = [func_id, obj.execution_order[obj.current_func_id_idx]]
                    activate_next_local_func(obj, func_to_activate)
                else:
                    func_id = obj.next_func_id()
                    activate_next_func(obj, func_id)

                    # check if end of cycle 
                    if end_of_cycle(obj, func_id):
                        disable_static()
                        set_execution_order_components_to_default_state(obj)
                        update_curr_num_of_iterations()
                        if obj.curr_target_data is not None:
                            obj.next_target_data()

                # update time
            obj.get_last_update_time()

def nllloss(obj:Persistent_Variables):
    """
    Crossentropy loss function
    """
    if obj.static or (obj.activate_nllloss and obj.pause):
        draw_nllloss_vertical_bar(obj)
        display_all_componenets(obj.nodes)
        display_all_componenets(obj.target_node)
        display_func_heading_text(obj, Persistent_Variables.NLLLOSS)

    if obj.activate_nllloss and not obj.pause:
        if obj.run_once:
            update_boolean_status(obj,
                                  use_local_exec_order=False,
                                  standalone=False,
                                  func_id_name=Persistent_Variables.NLLLOSS,
                                  bool_properties={'run_once':False, 'static':True})
        
            obj.activate_main_nllloss = True
        
        main_nllloss(obj, use_local_exec_order=True)
        move_nodes(obj, use_local_exec_order=True)

        if obj.end_of_local_execution_order: # end of crossentropy function

            obj.end_of_local_execution_order = False
            update_boolean_status(obj,
                                  use_local_exec_order=False,
                                  standalone=False,
                                  func_id_name=Persistent_Variables.NLLLOSS,
                                  bool_properties={'run_once':True, 'static':False})

            # call next function and update time
            func_id = obj.next_func_id()
            activate_next_func(obj, func_id)
            obj.get_last_update_time()

            # check if end of cycle 
            if end_of_cycle(obj, func_id):
                disable_static()
                set_execution_order_components_to_default_state(obj)
                update_curr_num_of_iterations()

                if obj.curr_target_data is not None:
                    obj.next_target_data()
                obj.get_last_update_time()

def ce_nllloss(obj:Persistent_Variables, use_local_exec_order=False, standalone=False):
    """
    obj: it is a softmax persistent variable object
    log_node_idx: node idx to perform log operation on
    """
    target_node = obj.target_node
    static = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.CE_NLLLOSS, property_name='static')
    if (static or (obj.pause and obj.activate_ce_nllloss)) and not use_local_exec_order: 
        # meaning do not display when it is using local execution order 
        #because the function that it is in will call the required components
        draw_nllloss_vertical_bar(obj)
        display_all_componenets(obj.nodes)
        display_all_componenets(target_node)

    if obj.activate_ce_nllloss and not obj.pause:
        obj.elapsed_time = obj.current_time - obj.last_update_time
        run_once = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.CE_NLLLOSS, property_name='run_once')
        if run_once:
            log_softmax = obj.extra_data[Persistent_Variables.LOSS_VAL].pop(0)
            obj.extra_data[Persistent_Variables.CURR_LOSS_VAL] = log_softmax
            obj.extra_data[Persistent_Variables.LOSS_VAL].append(log_softmax)

            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.CE_NLLLOSS, bool_properties={'run_once':False, 'static':True})

        target_data:int = obj.curr_target_data
        log_node_idx = map_target_node_to_nllloss_layer(obj, target_data)

        display_all_componenets(target_node)
        if not use_local_exec_order:
            display_all_componenets(obj.nodes)

        # off visibility of lines
        for line in obj.lines.values():
            line.visible=False
        
        # render log
        render_log_text_beside_node(obj, log_node_idx=log_node_idx)
        
        # throb node
        obj.nodes[log_node_idx].mass_update_state({'color': (150, 0, 0), 'throb_value': int(obj.throb_value * 5) + 1})

        mass_update_numerous_components(obj.target_node, {'text':target_data, 'color': (150, 0, 0), 'throb_value': int(obj.throb_value * 5) + 1}) 

        # update logsoftmax text
        if obj.elapsed_time >= obj.throb_duration/2:
            nllloss_value = obj.extra_data[Persistent_Variables.CURR_LOSS_VAL]
            obj.nodes[log_node_idx].mass_update_state({'text':nllloss_value})      

        if obj.elapsed_time > obj.throb_duration:

            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.CE_NLLLOSS, bool_properties={'run_once':True})

            # default state for throb value is None
            mass_update_numerous_components(obj.target_node, {'throb_value':None})
            obj.nodes[log_node_idx].mass_update_state({'throb_value':None})

            if not standalone:
                if use_local_exec_order:
                    func_id = obj.next_local_func_id()
                    func_to_activate = [func_id, obj.execution_order[obj.current_func_id_idx]]
                    activate_next_local_func(obj, func_to_activate)
                else:
                    func_id = obj.next_func_id()
                    activate_next_func(obj, func_id)

                    # check if end of cycle 
                    if end_of_cycle(obj, func_id):
                        disable_static()
                        set_execution_order_components_to_default_state(obj)
                        update_curr_num_of_iterations()
                        if obj.curr_target_data is not None:
                            obj.next_target_data()

                # update time
            obj.get_last_update_time()

def get_softmax_node_idx(obj:Persistent_Variables):
    """returns node index"""
    from_layer = obj.from_layer
    sm_node_idx = f'node1{from_layer + 1}'
    return sm_node_idx

def map_target_node_to_nllloss_layer(obj:Persistent_Variables, target_data)->str:
    """
    According to training data formats, for classification, the target is the index of the true label
    returns node index
    """
    if not isinstance(target_data, int):
        raise TypeError(f"The target value {target_data} should be an integer")
    
    to_layer = obj.to_layer

    if to_layer is None:
        to_layer = len(obj.ideal_nn_structure)

    selected_node = f'node{target_data+1}{to_layer}' # Added 1 because target data are indices 

    return selected_node


def transfer_prev_node_obj_text_to_curr_obj(obj:Persistent_Variables):
    prev_obj_store = []
    prev_node_indices, prev_obj = get_last_layer_node_indices_of_prev_object()
    curr_indices = get_obj_last_layer_node_indices(obj)
    for node_idx in prev_obj.nodes:
        if node_idx in prev_node_indices:
            prev_obj_store.append(prev_obj.nodes[node_idx])

    assert len(curr_indices) == len(prev_obj_store)

    for prev_node_obj, curr_index in zip(prev_obj_store, curr_indices):
        obj.nodes[curr_index].text = prev_node_obj.text


def get_last_layer_node_indices_of_prev_object():
    curr_func_id = Persistent_Variables.current_func_id_idx
    prev_func_id = Persistent_Variables.execution_order[curr_func_id - 1]

    prev_obj:Persistent_Variables = Persistent_Variables.execution_function_objects[prev_func_id]

    nodes_idx = get_obj_last_layer_node_indices(prev_obj)

    return nodes_idx, prev_obj


def get_obj_last_layer_node_indices(obj:Persistent_Variables)->list[str]:
    """
    only the last layer nodes should be moved
    returns a list of node indices
    """

    node_indices = []

    layer_to_move = obj.to_layer

    if layer_to_move is None:
        layer_to_move = len(obj.ideal_nn_structure)

    num_nodes = obj.ideal_nn_structure[-1]

    for node_num in range(num_nodes):
        node_indices.append(f'node{node_num+1}{layer_to_move}')

    return node_indices

def nodes_to_move(obj:Persistent_Variables):
    return get_obj_last_layer_node_indices(obj)

def turn_off_visibility_for_a_layer(obj:Persistent_Variables, layer_num:int, from_layer:int, exclude:Iterable=[]):
    layer_nodes_gen = layer_nodes_generator(nn_structure=[obj.nn_structure[layer_num - 1]],
                                            from_layer=from_layer)
    
    for layer_nodes in layer_nodes_gen:
        for node in layer_nodes:
            if node not in exclude:
                obj.nodes[node].visible = False

def get_position_to_move_to():
    execution_order = Persistent_Variables.execution_order
    execution_function_objects = Persistent_Variables.execution_function_objects

    for func_id  in execution_order:
        if func_id[0] == Persistent_Variables.BACKWARD_PASS:
            target_node = next(reversed(execution_function_objects[func_id].nodes.values()))
            return target_node.x, target_node.y
    else:
        # setting x  coordinate to None make the move component function replace None with the x coor of the node to be moved
        return None, Persistent_Variables.screen_height/2

def move_nodes(obj:Persistent_Variables, use_local_exec_order=False, standalone=False):
    """This function was built for nllloss"""
     
    static = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MOVE_NODES, property_name='static')
    if (static or (obj.pause and obj.activate_move_nodes)) and not use_local_exec_order:
        display_all_componenets(obj.nodes)

    if obj.activate_move_nodes:
        nodes:dict[str, Components] = obj.nodes
        nodes_idx_to_move = nodes_to_move(obj)
        target_data = obj.curr_target_data
        height = obj.screen_height

        selected_node_idx = map_target_node_to_nllloss_layer(obj, target_data)

        # get position to move to
        move_coor = get_position_to_move_to()

        run_once = map_func_to_boolean_property(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MOVE_NODES, property_name='run_once')
        if run_once:
            obj.buffer = nodes[selected_node_idx].move_component_generator(move_coor)
            
            # off text in nodes execpt selected nodes
            for node_index in nodes_idx_to_move:
                if node_index != selected_node_idx:
                    obj.nodes[node_index].mass_update_state({'text':''})

            # start generator
            for node_idx, node in nodes.items():
                if node_idx in nodes_idx_to_move:
                    node.move_component_gen = node.move_component_generator((nodes[node_idx].x, height/2))
            update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MOVE_NODES, bool_properties={'run_once':False})

        try:
            # get elements from generator
            for node_idx, node in nodes.items():
                if node_idx in nodes_idx_to_move:
                    next(node.move_component_gen)
        except StopIteration:
            # End of movement

            # off all nodes apart from selected node 
            turn_off_visibility_for_a_layer(obj=obj, layer_num=len(obj.nn_structure), from_layer=obj.to_layer, exclude=[selected_node_idx])
            
            if len(obj.nn_structure)>1:
                # Turn off softmax node
                turn_off_visibility_for_a_layer(obj=obj, layer_num=len(obj.nn_structure)-1, from_layer=obj.to_layer-1)
            
            # off visibility of lines
            for line in obj.lines.values():
                line.visible=False

            """Move target node horizontally to start back propagation"""

            try:
                next(obj.buffer)
            except StopIteration:

                update_boolean_status(obj, use_local_exec_order, standalone, func_id_name=Persistent_Variables.MOVE_NODES, bool_properties={'run_once':True})

                if not standalone:
                    # call next function and update time
                    if use_local_exec_order:
                        func_id = obj.next_local_func_id()
                        func_to_activate = [func_id, obj.execution_order[obj.current_func_id_idx]]
                        activate_next_local_func(obj, func_to_activate)
                    else:
                        func_id = obj.next_func_id()
                        activate_next_func(obj, func_id)

                        # check if end of cycle 
                        if end_of_cycle(obj, func_id):
                            set_execution_order_components_to_default_state(obj)
                            update_curr_num_of_iterations()
                            if obj.curr_target_data is not None:
                                obj.next_target_data()
                
                    obj.get_last_update_time()

        pygame.display.flip()
        pygame.time.delay(15)

def turn_off_execution_order_components(obj:Persistent_Variables, exclude:list[str] = None):
    """Exclude is a list that contains function id name"""

    for obj_idx, storage_obj in obj.execution_function_objects.items():
        for id_name in exclude:
            if obj_idx[0] != id_name:
                for node in storage_obj.nodes.values():
                    node.visible = False
                
                for line in storage_obj.lines.values():
                    line.visible = False

                # check for target nodes
                if storage_obj.target_node is not None:
                    for node in storage_obj.target_node.values():
                        node.visible = False
                
                # check for minor components 
                for minor_comp in func_minor_components.func_minor_components_dict.values():
                    minor_comp.visible = False

def get_loss_value_for_backward_pass():
    func_id_loss_func = Persistent_Variables.execution_order[-2]
    loss_func_obj = Persistent_Variables.execution_function_objects[func_id_loss_func]

    return loss_func_obj.extra_data[Persistent_Variables.LOSS_VAL]

def backward_pass(obj:Persistent_Variables):

    if obj.activate_backward_pass and obj.pause:
        display_all_componenets(obj.nodes)
        display_all_componenets(obj.lines)
        loss_value = get_loss_value_for_backward_pass()
        display_text_above_layer(obj, layer_num=len(obj.nn_structure), text=f'Loss = {loss_value}')

    if obj.activate_backward_pass and not obj.pause:
        obj.elapsed_time = obj.current_time - obj.last_update_time
        
        if obj.run_once:
            turn_off_execution_order_components(obj, exclude=[Persistent_Variables.BACKWARD_PASS])

            # activate first function in the execution order
            funcs_to_activate = [obj.local_execution_order[0], obj.execution_order[obj.current_func_id_idx]]
            activate_next_local_func(obj, func_ids=funcs_to_activate)

            func_minor_components.func_minor_components_dict[Persistent_Variables.FUNC_HEADING_TEXT].visible = True
            obj.run_once = False


        display_all_componenets(obj.nodes)
        display_all_componenets(obj.lines)
        loss_value = get_loss_value_for_backward_pass()
        display_text_above_layer(obj, layer_num=len(obj.nn_structure), text=f'Loss = {loss_value}')


        call_local_func_with_obj(obj)

        if obj.end_of_local_execution_order:
            obj.end_of_local_execution_order = False
            obj.run_once = True
            # call next function and update time
            func_id = obj.next_func_id()
            activate_next_func(obj, func_id)
            obj.get_last_update_time()

            # check if end of cycle 
            if end_of_cycle(obj, func_id):
                disable_static()
                set_execution_order_components_to_default_state(obj)
                update_curr_num_of_iterations()

                if obj.curr_target_data is not None:
                    obj.next_target_data()
                obj.get_last_update_time()

def crossentropy_loss(obj:Persistent_Variables):
    """
    Crossentropy loss function
    """
    if obj.static or (obj.activate_crossentropy_loss and obj.pause):
        display_all_componenets(obj.target_node)
        display_all_componenets(obj.nodes)
        display_all_componenets(obj.lines)
        display_func_heading_text(obj, 'CROSSENTROPY LOSS')

    if obj.activate_crossentropy_loss and not obj.pause:
        if obj.run_once:
            update_boolean_status(obj,
                                  use_local_exec_order=False,
                                  standalone=False,
                                  func_id_name=Persistent_Variables.CROSSENTROPY_LOSS,
                                  bool_properties={'run_once':False, 'static':True})
        
            obj.activate_softmax = True
            
        softmax(obj, use_local_exec_order=True)
        ce_nllloss(obj, use_local_exec_order=True)
        move_nodes(obj, use_local_exec_order=True)

        if obj.end_of_local_execution_order: # end of crossentropy function

            obj.end_of_local_execution_order = False
            update_boolean_status(obj,
                                  use_local_exec_order=False,
                                  standalone=False,
                                  func_id_name=Persistent_Variables.CROSSENTROPY_LOSS,
                                  bool_properties={'run_once':True, 'static':False})

            # call next function and update time
            func_id = obj.next_func_id()
            activate_next_func(obj, func_id)
            obj.get_last_update_time()

            # check if end of cycle 
            if end_of_cycle(obj, func_id):
                disable_static()
                set_execution_order_components_to_default_state(obj)
                update_curr_num_of_iterations()

                if obj.curr_target_data is not None:
                    obj.next_target_data()
                obj.get_last_update_time()
    

def call_funcs_with_objs():
    execution_order = Persistent_Variables.execution_order
    execution_function_objects = Persistent_Variables.execution_function_objects

    for func_id in execution_order:
        func_id_name = func_id[0]
        obj = execution_function_objects[func_id]
        if func_id_name == Persistent_Variables.FORWARD_PASS:
            forward_pass(obj)
        elif func_id_name == Persistent_Variables.ACTIVATION:
            activation(obj)
        elif func_id_name == Persistent_Variables.SOFTMAX:
            softmax(obj)
        elif func_id_name == Persistent_Variables.LOGSOFTMAX:
            log_softmax(obj)
        elif func_id_name == Persistent_Variables.NLLLOSS:
            nllloss(obj)
        elif func_id_name == Persistent_Variables.CROSSENTROPY_LOSS:
            crossentropy_loss(obj)
        elif func_id_name == Persistent_Variables.CE_NLLLOSS:
            ce_nllloss(obj)
        elif func_id_name == Persistent_Variables.BACKWARD_PASS:
            backward_pass(obj)
        else:
            raise NameError(f'cannot run function: invalid function ID name {func_id}')

        
def call_local_func_with_obj(obj:Persistent_Variables):
    local_func_idx = obj.current_local_func_id_idx
    exec_order = obj.local_execution_order

    func_id_name, _ = exec_order[local_func_idx]

    if func_id_name == Persistent_Variables.FORWARD_PASS:
        forward_pass(obj, use_local_exec_order=True)
    elif func_id_name == Persistent_Variables.ACTIVATION:
        activation(obj, use_local_exec_order=True)
    elif func_id_name == Persistent_Variables.SOFTMAX:
        softmax(obj, use_local_exec_order=True)
    elif func_id_name == Persistent_Variables.LOGSOFTMAX:
        log_softmax(obj, use_local_exec_order=True)
    elif func_id_name == Persistent_Variables.MAIN_NLLLOSS:
        main_nllloss(obj, use_local_exec_order=True)
    elif func_id_name == Persistent_Variables.CE_NLLLOSS:
        ce_nllloss(obj, use_local_exec_order=True)
    else:
        raise NameError(f'cannot run function: invalid function ID name {func_id_name}')

def initialise_activation_function():
    execution_function_objects:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects

    for func_id, objs in execution_function_objects.items():
        if func_id[0] == Persistent_Variables.ACTIVATION:
            objs.initialise_activation_data()

        # if local execution order is present 
        if objs.local_execution_order is not None:
            for local_func_id in objs.local_execution_order:
                if local_func_id[0] == Persistent_Variables.ACTIVATION:
                    # initialise once for local execution order
                    objs.initialise_activation_data()
                    break

def update_curr_num_of_iterations():
    if GlobalParameters.curr_num_iterations < GlobalParameters.total_num_iterations:
        GlobalParameters.curr_num_iterations += 1
    else:
        GlobalParameters.curr_num_iterations = 1
