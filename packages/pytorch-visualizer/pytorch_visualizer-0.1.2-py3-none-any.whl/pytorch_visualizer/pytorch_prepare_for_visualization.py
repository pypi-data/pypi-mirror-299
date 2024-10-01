import torch.nn as nn
import torch
import torch.nn.functional as F
from typing import Iterable, Any
from .constants import String_Constants

class Visual_Var(String_Constants):
    @classmethod
    def initialize_visual_var(cls):
        cls.training_loop_count = 0
        cls.update_once = True
        cls.extracted_nn_structure = []
        cls.execution_order = []
        cls.end_of_first_iteration = False
        cls.forward_pass_count = 0

        cls.end_of_forward_pass = False
        
        cls.all_forward_pass_data =[]
        cls.all_backward_pass_data = []
        cls.target_data = []

        cls.forward_pass_buffer_storage = []
        cls.backward_pass_buffer_storage = []

        cls.total_num_of_iterations_to_visualize = 0

        cls.loss_list = []
        cls.label_gen = None
        cls.all_weights_data = []
        cls.weights_data_buffer_storage = []

        cls.order_of_layers = [] # order of layers or modules in the forward pass, it does not contain activation layers

        cls.weight_grad_map:dict[str, list[torch.Tensor]] = {} # where each element in the list contains the grad of the weight per iteration for that layer
        cls.bias_grad_map:dict[str, list[torch.Tensor]] = {}
        cls.weight_map:dict[str, list[torch.Tensor]] = {}
        cls.bias_map: dict[str, list[torch.Tensor]] = {}

        cls.extra_data:dict[str, list|Any] = {} # miscelleanous data to be used during visualization

        cls.is_activation_first = False

# initialise visual_var
Visual_Var.initialize_visual_var()

# ------------------------------------------Data validation---------------------------------------------#
def validate_weight_maps(weight_maps:Iterable[dict[str, list]]):

    first_map_len = None
    for idx, maps in enumerate(weight_maps):
        first_len = None
        for val in maps.values():
            # confirm if the values in each in map have the same length
            if first_len is None:
                first_len = len(val)
            else:
                # raise assertion error if they are not equal
                assert first_len == len(val), f"Weight map at index {idx}, has values with unequal length."

        # to check if all map values have the same length 
        if first_map_len is None:
            first_map_len = first_len
        else:
            assert first_map_len == len(val), f"Weight map at index {idx}, has values with a length different from other weight maps."

def validate_all_pass_data(all_pass_data:Iterable[list[list[list[float]]]]):

    for idx, data in enumerate(all_pass_data):
        # if list is empty
        if not data:
            del all_pass_data[idx]

    first_all_data_len = None 
    for all_data_idx, all_data in enumerate(all_pass_data):

        if first_all_data_len is None:
            first_all_data_len = len(all_data)
        else:
            assert first_all_data_len == len(all_data), f"Data at index {all_data_idx} has a length different from other data in the Iterable"

        first_len_per_epoch = None
        for epoch_idx, per_epoch_data in enumerate(all_data):
            if first_len_per_epoch is None:
                first_len_per_epoch = len(per_epoch_data)
            else:
                assert first_len_per_epoch == len(per_epoch_data), f"Epoch {epoch_idx+1} data, present in data at index {all_data_idx} has a length different from other epochs"

def validate_execution_order():
    if not Visual_Var.execution_order or Visual_Var.execution_order[0] == Visual_Var.ACTIVATION:
        raise TypeError('Cannot Visualize the forward pass functions, add a Linear layer')

def decorator_validator(args, epoch, labels, loss_func, backward):
    if args[1].dim() != 1:
        raise ValueError(f'Iterate over each sample in the dataset individually, input data dim:{args[1].dim()} !=1')
    
    if loss_func and labels is None:
        raise ValueError('labels is needed for visualization, it can either be a Tensor or a numpy array')
    
    if backward and loss_func is None:
        raise ValueError(f'loss_func should be any of {Visual_Var.AVAILABLE_LOSS_FUNC}')
    
    # check if loss function is valid 
    if loss_func is not None and loss_func not in Visual_Var.AVAILABLE_LOSS_FUNC:
        raise ValueError(f"Invalid loss function types, loss function available are; {Visual_Var.AVAILABLE_LOSS_FUNC}")
    
    if epoch < 1:
        raise ValueError(f"Epoch should be greater than zero")
    
    if backward and epoch < 2:
        raise ValueError(f"To visualize back propagation that is if backward=True, then epoch >= 2")
    

