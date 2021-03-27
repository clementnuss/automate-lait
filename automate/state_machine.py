import time

class AutomateLait():
    def __init__(self):
        self.state = Veille()
        
    def update(self):
        self.state = self.state.update()


class Veille(State):
    def on_enter(self):
        pass
    
    def update(self):
        if commande_lait():
            return Distribution()
        else:
            return self

class Distribution(State):
    def on_enter(self):
        pompe.on()
    def update(self):
        if commande_lait():
            return self
        else:
            pompe.off()
            return Veille()
    
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


# Inspired from https://laptrinhx.com/building-a-simple-state-machine-in-python-2329051726/
class State(object):
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """
    
    def __init__(self):
        self.enter_time = time.time()
        print(f'Etat courant: {str(self)}')
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