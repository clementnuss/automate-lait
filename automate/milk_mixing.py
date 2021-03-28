import time
import automate
hw_if = automate.hardware_interface.hw_if


def milk_mixing():
    #TODO: reimplement this section using pigpiod and hardware PWM.
    hw_if.controleur_moteur.on()

    microstepping = 1
    steps_per_revolution = microstepping * 200

    rev_per_sec = 2
    frequency = rev_per_sec * steps_per_revolution
    
    hw_if.moteur_en.off()

    delay = 1/frequency
    for x in range(int(20 * rev_per_sec * steps_per_revolution)):
        hw_if.moteur_step.on()
        time.sleep(delay)
        hw_if.moteur_step.off()
        time.sleep(delay)

    hw_if.moteur_en.on()
    hw_if.controleur_moteur.off()