def validate_data_and_weight_maps(backward):
    validate_weight_maps([Visual_Var.weight_map, Visual_Var.bias_map, Visual_Var.bias_grad_map, Visual_Var.weight_grad_map])
    if backward:
        validate_data_list = [Visual_Var.all_forward_pass_data, Visual_Var.all_backward_pass_data]
    else:
        validate_data_list = [Visual_Var.all_forward_pass_data]
    validate_all_pass_data(validate_data_list)


def check_data_completeness_across_exec_func_objects(exec_fun_objs:dict[tuple, object]):
    for func_id, obj in exec_fun_objs.items():
        all_pass_data = obj.total_data
        nn_structure = obj.nn_structure
        assert len(all_pass_data[0]) == len(nn_structure), f"{func_id[0]} per epoch data is incomplete {len(all_pass_data[0])} != {len(nn_structure)}"

#------------------------------------Pytorch hooks----------------------------------------------#
# A utility function to check if a layer is an activation function
def is_activation_function(layer):
    # Tuple of activation function classes in PyTorch
    activation_classes = (nn.ReLU, 
                          nn.Sigmoid, 
                          nn.Tanh, 
                          nn.ELU,
                          nn.Hardshrink,
                          nn.Hardtanh,
                          nn.Hardsigmoid,
                          nn.Hardswish,
                          nn.LeakyReLU,
                          nn.LogSigmoid,
                          nn.PReLU,
                          nn.ReLU6,
                          nn.RReLU,
                          nn.SELU,
                          nn.CELU,
                          nn.SiLU,
                          nn.Mish,
                          nn.Softplus,
                          nn.Tanhshrink)
    
    # Check if the layer is an instance of any activation function class
    return isinstance(layer, activation_classes)


def activation_func_starts_first():
    if (Visual_Var.execution_order[0] == Visual_Var.ACTIVATION or Visual_Var.execution_order[0] in Visual_Var.FUNCS_ID_USED_AS_ACTIVATION):
        return True 
    else:
        return False

def modify_execution_order_if_activation_comes_first():
    """
    This function should be called before the execution order elements are converted to tuples
    and after the appropriate func_id has been converted to activation function
    """
    if Visual_Var.execution_order[0] == Visual_Var.ACTIVATION:
        del Visual_Var.execution_order[0]
        Visual_Var.is_activation_first = True
        validate_execution_order()

# Define a hook function
def forward_hook(layer_name):

    def child_forward_hook(child, input, output):

        """Get execution order"""
        #print(f"Layer: {child.__class__.__name__}, Input: {input}, Output: {output}")
        if not Visual_Var.end_of_forward_pass:
            if isinstance(child, nn.Linear):
                Visual_Var.execution_order.append(Visual_Var.FORWARD_PASS)
                Visual_Var.extracted_nn_structure.append(child.out_features)
                Visual_Var.order_of_layers.append(layer_name)
            elif is_activation_function(child):
                Visual_Var.execution_order.append(Visual_Var.ACTIVATION)
            elif child.__class__.__name__ == 'Softmax':
                Visual_Var.execution_order.append(Visual_Var.SOFTMAX)
            elif child.__class__.__name__ == 'LogSoftmax':
                Visual_Var.execution_order.append(Visual_Var.LOGSOFTMAX)
            else:
                raise TypeError(f'Visualization does not support {child.__class__.__name__}')

        """Getting forward pass data"""
        data_io = [input[0], output]
        child_io:list[list[float]] = []
        for tensor in data_io:
            layer_data = list(map(lambda x: round(x, 2), tensor.tolist()))
            child_io.append(layer_data)

        Visual_Var.forward_pass_buffer_storage.append(child_io)

        Visual_Var.forward_pass_count += 1
        if activation_func_starts_first():
            # ensures that there other func in the execution order, useful in case of softmax or logsoftmax
            if Visual_Var.forward_pass_count == 2:
                del Visual_Var.forward_pass_buffer_storage[0]
            
    return child_forward_hook

