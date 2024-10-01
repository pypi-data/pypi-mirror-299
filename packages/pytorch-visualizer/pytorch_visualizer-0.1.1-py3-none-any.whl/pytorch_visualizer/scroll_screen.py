import pygame
from .persistent_vars import Persistent_Variables
from .parameters import GlobalParameters
from .minor_components import Nav_Buttons, Pause_button

def get_max_min_x_position(obj:Persistent_Variables):
    """
    A fuunction that fetches the maximum and minimum value of the component/func x postion
    returns --> (min, max)
    """

    max_x = -float('inf')
    min_x = float('inf')
    for node_obj in obj.nodes.values():
        x = node_obj.x

        max_x = max(x, max_x)
        min_x = min(x, min_x)

    if obj.target_node is not None:
        for target_node in obj.target_node.values():
            max_x = max(target_node.x, max_x)

    # Adding the radius to get the true min and max value
    max_x += node_obj.node_radius
    min_x -= node_obj.node_radius

    return max_x, min_x

def get_max_min_y_position(obj:Persistent_Variables):
    """
    A fuunction that fetches the maximum and minimum value of the component/func y postion
    returns --> (min, max)
    """

    max_y = -float('inf')
    min_y = float('inf')
    for node_obj in obj.nodes.values():
        y = node_obj.y

        max_y = max(y, max_y)
        min_y = min(y, min_y)

    # Adding the radius to get the true min and max value
    max_y += node_obj.node_radius
    min_y -= node_obj.node_radius

    return max_y, min_y

def get_current_max_position():
    """
    A fuunction that fetches the maximum and minimum value of the component/func x postion
    returns --> (min, max)
    """
    func_id_idx = Persistent_Variables.current_func_id_idx
    exec_order = Persistent_Variables.execution_order
    exec_func_objects = Persistent_Variables.execution_function_objects

    curr_active_obj:Persistent_Variables = exec_func_objects[exec_order[func_id_idx]]
    
    max_x, _ = get_max_min_x_position(curr_active_obj)

    return max_x

def is_curr_position_outside_screen_width(x:float):
    screen_width = Persistent_Variables.screen_width

    if x > screen_width:
        return True
    else:
        return False 
    
def is_curr_position_outside_screen_height(height:float):
    min_screen_height = Pause_button.rect_height/2 + Pause_button.y + 2
    max_screen_height = Persistent_Variables.screen_height - (Nav_Buttons.height_from_base_of_screen + Nav_Buttons.triangle_height) - 2

    screen_height = max_screen_height - min_screen_height

    if height > screen_height:
        return True
    else:
        return False
    
def is_any_func_height_greater_than_screen_height():
    exec_func_objects = Persistent_Variables.execution_function_objects
    for func_id, obj in exec_func_objects.items():

        max_y, min_y = get_max_min_y_position(obj)

        if func_id[0] in Persistent_Variables.AVAILABLE_LOSS_FUNC:
            # in order to account for text
            tolerance = 20 # correlates to font size
            min_y = min_y - (2*Persistent_Variables.node_radius + tolerance)


        height = max_y - min_y

        result = is_curr_position_outside_screen_height(height)

        if result:
            raise AssertionError(f'Neural network is too large, reduce the number of nodes')

    return result
    
def is_any_func_width_greater_than_screen_width():
    """
    No display on the screen should have a width greater than the screen width, it lead to display issues
    Because there not yet an implemented method to know which part of the screen an activity is occuring.
    """
    exec_func_objects = Persistent_Variables.execution_function_objects
    for func_id, obj in exec_func_objects.items():
        max_x, min_x = get_max_min_x_position(obj)

        width = max_x - min_x

        result = is_curr_position_outside_screen_width(width)

        if result:
            raise AssertionError(f'Neural network is too large, reduce the hidden layers')

    return result

def is_active_func_outside_screen_view():
    """
    checks if current active function is within view
    """
    max_x = get_current_max_position()

    min_x = Persistent_Variables.initial_x - Persistent_Variables.node_radius

    width = max_x - min_x

    result = is_curr_position_outside_screen_width(width)

    return result

def render_display_surface_on_screen():
    scroll_with_key_pressed()
    scroll_screen_on_func_id_change()
    x = Persistent_Variables.surface_x_pos
    y = Persistent_Variables.surface_y_pos
    Persistent_Variables.screen.blit(Persistent_Variables.display_surface,
                                     (x, y))
def scroll(x:float):
    if is_curr_position_outside_screen_width(x):
        tolerance = 20
        move_x_origin_by = x - Persistent_Variables.screen_width
        GlobalParameters.surface_x_pos -= move_x_origin_by + tolerance

def scroll_screen_on_func_id_change():
    """There is no need to check for local exec order because they share one object."""
    if Persistent_Variables.is_func_id_changed:
        x_pos = GlobalParameters.surface_x_pos
        if x_pos!=0 and not is_active_func_outside_screen_view():
            GlobalParameters.surface_x_pos = 0
            GlobalParameters.is_func_id_changed = False
        elif is_active_func_outside_screen_view():
            max_x = get_current_max_position()
            scroll(max_x)
            GlobalParameters.is_func_id_changed = False

def scroll_with_key_pressed():
    # Get keys pressed
    keys = pygame.key.get_pressed()
    if is_active_func_outside_screen_view():
        SCROLL_SPEED = Persistent_Variables.scroll_speed
        # Scroll left or right with arrow keys
        if keys[pygame.K_RIGHT]:
            GlobalParameters.scroll_camera_x += SCROLL_SPEED
        elif keys[pygame.K_LEFT]:
            GlobalParameters.scroll_camera_x -= SCROLL_SPEED
        else:
            return 

        # Clamp the camera position so it doesn't scroll out of bounds
        max_x = get_current_max_position()
        tolerance = 20
        max_scroll_width = max_x - Persistent_Variables.screen_width + tolerance
        scroll_camera_x = max(0, min(GlobalParameters.scroll_camera_x, max_scroll_width))
        GlobalParameters.surface_x_pos = -scroll_camera_x