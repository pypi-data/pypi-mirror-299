from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import torch

def lines_to_throb_generator(nn_structure:list|None=None, main_nn_structure=None, from_layer=1, to_layer=None):
    """
    Generates indexes of lines to throb in a sequential manner
    Note that nn_structure overides main_nn_structure if it is present
    """
    
    start_layer_idx = from_layer - 1
    if nn_structure is None:
        nn_structure = main_nn_structure[start_layer_idx:to_layer]

    num_layers = len(nn_structure)

    for line_start_idx, layer_idx in enumerate(range(num_layers - 1), start=start_layer_idx): # subtracted 1 to avoid error when getting future_node_idx
        for future_node_idx in range(nn_structure[layer_idx+1]):
            lines_to_throb = []
            for prev_node_idx in range(nn_structure[layer_idx]):
                line_idx = f'line{prev_node_idx + 1}{future_node_idx + 1}{line_start_idx + 1}'
                lines_to_throb.append(line_idx)
            yield lines_to_throb


def backward_lines_to_throb_generator(nn_structure:list|None=None, main_nn_structure=None, from_layer=1, to_layer=None):
    """
    Generates indexes of lines to throb in a sequential manner from the last layer to the first.
    Note that nn_structure overides main_nn_structure if it is present
    """

    start_layer_idx = from_layer - 1
    if nn_structure is None:
        nn_structure = main_nn_structure[start_layer_idx:to_layer]

    
    to_layer = start_layer_idx + len(nn_structure)

    num_layers = len(nn_structure)


    for layer_idx, line_start_idx in zip(range(num_layers - 2, -1, -1), range(to_layer-2, -1, -1)):  # Start from the last layer and move backward
        for prev_node_idx in range(nn_structure[layer_idx]):
            lines_to_throb = []
            for future_node_idx in range(nn_structure[layer_idx+1]):
                line_idx = f'line{prev_node_idx + 1}{future_node_idx + 1}{line_start_idx + 1}'
                lines_to_throb.append(line_idx)
            yield lines_to_throb



def generate_node_idx_for_nn(nn_structure:list|None=None, main_nn_structure=None, from_layer=1, to_layer=None)->list[list[str]]:
    """
    Returns a list of lists, where each inner list contains the indices of nodes for a specific layer.

    Each inner list corresponds to a layer in a neural network, with the first layer's nodes at index 0,
    the second layer's nodes at index 1, and so on. The index in the outer list is equal to the layer number minus one.
    """
    start_layer_idx = from_layer - 1
    if nn_structure is None:
        nn_structure = main_nn_structure[start_layer_idx:to_layer]

    node_idx_all_layers = [[f'node{node_idx+1}{layer_idx+1}' for node_idx in range(num_nodes)] 
                            for layer_idx, num_nodes in enumerate(nn_structure, start=start_layer_idx)]
    
    
    return node_idx_all_layers

def layer_nodes_generator(nn_structure=None, generate_from_layer=1, main_nn_structure=None, from_layer=1, to_layer=None, backward=False):
    """
    Generates layer nodes indices per iteration, therefore the output is a list
    nn_struture is always used unless nn_structure is not stated then main_nn_structure is used
    generate_from_layer: it starts generating the output from the specified layer in the nn_structure not from the first layer

    from_layer: it starts generating the indices from the first layer in the nn_structure but making the index starts from tha stated layer
    """

    if nn_structure is None:
        nn_structure = main_nn_structure

    all_idxs = generate_node_idx_for_nn(nn_structure=nn_structure,
                                        main_nn_structure=main_nn_structure,
                                        from_layer=from_layer,
                                        to_layer=to_layer)

    if backward:
        all_idxs.reverse()

    index_start_layer = generate_from_layer - 1


    for idxs in all_idxs[index_start_layer:]:
        yield idxs


def nodes_to_throb_generator(nn_structure:list, main_nn_structure=None, from_layer=1, to_layer=None, backward=False):
    """Generates indexes of nodes to throb in a sequential manner that is top to bottom, left to right"""

    nodes_indices_for_all_layers = []#generate_node_idx_for_nn(nn_structure)

    gen = layer_nodes_generator(nn_structure=nn_structure, 
                                main_nn_structure=main_nn_structure, 
                                from_layer=from_layer, 
                                to_layer=to_layer)
    
    for nodes_idx_per_layer in gen:
        nodes_indices_for_all_layers.append(nodes_idx_per_layer)
    
    if backward:
        nodes_indices_for_all_layers.reverse()

    for i, nodes_indices_per_layer in enumerate(nodes_indices_for_all_layers[1:], start=1):
        for node_idx in nodes_indices_per_layer:
            layer_nodes=nodes_indices_for_all_layers[i-1][:] # slicing does a shallow copy
            layer_nodes.append(node_idx)

            yield layer_nodes

def text_generator(text_for_all_layers:list[list], backward=False):
    """puts text in the right format to be displayed, same code as nodes_to_throb_generator, just rewrote it for convinience"""
    if backward:
        text_for_all_layers = text_for_all_layers[::-1]
    for i, texts in enumerate(text_for_all_layers[1:], start=1):
        for text in texts:
            layer_text=text_for_all_layers[i-1][:] # slicing does a shallow copy
            layer_text.append(text)

            yield layer_text


