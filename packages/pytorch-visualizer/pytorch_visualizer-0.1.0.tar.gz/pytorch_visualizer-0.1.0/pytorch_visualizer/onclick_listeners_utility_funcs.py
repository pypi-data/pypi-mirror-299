from .persistent_vars import Persistent_Variables
from .parameters import GlobalParameters

highlight_color = (0, 0, 200)
black_color = (0, 0, 0)

def turn_off_highlighted_previous_line():
    exec_func_objs:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects
    # off previously highlighted line
    if GlobalParameters.line_weight_idx[0]:
        former_line_idx = GlobalParameters.line_weight_idx[0]
        for former_obj in exec_func_objs.values():
            if former_line_idx in former_obj.lines:
                line_obj = former_obj.lines[former_line_idx]
                if line_obj.color == highlight_color:
                    line_obj.mass_update_state({'color': black_color})
                    break

def turn_off_highlighted_previous_node():
    exec_func_objs:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects
    # off previously highlighted line
    if GlobalParameters.node_bias_idx[0]:
        former_node_idx = GlobalParameters.node_bias_idx[0]
        for former_obj in exec_func_objs.values():
            if former_node_idx in former_obj.nodes:
                node_obj = former_obj.nodes[former_node_idx]
                if node_obj.color == highlight_color:
                    node_obj.mass_update_state({'color': GlobalParameters.node_color_before_click})
                    break


def highlight_current_node(obj:Persistent_Variables, node_idx:str):
    # highlignt current clicked line 
    curr_node_obj = obj.nodes[node_idx]
    curr_node_obj.mass_update_state({'color': highlight_color})


def highlight_current_line(obj:Persistent_Variables, line_idx:str):
    # highlignt current clicked line 
    curr_line_obj = obj.lines[line_idx]
    curr_line_obj.mass_update_state({'color': highlight_color})

def clicked_line_highlighter(obj:Persistent_Variables, line_idx:str):
    turn_off_highlighted_previous_line()
    highlight_current_line(obj, line_idx)

def clicked_node_highlighter(obj:Persistent_Variables, node_idx:str):
    node_obj = obj.nodes[node_idx]
    turn_off_highlighted_previous_node()
    GlobalParameters.node_color_before_click = node_obj.color
    highlight_current_node(obj, node_idx)
    
def is_backward_pass_visible():
    exec_func_objects:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects
    for func_id, obj in exec_func_objects.items():
        if func_id[0] == Persistent_Variables.FORWARD_PASS:
            # check if nodes and lines visible property is set to True 
            for node_obj in obj.nodes.values():
                # breaks the loop immediately if one node object is detected to not be visible
                # there is no need to check for lines
                if not node_obj.visible:
                    return True 
                
def func_id_to_detect_clicks():
    if is_backward_pass_visible():
        return Persistent_Variables.BACKWARD_PASS
    else:
        return Persistent_Variables.FORWARD_PASS