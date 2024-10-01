from copy import deepcopy
from .draw_on_screen import Nodes, Rect, Line
import random
from .persistent_vars import Persistent_Variables
from .generators_and_utility_functions import layer_nodes_generator, generate_node_idx_for_nn
from .generate_coordinates import *
from .components_generator_functions import generate_componets, generate_components_for_softmax


def generate_main_nn_structure(execution_order:list, extracted_nn_structure):
    """
    dependent functions are functions that dont need its own component, but rather interacts with components of other functions
    example: activation functions
    """

    main_nn_structure = []

    layer_starting_from = []

    # note that execution order >= extracted_nn_structure
    # the idea of this loop is that it is only the number of nodes for each layer of the model structure that is stored in extracted_nn_structure
    # which means that it is only the forward_pass id func type that stores its number of nodes in extracted_nn_structure
    count = 0
    main_nn_structure.append(extracted_nn_structure[0])
    #   TODO Ensure that is the execution order did not start from forward pass the 
    #   extracted_nn_structure should be updated with the length of the input data, also update the execution order
    for func_id in execution_order:
        func_id_name = func_id[0]

        if func_id_name == Persistent_Variables.FORWARD_PASS:
            main_nn_structure.append(extracted_nn_structure[count+1])
            layer_starting_from.append(len(main_nn_structure)-1)
            count+=1
        elif func_id_name == Persistent_Variables.ACTIVATION:
            layer_starting_from.append(len(main_nn_structure))
        elif func_id_name in [Persistent_Variables.SOFTMAX, Persistent_Variables.LOGSOFTMAX]:
            # softmax has two layers
            main_nn_structure.extend([1, main_nn_structure[-1]])
            layer_starting_from.append(len(main_nn_structure)-2)#starts from the previous layer
        elif func_id_name == Persistent_Variables.NLLLOSS:
            # nllloss has two layers
            main_nn_structure.extend([main_nn_structure[-1], 1])
            layer_starting_from.append(len(main_nn_structure) - 1)
        elif func_id_name == Persistent_Variables.CROSSENTROPY_LOSS:
            # for crossentropy nllloss layer is not created, just the softmax and target node

            main_nn_structure.extend([1, main_nn_structure[-1], 1]) # for softmax

            layer_starting_from.append(len(main_nn_structure) - 2)

    return main_nn_structure, layer_starting_from

def validate_spaces_between_layers(main_nn_structure):
    buffer_space_btw_layers = Persistent_Variables.spaces_between_layers[:]

    if len(main_nn_structure) - len(buffer_space_btw_layers) >= 2:
        """Duplicates the spaces between layers if they are not the required length"""
        result = []
        target_length = len(main_nn_structure) - 1
        while len(result) < target_length:
            result.extend(buffer_space_btw_layers)
        
        buffer_space_btw_layers = result[:target_length]
    return buffer_space_btw_layers

def create_text_dict(execution_order:list[tuple]):
    text_dict = {func_id:[] for func_id in execution_order}
    return text_dict

def put_data_for_backward_pass(backward_pass_data:list[list[list[float]]], data_dict:dict[tuple, list], execution_order:list):
    for func_id in execution_order:
        if func_id[0] == Persistent_Variables.BACKWARD_PASS:
            data_dict[func_id] = backward_pass_data
            break

def turn_activation_nodes_green_for_backward_pass(local_execution_order, main_nn_structure, layer_starting_from, backward_nodes:dict[str, Nodes]):
    nodes_idx_to_turn_green = []
    for idx, func_id in enumerate(local_execution_order):
        if func_id[0] == Persistent_Variables.ACTIVATION:
            layer_idx = layer_starting_from[idx]
            nodes_indices = generate_node_idx_for_nn(main_nn_structure=main_nn_structure, from_layer=layer_idx, to_layer=layer_idx)
            nodes_idx_to_turn_green.extend(*nodes_indices)
    
    for nodes_idx in nodes_idx_to_turn_green:
        if nodes_idx in backward_nodes:
            backward_nodes[nodes_idx].mass_update_state({'color':(0, 200, 0)})
    
