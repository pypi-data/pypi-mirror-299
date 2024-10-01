from __future__ import annotations
from typing import Any
from .screen_operations import *
import copy

class ScreenState:
    # Variables were given a default value of None so that a state can be instantiated without any input variable.
    # Variables whose default values are not None get their values from default values of functions that utilizes them
    def __init__(
            self, 
            x=None, 
            y=None, 
            start_center=None, 
            end_center=None,

            text=None, 
            color=None, 
            width=3, 
            render_text=True, 
            layer_of_node=None, 
            curr_layer=None, 
            throb_value=None, 
            thickness=2,
            ) -> None:
        
        self.x = x
        self.y = y
        self.start_center = start_center
        self.end_center = end_center
        self.text = text
        self.color = color
        self.width = width
        self.render_text = render_text
        self.throb_value = throb_value
        self.thickness = thickness

        # default state 
        self.default_state = copy.copy(self.state())


    def state(self):
        return self.__dict__

    def update_state(self, param:str, value):
        """Update the value of an initialized variable"""
        update_component_state(self, param, value)
    
    def mass_update_state(self, state_updates:Dict[str, Any]):
        """A function that updates many variables at once in a state"""
        mass_update_component_state(self, state_updates)

    def display(self):
        display_component(self)
    
    def update_default_state(self, var_dict:dict|list[str]=None, update_all=True):
        """
        var_dict: to update specific variables, update_all must be set to False
        var_dict is either a dictionary or a list, if it is a dict it updates the property (keys) with the stated value
        if it is a list it just updates the default state with the current value of the listed property
        update_all: to update all variables based on its current state it overrides var_dict
        """
        update_component_default_state(self, var_dict, update_all)
        

if __name__ == "__main__":
    screenstate = ScreenState(1, 2, 3, 4)
    screenstate.update_state('thickness', 3)
    print(screenstate.state())
    print(screenstate.update_state.__self__.__class__.__bases__)

    class b(ScreenState):
        def __init__(self) -> None:
            super().__init__(x=None, y=None)
            self.activated= True
        def add(self, x, y, **kwargs):
            print(x + y)
    bb = b()
    
    bb.mass_update_state(params=['x', 'y'], values=[3, 5])
    ScreenState.display_component(bb.add)

        
    
    