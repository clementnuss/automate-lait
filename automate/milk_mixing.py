import time
import automate
hw_if = automate.hardware_interface.hw_if


def milk_mixing():
    
    hw_if.pi.write(hw_if.moteur_en, 0)
    hw_if.pi.write(hw_if.controleur_moteur, 1)
    
    microstepping = 1
    steps_per_revolution = microstepping * 200
    rot_per_sec = 2
    frequency = rot_per_sec * steps_per_revolution

    for i in range(1, 101):
        hw_if.pi.hardware_PWM(hw_if.moteur_step, i * frequency / 100, 500e3)
        time.sleep(10e-3)

    time.sleep(19)

    for i in range(1, 101):
        hw_if.pi.hardware_PWM(hw_if.moteur_step, (101-i) * frequency / 100, 500e3)
        time.sleep(10e-3)
    
    hw_if.pi.hardware_PWM(hw_if.moteur_step, 0,0)
    hw_if.pi.write(hw_if.moteur_en, 1)
    hw_if.pi.write(hw_if.controleur_moteur, 0)

    # for x in range(int(20 * rev_per_sec * steps_per_revolution)):
    #     hw_if.moteur_step.on()
    #     time.sleep(delay)
    #     hw_if.moteur_step.off()
    #     time.sleep(delay)

    