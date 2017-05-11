# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import pygame
import pygame.midi
import time
import statistics

#Set output(trigger) and input(echo) ready
def prepare(GPIO_TRIGGER, GPIO_ECHO):
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, False)
    #print("Sensor is getting ready")
    time.sleep(1)

#This function get the distance from the sensor      
def get_distance(GPIO_TRIGGER, GPIO_ECHO):
    #Set output to true for 0.00001ms,
    #this triggers the sensor to send an ultrasonic pulse (8 ultrasound burst at 40kHz)
    #the ultrasonic sound will the be reflected by closed by solid object
    #and be detected by the receiver of the sensor
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    #print("Sent pulse")
    #The sensor then set the echo=1 until the pulse comes back
    #so we have to record the last timestamp before echo goes high
    try:
        while GPIO.input(GPIO_ECHO)==0:
            start = time.time()
            #print("echo is now on high, waiting for reflected pulse")
    except Exception:
        pass
    #and record the last timestamp when echo is high
    try:
        while GPIO.input(GPIO_ECHO)==1:
            stop = time.time()
            #print("reflection detected")
    except Exception:
        pass
    #that gives the elapsed time for the pulse to goes and comes back
    time.sleep(0.07)
    elapsed = stop - start
    #the sound traveled double the distance, so we get
    distance = (elapsed * 34300)/2
    return int(distance)
 
#This function set the parameters for the midi data
def conf_midi():
    instrument = 79
    device_id = 2
    latency = 0
    buffer_size = 0
    global midiOutput
    midiOutput = pygame.midi.Output(device_id, latency, buffer_size)  
    midiOutput.set_instrument(instrument)

#This function declare the range of the tone and convert the distance into the note value,
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

#This function defines the action of playing a tone
def play_midi(note, b4note):
    if (note != b4note):
        midiOutput.note_off(b4note, 0)
        midiOutput.note_on(note, 127)
    
#Start module pygame midi
pygame.init()
pygame.midi.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Tell the Pi which GPIO_Pin you are using
GPIO_TRIGGER = 23
GPIO_ECHO = 24

#Get the sensor ready
prepare(GPIO_TRIGGER, GPIO_ECHO)

#Configure the midi data
note = 0
conf_midi()


try:
    while True:
        b4note = note
        #Create a list to record the distance values
        liste = []
        print("start measurement")
        while len(liste) < 2:
            single_dist = get_distance(GPIO_TRIGGER, GPIO_ECHO)
            print("single_dist:", single_dist)
            if single_dist is None:
                single_dist = dist_alt
            liste.append(single_dist)
        time.sleep(0.1)
        #Get the median value of the list
        median_dist = statistics.median(liste)
        print("median:", median_dist)
        #str(median_dist)
        #Empty the list
        del liste [:]
        #Get the note from the median value of the distances measured
        note = get_note(median_dist)
        print("note:", note)
        #str(note)
        dist_alt = single_dist
        #Play the newly calculated note and shut off the previous one
        play_midi(note, b4note)
        time.sleep(0.2)
        

except Exception:
    pass
       
except KeyboardInterrupt:
    GPIO.cleanup()
    del midiOutput
    pygame.midi.quit()
GPIO.cleanup()
