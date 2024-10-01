from .pytorch_prepare_for_visualization import *
def visualize(epochs, labels=None, loss_func=None, backward=True):
    def decorator(forward):
        def wrapper(*args):

            if Visual_Var.training_loop_count < epochs:
                Visual_Var.training_loop_count += 1

            # actions to carry out once
            if Visual_Var.update_once:

                decorator_validator(args, epochs, labels, loss_func, backward)

                # initialise label/target data gen 
                Visual_Var.label_gen = start_label_gen(labels)

                # Register hooks to track forward pass
                for layer_name, layer in args[0].named_children():
                    layer.register_forward_hook(forward_hook(layer_name))
                    
                    layer.register_full_backward_hook(backward_hook)

                # Register hooks to track grad of model parameters 
                for param_name, param in args[0].named_parameters():
                    """param type is whether it is a bias or a weight"""
                    layer_name, param_type = param_name.split('.')
                    param.register_hook(param_weight_grad_hook(param, layer_name, param_type))

                # append the shape of the input data
                Visual_Var.extracted_nn_structure.append(args[1].shape[0])
                Visual_Var.update_once = False

            update_all_backward_pass_data()

            output = forward(*args)
            Visual_Var.forward_pass_count = 0
            Visual_Var.end_of_forward_pass = True

            update_all_forward_pass_data()

            if loss_func is not None:
                # loss function code should be here
                label_per_epoch = get_label_singly()
                loss_function(output, label_per_epoch, loss_func=loss_func)

            if Visual_Var.training_loop_count == epochs:

                # convert funcs like softmax to activation func if they are not the last element in the execution order
                convert_funcid_to_activation()

                modify_execution_order_if_activation_comes_first()

                if loss_func is not None:
                    # Add loss function
                    Visual_Var.execution_order.append(loss_func)
                    
                    # Add loss values to backward pass data
                    if backward:
                        for i in range(epochs-1): # because the last backward pass is not executed 
                            #loss_value = [round(Visual_Var.loss_list[i], 2)]
                            Visual_Var.all_backward_pass_data[i].append([1.0])
                
                
                # make forward pass the same length as backward pass
                if epochs > 1 and backward:
                    Visual_Var.all_forward_pass_data = Visual_Var.all_forward_pass_data[:-1]
                    if Visual_Var.LOSS_VAL in Visual_Var.extra_data:
                        Visual_Var.extra_data[Visual_Var.LOSS_VAL] = Visual_Var.extra_data[Visual_Var.LOSS_VAL][:-1]

                # Add backward pass to execution order
                if backward and loss_func is not None:
                    Visual_Var.execution_order.append(Visual_Var.BACKWARD_PASS)

                # start visualization
                Visual_Var.total_num_of_iterations_to_visualize = Visual_Var.training_loop_count - 1

                validate_data_and_weight_maps(backward)

                start_visualization()

            return output
        return wrapper
    return decorator