def update_all_forward_pass_data():
    epoch_data = []
    buffer_storage_data = Visual_Var.forward_pass_buffer_storage
    for i, data in enumerate(buffer_storage_data):
        # Add the input
        epoch_data.append(data[0])
        if i == len(buffer_storage_data) - 1:
            # Add the output
            epoch_data.append(data[1])
    Visual_Var.all_forward_pass_data.append(epoch_data)
    Visual_Var.forward_pass_buffer_storage = []

def backward_hook(child, grad_input, grad_output):

    grad_io = [grad_input[0], grad_output[0]]
    #print(f"Layer: {child.__class__.__name__}")
    #print(f"Gradient input: {grad_input}")
    #print(f"Gradient output: {grad_output}")

    child_grad_oi:list[list[float]] = [] # child grad output input

    for tensor in grad_io:
        if tensor is not None:
            layer_data = list(map(lambda x: round(x, 2), tensor.tolist()))
            child_grad_oi.append(layer_data)
        else:
            if isinstance(child, nn.Linear):
                child_grad_oi.append([0 for _ in range(child.in_features)])
    Visual_Var.backward_pass_buffer_storage.append(child_grad_oi)
    
def update_all_backward_pass_data():
    if not Visual_Var.backward_pass_buffer_storage:
        return 
    
    epoch_data = []
    buffer_storage_data = Visual_Var.backward_pass_buffer_storage
    for i, data in enumerate(buffer_storage_data):
        # Add the output
        epoch_data.append(data[1])
        if i == len(buffer_storage_data) - 1:
            # Add the input
            epoch_data.append(data[0])
    epoch_data.reverse()
    Visual_Var.all_backward_pass_data.append(epoch_data)
    Visual_Var.backward_pass_buffer_storage = []


def loss_function(output:torch.Tensor, label, loss_func:str):

    output = output.clone()
    if output.dim() == 1:
        output = output.unsqueeze(0)

    if not isinstance(label, torch.Tensor):
        label_tensor = torch.tensor(label, dtype=torch.long)
    else:
        label_tensor = label.clone()

    if output.dim()>1:
        label_tensor = label_tensor.unsqueeze(0)

    if loss_func == 'crossentropy_loss':

        softmax = F.softmax(output, dim=1)
        softmax_list = list(map(lambda x: round(x, 2), softmax.tolist()[0]))
        Visual_Var.all_forward_pass_data[Visual_Var.training_loop_count-1].append(softmax_list)

        log_softmax =  torch.log(softmax)

        nl_loss = F.nll_loss(log_softmax, label_tensor)

        #Visual_Var.loss_list.append(nl_loss.item())

        if Visual_Var.LOSS_VAL in Visual_Var.extra_data:
            Visual_Var.extra_data[Visual_Var.LOSS_VAL].append(round(nl_loss.item(), 2))
        else:
            Visual_Var.extra_data[Visual_Var.LOSS_VAL] = [round(nl_loss.item(), 2)]

    elif loss_func == 'nllloss':
        nl_loss = F.nll_loss(output, label_tensor)
        #Visual_Var.loss_list.append(nl_loss.item())

    
def start_label_gen(labels):

    # Store labels/traget data
    if isinstance(labels, torch.Tensor):
        Visual_Var.target_data = labels.tolist()
    elif hasattr(labels, '__class__') and labels.__class__.__name__ == 'ndarray':
        # Convert numpy array to a list
        Visual_Var.target_data = labels.tolist()
    elif isinstance(labels, list):
        Visual_Var.target_data = labels
    else:
        raise TypeError("Labels can either be a tensor, numpy array or a list.")
    for label in Visual_Var.target_data:
        yield label

def get_label_singly():

    try:
        label = next(Visual_Var.label_gen)
    except StopIteration:
        pass

    return label
    
def param_weight_grad_hook(param, layer_name, param_type):
    def child_weight_grad_hook(grad):

        if param_type == 'weight':
            grad_dict_map = Visual_Var.weight_grad_map
            param_dict_map = Visual_Var.weight_map
        elif param_type == 'bias':
            grad_dict_map = Visual_Var.bias_grad_map
            param_dict_map = Visual_Var.bias_map
        else:
            raise NameError("The parameter type is neither a weight or bias")
        
        if layer_name in grad_dict_map:
            grad_dict_map[layer_name].append(grad.clone())
            param_dict_map[layer_name].append(param.clone())
        else:
            grad_dict_map[layer_name] = [grad.clone()]
            param_dict_map[layer_name] = [param.clone()]

    return child_weight_grad_hook

