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
    time.sleep(0.1)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
    elapsed = stop - start
    distance = (elapsed * 34300)/2
    return int(distance)
 

def conf_midi():
    instrument = 79
    device_id = 2
    latency = 0
    buffer_size = 512
    global midiOutput
    midiOutput = pygame.midi.Output(device_id, latency, buffer_size)  
    midiOutput.set_instrument(instrument)
      

def get_note(dist):
    minDist = 5
    maxDist = 70
    octaves = 1
    minNote = 68
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

def append_list (liste, single_dist):
    liste.pop(0)
    liste.append(single_dist)
    return liste
        
pygame.init()
pygame.midi.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 23
GPIO_ECHO = 24

prepare(GPIO_TRIGGER, GPIO_ECHO)

note = 0
conf_midi()

liste = [0,0,0,0,0]

try:
    while True:
        b4note = note
        single_dist = get_distance(GPIO_TRIGGER, GPIO_ECHO)
        liste = append_list (liste, single_dist)
        median_dist = statistics.median(liste)
        note = get_note(median_dist) 
        play_midi(note, b4note)

except Exception:
    pass
       
except KeyboardInterrupt:
    GPIO.cleanup()
    del midiOutput
    pygame.midi.quit()
GPIO.cleanup()
