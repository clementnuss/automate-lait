import time

import automate
hw_if = automate.hardware_interface.hw_if


# Inspired from https://laptrinhx.com/building-a-simple-state-machine-in-python-2329051726/
class State(object):
   
    def __init__(self):
        self.enter_time = time.time()
        print(f'Current state: {str(self)}')
        self.on_enter()

    def on_enter(self):
        pass
        
    def update(self):
        """
        Handle events that are delegated to this State.
        """
        pass

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__

class Veille(State):
    def on_enter(self):
        pass
    
    def update(self):
        if hw_if.read_milk_button():
            return Distribution()
        else:
            return self

class Distribution(State):
    def on_enter(self):
        hw_if.set_pump(1)
    def update(self):
        if hw_if.read_milk_button():
            return self
        else:
            hw_if.set_pump(0)
            return Veille()

class AutomateLait():
    def __init__(self):
        self.state = Veille()
        
    def update(self):
        self.state = self.state.update()