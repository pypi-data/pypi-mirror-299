from .draw_on_screen import Line, Nodes, Rect
from .screen_operations import * 
from .generators_and_utility_functions import *
from .generate_coordinates import *
from .constants import String_Constants
import math


def generate_componets(window, font, spaces_between_layers, height, node_radius, nn_structure=None, initial_x=100, y_space_center_to_center=100, from_layer=1, to_layer=None, main_nn_structure=None):
    """
    Generates nodes and connecting lines as dictionaries.

    Parameters:
    - window: The display window where the components will be drawn.
    - font: The font used for rendering text on the nodes.
    - spaces_between_layers: The horizontal space between layers in the neural network.
    - height: The height of the display area for the components.
    - node_radius: The radius of each node in the neural network.
    - nn_structure (optional): A list defining the neural network to generate components for. If not provided, `main_nn_structure` will be used.
    - initial_x (optional): The x-coordinate of the first component or layer starting from the left of the screen. Defaults to 100.
    - y_space_center_to_center (optional): The vertical space from the center of one node to the center of another. Defaults to 100.
    - from_layer (optional): The starting layer for generating components. Useful for generating a subset of components from `main_nn_structure` while preserving node and line indices. Defaults to 1.
    - to_layer (optional): The ending layer for generating components. If not provided, it defaults to the end of the structure.
    - main_nn_structure (optional): The parent structure used as a template when generating components for a subset of layers. 

    Description:
    - If `from_layer` is not 1, `initial_x` represents the x-coordinate of the first component or layer starting from the left of the screen.
    - If `from_layer` is greater than 1 and `main_nn_structure` is provided, `nn_structure` will be inferred from `main_nn_structure`, generating components starting from `from_layer` to `to_layer`.
    - `spaces_between_layers` must correspond to the space between layers of the `main_nn_structure` if `from_layer` is used.
    - If both `nn_structure` and `main_nn_structure` are provided and `from_layer` is greater than 1, the input `nn_structure` will be used instead of inferring from `main_nn_structure`.
    
    """
    nodes:dict[str, Nodes] = dict()
    lines:dict[str, Line] = dict()
    if from_layer > 1:

        if from_layer > len(main_nn_structure):
            raise ValueError(f"The starting layer '{from_layer}' should be less than the number of layers in main_nn_structure {main_nn_structure}")
        
        if nn_structure is None:
            nn_structure = main_nn_structure[from_layer-1:to_layer]

        if len(main_nn_structure) - len(spaces_between_layers) >= 2:
            """Duplicates the spaces between layers if they are not the required length"""
            result = []
            target_length = len(main_nn_structure) - 1
            while len(result) < target_length:
                result.extend(spaces_between_layers)
            
            spaces_between_layers = result[:target_length]

        # get the starting coordinate of the component
        for space in spaces_between_layers[:from_layer-1]:
            initial_x += space


    layers = generate_coordinates_with_flexible_layer_position(nn_structure, spaces_between_layers, height, node_radius, initial_x=initial_x, y_space_center_to_center=y_space_center_to_center)

    # generating circles/nodes 
    for layer_idx, layer in enumerate(layers, start=from_layer):
        for node_idx, node_coor in enumerate(layer, start=1):
            component = Nodes(window, font)#Components(window, font)
            params = ['x', 'y', 'text']
            values = [*node_coor, '']
            components = dict(zip(params, values))
            component.mass_update_state(components)
            # e.g key node12 will be node 1 in layer 2, i am counting from top to bottom for nodes and left to right for layers
            nodes[f'node{node_idx}{layer_idx}'] = component

    # generate lines 
    for layer_idx, layer_pair in enumerate(zip(layers, layers[1:]), start=from_layer):

        layer1 = layer_pair[0]
        layer2 = layer_pair[1]

        for start_node, node_coor1 in enumerate(layer1, start=1):
            for end_node, node_coor2 in enumerate(layer2, start=1):
                component = Line(window)
                params = ['start_center', 'end_center']
                values = [node_coor1, node_coor2]
                components = dict(zip(params, values))
                component.mass_update_state(components)
                #e.g key line132 will be line from node 1 of layer 2 to node 3 of the next layer
                lines[f'line{start_node}{end_node}{layer_idx}'] = component
    
    return nodes, lines

