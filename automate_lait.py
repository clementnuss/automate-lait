#!/usr/bin/python3
# coding: utf-8

import time, threading
import datetime

import signal

import automate



running = True

def thread_automate():
    automate = AutomateLait()
    while running:
        automate.update()
        time.sleep(2 * 0.001) # sleep 2 millis
        
    for r in relais:
        r.off()
                
    print('Thread automate terminé')

def thread_brassage_lait():
    while running:
        
        now = datetime.datetime.now()
        if now.minute % 15 == 0:
            brassage_lait()
            time.sleep(60)
        
        time.sleep(1)
        
    moteur_en.on()
    controleur_moteur.off()
        
    print('Thread moteur  terminé')

def brassage_lait():
    #TODO: reimplement this section using pigpiod and hardware PWM.
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

def exit_gracefully(signum, frame):
    global running
    running = False

def main_function():
    thread_automate = threading.Thread(target=thread_automate)
    thread_brassage_lait = threading.Thread(target=thread_brassage_lait)
    thread_automate.start()
    thread_brassage_lait.start()
    
    thread_automate.join() #  only join on the automate thread, as the brassage_lait thread sometimes hangs

if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    
    # makes a clicking noise to show the software has started
    controleur_moteur.on()
    time.sleep(0.2)
    controleur_moteur.off()

    main_function()


