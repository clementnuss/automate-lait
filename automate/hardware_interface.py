
import pigpio
import time

class HardwareInterface():

    controleur_moteur = 9
    pompe = 10
    commande_lait = 19
    moteur_en = 11
    moteur_dir = 8
    moteur_step = 13
    
    def __init__(self):
        self.pi = pigpio.pi('localhost', 8888)
        print(f"Correctly connected to the pigpio daemon: {self.pi.connected}")

        self.pi.set_mode(self.commande_lait, pigpio.INPUT)
        self.pi.set_pull_up_down(self.commande_lait, pigpio.PUD_DOWN)


    def read_milk_button(self):
        return self.pi.read(self.commande_lait)

    def set_pump(self, state: bool):
        self.pi.write(self.pompe, state)

hw_if = HardwareInterface()
