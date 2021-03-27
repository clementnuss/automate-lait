
from gpiozero import DigitalOutputDevice, Button
import time

                    
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

def commande_lait():
    return int_commande_lait.is_pressed
def commande_rincage():
    return int_bypass.is_pressed

relais = [relais_1, relais_2, relais_3, relais_4, relais_5, relais_6, relais_7, relais_8]
for r in relais:
    r.off()


# class that emulates the behavior of a relay, but under the hood calls multiple relays.
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
