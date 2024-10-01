from typing import Dict
from typing import Iterable, Any
import copy

def display_component(component:object):
    if component.visible: # getting the object and checking if its visibility is true
        component.get_component()(**component.state())

def display_all_componenets(components:Dict[str, object]):
    for component in components.values():
        display_component(component)

def update_component_state(obj:object, param:str, value):
    """Update the value of an initialized variable for just one component at a time"""
    if param in obj.state():
        setattr(obj, param, value)
    else:
        raise NameError(f"Variable {param} was not initialized")

def mass_update_component_state(obj, state_updates:Dict[str, Any]):
    """A function that updates many variables at once in a state for just one component"""
    for param, value in state_updates.items():
        update_component_state(obj, param, value)

def mass_update_numerous_components(components:Dict[str, object], state_updates:Dict[str, Any]):
    """To update numerous components in a dict at once"""
    for val in components.values():
        mass_update_component_state(val, state_updates)

def update_set_of_components_states(keys: Iterable[str], components: Dict[str, object], state_updates: Dict[str, Any]):
    """
    Updates the states of specified components with new values from a state updates dictionary. 
    it is to be used majorly for updating the states of several component at once.

    Parameters:
    - keys (Iterable[str]): An iterable of component identifiers whose states need to be updated.
    - components (Dict[str, object]): A dictionary where keys are component identifiers and values are component objects.
    - state_updates (Dict[str, Any]): A dictionary where keys are component identifiers and values are the new state values for those components.

    Description:
    This function updates the state of components found in the 'components' dictionary. 
    For each key in 'keys', it checks if the key exists in 'components'. 
    If so, it updates the component's state using the corresponding value from 'state_updates'.
    meaning all components are updated with the same state_dict
    """

    for key in keys:
        if key in components:
            mass_update_component_state(components[key], state_updates)

def set_all_comoponents_to_default_state(component_types:Iterable[Dict[str, object]], var_iterable:Iterable=None, update_all=True):
    """
    component_types is preferably a list of different component types. 
    it should have the structure List[Dict[str, Component], Dict[str, Component], ...]
    var_iterable contains param strings/keys to update
    if update_all is False the var_iterable must be given 
    """
    if not update_all and var_iterable is None:
        raise ValueError('var_iterable cannot be None')
    
    if isinstance(component_types, dict):
        component_types = [component_types]

    for component_type in component_types:
        for component in component_type.values():
            if update_all:
                mass_update_component_state(component, component.default_state)
            else:
                var_to_set_to_default_state = {key:component.default_state[key] for key in var_iterable}
                mass_update_component_state(component, var_to_set_to_default_state)

def update_defualt_states_of_components(component_types:Iterable[dict[str, object]], var_dict:dict, update_all:bool):
    """
    updates default state of all components
    var_dict: used only when you want to update some specific variables in the default state.
    """
    if isinstance(component_types, dict):
        component_types = [component_types]

    for components in component_types:
        for component in components.values():
            update_component_default_state(component, var_dict, update_all)

def update_component_default_state(obj:object, var_dict:dict|list[str]=None, update_all=True):
    """
    var_dict: to update specific variables, update_all must be set to False
    var_dict is either a dictionary or a list, if it is a dict it updates the property (keys) with the stated value
    if it is a list it just updates the default state with the current value of the listed property
    update_all: to update all variables based on its current state it overrides var_dict
    """
    if isinstance(var_dict, list):
        buffer_dict = {}
        for property_name in var_dict:
            buffer_dict[property_name] = copy.deepcopy(getattr(obj, property_name))

        var_dict = buffer_dict

    if hasattr(obj, 'default_state'):
        if update_all:
            del obj.default_state
        else:
            obj.default_state.update(var_dict) # update is a python dictionary api

    if update_all:
        obj.default_state = copy.copy(obj.state())