def share_backward_pass_data_single_epoch(backward_data_per_epoch:list[list[float]], local_execution_order:list[tuple], activation_data_dict:dict[tuple, list], indices):
    """Modifies inplace backward_data_epoch"""

    """for func_id in local_execution_order:
        if func_id[0] == Persistent_Variables.ACTIVATION:
            activation_data_dict[func_id].append([backward_data_per_epoch[func_id[1]+1]])

    for i in sorted(indices, reverse=True):
        del backward_data_per_epoch[i]"""

    for func_id in local_execution_order:
        if func_id[0] == Persistent_Variables.ACTIVATION:
            activation_data_dict[func_id].append([backward_data_per_epoch[func_id[1]+1]])
            backward_data_per_epoch[func_id[1]+1] = 'placeholder'

    for func_id in local_execution_order:
        if func_id[0] == Persistent_Variables.SOFTMAX:
            backward_data_per_epoch.insert(func_id[1]+1, [Persistent_Variables.SOFTMAX])
        elif func_id[0] == Persistent_Variables.LOGSOFTMAX:
            backward_data_per_epoch.insert(func_id[1]+1, [Persistent_Variables.LOGSOFTMAX])
    
    length = len(backward_data_per_epoch) - 1
    for idx, data in enumerate(backward_data_per_epoch[::-1]):
        if data == 'placeholder':
            del backward_data_per_epoch[length-idx] 
    


def share_backward_pass_data_multiple_epoch(backward_pass_data:list[list[list[float]]], local_execution_order:list[tuple]):
    """Modifies inplace backward_data_epoch"""
    
    activation_data_dict:dict[tuple, list] = create_text_dict(local_execution_order)
    indices = []
    for idx, func_id in enumerate(local_execution_order):
        if func_id[0] == Persistent_Variables.ACTIVATION:
            indices.append(idx+1)
    for backward_data_per_epoch in backward_pass_data:
        share_backward_pass_data_single_epoch(backward_data_per_epoch, local_execution_order, activation_data_dict, indices)
    
    return activation_data_dict

def share_data_single_epoch(data_per_epoch:list[list[int|float]], execution_order:list[tuple], data_dict:dict[tuple, list]=None):
    stop_index = 0
    for func_id in execution_order:
        if func_id[0] == Persistent_Variables.FORWARD_PASS:
            start_idx = stop_index
            end_idx = stop_index + 2

            data_dict[func_id].append(data_per_epoch[start_idx:end_idx])

            stop_index = end_idx - 1
        elif func_id[0] == Persistent_Variables.ACTIVATION:
            start_idx = stop_index + 1

            data_dict[func_id].append([data_per_epoch[start_idx]])

            stop_index = start_idx
        elif func_id[0] in [Persistent_Variables.SOFTMAX, Persistent_Variables.LOGSOFTMAX]:

            start_idx = stop_index
            end_idx = start_idx + 2

            data = data_per_epoch[start_idx:end_idx]
            data.insert(1, [func_id[0].capitalize()])
            data_dict[func_id].append(data)

            stop_index = end_idx - 1
        elif func_id[0] == Persistent_Variables.NLLLOSS: # the data or text for the target node will be gotten seperately
            start_idx = stop_index

            data_dict[func_id].append([data_per_epoch[start_idx]])
        
        elif func_id[0] == Persistent_Variables.CROSSENTROPY_LOSS:
            start_idx = stop_index
            end_idx = start_idx + 2
            data = data_per_epoch[start_idx:end_idx]
            data.insert(1, [Persistent_Variables.SOFTMAX])
            data_dict[func_id].append(data)
            stop_index = end_idx - 1
            
    
def share_data_multiple_epoch(total_data:list[list[list[float]]], execution_order:list[tuple]):
    data_dict = create_text_dict(execution_order)
    for data_per_epoch in total_data:
        share_data_single_epoch(data_per_epoch=data_per_epoch, execution_order=execution_order, data_dict=data_dict)
    return data_dict

