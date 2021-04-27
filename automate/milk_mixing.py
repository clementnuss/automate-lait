import time
import automate
hw_if = automate.hardware_interface.hw_if


def milk_mixing():
    
    hw_if.pi.write(hw_if.moteur_en, 0)
    hw_if.pi.write(hw_if.controleur_moteur, 1)
    
    microstepping = 1
    steps_per_revolution = microstepping * 200
    rot_per_sec = 2
    frequency = rot_per_sec * steps_per_revolution / 2 # divide by two as we are setting this using PWM.

    for i in range(1, 101):
        hw_if.pi.hardware_PWM(hw_if.moteur_step,
        int(i * frequency / 100) , 500000)
        time.sleep(20e-3)

    time.sleep(19)

    for i in range(1, 101):
        hw_if.pi.hardware_PWM(hw_if.moteur_step,
            int( (101-i) * frequency / 100), 500000)
        time.sleep(20e-3)
    
    hw_if.pi.hardware_PWM(hw_if.moteur_step, 0,0)
    hw_if.pi.write(hw_if.moteur_en, 1)
    hw_if.pi.write(hw_if.controleur_moteur, 0)
    