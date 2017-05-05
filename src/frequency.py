# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 00:43:51 2016

@author: ABC
"""
import RPi.GPIO as GPIO
import pygame
import pygame.midi
import time
import math
import statistics

def prepare(GPIO_TRIGGER, GPIO_ECHO):
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, False)
    time.sleep(0.1)
    
def get_distance(GPIO_TRIGGER, GPIO_ECHO):
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    try:
        while GPIO.input(GPIO_ECHO)==0:
            start = time.time()
    except Exception:
        pass
    try:
        while GPIO.input(GPIO_ECHO)==1:
            stop = time.time()
    except Exception:
        pass
    elapsed = stop - start
    distance = (elapsed * 34300)/2
    return int(distance)
 

def conf_midi():
    instrument = 79
    device_id = 2
    latency = 0
    buffer_size = 0
    global midiOutput
    midiOutput = pygame.midi.Output(device_id, latency, buffer_size)  
    midiOutput.set_instrument(instrument)
      

def get_note(dist):
    minDist = 5
    maxDist = 60
    octaves = 2
    minNote = 44
    maxNote = minNote + 12*octaves

    if (dist>maxDist):
      note = minNote
    elif (dist<minDist):
      note = maxNote
    else:  
      fup = (dist - minDist)*(maxNote-minNote)
      fdown = (maxDist - minDist)
      note = maxNote - (fup/fdown)
    return int (note) 

def play_midi(note, b4note):
    if (note != b4note):
        midiOutput.note_off(b4note, 0)
        midiOutput.note_on(note, 127)
    
        
pygame.init()
pygame.midi.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO = 24

prepare(GPIO_TRIGGER, GPIO_ECHO)

note = 0
conf_midi()


try:
    while True:
        b4note = note
        liste = []
        print('starte Messung')
        while len(liste) < 2:
            single_dist = get_distance(GPIO_TRIGGER, GPIO_ECHO)
            print("single_dist:", single_dist)
            if single_dist is None:
                single_dist = dist_alt
            liste.append(single_dist)
        time.sleep(0.1)
        median_dist = statistics.median(liste)
        print("median:", median_dist)
        str(median_dist)
        del liste [:]
        note = get_note(median_dist)
        print("note:", note)
        str(note)
        dist_alt = single_dist
        play_midi(note, b4note)
        time.sleep(0.2)
        

except Exception:
    pass
       
except KeyboardInterrupt:
    GPIO.cleanup()
    del midiOutput
    pygame.midi.quit()
GPIO.cleanup()