def update_all_activation_data_appropriately(obj:Persistent_Variables, data):
    """This function is created most especially for cases where by two activation function shares one object"""
    if obj.all_activation_data is None:
        obj.all_activation_data = data
    else:
        # merges the data such that all the data in the same epoch are located in the same list
        obj.all_activation_data = [x + y for x, y in zip(obj.all_activation_data, data)]

def inherit_previous_layer_nodes(idx, execution_order, execution_function_objects:dict[tuple, Persistent_Variables], start_layer, main_nn_structure, nodes:dict):
    if idx != 0:
        """
            Inherits nodes from the last layer of the previous component and assigns them to the current layer.
            Args:
                idx: The current index in the execution order.
                start_layer: The starting layer index of the current component.
                main_nn_structure: The main neural network structure.
                nodes: The current nodes being processed.
        """
        prev_func_id = execution_order[idx-1]
        prev_object = execution_function_objects[prev_func_id]
        prev_component_last_layer_idx = start_layer - 1
        layer_nodes_gen = layer_nodes_generator(nn_structure=[main_nn_structure[prev_component_last_layer_idx]],
                                from_layer=start_layer)
        
        for layer_node_indices in layer_nodes_gen:
            for node_idx in layer_node_indices:
                if node_idx in prev_object.nodes:
                    nodes[node_idx] = prev_object.nodes[node_idx]

def mirrow_forward_pass_function(nodes:dict[str, Nodes], lines:dict[str, Line], local_exec_order:list[tuple], execution_function_objects:dict[tuple, Persistent_Variables]):
    # Mirror important changes
    for id, obj in execution_function_objects.items():
        if id in local_exec_order:
            for node_id, node_obj in obj.nodes.items():
                if isinstance(node_obj, Rect):
                    rect_obj = Rect(Persistent_Variables.display_surface, Persistent_Variables.font)
                    state = node_obj.state()
                    rect_obj.mass_update_state(state)
                    nodes[node_id] = rect_obj
            for line_id, line_obj in obj.lines.items():
                if line_obj.custom_line_coor_func is not None:
                    lines[line_id].custom_line_coor_func = line_obj.custom_line_coor_func


