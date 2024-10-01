from typing import Any, Callable, Iterable
from .screen_components import Components
import math 
import pygame
class Line(Components):
    def __init__(self, window, node_to_node=True) -> None:
        super().__init__(window)
        self.start_point = None
        self.end_point = None
        self.node_to_node = node_to_node
        self.custom_line_coor_func:Callable[[Any], tuple[tuple, tuple]] = None

    def get_component(self):
        return self.draw_line

    # Calculate the point on the circumference of the circle where the line should start/end
    def calculate_circumference_point(self, center, angle):
        return (
            center[0] + self.node_radius * math.cos(angle),
            center[1] + self.node_radius * math.sin(angle)
        )

    # Draw a throbbing line between the circumferences of two circles
    def draw_line(self, start_center, end_center, thickness=2, color=None, throb_value=None, **kwargs):
        if color is None:
            color = self.color

        if throb_value is not None:
            thickness = throb_value

        if self.node_to_node:
            angle = math.atan2(end_center[1] - start_center[1], end_center[0] - start_center[0])
            if self.custom_line_coor_func is None:
                self.start_point = self.calculate_circumference_point(start_center, angle)
                self.end_point = self.calculate_circumference_point(end_center, angle + math.pi)
            else:
                self.start_point, self.end_point = self.custom_line_coor_func(start_center, end_center, **kwargs)
        
        pygame.draw.line(self.window, color, self.start_point, self.end_point, thickness)

class Nodes(Components):
    def __init__(self, window, font) -> None:
        super().__init__(window, font)

    def get_component(self):
        return self.draw_node

    # Function to draw a node with its value
    def draw_node(self, x, y, text=None, color=None, width=3, render_text=True, throb_value=None, **kwargs):
        if color is None:
            color = self.color 
        
        if throb_value is not None:
            width = throb_value

        pygame.draw.circle(self.window, color, (x, y), self.node_radius, width=width)

        if render_text:
            text_surface = self.font.render(str(text), True, color)
            text_rect = text_surface.get_rect(center=(x, y))
            self.window.blit(text_surface, text_rect)
        

class Text(Components):
    def __init__(self, window, font) -> None:
        super().__init__(window, font)

    def get_component(self):
        return self.display_text

    def display_text(self, text, x, y, color, **kwargs):
        text_surface = self.font.render(str(text), True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window.blit(text_surface, text_rect)

class Rect(Text):
    def __init__(self, window, font=None, rect_width=None, rect_height=None) -> None:
        super().__init__(window, font)

        self.rect_width = rect_width
        self.rect_height = rect_height
        self.text_color = None
        self.rect:pygame.Rect = None

    def __call__(self) -> Any:
        if self.rect is None:
            self.create_rect_object(self.x, self.y, self.rect_width, self.rect_height)
        return self.rect
    
    def get_component(self):
        return self.draw_rect
    
    def create_rect_object(self, x, y, rect_width, rect_height):
        self.rect = pygame.Rect(0, 0, rect_width, rect_height)

        self.rect.center = (x, y)
        return self.rect
    
    def draw_rect(self, x, y, rect_width, rect_height, text, color, width, **kwargs):
        if self.text_color is None:
            self.text_color = color

        rect = self.create_rect_object(x, y, rect_width, rect_height)

        self.display_text(text, x, y, self.text_color)

        pygame.draw.rect(self.window, color, rect, width)

class Triangle(Components):
    def __init__(self, window, vertex1, vertex2, vertex3) -> None:
        super().__init__(window)
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.vertex3 = vertex3
    
    def get_component(self):
        return self.draw_triangle
    
    def draw_triangle(self, vertex1, vertex2, vertex3, **kwargs):
        pygame.draw.polygon(self.window, self.color, [vertex1, vertex2, vertex3])


if __name__ == "__main__":
    pass

