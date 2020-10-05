#!/usr/bin/python3
# coding: utf-8

import time, threading
import datetime

from gpiozero import DigitalOutputDevice, Button
import signal

pompe = relais_1 = DigitalOutputDevice('J8:21')
relais_2 = DigitalOutputDevice('J8:19')
relais_3 = DigitalOutputDevice('J8:18')
eau_sale = relais_4 = DigitalOutputDevice('J8:16')
eau_propre = relais_5 = DigitalOutputDevice('J8:15')
bypass = relais_6 = DigitalOutputDevice('J8:13')
lait = relais_7 = DigitalOutputDevice('J8:11')
eau = relais_8 = DigitalOutputDevice('J8:12')

int_eau_lait = Button('J8:29')
int_pompe = Button('J8:31')
int_bypass = Button('J8:32')
int_commande_lait = Button('J8:33')
int_reserve = Button('J8:35')

moteur_en = DigitalOutputDevice('J8:23')
moteur_dir = DigitalOutputDevice('J8:24')
moteur_step = DigitalOutputDevice('J8:26')

running = True
rincage_fait = False

relais = [relais_1, relais_2, relais_3, relais_4, relais_5, relais_6, relais_7, relais_8]
for r in relais:
    r.off()
    
vannes = [relais_4, relais_5, relais_6, relais_7, relais_8]

for r in vannes:
    r.on()
    time.sleep(0.05)
    
time.sleep(0.2)

for r in vannes:
    r.off()
    time.sleep(0.05)

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

duree_vidange_circuit = 10
duree_descente_eau = 10
duree_bypass_vide = 0.6
duree_entre_videbypass = 10
duree_rincage_eau = 5

duree_attente_tirage = 60

def vidage_circuit(circuit):
    bypass.on()
    
    if (circuit == 'lait'):
        lait.on()
    elif (circuit == 'eau'):
        eau.on()
        eau_sale.on()
        time.sleep(6)

    pompe.on()
    time.sleep(duree_bypass_vide)
    pompe.off()
    time.sleep(duree_entre_videbypass)

    pompe.on()
    time.sleep(duree_bypass_vide)
    pompe.off()
    time.sleep(duree_entre_videbypass)

    pompe.on()
    time.sleep(duree_bypass_vide)
    pompe.off()

    time.sleep(duree_vidange_circuit)

    if (circuit == 'lait'):
        lait.off()
    elif (circuit == 'eau'):
        eau.off()
        eau_sale.off()
    
    bypass.off()

class Veille(State):
    def on_enter(self):
        print("arrêt des relais")
        for r in relais:
            r.off()
    
    def update(self):
        if commande_lait():
            return Preparation()
        if commande_rincage() and not rincage_fait:
            rincage_fait = True
            return Rincage()
        if time.time() - self.enter_time > 3600 and not rincage_fait:
            rincage_fait = True
            return Rincage()
        else:
            return self
        
class Rincage(State):
    
    def update(self):
        vidage_circuit('lait')
        
        eau.on()
        eau_propre.on()
        pompe.on()
        time.sleep(duree_rincage_eau)
        pompe.off()
        eau_propre.off()

        vidage_circuit('eau')
        
        return Veille()    

        
class Preparation(State):
    def on_enter(self):
        #tirer du lait jusqu'en haut mais dépasser le point le plus haut (= sans faire couler)
        lait.on()
        bypass.off()
        pompe.on()
        time.sleep(1)
        
        rincage_fait = False
    
    def update(self):
        if commande_lait():
            return Distribution()
        else:
            return Attente()

class Attente(State):
    def on_enter(self):
        pompe.off()
        #vidage du coude
        bypass.on()
        time.sleep(0.4)
        bypass.off()
    
    def update(self):
        if time.time() - self.enter_time > duree_attente_tirage:
            return Vidange()
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
            return Attente()
        
class Vidange(State):
    def update(self):
        print('vidange en cours, attendre')
        bypass.on()
        time.sleep(duree_vidange_circuit)
        bypass.off()
        
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

    microstepping = 1
    steps_per_revolution = microstepping * 200

    rev_per_sec = 2
    frequency = rev_per_sec * steps_per_revolution
    moteur_en.off()

    delay = 1/frequency
    for x in range(int(15 * rev_per_sec * steps_per_revolution)):
        moteur_step.on()
        time.sleep(delay)
        moteur_step.off()
        time.sleep(delay)

    moteur_en.on()

def thread_moteur():
    while running:
        
        now = datetime.datetime.now()
        if now.minute % 15 == 0:
            brassage_lait()
            time.sleep(60)
        
        time.sleep(1)
        
    moteur_en.on()
        
    print('Thread moteur  terminé')

def exit_gracefully(signum, frame):
    eau_sale.on()
    time.sleep(0.1)
    eau_sale.off()
    global running
    running = False
    

def main_function():
    thr_automate = threading.Thread(target=automate)
    thr_moteur = threading.Thread(target=thread_moteur)
    thr_automate.start()
    thr_moteur.start()
    
    thr_moteur.join()
    thr_automate.join()



if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    
    main_function()