def generate_objects(main_nn_structure, layer_starting_from, execution_order:list[tuple], data_dict:dict[tuple, list], extra_data):
    execution_function_objects:dict[tuple, Persistent_Variables] = {}
    
    for idx, func_id in enumerate(execution_order):
        func_id_name = func_id[0]
        if func_id_name == Persistent_Variables.FORWARD_PASS:
            start_layer = layer_starting_from[idx]
            nn_structure = main_nn_structure[start_layer-1:start_layer+1]
            nodes, lines = generate_componets(window=Persistent_Variables.display_surface,
                                              font=Persistent_Variables.font,
                                              spaces_between_layers=Persistent_Variables.spaces_between_layers,
                                              height=Persistent_Variables.screen_height,
                                              node_radius=Persistent_Variables.node_radius,
                                              nn_structure=nn_structure,
                                              main_nn_structure=main_nn_structure,
                                              initial_x=Persistent_Variables.initial_x,
                                              from_layer=start_layer,
                                              to_layer=start_layer + 1,)
            inherit_previous_layer_nodes(idx=idx,
                                         execution_order=execution_order,
                                         execution_function_objects=execution_function_objects,
                                         start_layer=start_layer,
                                         main_nn_structure=main_nn_structure,
                                         nodes=nodes)
            
            obj = Persistent_Variables(nodes=nodes,
                                       lines=lines,
                                       nn_structure=nn_structure,
                                       total_data=data_dict[func_id],
                                       from_layer=start_layer,
                                       to_layer=start_layer+1)
            execution_function_objects[func_id] = obj

        elif func_id_name == Persistent_Variables.ACTIVATION:
            """activation functions takes the previous object in the execution order"""

            execution_function_objects[func_id] = execution_function_objects[execution_order[idx-1]]
            #execution_function_objects[func_id].all_activation_data = data_dict[func_id]
            update_all_activation_data_appropriately(obj=execution_function_objects[func_id], data=data_dict[func_id])
        
        elif func_id_name in [Persistent_Variables.SOFTMAX, Persistent_Variables.LOGSOFTMAX]:
            start_layer = layer_starting_from[idx]
            nn_structure = main_nn_structure[start_layer-1:start_layer+2]

            nodes, lines = generate_components_for_softmax(window=Persistent_Variables.display_surface,
                                                            font=Persistent_Variables.font,
                                                            space_between_layers=Persistent_Variables.spaces_between_layers,
                                                            height=Persistent_Variables.screen_height,
                                                            nn_structure=nn_structure,
                                                            main_nn_structure=main_nn_structure,
                                                            node_radius=Persistent_Variables.node_radius,
                                                            from_layer=start_layer,
                                                            to_layer=start_layer+2,
                                                            func_type=func_id_name.capitalize())
            inherit_previous_layer_nodes(idx=idx,
                                         execution_order=execution_order,
                                         execution_function_objects=execution_function_objects,
                                         start_layer=start_layer,
                                         main_nn_structure=main_nn_structure,
                                         nodes=nodes)
            
            obj = Persistent_Variables(nodes=nodes,
                                       lines=lines,
                                       nn_structure=nn_structure,
                                       total_data=data_dict[func_id],
                                       from_layer=start_layer,
                                       to_layer=start_layer+2)
            
            execution_function_objects[func_id] = obj
        
        elif func_id_name == Persistent_Variables.NLLLOSS:
            start_layer = layer_starting_from[idx]
            nn_structure = main_nn_structure[start_layer-1:start_layer]

            nodes, lines = generate_componets(window=Persistent_Variables.display_surface,
                                              font=Persistent_Variables.font,
                                              spaces_between_layers=Persistent_Variables.spaces_between_layers,
                                              height=Persistent_Variables.screen_height,
                                              nn_structure=nn_structure,
                                              main_nn_structure=main_nn_structure,
                                              node_radius=Persistent_Variables.node_radius,
                                              from_layer=start_layer,
                                              to_layer=start_layer)

            index = start_layer
            target_nn_structure = main_nn_structure[index:index+1]

            target_node, _ = generate_componets(window=Persistent_Variables.display_surface,
                                                font=Persistent_Variables.font,
                                                spaces_between_layers=Persistent_Variables.spaces_between_layers,
                                                height=Persistent_Variables.screen_height,
                                                nn_structure=target_nn_structure,
                                                main_nn_structure=main_nn_structure,
                                                node_radius=Persistent_Variables.node_radius,
                                                from_layer=index+1)
            obj = Persistent_Variables(nodes=nodes,
                                       lines=lines,
                                       nn_structure=nn_structure,
                                       total_data=data_dict[func_id],
                                       local_execution_order=[(Persistent_Variables.MAIN_NLLLOSS, 0), (Persistent_Variables.MOVE_NODES, 1)],
                                       from_layer=start_layer,
                                       to_layer=start_layer)

            obj.target_node = target_node
            
            execution_function_objects[func_id] = obj

        elif func_id_name == Persistent_Variables.CROSSENTROPY_LOSS:
            sm_start_layer = layer_starting_from[idx] - 1 # subtracted because it is to start from the previous layer
            sm_nn_structure = main_nn_structure[sm_start_layer-1:sm_start_layer+2]

            sm_nodes, sm_lines = generate_components_for_softmax(window=Persistent_Variables.display_surface,
                                                            font=Persistent_Variables.font,
                                                            space_between_layers=Persistent_Variables.spaces_between_layers,
                                                            height=Persistent_Variables.screen_height,
                                                            nn_structure=sm_nn_structure,
                                                            main_nn_structure=main_nn_structure,
                                                            node_radius=Persistent_Variables.node_radius,
                                                            from_layer=sm_start_layer,
                                                            to_layer=sm_start_layer+2)
            index = sm_start_layer + 2
            target_nn_structure = main_nn_structure[index:index+1]
            target_node, _ = generate_componets(window=Persistent_Variables.display_surface,
                                                font=Persistent_Variables.font,
                                                spaces_between_layers=Persistent_Variables.spaces_between_layers,
                                                height=Persistent_Variables.screen_height,
                                                nn_structure=target_nn_structure,
                                                main_nn_structure=main_nn_structure,
                                                node_radius=Persistent_Variables.node_radius,
                                                from_layer=index+1)
            inherit_previous_layer_nodes(idx=idx,
                                         execution_order=execution_order,
                                         execution_function_objects=execution_function_objects,
                                         start_layer=sm_start_layer,
                                         main_nn_structure=main_nn_structure,
                                         nodes=sm_nodes)
            
            obj = Persistent_Variables(nodes=sm_nodes,
                                       lines=sm_lines,
                                       nn_structure=sm_nn_structure,
                                       total_data=data_dict[func_id],
                                       local_execution_order=[(Persistent_Variables.SOFTMAX, 0), (Persistent_Variables.CE_NLLLOSS, 1), (Persistent_Variables.MOVE_NODES, 2)],
                                       from_layer=sm_start_layer,
                                       to_layer=sm_start_layer+2)
            
            obj.target_node = target_node
            obj.extra_data = {Persistent_Variables.LOSS_VAL:extra_data[Persistent_Variables.LOSS_VAL]}
            #obj.ideal_nn_structure = sm_nn_structure            
            execution_function_objects[func_id] = obj
        
        elif func_id_name == Persistent_Variables.BACKWARD_PASS:
            # get index of loss function
            loss_function_names = Persistent_Variables.AVAILABLE_LOSS_FUNC
            start_layer_of_loss_func = None
            index_of_loss_func = None
            for func_id_tuple in execution_order:
                if func_id_tuple[0] in loss_function_names:
                    index_of_loss_func = execution_order.index(func_id_tuple)
                    start_layer_of_loss_func = layer_starting_from[index_of_loss_func]
                    break
            else:
                """For a case where there is no loss function"""
                start_layer_of_loss_func = len(main_nn_structure) + 1
                index_of_loss_func = -1

            bk_nn_structure:list = main_nn_structure[:start_layer_of_loss_func-1]
            bk_nn_structure.append(1) # Adding loss node

            local_exec_order = execution_order[:index_of_loss_func]

            # because of loss node
            local_exec_order.append((Persistent_Variables.FORWARD_PASS, len(local_exec_order)))


            nodes, lines = generate_componets(window=Persistent_Variables.display_surface, 
                                              font=Persistent_Variables.font,
                                              spaces_between_layers=Persistent_Variables.spaces_between_layers,
                                              height=Persistent_Variables.screen_height,
                                              node_radius=Persistent_Variables.node_radius,
                                              nn_structure=bk_nn_structure,)
            
            mirrow_forward_pass_function(nodes, lines, local_exec_order[:-1], execution_function_objects)

            activation_data_dict = share_backward_pass_data_multiple_epoch(data_dict[func_id], local_exec_order)

            reversed_local_exec_order = local_exec_order[::-1]
            obj = Persistent_Variables(nodes=nodes,
                                       lines=lines,
                                       nn_structure=bk_nn_structure,
                                       total_data=data_dict[func_id],
                                       local_execution_order=reversed_local_exec_order,
                                       backward=True)
            
            for id, activation_data in activation_data_dict.items():
                if id[0] == Persistent_Variables.ACTIVATION:
                    update_all_activation_data_appropriately(obj=obj, data=activation_data)
            
            turn_activation_nodes_green_for_backward_pass(local_exec_order, 
                                                          main_nn_structure, 
                                                          layer_starting_from, 
                                                          obj.nodes)
            execution_function_objects[func_id] = obj
    
    return execution_function_objects


