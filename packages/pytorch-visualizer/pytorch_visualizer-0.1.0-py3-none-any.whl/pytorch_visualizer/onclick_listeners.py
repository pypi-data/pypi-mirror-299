from __future__ import annotations
from .persistent_vars import Persistent_Variables
from .parameters import GlobalParameters
from .minor_components import Nav_Buttons, Pause_button
from .onclick_listeners_utility_funcs import *
import math
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .draw_on_screen import Triangle, Nodes

def align_mouse_pos_to_component_position(mouse_pos):
    x_pos = Persistent_Variables.surface_x_pos
    y_pos = Persistent_Variables.surface_y_pos
    x, y = mouse_pos
    return (x-x_pos, y-y_pos)

def is_point_near_line_segment(start_point, end_point, mouse_pos, threshold=4):

    mouse_pos = align_mouse_pos_to_component_position(mouse_pos)

    x1, y1 = start_point
    x2, y2 = end_point
    x0, y0 = mouse_pos

    # Calculate perpendicular distance from point to line
    A = (y2 - y1)
    B = -(x2 - x1)
    C = x2*y1 - y2*x1

    num = abs(A*x0 + B*y0 + C)
    denom = (A**2 + B**2)**0.5
    distance = num/denom

    #------------------Check if point is within the segment bounds------------------------#

    # vector from start_point to mouse point 
    ui, uj = (x0 - x1), (y0 - y1)

    # vector from start point to end point
    vi, vj = (x2 - x1), (y2 - y1)

    u_dot_v = (ui * vi) + (uj * vj)

    # Normalising 
    mag_v = (vi**2 + vj**2)

    proj_mag = u_dot_v/mag_v

    #dot_product = ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / ((x2 - x1)**2 + (y2 - y1)**2)

    is_within_segment = 0 <= proj_mag <= 1

    return distance < threshold and is_within_segment

def line_clicked_listener(mouse_pos):
    execution_function_object:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects
    id_to_detect_clicks = func_id_to_detect_clicks()
    for func_id, obj in execution_function_object.items():
        if func_id[0] == id_to_detect_clicks:
            obj_lines = obj.lines
            if obj_lines is not None:
                for line_idx, line_obj in obj_lines.items():
                    start_point, end_point = line_obj.start_point, line_obj.end_point
                    if start_point is not None:
                        if is_point_near_line_segment(start_point, end_point, mouse_pos):
                            #if line_idx in GlobalParameters.line_idx_to_weight_map or line_idx in GlobalParameters.line_idx_to_grad_map:

                            if GlobalParameters.line_weight_idx != (line_idx, id_to_detect_clicks):
                                turn_off_highlighted_previous_node()
                                clicked_line_highlighter(obj, line_idx)
                                GlobalParameters.line_weight_idx = (line_idx, id_to_detect_clicks)
                                # set the other component index to None
                                GlobalParameters.node_bias_idx = (None, None)

                            GlobalParameters.update_line_weight_and_grad(line_idx, Nav_Buttons.curr_num_iterations-1)
                            Nav_Buttons.update_line_weight_grad_text()
                            Nav_Buttons.curr_text_idx = 0
                        
                            return line_idx


def is_point_in_triangle(vertex1, vertex2, vertex3, mouse_pos):

    # Calculate the barycentric coordinates
    # of point P with respect to triangle ABC
    denominator = ((vertex2[1] - vertex3[1]) * (vertex1[0] - vertex3[0]) +
                   (vertex3[0] - vertex2[0]) * (vertex1[1] - vertex3[1]))
    a = ((vertex2[1] - vertex3[1]) * (mouse_pos[0] - vertex3[0]) +
         (vertex3[0] - vertex2[0]) * (mouse_pos[1] - vertex3[1])) / denominator
    b = ((vertex3[1] - vertex1[1]) * (mouse_pos[0] - vertex3[0]) +
         (vertex1[0] - vertex3[0]) * (mouse_pos[1] - vertex3[1])) / denominator
    c = 1 - a - b
 
    # Check if all barycentric coordinates
    # are non-negative
    if a >= 0 and b >= 0 and c >= 0:
        return True
    else:
        return False
    
