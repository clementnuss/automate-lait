#!/usr/bin/python3
# coding: utf-8

import time, datetime
import threading, signal

exit = threading.Event()

import automate
hw_if = automate.hardware_interface.hw_if

running = True

def milk_automata_fn():
    automata = automate.state_machine.AutomateLait()
    while running:
        automata.update()
        time.sleep(2 * 0.001) # sleep 2 millis

    print('Thread automate terminé')

def milk_mixing_fn():
    while running:
        now = datetime.datetime.now()
        if now.minute % 15 == 0:
            automate.milk_mixing.milk_mixing()
            exit.wait(60)

        exit.wait(1)

    print('Thread moteur  terminé')

def exit_gracefully(signum, frame):
    global running
    running = False

    exit.set()

    hw_if.set_pump(0)

    hw_if.pi.hardware_PWM(hw_if.moteur_step, 0,0)
    hw_if.pi.write(hw_if.moteur_en, 1)
    hw_if.pi.write(hw_if.controleur_moteur, 0)

def main_function():
    # makes a clicking noise to show the software has started
    hw_if.pi.write(hw_if.controleur_moteur, 1)
    time.sleep(0.2)
    hw_if.pi.write(hw_if.controleur_moteur, 0)

    automata_thread = threading.Thread(target=milk_automata_fn)
    mixing_thread = threading.Thread(target=milk_mixing_fn)
    automata_thread.start()
    mixing_thread.start()

    automata_thread.join() #  only join on the automate thread, as the brassage_lait thread sometimes hangs

if __name__ == "__main__":

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    main_function()


