from .persistent_vars import Persistent_Variables
from .generate_objs_and_components import generate_main_nn_structure, share_data_multiple_epoch, put_data_for_backward_pass, generate_objects
from .generators_and_utility_functions import map_line_idxs_to_weight, generate_all_weight_or_grad_data, map_nodes_to_weights, layer_nodes_generator
from .generators_and_utility_functions import convert_tensors_to_lists, add_bias_for_input_nodes, add_initial_grad_for_lines_and_nodes
from .minor_components import Pause_button, Nav_Buttons, Iteration_Count
from .parameters import GlobalParameters

def initialise_class_parameters():
    GlobalParameters.initialize_core_params()
    Pause_button.initialize_pause_button_params()
    Nav_Buttons.initialize_nav_buttons_params()
    Iteration_Count.initialize_iter_count_params()
    
def prepare_and_initialise_exec_order(execution_order):
    # Prepare execution order
    execution_order = [(func_id_name, idx) for idx, func_id_name in enumerate(execution_order)]
    Persistent_Variables.execution_order = execution_order
    Persistent_Variables.initialise_exec_order()

def set_target_data_for_visualization(target_data):
    # initialise target data
    Persistent_Variables.all_target_data = target_data
    Persistent_Variables.initialise_target_data()

def generate_objects_for_visualization(all_forward_pass_data, all_backward_pass_data, extracted_nn_structure, extra_data):
    # Generate object
    main_nn_structure, layer_starting_from = generate_main_nn_structure(execution_order=Persistent_Variables.execution_order, extracted_nn_structure=extracted_nn_structure)
    Persistent_Variables.main_nn_structure = main_nn_structure

    data_dict = share_data_multiple_epoch(total_data=all_forward_pass_data, execution_order=Persistent_Variables.execution_order)
    put_data_for_backward_pass(backward_pass_data=all_backward_pass_data, data_dict=data_dict, execution_order=Persistent_Variables.execution_order)

    execution_function_objects = generate_objects(main_nn_structure, layer_starting_from, Persistent_Variables.execution_order, data_dict, extra_data)
    Persistent_Variables.execution_function_objects = execution_function_objects

    # setting node grad data for click display
    # the backward pass data has been modified inplace during backward pass object generation
    #TODO Remove this from here
    set_node_grad_data_from_data_dict(data_dict)

"""sets the map to enable clicking of lines and nodes"""
def set_weight_data(forward_pass_order, weight_map):
    all_weight_data = generate_all_weight_or_grad_data(forward_pass_order, weight_map)
    line_idx_to_weight_map = {}

    if all_weight_data:
        for weight_per_epoch in all_weight_data:
            map_line_idxs_to_weight(weight_per_epoch, line_idx_to_weight_map)

    GlobalParameters.line_idx_to_weight_map = line_idx_to_weight_map

def set_weight_grad_data(forward_pass_order, weight_grad_map):
    all_grad_data = generate_all_weight_or_grad_data(forward_pass_order, weight_grad_map)

    line_idx_to_grad_map = {}
    if all_grad_data:
        for grad_per_epoch in all_grad_data:
            map_line_idxs_to_weight(grad_per_epoch, line_idx_to_grad_map)

    line_idx_to_grad_map = add_initial_grad_for_lines_and_nodes(line_idx_to_grad_map)
    GlobalParameters.line_idx_to_grad_map = line_idx_to_grad_map

def set_node_bias_data(forward_pass_order, node_bias_map):
    node_bias_map = convert_tensors_to_lists(node_bias_map)
    all_bias_data = generate_all_weight_or_grad_data(forward_pass_order, node_bias_map)

    node_idx_to_bias_map = {}

    if all_bias_data:
        all_bias_data = add_bias_for_input_nodes(Persistent_Variables.main_nn_structure, all_bias_data)

        for bias_per_epoch in all_bias_data:
            map_nodes_to_weights(bias_per_epoch, node_idx_to_bias_map)

    GlobalParameters.node_idx_to_bias_map = node_idx_to_bias_map

def set_node_grad_data(all_backward_pass_data):
    node_idx_to_grad_map = {}

    for node_grad_per_epoch in all_backward_pass_data:
        map_nodes_to_weights(node_grad_per_epoch, node_idx_to_grad_map)
        
    node_idx_to_grad_map = add_initial_grad_for_lines_and_nodes(node_idx_to_grad_map)
    GlobalParameters.node_idx_to_grad_map = node_idx_to_grad_map

def set_node_grad_data_from_data_dict(data_dict:dict[str, list[list[list[float]]]]):
    for func_id in data_dict:
        if func_id[0] == Persistent_Variables.BACKWARD_PASS:
            set_node_grad_data(data_dict[func_id])
            break

def set_line_weights_and_grad_data(forward_pass_order, weight_map, weight_grad_map):
    set_weight_data(forward_pass_order, weight_map)
    set_weight_grad_data(forward_pass_order, weight_grad_map)


def activate_first_layer_node():
    # make nodes green if activation function starts first
    # note that if an activation function starts first the func_id will be changed to a forward_pass
    obj = Persistent_Variables.execution_function_objects[Persistent_Variables.execution_order[0]]

    for node_idx_list in layer_nodes_generator(nn_structure=[obj.nn_structure[0]]):
        for node_idx in node_idx_list:
            obj.nodes[node_idx].mass_update_state({'color': (0, 200, 0)})