def convert_funcid_to_activation():
    """
    This function should be called before the execution order elements are converted to tuples
    and before the loss function and backward pass are added    
    """

    for idx, func_id_name in enumerate(Visual_Var.execution_order):
        # Only converts to activation if the func_id_name is not the last element in the execution order
        if func_id_name in Visual_Var.FUNCS_ID_USED_AS_ACTIVATION and idx != len(Visual_Var.execution_order)-1:
            Visual_Var.execution_order[idx] = Visual_Var.ACTIVATION

def start_visualization():
    from .persistent_vars import Persistent_Variables
    from .initialization_funcs import prepare_and_initialise_exec_order, set_target_data_for_visualization, activate_first_layer_node
    from .initialization_funcs import initialise_class_parameters, generate_objects_for_visualization, set_line_weights_and_grad_data, set_node_bias_data
    from .main import display_all_forward_pass_components, call_funcs_with_objs
    from .main import initialise_activation_function, activate_next_func, update_execution_order_components_default_states 
    from .onclick_listeners import line_clicked_listener, is_triangle_clicked_listener, is_node_clicked_listener, is_pause_button_clicked_listener
    from .onclick_listeners import node_hover_animation
    from .minor_components import Nav_Buttons, Pause_button, func_minor_components, Iteration_Count
    from .parameters import GlobalParameters
    from .scroll_screen import render_display_surface_on_screen, is_any_func_width_greater_than_screen_width, is_any_func_height_greater_than_screen_height
    import pygame 
    import sys
    
    # initialise class parameters 
    initialise_class_parameters()
    
    # Prepare execution order
    prepare_and_initialise_exec_order(Visual_Var.execution_order)

    # initialise target data
    set_target_data_for_visualization(Visual_Var.target_data)

    # Generate object
    generate_objects_for_visualization(Visual_Var.all_forward_pass_data, Visual_Var.all_backward_pass_data, Visual_Var.extracted_nn_structure, extra_data=Visual_Var.extra_data)

    # set grad and weight data
    set_line_weights_and_grad_data(Visual_Var.order_of_layers, Visual_Var.weight_map, Visual_Var.weight_grad_map)

    # set node bias data
    set_node_bias_data(Visual_Var.order_of_layers, Visual_Var.bias_map)

    # Initialise activation function if present
    initialise_activation_function()

    # Get the first function in the execution order to kick off training 
    activate_next_func(Persistent_Variables.execution_function_objects[Persistent_Variables.execution_order[0]], Persistent_Variables.execution_order[0])

    # initialise function minor internal components e.g vertical bar, function text heading etc.
    func_minor_components()

    # validate function width
    is_any_func_width_greater_than_screen_width()

    # validate function height
    is_any_func_height_greater_than_screen_height()

    # validate data completeness
    check_data_completeness_across_exec_func_objects(Persistent_Variables.execution_function_objects)

    # make nodes green if activation function is the first in the execution order
    if Visual_Var.is_activation_first:
        activate_first_layer_node()

    running = True
    update_execution_order_components_default_states()
    white = (255, 255, 255)
    
    nav_buttons = Nav_Buttons()
    pause_button = Pause_button()
    iter_count = Iteration_Count()
    GlobalParameters.total_num_iterations = Visual_Var.total_num_of_iterations_to_visualize

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                # reset params for statefull apps like jupyter notebooks
                Visual_Var.initialize_visual_var()
                sys.exit()
                # Handle mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked = True

                if clicked:
                    clicked = is_pause_button_clicked_listener(mouse_pos)
                if not clicked:
                    clicked = is_triangle_clicked_listener(mouse_pos)
                if not clicked:
                    clicked = is_node_clicked_listener(mouse_pos)
                if not clicked:
                    clicked = line_clicked_listener(mouse_pos)

        Persistent_Variables.display_surface.fill(white)

        nav_buttons.display_buttons_and_text()

        pause_button.display_button()

        iter_count.display_iter_count()

        display_all_forward_pass_components()

        call_funcs_with_objs()

        render_display_surface_on_screen()

        pygame.display.flip()
        Persistent_Variables.clock.tick(60)