
def generate_node_coordinates(nodes_per_layer:list, height, node_radius, initial_x=100, y_space_between_nodes=20, y_space_center_to_center=100, x_space_center_to_center=200):
    """nodes_per_layer is a list of the number of nodes present in each layer"""

    height_center = height/2
    result = list()
    stop_x = len(nodes_per_layer) * x_space_center_to_center

    for i, x in enumerate(range(initial_x, stop_x, x_space_center_to_center)):
        
        layer_coor = []
        if nodes_per_layer[i] == 1:
            layer_coor.append((x, height_center))
            nodes_left = 0
        elif nodes_per_layer[i] % 2 != 0:
            up = (x, height_center-y_space_center_to_center)
            down = (x, height_center + y_space_center_to_center)
            
            layer_coor.append((x, height_center))
            layer_coor.append(up)
            layer_coor.append(down)

            nodes_left = nodes_per_layer[i] - 3
        else:
            up = (x, height_center-(y_space_between_nodes/2 + node_radius))
            down = (x, height_center+(y_space_between_nodes/2 + node_radius))
            layer_coor.append(up)
            layer_coor.append(down)
            nodes_left = nodes_per_layer[i] - 2

        for j in range(1, nodes_left+1):
            if j%2==0:
                up = (x, up[1] - y_space_center_to_center)
                down = (x, down[1] + y_space_center_to_center)
                layer_coor.append(up)
                layer_coor.append(down)
            elif j == nodes_left:
                down = (x, down[1] + y_space_center_to_center)
                layer_coor.append(down)
        layer_coor = sorted(layer_coor, key=lambda x:x[1]) # sorting based on the y-axis 
        result.append(layer_coor)
    return result

def generate_layer_coordinates(num_nodes :int, height, node_radius, x_coor=100, y_space_center_to_center=100)->list[tuple]:
    """
    Generates a coordinates for a single layer
    x_coor: initial value for x
    """
    height_center = height/2
    y_space_between_nodes = y_space_center_to_center - node_radius * 2
    layer_coor = []

    if num_nodes == 1:
        layer_coor.append((x_coor, height_center))
        nodes_left = 0
    elif num_nodes % 2 != 0:
        up = (x_coor, height_center-y_space_center_to_center)
        down = (x_coor, height_center + y_space_center_to_center)
        
        layer_coor.append((x_coor, height_center))
        layer_coor.append(up)
        layer_coor.append(down)

        nodes_left = num_nodes - 3
    else:
        up = (x_coor, height_center-(y_space_between_nodes/2 + node_radius))
        down = (x_coor, height_center+(y_space_between_nodes/2 + node_radius))
        layer_coor.append(up)
        layer_coor.append(down)
        nodes_left = num_nodes - 2

    for j in range(1, nodes_left+1):
        if j%2==0:
            up = (x_coor, up[1] - y_space_center_to_center)
            down = (x_coor, down[1] + y_space_center_to_center)
            layer_coor.append(up)
            layer_coor.append(down)
        elif j == nodes_left:
            down = (x_coor, down[1] + y_space_center_to_center)
            layer_coor.append(down)

    layer_coor = sorted(layer_coor, key=lambda x:x[1]) # sorting based on the y-axis 

    return layer_coor


def generate_coordinates_with_flexible_layer_position(nodes_per_layer:list, spaces_between_layers:list, height, node_radius, initial_x=100, y_space_center_to_center=100,):
    """Generates node coordinates including those of the loss function
    It generates layers of coordinates based on a list of different length of center to center distances in the x dimension
    It duplicates the spaces between layers e.g if nodes_per_layer = [3, 4, 5, 6, 7] spaces_between_layers = [200, 100]
    it will duplicates it to [200, 100, 200, 100]
    
    height: height of the screen  or canvas  
    """
    main_spaces_between_layers = spaces_between_layers[:]
    
    if not nodes_per_layer:
        raise ValueError(f"nodes_per_layer is {nodes_per_layer} is empty")
    elif not main_spaces_between_layers:
        raise ValueError(f"spaces_between_layers is empty{main_spaces_between_layers} is empty")
    
    if len(nodes_per_layer) - len(main_spaces_between_layers) >= 2:
        """Duplicates the spaces between layers if they are not the required length"""
        result = []
        target_length = len(nodes_per_layer)
        while len(result) < target_length:
            result.extend(main_spaces_between_layers)
        
        main_spaces_between_layers = result[:target_length]
    
    
    if len(nodes_per_layer) - len(main_spaces_between_layers) == 1:
        main_spaces_between_layers.append(0)

    layers_coor = []
    for num_nodes_per_layer, space in zip(nodes_per_layer, main_spaces_between_layers):
        layer = generate_layer_coordinates(num_nodes_per_layer, height, node_radius, x_coor=initial_x, y_space_center_to_center=y_space_center_to_center)
        layers_coor.append(layer)
        initial_x += space

    return layers_coor

if __name__ == '__main__':
    layer1 = generate_node_coordinates([2, 3, 3], 668, 40)
    layer2 = generate_coordinates_with_flexible_layer_position([2, 3, 3], [200], 668, 40)
    layer3 = generate_layer_coordinates(3, 668, 40, x_coor=300)

    print(layer1, "\n")
    print(layer2, "\n")
    print(layer3)