def is_triangle_clicked_listener(mouse_pos):
    nav_arrows:dict[str, Triangle] = Nav_Buttons.nav_arrows
    for idx, triangle in nav_arrows.items():
        if is_point_in_triangle(triangle.vertex1, triangle.vertex2, triangle.vertex3, mouse_pos):
            Nav_Buttons.get_last_update_time()
            Nav_Buttons.clicked_button = idx

            line_idx = Nav_Buttons.line_weight_idx[0]
            node_idx = Nav_Buttons.node_bias_idx[0]

            if line_idx is not None or node_idx is not None:
                if idx == Persistent_Variables.PREV_ARROW:
                    Nav_Buttons.update_curr_text_idx(back=True)
                elif idx == Persistent_Variables.NEXT_ARROW:
                    Nav_Buttons.update_curr_text_idx()

                if line_idx:
                    GlobalParameters.update_line_weight_and_grad(line_idx, Nav_Buttons.curr_text_idx)
                    Nav_Buttons.update_line_weight_grad_text()
                elif node_idx:
                    GlobalParameters.update_node_grad_and_bias(node_idx, Nav_Buttons.curr_text_idx)
                    Nav_Buttons.update_node_bias_grad_text()
            return idx 
        
def is_point_in_circle(mouse_pos, circle_center, radius):
    mouse_pos = align_mouse_pos_to_component_position(mouse_pos)
    x, y = mouse_pos
    cx, cy = circle_center
    distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    return distance <= radius

def is_node_clicked_listener(mouse_pos):
    execution_function_object:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects
    id_to_detect_clicks = func_id_to_detect_clicks()
    for func_id, obj in execution_function_object.items():
        if func_id[0] == id_to_detect_clicks:
            obj_nodes = obj.nodes
            if obj_nodes is not None:
                for node_idx, node_obj in obj_nodes.items():
                    x, y = node_obj.x, node_obj.y
                    if x is not None:
                        point = (x, y)
                        if is_point_in_circle(mouse_pos, point, node_obj.node_radius):
                            #if node_idx in GlobalParameters.node_idx_to_bias_map or node_idx in GlobalParameters.node_idx_to_grad_map:

                            if GlobalParameters.node_bias_idx != (node_idx, id_to_detect_clicks):
                                turn_off_highlighted_previous_line()
                                clicked_node_highlighter(obj, node_idx)
                                GlobalParameters.node_bias_idx = (node_idx, id_to_detect_clicks)
                                # set the other component index to none
                                GlobalParameters.line_weight_idx = (None, None)

                            GlobalParameters.update_node_grad_and_bias(node_idx, Nav_Buttons.curr_num_iterations-1)
                            Nav_Buttons.update_node_bias_grad_text()
                            Nav_Buttons.curr_text_idx = 0
                            return node_idx

def is_pause_button_clicked_listener(mouse_pos):
    pause_button = Pause_button.pause_button
    if pause_button.collidepoint(mouse_pos):
        if Pause_button.rect_obj.text == Persistent_Variables.PAUSE_TEXT:
            Pause_button.rect_obj.update_state(param='text', value=Persistent_Variables.PLAY_TEXT)
            GlobalParameters.pause = True 
        else:
            Pause_button.rect_obj.update_state(param='text', value=Persistent_Variables.PAUSE_TEXT)
            GlobalParameters.pause = False
        return True

#-------Hover animation-------#
def hover_color_change(node_obj:Nodes, clicked_node_idx, color_change=True):
    node_hover_color = (170, 170, 170)
    if not clicked_node_idx:
        if color_change:
            node_obj.mass_update_state({'color':node_hover_color})
        else:
            node_obj.mass_update_state({'color':(0, 0, 0)})


def node_hover_animation(clicked_node_idx):
    mouse_pos = pygame.mouse.get_pos()
    execution_function_object:dict[tuple, Persistent_Variables] = Persistent_Variables.execution_function_objects
    id_to_detect_clicks = func_id_to_detect_clicks()
    for func_id, obj in execution_function_object.items():
        if func_id[0] == id_to_detect_clicks:
            obj_nodes = obj.nodes
            if obj_nodes is not None:
                for node_idx, node_obj in obj_nodes.items():
                    x, y = node_obj.x, node_obj.y
                    if x is not None:
                        point = (x, y)
                        if is_point_in_circle(mouse_pos, point, node_obj.node_radius):
                            hover_color_change(node_obj, clicked_node_idx=clicked_node_idx)
                        else:
                            hover_color_change(node_obj, clicked_node_idx=clicked_node_idx, color_change=False)