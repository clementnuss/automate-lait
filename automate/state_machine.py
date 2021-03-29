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
        if hw_if.commande_lait():
            return Distribution()
        else:
            return self

class Distribution(State):
    def on_enter(self):
        hw_if.pompe.on()
    def update(self):
        if hw_if.commande_lait():
            return self
        else:
            hw_if.pompe.off()
            return Veille()

class AutomateLait():
    def __init__(self):
        self.state = Veille()
        
    def update(self):
        self.state = self.state.update()
    
# Waiting state. not used anymore currently
# class Attente(State):
#     def on_enter(self):
#         pass

#     def update(self):
#         if time.time() - self.enter_time > 100:
#             pass

#         if commande_lait():
#             return Distribution()
        
#         return self