def generate_componenets_for_backward_pass(window, font, height, spaces_between_layers:list, node_radius, main_nn_structure:list, layer_starting_from:list, execution_order:list):
    main_spaces_between_layers = spaces_between_layers[:]

    # get index of loss function
    loss_function_names = String_Constants.AVAILABLE_LOSS_FUNC
    start_layer_of_loss_func = None
    for func_id_tuple in execution_order:
        if func_id_tuple[0] in loss_function_names:
            start_layer_of_loss_func = layer_starting_from[execution_order.index(func_id_tuple)]
            break
    bk_nn_structure:list = main_nn_structure[:start_layer_of_loss_func]
    bk_nn_structure.append(1) # Adding loss node

    # To get spaces between layers, the idea is that if there is an activation funciton in the execution order,
    # the space between layers should be half of the original space between layers. in this case i am rendering nodes for activation functions
    if len(main_nn_structure) - len(main_spaces_between_layers) >= 2:
        """Duplicates the spaces between layers if they are not the required length"""
        result = []
        target_length = len(main_nn_structure) - 1
        while len(result) < target_length:
            result.extend(main_spaces_between_layers)
        
        main_spaces_between_layers = result[:target_length]

    main_spaces_between_layers = main_spaces_between_layers[:len(bk_nn_structure)-1]


    indices_of_activation_funcs = []
    for func_id in execution_order:
        if func_id[0] == 'activation':
            start_layer_of_activation_func = layer_starting_from[execution_order.index(func_id)]
            indices_of_activation_funcs.append(start_layer_of_activation_func-1)

    # Create new lists to store the results
    result_structure = []
    result_spaces = []
    activation_layers = []
    
    # Iterate through the bk_nn_structure and duplicate elements based on indices_of_activation_funcs
    for i in range(len(bk_nn_structure)):
        result_structure.append(bk_nn_structure[i])  # Add the current layer from bk_nn_structure

        if i in indices_of_activation_funcs:  # Duplicate the layer if index is in indices_of_activation_funcs
            result_structure.append(bk_nn_structure[i])  # Add the duplicate layer
            activation_layers.append(len(result_structure))

            if i < len(main_spaces_between_layers):  # Adjust the spacing for the duplicate
                new_space = main_spaces_between_layers[i] - 50
                new_space = new_space if new_space > 150 else 150
                result_spaces.append(150)  # Halve the spacing for the duplicated layer

        if i < len(main_spaces_between_layers):  # Only add spacing if we're not at the last layer
            result_spaces.append(main_spaces_between_layers[i])  # Add the current spacing from main_spaces_between_layers
    
    bk_nn_structure = result_structure
    main_spaces_between_layers = result_spaces

    nodes, lines = generate_componets(window=window, 
                                        font=font,
                                        spaces_between_layers=main_spaces_between_layers,
                                        height=height,
                                        node_radius=node_radius,
                                        nn_structure=bk_nn_structure,)
            
            
    return nodes, lines, bk_nn_structure

def generate_components_for_softmax(window, font, space_between_layers, height, node_radius, initial_x=100, nn_structure=None, from_layer=1, to_layer=None, main_nn_structure=None, func_type='Softmax'):
    
    nodes, lines = generate_componets(window, 
                                      font, 
                                      space_between_layers, 
                                      height, 
                                      node_radius, 
                                      nn_structure=nn_structure, 
                                      initial_x=initial_x, 
                                      from_layer=from_layer, 
                                      to_layer=to_layer, 
                                      main_nn_structure=main_nn_structure)
    
    # changing one of the nodes to rectangle 
    rectangle = Rect(window, font)
    #x_sm = x_coor_of_last_nn_layer + space_btw_nn_and_softmax
    x = nodes[f'node1{from_layer+1}'].x
    y = nodes[f'node1{from_layer+1}'].y

    rectangle.mass_update_state({'rect_width':100, 'rect_height':100, 'color':(0, 0, 0), 'text':func_type, 'x':x, 'y':y})
    nodes[f'node1{from_layer+1}'] = rectangle

    # Adjust lines 
    line_gen = line_from_layer_to_layer_generator(nn_structure=nn_structure,
                                       main_nn_structure=main_nn_structure, 
                                       from_layer=from_layer,
                                       to_layer=to_layer,)

    line_from_node_to_rectangle = next(line_gen)

    line_from_rectangle_to_node = next(line_gen)

    for line_idx in line_from_node_to_rectangle:
        lines[line_idx].custom_line_coor_func = custom_line_coor_func(node_radius, 50)

    for line_idx in line_from_rectangle_to_node:
        lines[line_idx].custom_line_coor_func = custom_line_coor_func(50, node_radius)

    return nodes, lines 

def custom_line_coor_func(radius1, radius2):
    def main_line_coor_func(start_center, end_center, **kwargs):
        angle = math.atan2(end_center[1] - start_center[1], end_center[0] - start_center[0])

        start_point = start_center[0] + radius1 * math.cos(angle), start_center[1] + radius1 * math.sin(angle)
        end_point = end_center[0] + radius2 * math.cos(angle+math.pi), end_center[1] + radius2 * math.sin(angle+math.pi)

        return start_point, end_point
        
    return main_line_coor_func