def convert_list_to_generator(total_data:list):
    for data in total_data:
        yield data

def line_from_layer_to_layer_generator(nn_structure=None, generate_from=1, main_nn_structure=None, from_layer=1, to_layer=None):
    """Line indices from a layer to another layer"""
    start_layer_idx = from_layer - 1
    if nn_structure is None:
        nn_structure = main_nn_structure[start_layer_idx:to_layer]

    if len(nn_structure) == 1:
        raise ValueError(f"nn_structure {nn_structure} should have a length greater than 1")

    layer_pair = zip(nn_structure, nn_structure[1:])

    for layer_idx, pair in enumerate(layer_pair, start=start_layer_idx):
        if layer_idx < generate_from - 1:
            continue 

        layer_line_idxs:list[str] = []
        layer1, layer2 = pair

        for start_idx in range(layer1):
            for end_idx in range(layer2):
                line_idx = f'line{start_idx+1}{end_idx+1}{layer_idx+1}'
                layer_line_idxs.append(line_idx)

        yield layer_line_idxs


#-------------------------------------utility functions----------------------------------------#
def map_line_idxs_to_weight(weights_per_iteration:list[torch.Tensor], line_idx_to_weight_map:dict[str, list]):
    """modifies inplace line_idx_to_weight_map"""
    for layer_idx, weights in enumerate(weights_per_iteration):
        for node_to_idx, nodes_weights in enumerate(weights):
            for node_from_idx, node_weight in enumerate(nodes_weights):
                line_idx = f'line{node_from_idx+1}{node_to_idx+1}{layer_idx+1}'
                n_weight = round(node_weight.item(), 2)
                if line_idx in line_idx_to_weight_map:
                    line_idx_to_weight_map[line_idx].append(n_weight)
                else:
                    line_idx_to_weight_map[line_idx] = [n_weight]

def map_nodes_to_weights(weights_per_iteration:list[list[float]], node_idx_to_weight_map:dict[str, list]):
    """modifies inplace node_idx_to_weight map"""
    for layer_idx, layer_weights in enumerate(weights_per_iteration):
        for node_id, weight in enumerate(layer_weights):
            node_idx = f'node{node_id+1}{layer_idx+1}'
            if node_idx in node_idx_to_weight_map:
                node_idx_to_weight_map[node_idx].append(weight)
            else:
                node_idx_to_weight_map[node_idx] = [weight]

def convert_tensors_to_lists(input_dict):
    """
    Converts all tensors in the lists (which are the values of the input_dict) 
    to lists.

    Args:
        input_dict (dict): Dictionary where values are lists of tensors.

    Returns:
        dict: Updated dictionary with tensors converted to lists.
    """
    updated_dict = {}
    
    for key, tensor_list in input_dict.items():
        # Ensure the value is a list of tensors
        updated_dict[key] = [list(map(lambda x: round(x, 2), tensor.tolist())) for tensor in tensor_list]
    
    return updated_dict

def map_to_comp_weights(comp_idx:str, weight_idx:int, comp_idx_to_weight_map:dict[str, list]):
    if comp_idx_to_weight_map is None:
        return None
    
    if comp_idx in comp_idx_to_weight_map:
        weights = comp_idx_to_weight_map[comp_idx]

        return weights[weight_idx]
    else:
        return None

def generate_all_weight_or_grad_data(forward_pass_order:list[str], weight_or_grad_map:dict[str, list]):
    all_grad_data:list[list[torch.Tensor]] = []

    # infer length because all values in the dict should have the same length
    if forward_pass_order and forward_pass_order[0] in weight_or_grad_map:
        data_len = len(weight_or_grad_map[forward_pass_order[0]])
    else:
        return 

    for idx in range(data_len):
        grad_per_iteration = []
        for order_idx in forward_pass_order:
            grad_per_iteration.append(weight_or_grad_map[order_idx][idx])
        all_grad_data.append(grad_per_iteration)
        
    return all_grad_data

def add_bias_for_input_nodes(main_nn_structure, all_bias_data:list[list[list[float]]]):
    """performs an inplace modifcation to all_bias_data"""
    bias_data = [0 for _ in range(main_nn_structure[0])]

    for epoch_data in all_bias_data:
        epoch_data.insert(0, bias_data)

    return all_bias_data

def add_initial_grad_for_lines_and_nodes(dict_map:dict[str, list]):
    """Modifies inplace dict map"""
    for val in dict_map.values():
        val.insert(0, 0.0)
        del val[-1]
        
    return dict_map



if __name__ == "__main__":
    gen = backward_lines_to_throb_generator(main_nn_structure=[2, 3, 3, 4, 5, 6], from_layer=2, to_layer=51)
    gen2 = lines_to_throb_generator([2, 3, 3], main_nn_structure=[2, 3, 3, 4, 5, 6], from_layer=1, to_layer=5)
    gen3 = layer_nodes_generator([2, 3, 3], generate_from_layer=2)
    gen4 = line_from_layer_to_layer_generator(main_nn_structure=[2, 4, 3], from_layer=1, to_layer=None)
    gen5 = nodes_to_throb_generator(nn_structure=[4, 2])
    for i in gen4:
        print(i)



