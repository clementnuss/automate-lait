#!/usr/bin/python3
# coding: utf-8

import time, threading
import datetime

from gpiozero import DigitalOutputDevice, Button
import signal

class Multirelay():
    
    def __init__(self):    
        self.relays = []
    
    def add_relay(self, relay):
        self.relays.append(relay)
    
    def on(self):
        for r in self.relays:
            r.on()
            
    def off(self):
        for r in self.relays:
            r.off()
            
                    
controleur_moteur = relais_1 = DigitalOutputDevice('J8:21')
pompe = relais_2 = DigitalOutputDevice('J8:19')
relais_3 = DigitalOutputDevice('J8:18')
relais_4 = DigitalOutputDevice('J8:16')
relais_5 = DigitalOutputDevice('J8:15')
relais_6 = DigitalOutputDevice('J8:13')
relais_7 = DigitalOutputDevice('J8:11')
relais_8 = DigitalOutputDevice('J8:12')

int_eau_lait = Button('J8:29')
int_pompe = Button('J8:31')
int_bypass = Button('J8:32')
int_commande_lait = Button('J8:33')
int_reserve = Button('J8:35')

moteur_en = DigitalOutputDevice('J8:23')
moteur_dir = DigitalOutputDevice('J8:24')
moteur_step = DigitalOutputDevice('J8:26')

running = True

relais = [relais_1, relais_2, relais_3, relais_4, relais_5, relais_6, relais_7, relais_8]
for r in relais:
    r.off()
    

controleur_moteur.on()
time.sleep(0.2)
controleur_moteur.off()

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

def commande_lait():
    return int_commande_lait.is_pressed
def commande_rincage():
    return int_bypass.is_pressed

class AutomateLait():
    def __init__(self):
        self.state = Veille()
        
    def update(self):
        # The next state will be the result of the on_event function.
        self.state = self.state.update()


############# CONSTANTES #############



class Veille(State):
    def on_enter(self):
        pass
    
    def update(self):
        global rincage_fait
        if commande_lait():
            return Distribution()
        else:
            return self
    
class Attente(State):
    def on_enter(self):
        pass

    def update(self):
        if time.time() - self.enter_time > 100:
            pass

        if commande_lait():
            return Distribution()
        
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
        
def automate():
    automate = AutomateLait()
    while running:
        automate.update()
        time.sleep(2 * 0.001) # sleep 2 millis
        
    for r in relais:
        r.off()
                
    print('Thread automate terminé')

def brassage_lait():

    controleur_moteur.on()

    microstepping = 1
    steps_per_revolution = microstepping * 200

    rev_per_sec = 2
    frequency = rev_per_sec * steps_per_revolution
    moteur_en.off()

    delay = 1/frequency
    for x in range(int(20 * rev_per_sec * steps_per_revolution)):
        moteur_step.on()
        time.sleep(delay)
        moteur_step.off()
        time.sleep(delay)

    moteur_en.on()
    controleur_moteur.off()

def thread_moteur():
    while running:
        
        now = datetime.datetime.now()
        if now.minute % 15 == 0:
            brassage_lait()
            time.sleep(60)
        
        time.sleep(1)
        
    moteur_en.on()
    controleur_moteur.off()
        
    print('Thread moteur  terminé')

def exit_gracefully(signum, frame):
    global running
    running = False
    

def main_function():
    thr_automate = threading.Thread(target=automate)
    thr_moteur = threading.Thread(target=thread_moteur)
    thr_automate.start()
    thr_moteur.start()
    
    thr_automate.join()



if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    
    main_function()


